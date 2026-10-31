# Security and Repository Classification

本仓库包含 AEOS 企业架构、数据所有权、接口契约、开发治理和后续业务 Evidence。正式运行前应按“内部受控资料仓库”管理。

## 当前控制要求

- 仓库应设置为 Private。
- 禁止提交真实密码、Token、API Secret、证书私钥。
- 禁止提交未经脱敏的生产客户、供应商、员工、财务和日志数据。
- 生产数据只允许通过受控接口、Evidence 引用或脱敏样例进入开发流程。
- 发现误提交敏感信息时，应立即轮换凭据并清理 Git 历史；仅删除最新文件不足以消除历史暴露。
- 重大权限、Data Owner、核心 Contract 和一级架构变更必须走受控变更流程。
