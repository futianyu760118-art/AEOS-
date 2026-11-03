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
    [string]$StatusUrl = "",
    [int]$PollSeconds = 2,
    [int]$MaxPolls = 10,
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
$eventId = [Guid]::NewGuid().ToString("N")
$correlationId = [Guid]::NewGuid().ToString("N")
$traceId = [Guid]::NewGuid().ToString("N")
$revision = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
$status = if ($EventType -eq "person.offboarded") { "inactive" } else { "active" }
$employmentAction = if ($EventType -eq "person.offboarded") { "offboard" } else { "reinstate" }
$body = [ordered]@{
    event_id = $eventId
    event_type = $EventType
    event_version = 1
    tenant_id = $TenantId
    source_system = "M01_KERNEL"
    object_type = "Person"
    object_id = $PersonId
    revision = $revision
    occurred_at = $now.ToString("o")
    effective_at = $now.ToString("o")
    correlation_id = $correlationId
    trace_id = $traceId
    idempotency_key = "person-lifecycle:${TenantId}:${PersonId}:${revision}"
    status = $status
    employment_action = $employmentAction
    occurred_by = "manual-e2e"
    person = [ordered]@{
        person_id = $PersonId
        emp_code = $EmployeeCode
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
if ($StatusUrl) {
    for ($index = 0; $index -lt [Math]::Max(1, $MaxPolls); $index++) {
        Start-Sleep -Seconds ([Math]::Max(1, $PollSeconds))
        try {
            $progress = Invoke-RestMethod -Uri $StatusUrl -Method Get -TimeoutSec 15
            $progress | ConvertTo-Json -Depth 8
            $states = @($progress.targets | ForEach-Object { $_.status })
            if ($states.Count -gt 0 -and ($states | Where-Object { $_ -in @('failed', 'dlq') }).Count -gt 0) { break }
            if ($states.Count -gt 0 -and ($states | Where-Object { $_ -notin @('pending', 'scheduled', 'retrying') }).Count -eq $states.Count) { break }
        } catch {
            Write-Warning "进度查询暂时失败，未输出内部错误。"
        }
    }
}

