# AEOS Baseline Manifest

更新时间：2026-09-22

以下四个文件为当前要求纳入仓库的最小正式基线。SHA-256 来自本次用户提供/项目文件的原始字节，用于重建后核验。

| 文件 | 期望大小(bytes) | SHA-256 | 当前 main 状态（核查时） |
|---|---:|---|---|
| AEOS_V7.2_分模块分阶段具体执行方案_V1.0.docx | 528704 | 77fce188fa7f5f8780c5324dc73a5a89afdb3a66bef79c9e9b0149fa7684d7b0 | 缺失 |
| AEOS_项目开发执行手册_V1.0.docx | 48367 | 9c93ad7b3b0a540506ae837f0d4381010b013abf7f46afa428014a5d6ba69535 | 缺失；staging 仅有部分分片 |
| AEOS_开发点检与进度表_V1.0.xlsx | 55114 | 0bce8229ced21817a7e9e7588f897f4d6f5de5ac751e459aadd19627331150ec | 存在 7509-byte 非正式版本，需替换 |
| AEOS_企业数据与智能中台_Data_Foundation_总体方案_V0.2_AEOS_V7.2.docx | 1580452 | 871b02246d07c4f0909aa613d3f6e68fc8b0fa72e1bd6f15ab885d703ccc128f | 缺失 |

## 放行规则

只有同时满足以下条件才允许标记为 BASELINE_READY：

- 四个正式文件均存在于 `docs/`
- 文件大小与本清单一致
- SHA-256 与本清单一致
- 重建/上传过程有 commit SHA
- Accountable Owner 确认

任何缺失或校验失败均视为 NOT_READY。
