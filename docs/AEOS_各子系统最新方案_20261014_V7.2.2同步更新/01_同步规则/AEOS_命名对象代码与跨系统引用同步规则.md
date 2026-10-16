# AEOS 命名对象代码与跨系统引用同步规则

本文件把审查意见转为同步更新规则。

## 系统代码

所有系统使用 `module_id + system_code + system_name + system_name_en` 四字段。代码表见 System Registry V1.3 候选。

## 对象代码

- 数据库、Event、内部 API 统一 snake_case ID。
- 对象实体 PascalCase；禁止用 `/` 组合多个实体。
- `Verification` 是对象实体，`verify` 是动作。
- 统一字段：`fact_owner`、`record_owner`、`processor`、`consumer`、`verifier`。

## 闭环

`Object → Event → Exception（可选）→ Decision（可选）→ Action → Result → Verification → Evidence → Value → Learning`。

## 当前状态

命名与对象代码为同步候选，需 M00、M01、M02、M12、M13、M14 Owner 和 PMO 签批后进入正式 P0-01/P0-02。
