# POMS Mobile Input Contract V1（提议草案）
状态：P0 DRAFT。M10 负责采集体验，M11 负责设备/连接，M02 负责证据及治理，源业务中心对专业记录负责。
## 输入 Envelope
```yaml
tenant_id: string
source_system: M10
actor_id: string
role_context: string
device_id: string
object_ref: {object_type: string, object_id: string}
action_id: string
captured_at: datetime
capture_type: scan|image|voice|text|sensor
payload_schema_version: string
raw_evidence_ref: string
correlation_id: string
trace_id: string
idempotency_key: string
sync_state: pending|sent|accepted|rejected|conflict
```
不要求所有采集都存在 action_id：自发异常可用 source_type/object_ref 生成 Action；无关联任务时 action_id 可为 null，须标明源事件。
## 审核路径
采集 -> 源系统人机审核 -> EDP 清洗分类与质量评分 -> 管理系统授权复核 -> 归档；非关键低风险数据可通过经批准的自动化规则代替人工逐笔签批；风险高的事实必须人工确认。
## 离线与安全
本地加密、有效期及最小化存储、断网可展示未同步状态；自动重试必须幂等；冲突要求人工/规则审定；不允许未获授权离线审批或向 PLC 发控制指令。
## 结果
scan/voice/image 不等于已核准事实；原始来源、修订版本、文件 checksum、数据处理流程、验证人及时间必须可追溯。
## 质量指标（建议阈值，待现场压测）
首页/常用任务 P95 响应目标 <=2s（明确网络设备口径）；关键采集可追踪率 100%；重复业务对象非必要人工录入率趋零；重要结果证据链完整率 100%。
