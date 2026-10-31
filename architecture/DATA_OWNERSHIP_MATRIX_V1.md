# Data Ownership Matrix V1

状态：P0 待业务 Owner 正式确认。

| 对象/事实 | 正式 Owner | 消费方示例 | 规则 |
|---|---|---|---|
| Person / Organization / Position | M01 AEOS Kernel | M03/M04/M05/M06/M07/M08/M09/M10 | M07 只能引用，不得成为第二主数据 Owner |
| Customer / Lead / Inquiry / Quote | M05 Sales | M03/M03A/M02 | 跨域通过 Contract/Result，不直接写 Sales 表 |
| Product / Requirement / Drawing / BOM / ECO / Release | M04 R&D | M03/M05/M06/M08/M02 | 正式 BOM/Release 必须 Guard + 人类责任 |
| Order 商务事实 | M05 Sales | M03/M06/M09/M02 | 订单承诺需 Delivery 能力验证 |
| OrderExecution / Demand / Material / PO / Plan / Capacity / Shipment | M06 Delivery | M03/M05/M08/M09/M02 | 不拥有销售商务、研发 EBOM、会计事实 |
| Inspection / Test / NC / CAPA / Complaint / ReleaseGate | M08 Quality | M03/M04/M06/M02 | 重大风险必须可阻断 Release/Shipment |
| Revenue / Cost / Margin / Cash / AR / AP / Budget / ROI / Value | M09 Finance | M03/M03A/M02 | EBMS 不独立维护第二套正式财务事实 |
| Event / Evidence / Audit / Result / Value Ledger | M02 Data & Evidence | 全系统 | 作为企业统一事实与证据底座 |

## 待确认

每个正式 Owner 必须落实到具体 Accountable Business Owner 与 System Lead。未明确 Owner 的对象不得进入正式跨域 Contract。
