# AEOS Baseline Manifest

更新时间：2026-11-21（代际与现行状态列；2026-09-22 首次发布）

以下四个文件为当前要求纳入仓库的项目级最小正式基线。SHA-256 来自用户提供/项目文件的原始字节，用于重建后核验。

**代际说明**：这 4 份文件属于 **2026-09 代（V1.0，12 个月路线）**；项目自 2026-10-14 起实际执行口径为 V7.2.2 资料包（9 个月 / 36 周、M00–M14），该资料包仍是「候选 / 待评审签批」，未替换本清单条目。代际关系、升级 V1.1 的条件与 `check_baseline.py` 的语义见 `adr/ADR-2026-011-baseline-generation-v1-vs-v722.md`。

| 文件 | 代际 | 期望大小(bytes) | SHA-256 | 现行状态（2026-11-21） |
|---|---|---:|---|---|
| AEOS_V7.2_分模块分阶段具体执行方案_V1.0.docx | 2026-09 / V1.0（12 个月） | 528704 | 77fce188fa7f5f8780c5324dc73a5a89afdb3a66bef79c9e9b0149fa7684d7b0 | 已回填（2026-11-21，原始受控字节，SHA 匹配） |
| AEOS_项目开发执行手册_V1.0.docx | 2026-09 / V1.0（19 条宪法） | 48367 | 9c93ad7b3b0a540506ae837f0d4381010b013abf7f46afa428014a5d6ba69535 | 已回填（2026-11-21，原始受控字节，SHA 匹配） |
| AEOS_开发点检与进度表_V1.0.xlsx | 2026-09 / V1.0（27 项检查） | 55114 | 0bce8229ced21817a7e9e7588f897f4d6f5de5ac751e459aadd19627331150ec | 已替换为受控版本（2026-11-21，此前为 7509-byte 截断件） |
| AEOS_企业数据与智能中台_Data_Foundation_总体方案_V0.2_AEOS_V7.2.docx | 2026-09 / V0.2（V7.2.2 沿用） | 1580452 | 871b02246d07c4f0909aa613d3f6e68fc8b0fa72e1bd6f15ab885d703ccc128f | 已回填（2026-11-21，原始受控字节，SHA 匹配） |

## P0 架构冻结受控交付物

以下文件属于 P0 受控架构交付物，独立于上面的“四份项目级最小基线”：

| 路径 | 大小(bytes) | SHA-256 | 文档状态 |
|---|---:|---|---|
| docs/P0/AEOS_P0-01_System_Registry_V1.docx | 48389 | 07969ed5e1058a7d85a8b2c22638f6c1ef6950bbc45bfb8d4796640dbbd54ed0 | 待签批；签批后 FROZEN / EFFECTIVE |
| docs/P0/AEOS_P0-02_Module_Mapping_Matrix_V1.docx | 52122 | faf55fe69d82be040686ff00c69ac274bb9c1ff32c098fc91351f078fb289291 | 待签批；签批后生效 |

## 项目级最小基线放行规则

只有同时满足以下条件才允许标记为 BASELINE_READY：

- 四个项目级正式文件均存在于 `docs/`
- 文件大小与本清单一致
- SHA-256 与本清单一致
- 重建/上传过程有 commit SHA
- Accountable Owner 确认

任何缺失或校验失败均视为 NOT_READY。

P0-01 / P0-02 的业务生效状态以文件内签批条件和 Development Ledger 记录为准，不能仅因文件进入 GitHub 即自动视为 EFFECTIVE。


## AEOS V7.2.2 增补受控架构原则

| 路径 | 文档状态 | 适用范围 |
|---|---|---|
| architecture/PROFESSIONAL_OPERATION_SURFACE_V1.md | P0 架构执行原则 | M04～M14 所有专业自治系统 |

该原则定义“专业业务必须在所属自治系统拥有正式操作界面”，并约束 POMS、EBMS、Agent 与 Domain Operation Surface 的职责边界。
