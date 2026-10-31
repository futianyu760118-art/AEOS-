# AEOS 总仓正式基线缺失整改执行记录
核查：2026-10-10。状态：OPEN / NOT_READY。不得以新的同名 DOCX 替代历史受控字节。
## 问题
以 docs/BASELINE_MANIFEST.md 为受控期望基准：正式总纲、开发执行手册、EDP V0.2 DOCX 缺失，点检 XLSX 文件与期望摘要不符；P0-01、P0-02 待签批。
## 修复方法
1. 由档案责任人获取 4 份原件，核对文件名、大小、SHA256（数值以 BASELINE_MANIFEST.md 为准）。
2. 恢复到 docs/ 指定路径；禁止用空文件、自动生成的近似文本或重新导出 DOCX 冒充原件。
3. 如原件不可恢复，创建新版本及变更 ADR，业务/架构 Owner 审核，再建立新的受控 Manifest；旧版本保留为不可恢复状态。
4. 恢复后运行 SHA256 核验并留存 commit SHA、上传者、审核者和校验输出。
5. P0-01/P0-02 的业务 Owner 正式签批后才能标记 FROZEN/EFFECTIVE。
6. 未同时满足 4 文件校验、commit、Owner 确认之前，BASELINE_READY 必须为 false。
## 本轮可核实改善
记录了明确的责任边界、恢复工作流、禁止伪造受控资料的门禁，并新增 POMS 架构和契约草案；原 DOCX/XLSX 恢复及签批仍未完成，绝不误标 DONE。
## 建议责任
M00 项目治理 Owner 负责基线，M02 Owner 负责 EDP 文档，M12 负责 SHA256 自动检查；具体人员需在 Ledger 指定。
