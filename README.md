# AEOS V7.2 受控执行资料仓库

本仓库是宁波恒剑光电科技有限公司 AEOS V7.2 的执行级受控基线仓库。

## 基线层级

1. `docs/AEOS_V7.2_分模块分阶段具体执行方案_V1.0.docx` — 执行总纲
2. `docs/AEOS_项目开发执行手册_V1.0.docx` — 开发治理与执行标准
3. `docs/AEOS_开发点检与进度表_V1.0.xlsx` — 点检与进度快照
4. `docs/AEOS_企业数据与智能中台_Data_Foundation_总体方案_V0.2_AEOS_V7.2.docx` — M02 专业基线

执行口径：先边界、后功能；先闭环、后扩展；先 A0/A1、后 A2/A3；代码完成不等于业务完成。

## 目录

- `docs/`：正式受控文档
- `architecture/`：System Registry、Domain Boundary、Data Ownership
- `contracts/`：Object/API/Event/Result/Evidence/Decision/Action 契约
- `ledger/`：Development Ledger 与 Gate 状态
- `adr/`：Architecture Decision Record
- `staging/`：二进制文档临时重建区，禁止作为正式事实源
- `.github/`：CI、模板、CODEOWNERS

## 管理原则

- 每个模块必须有唯一 Accountable Owner。
- 以闭环验收，不以页面数量验收：Fact → Event → Decision → Action → Result → Evidence。
- PR merged 仅代表代码进度，不代表业务完成。
- 任何跨域直连、临时复制数据必须登记技术债、Owner 和到期日。
- 正式状态以 Gate、测试、部署、UAT、Evidence 和 Owner Verify 为准。

## 当前仓库状态

正式二进制基线以 `docs/BASELINE_MANIFEST.md` 为准。缺失或校验失败的文件不得作为受控基线使用。
