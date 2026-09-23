# meeting-helper → AEOS DEH P0 改造执行清单 V1

状态：执行基线  
目标：不先重写 UI，先消除架构耦合并具备 AEOS 接入条件。

## A. P0-1 数据模型

- [ ] 新增 Decision 实体
- [ ] Action 增加 source_type/source_id
- [ ] Action 增加 goal_id
- [ ] Action 增加 object_type/object_id
- [ ] Action 的 meeting_id 从强依赖改为兼容字段
- [ ] 新增 Result 实体
- [ ] Evidence 独立实体化
- [ ] 全部对象增加 correlation_id / trace_id
- [ ] 保留 legacy id 映射表

验收：非 Meeting 来源可独立创建并闭环一条 Action。

## B. P0-2 事件

- [ ] 实现标准事件 Envelope
- [ ] ActionCreated
- [ ] ActionAssigned
- [ ] ActionStarted
- [ ] ActionBlocked
- [ ] ActionOverdue
- [ ] ActionCompleted
- [ ] ResultSubmitted
- [ ] ResultVerified
- [ ] EvidenceSubmitted
- [ ] 幂等键
- [ ] Event replay 测试

验收：重复消费同一事件不得重复创建 Action/Result。

## C. P0-3 Result / Evidence

- [ ] 将“完成”与“验收通过”拆分
- [ ] 完成后生成 Result
- [ ] Result 必须支持 Expected / Actual
- [ ] Evidence 与 Result 关联
- [ ] V/X/0 映射到 Verify 语义
- [ ] 保留原始附件与来源
- [ ] 增加 checksum / version / source

验收：任一 Verified Result 可反查证据与原始来源。

## D. P0-4 权限

- [ ] admin 与业务角色分离
- [ ] manager 映射 Decision Maker / Observer
- [ ] employee 映射 Executor
- [ ] 增加 System Agent 身份
- [ ] LLM 写正式 Decision 前走 Guard
- [ ] Result Verify 权限独立

验收：执行者不能自行把自己的 Result 标记为 Verified，除非规则显式允许。

## E. P0-5 接口

- [ ] /api/v1/decisions
- [ ] /api/v1/actions
- [ ] /api/v1/results
- [ ] /api/v1/evidence
- [ ] /api/v1/events
- [ ] 标准错误码
- [ ] Idempotency-Key
- [ ] API audit
- [ ] OpenAPI/Schema

验收：所有新增接口通过契约测试。

## F. P0-6 兼容迁移

- [ ] 现有 Meeting 页面保持可用
- [ ] 现有行动项数据迁移为 source_type=meeting
- [ ] 原 meeting_id 保存为 legacy_ref/source_id
- [ ] OA/企微/IM 推送继续运行
- [ ] 周/月看板保持原口径
- [ ] 建立回滚脚本
- [ ] 双写期间增加一致性检查

验收：迁移不破坏现有会议和待办生产流程。

## G. DoD

P0 完成必须同时满足：
1. Meeting 不再是 Action 的强制父对象。
2. 非会议事件能产生 Action。
3. done 与 verified 分离。
4. Result 与 Evidence 有标准对象。
5. Event 支持幂等与追踪。
6. Contract Test 通过。
7. 旧流程回归通过。
8. 有迁移和回滚证据。
