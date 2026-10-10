# POMS V2.1 vs AEOS V7.2 差异整改台账
日期：2026-10-10。设计对齐 != 代码实现通过。
| ID | 差异 | 修正动作 | Owner模块 | 状态 |
|---|---|---|---|---|
| D01 | 公共 Kernel 重复 | M10 仅动态装配；M01 拥有共享治理 | M01/M10 | DESIGN_DEFINED |
| D02 | 数据归属 | M02 Evidence/Audit、专业中心专业事实 | M02/M04~M09 | DESIGN_DEFINED |
| D03 | DEH状态 | done != verified，直接复用 DEH Contract | M01/M10 | DESIGN_DEFINED |
| D04 | 自动装配契约 | Capability/Role/UI Schema 草案 | M10 | DRAFT |
| D05 | 专用包契约 | Manifest/版本/回滚/兼容 | M10+领域Owner | DRAFT |
| D06 | 迁移 | 灯具->定时器双租户/多产品、G6试验 | M10/M00 | TEST_PENDING |
| D07 | 手机 | 采集 Envelope/离线/扫码语音照片 | M10/M11 | DRAFT |
| D08 | 设备 | PLC 联锁，LLM 不直接控制 | M11 | DESIGN_DEFINED |
| D09 | 专业业务归属 | 业务规则只在 M04~M09 | M04~M10 | DESIGN_DEFINED |
| D10 | Skill | M01 统一 Skill/Guard/评测/回滚 | M01/M12 | TEST_PENDING |
| D11 | Result 验证 | 执行和验证身份分离 | M01/M10 | DESIGN_DEFINED |
| D12 | 门禁 | L0-L4 映射 G0-G6，不替代门禁 | M00/M12 | DESIGN_DEFINED |
| D13 | 三化 | 释义待总纲正式原件核验 | M00 | OPEN |
| D14 | 双层审核 | 源系统审核、EDP清洗、管理系统授权复核 | M02/领域 | DRAFT |
| D15 | 多产品版本 | 同租户多能力包及工艺版本并行 | M10/领域 | TEST_PENDING |
## 出门条件
DRAFT/TEST_PENDING 不等于已整改完成。G0 需 Architecture Board/Owner 签批；G2 需契约测试；G3 需真实业务闭环；G5 Skill/Guard；G6 跨租户复制与价值基线。
