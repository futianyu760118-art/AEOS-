[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory)] [string]$PersonId,
    [Parameter(Mandatory)] [string]$TenantId,
    [ValidateSet("person.offboarded", "person.reinstated")] [string]$EventType = "person.offboarded",
    [string]$DisplayName = "",
    [string]$EmployeeCode = "",
    [string]$SourceUrl = $env:AEOS_PERSON_LIFECYCLE_URL,
    [string]$KeyId = $env:AEOS_PERSON_LIFECYCLE_KEY_ID,
    [string]$Secret = $env:AEOS_PERSON_LIFECYCLE_SECRET,
    [switch]$ConfirmDispatch
)

$ErrorActionPreference = "Stop"
if (-not $ConfirmDispatch) {
    Write-Host "预览模式：将测试 $EventType，人员 $PersonId（$DisplayName）。"
    Write-Host "如确认写入系统，请再次加 -ConfirmDispatch；脚本不会显示密码。"
    exit 0
}
if ([string]::IsNullOrWhiteSpace($SourceUrl) -or [string]::IsNullOrWhiteSpace($KeyId) -or [string]::IsNullOrWhiteSpace($Secret)) {
    throw "正式发送需要 AEOS_PERSON_LIFECYCLE_URL、AEOS_PERSON_LIFECYCLE_KEY_ID、AEOS_PERSON_LIFECYCLE_SECRET。"
}

$now = [DateTimeOffset]::UtcNow
$body = [ordered]@{
    event_id = [Guid]::NewGuid().ToString("N")
    event_type = $EventType
    tenant_id = $TenantId
    source_system = "M01_KERNEL"
    revision = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
    occurred_at = $now.ToString("o")
    person = [ordered]@{
        person_id = $PersonId
        display_name = $DisplayName
        employee_code = $EmployeeCode
        tenant_id = $TenantId
    }
} | ConvertTo-Json -Depth 8 -Compress

$timestamp = [string][DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
$hmac = [System.Security.Cryptography.HMACSHA256]::new([Text.Encoding]::UTF8.GetBytes($Secret))
try {
    $signature = [Convert]::ToHexString($hmac.ComputeHash([Text.Encoding]::UTF8.GetBytes("$timestamp.$body"))).ToLowerInvariant()
} finally { $hmac.Dispose() }

$headers = @{
    "X-AEOS-Key-Id" = $KeyId
    "X-AEOS-Timestamp" = $timestamp
    "X-AEOS-Signature" = $signature
    "Content-Type" = "application/json"
}
$result = Invoke-RestMethod -Uri $SourceUrl -Method Post -Headers $headers -Body $body -TimeoutSec 15
Write-Host "已提交。请在 M01、EDP 和各业务系统的人员状态页面查看办理状态。"
$result | ConvertTo-Json -Depth 8

