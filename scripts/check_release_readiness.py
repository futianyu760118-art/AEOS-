#!/usr/bin/env python
"""检查 M05 是否够格往 READY 走（Phase 4 的就绪门禁）。

注册表里把 ``lifecycle_state`` 从 ``INTEGRATING`` 提到 ``READY``，意味着「这套系统
可以按声明的方式上线并被别的系统依赖」。这件事不该靠记忆判断，所以这里把条件写成
可执行检查：

1. **pin 有效** —— manifest 里的 ``upstream_commit`` 在仓库里真实存在；
2. **pin 与 main 一致** —— 声明上线的那一版就是主线那一版（pin 落后等于拿旧版发）；
3. **工作分支已合并** —— 分支上的改动（ADR-003/004/005…）必须进 main 才谈得上 READY；
4. **契约与注册表自检通过** —— 调 ``validate_contracts.py`` / ``validate_registry.py``；
5. **签核齐备** —— ``sign_off.owner`` 与 ``sign_off.environment`` 都得是 ``APPROVED``。

只读，不改注册表。``--strict`` 时把「未合并」也算阻断（默认只警告）。

用法::

    python scripts/check_release_readiness.py --crm ../CRM-gitee-20261117
    python scripts/check_release_readiness.py --crm ../CRM --strict
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "registry" / "system-manifests" / "M05-CRM.yaml"

PASS, FAIL, WARN = "PASS", "FAIL", "WARN"

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")


@dataclass
class Check:
    name: str
    status: str
    detail: str


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def read_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def check_pin_exists(repo: Path, pin: str) -> Check:
    result = git(repo, "cat-file", "-e", f"{pin}^{{commit}}")
    if result.returncode != 0:
        return Check("pin 存在", FAIL, f"仓库里没有 {pin[:12]}")
    return Check("pin 存在", PASS, pin[:12])


def check_pin_matches_main(repo: Path, pin: str) -> Check:
    result = git(repo, "rev-parse", "refs/heads/main")
    if result.returncode != 0:
        result = git(repo, "rev-parse", "refs/remotes/origin/main")
    if result.returncode != 0:
        return Check("pin 对齐 main", WARN, "本地没有 main 引用，无法比对")
    main = result.stdout.strip()
    if main == pin:
        return Check("pin 对齐 main", PASS, f"main={main[:12]}")
    return Check("pin 对齐 main", FAIL, f"pin={pin[:12]}，main={main[:12]}（pin 已过期）")


def check_branch_merged(repo: Path, pin: str, branch: str, strict: bool) -> Check:
    result = git(repo, "rev-parse", f"refs/heads/{branch}")
    if result.returncode != 0:
        return Check("工作分支已合并", WARN, f"本地没有分支 {branch}")
    tip = result.stdout.strip()
    merged = git(repo, "merge-base", "--is-ancestor", tip, "main").returncode == 0
    if merged:
        return Check("工作分支已合并", PASS, f"{branch}@{tip[:12]} 已在 main 里")
    ahead = git(repo, "rev-list", "--count", f"main..{tip}").stdout.strip() or "?"
    status = FAIL if strict else WARN
    return Check("工作分支已合并", status, f"{branch} 领先 main {ahead} 个提交，尚未合并")


def run_script(name: str) -> Check:
    script = ROOT / "scripts" / name
    if not script.is_file():
        return Check(name, FAIL, "脚本不存在")
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        tail = (result.stdout or result.stderr).strip().splitlines()
        return Check(name, FAIL, tail[-1] if tail else f"退出码 {result.returncode}")
    return Check(name, PASS, "通过")


def check_sign_off(manifest: dict) -> Check:
    sign_off = manifest.get("sign_off") or {}
    owner = sign_off.get("owner", "PENDING")
    environment = sign_off.get("environment", "PENDING")
    if owner == "APPROVED" and environment == "APPROVED":
        return Check("签核", PASS, "owner/environment 均已批准")
    return Check("签核", FAIL, f"owner={owner}，environment={environment}")


def check_state(manifest: dict) -> Check:
    state = manifest.get("lifecycle_state", "UNKNOWN")
    if state == "READY":
        return Check("生命周期状态", PASS, "READY")
    return Check("生命周期状态", FAIL, f"{state}（未到 READY）")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="M05 就绪检查")
    parser.add_argument("--crm", required=True, help="CRM 检出目录")
    parser.add_argument(
        "--branch",
        default="aeos/p0-authority-consistency",
        help="待合并的工作分支（默认 aeos/p0-authority-consistency）",
    )
    parser.add_argument("--strict", action="store_true", help="未合并也算阻断")
    args = parser.parse_args(argv)

    repo = Path(args.crm).expanduser().resolve()
    if not (repo / ".git").exists():
        print(f"[FAIL] 不是 git 检出：{repo}")
        return 2

    manifest = read_manifest()
    pin = manifest.get("upstream_commit", "")

    checks = [
        check_state(manifest),
        check_sign_off(manifest),
        check_pin_exists(repo, pin),
        check_pin_matches_main(repo, pin),
        check_branch_merged(repo, pin, args.branch, args.strict),
        run_script("validate_contracts.py"),
        run_script("validate_registry.py"),
    ]

    for check in checks:
        print(f"[{check.status}] {check.name} —— {check.detail}")

    blocking = [c for c in checks if c.status == FAIL]
    print()
    if blocking:
        print(f"结论：还不能 READY，阻断项 {len(blocking)} 个：" + "、".join(c.name for c in blocking))
        print("下一步：合并工作分支 → 更新 manifest 的 upstream_commit → 补签核 → 再跑一次本脚本")
        return 1
    print("结论：READY 条件已满足")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
