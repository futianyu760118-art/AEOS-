# ADR-2026-001: 契约包指纹由脚本重建，manifest 视为锁文件

- Status: Accepted
- Owner: owner.m00（架构治理）
- Effective Date: 2026-11-18
- Supersedes: —

## Context

`contracts/manifest.json` 为 `contracts/v1/` 下 8 个 schema 锁定 `schema_version` 与 `sha256`。
2026-11-03 的合并提交（`4b4a5a5`）把 schema 与 manifest 一次性引入，但 manifest 里的 8 个
指纹全部与文件实际字节不符，导致：

```
$ python scripts/validate_contracts.py
ERROR: fingerprint mismatch for audit-event-v1.schema.json
...（8 个全中）
exit 1
```

`validate_contracts.py` 是这个仓库唯一的契约门禁，它红着意味着：

1. 下游（CRM/EBMS/EDP）无法用"契约包通过校验"作为集成前提；
2. 无法判断 schema 是被有意升级过、还是被误改过——指纹本来是唯一能回答这个问题的证据；
3. CI 里加入该门禁会立刻红，团队会习惯性忽略它（门禁失效比没有门禁更糟）。

根因不是 schema 错了，而是**缺少"改 schema 之后重新上锁"的受控动作**。人工改 manifest 里的
64 位哈希既容易打错，也没有审计价值。

## Decision

1. manifest 定位为**锁文件**：`schemas[].sha256` 必须等于对应文件的字节哈希，CI 以
   `python scripts/validate_contracts.py` 为唯一判据。
2. 新增 `scripts/update_manifest.py`：从 `contracts/v1/*.schema.json` 重新计算 `version`
   与 `sha256`，按仓库既有排版重写 manifest；`--check` 模式在过期时退出码 1，供 CI 使用。
3. 修改 schema 的流程固定为：改 schema → 跑 `update_manifest.py` → 校验通过 → 同一提交内
   一起提交（manifest 变更与 schema 变更不可分离）。
4. 本次按第 3 条对 8 个 schema 重新上锁，`generated_at` 更新为 2026-11-18，`generator`
   改为 `scripts/update_manifest.py`（原值指向校验器，语义错误）。

## Alternatives

- **A. 保留旧指纹、回滚 schema**：schema 是 11-03 合并进来的现行版本，下游已按它实现；
  回滚等于让下游编译到不存在的接口。
- **B. 删掉指纹校验**：失去"schema 是否被改过"的唯一证据，契约包退化为普通文档。
- **C. 人工改 manifest**：一次性可行，但无法防止下一次漂移，且改错时症状与"schema 被改"
  完全一样，排障成本高。

## Consequences

- 正向：契约门禁恢复可信；schema 变更留下可审计的两行 diff（schema + manifest）。
- 负向：多人同时改 schema 时会在 manifest 上产生冲突，需要 rebase 后重跑脚本——这是期望行为。
- 风险：若有人绕过脚本直接改 manifest，校验仍会通过但语义已错；靠 code review 兜底。

## Rollback

`git revert` 本次提交即可回到旧 manifest；脚本本身无副作用，可保留。

## Evidence

- `python scripts/update_manifest.py` → `updated contracts/manifest.json (8 schemas)`
- `python scripts/validate_contracts.py` → `AEOS contract validation passed`（exit 0）
- `python scripts/update_manifest.py --check` → `contracts/manifest.json is up to date`
- `python -m pytest scripts/test_validate_contracts.py scripts/test_validate_registry.py -q` → 12 passed
