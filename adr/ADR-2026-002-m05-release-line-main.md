# ADR-2026-002: M05-CRM 发布线切到 Gitee `main`，注册表按 commit 锁定

- Status: Accepted
- Owner: owner.m05（销售域）/ owner.m00（注册表）
- Effective Date: 2026-11-18
- Supersedes: —

## Context

注册表把 12 个系统的 `branch` 硬编码为 `aeos/phase1-v1.1`，`M05_CRM` 锁在
`66074b1b…`（2026-10-26）。实际情况是：

- CRM 的 Gitee 仓库（`ningbohengjianguangdian/CRM`，私有）默认分支为 `main`，
  2026-11-17 已推进到 `70da1b46…`，11-07 起 99 个提交全部落在 `main`；
- 本地 `aeos/phase1-v1.1-integration` 分支停在 11-03，已无意义；
- GitHub `futianyu760118-art/CRM` 是另一条线，与 Gitee 已分叉。

结果：注册表描述的版本与实际在跑的版本相差 21 天、数十个提交。`lifecycle_state` 仍是
`CANDIDATE`，没有任何一处记录"现在线上到底是哪一版"——这正是 12 月发布评审最需要回答的问题。

对校验器的约束：`validate_registry.py` 把 `branch != "aeos/phase1-v1.1"` 直接判错，因此
"把 branch 改成 main"在旧校验下必然失败。

## Decision

1. **Gitee `main` 为 M05-CRM 的唯一发布线**；GitHub 仓库降级为只读镜像（后续补镜像说明）。
2. 注册表 `systems.yaml` 与 `system-manifests/M05-CRM.yaml` 同步更新：
   `branch: main`、`upstream_commit: 70da1b465a0834f61683c63c8d953e24a383ab62`
   （2026-11-17 16:51，`feat(m06): 同步后自动用 EDP 补全订单与样品单…`）、
   `lifecycle_state: INTEGRATING`。
3. 校验器把 `branch` 从"等于常量"放宽为**白名单** `{aeos/phase1-v1.1, main}`：
   分支名只描述"从哪条线来"，真正的锁定物是 40 位 `upstream_commit`；新增分支必须先进
   白名单并补 ADR。
4. `sign_off` 保持 `PENDING`：本次只做"版本对上"，不做"责任人签字"。签字是治理动作，
   由 owner 本人在发布评审上完成，不由提交代劳。

## Alternatives

- **A. 保持 branch 为 `aeos/phase1-v1.1`，只改 commit**：注册表会声称"这版来自一条
  已废弃的分支"，下一个人按 branch 去 fetch 会拿到 11-03 的旧代码。
- **B. 把 CRM 回迁到 `aeos/phase1-v1.1` 分支**：等于让 99 个提交改道，成本远高于收益。
- **C. 注册表不再记 branch，只记 commit**：更彻底，但会同时改动校验器与 11 个系统的
  清单格式，超出本次止血范围，留待 ADR-2026-00x。

## Consequences

- 正向：注册表 pin 与 Gitee 实际 HEAD 一致；发布评审能回答"这一版是哪个 commit"。
- 负向：白名单放宽后，其他系统理论上也能填 `main`；靠 ADR 流程约束，暂不引入每系统配置。
- 遗留：`sign_off` 仍 PENDING，`lifecycle_state` 停在 `INTEGRATING`，未到 `READY`。

## Rollback

把两处 `branch`/`upstream_commit`/`lifecycle_state` 改回旧值并 `git revert` 校验器改动即可；
无数据迁移，无部署动作。

## Evidence

- `git -C CRM rev-parse HEAD` → `70da1b465a0834f61683c63c8d953e24a383ab62`
- `git -C CRM log -1 --format=%cI` → `2026-11-17T16:51:46+08:00`
- `python scripts/validate_registry.py` → `AEOS registry validation passed`（exit 0）
- `python -m pytest scripts/test_validate_registry.py -q` → 通过
