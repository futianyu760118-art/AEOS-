# P0 Architecture Baselines

本目录保存 P0 架构冻结阶段的正式受控交付物。

| 编号 | 文件 | 定位 | 当前文档状态 |
|---|---|---|---|
| P0-01 | AEOS_P0-01_System_Registry_V1.docx | 最终命名与一级架构冻结 / System Registry | 待签批，签批后 FROZEN / EFFECTIVE |
| P0-02 | AEOS_P0-02_Module_Mapping_Matrix_V1.docx | Current → Target Module Mapping Matrix | 待签批，签批后生效 |

P0-01 是 P0-02、P0-03、P0-04、P0-05 的一级归属依据。P0-02 只冻结现有系统的目标归属与迁移方向，不在该阶段重写代码。

完整性校验：
- P0-01: 48389 bytes, SHA-256 07969ed5e1058a7d85a8b2c22638f6c1ef6950bbc45bfb8d4796640dbbd54ed0
- P0-02: 52122 bytes, SHA-256 faf55fe69d82be040686ff00c69ac274bb9c1ff32c098fc91351f078fb289291


## meeting-helper / DEH P0 执行物

- `../../architecture/DEH_BOUNDARY_V1.md` — DEH 在 M01/M02/M03/M10/M11/M12 之间的边界和红线。
- `../../contracts/DEH_CONTRACT_V1.md` — Goal / Decision / Action / Result / Evidence / Event 最小执行契约。
- `MEETING_HELPER_DEH_P0_CHECKLIST_V1.md` — meeting-helper 从 Meeting-centric 向 AEOS DEH 迁移的 P0 执行与验收清单。

说明：本次不新增 AEOS 一级模块编号；DEH 按 System Registry V1 作为跨 M01+M02 的逻辑闭环能力实施。
