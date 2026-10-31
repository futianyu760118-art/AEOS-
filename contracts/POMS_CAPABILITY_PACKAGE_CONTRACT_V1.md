# POMS Capability / Role / UI Contract V1（提议草案）
状态：P0 DRAFT；正式 Schema/API 需 Architecture Board 批准。归属 M10 对装配，M01 对权限，M04~M09 对领域内容，M11 对外设。
## Capability Manifest 必填
```yaml
capability_id: quality.inspection.timer
version: 1.0.0
domain_owner: M08
tenant_scope: configurable
product_scope:
  family: timer
  model_ids: []
  process_revision: "1"
requires:
  platform_contract: "1"
  domain_api: "quality.v1"
roles: ["quality_inspector"]
permissions: ["quality.inspection.submit"]
ui_schema_ref: "schemas/inspection.form.json"
skills: ["timer.precision.check@1"]
evidence_policy_ref: "quality.evidence.v1"
rollback_version: null
```
要求：版本与依赖兼容、签名/校验和、发布审批、撤销/回滚、动态装载隔离、审计日志。
## Role Assembly Contract
输入：tenant_id、actor_id、positions[]、grants[]、object_ref、product_ref、device_capabilities[]、context_revision；输出：capability_refs[]、ui_manifest_version、expires_at。装配时只展示授权功能，执行时强制重新授权检查；不得仅凭 UI 隐藏控制权限。
## UI Schema
使用受控 widget_type / field_id / data_type / validation / visibility_policy / evidence_required / action_ref，拒绝任意脚本执行。专业规则不得注入 M10 内核。
## 域调用契约
所有写操作走受控 Domain API，继承 tenant_id、object_ref、actor、correlation_id、trace_id、idempotency_key、schema_version；Result/Evidence 引用既有 AEOS 契约。禁止 M10 直接跨域写 DB。
## 验收测试
同企业并行加载不同产品包；跨企业数据隔离；岗位变化撤权；错误 schema 拒绝；重复提交不重复生成 Action/Result；旧包回滚不篡改原记录；公共核心 git diff 无产品特定修改。
