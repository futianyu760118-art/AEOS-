# staging

此目录仅用于临时二进制重建，不是正式事实源。

规则：

1. 分片只能用于重建 `docs/` 正式文件。
2. 触发 `staging/READY` 前必须补齐所有规定分片。
3. 重建后必须核验 `docs/BASELINE_MANIFEST.md` 中的大小与 SHA-256。
4. 校验通过后删除 staging 分片与 READY。
5. 禁止将敏感业务数据、账号、密钥或生产导出放入 staging。
