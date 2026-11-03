[CmdletBinding()]
param(
    [string]$RegistryPath = (Join-Path $PSScriptRoot "..\registry\systems.yaml"),
    [string]$CapabilityGatePath = (Join-Path $PSScriptRoot "..\registry\capability-gates.yaml"),
    [switch]$Probe,
    [int]$TimeoutSec = 5
)

$ErrorActionPreference = "Stop"

function Read-JsonFile([string]$Path) {
    return (Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json)
}

$registry = Read-JsonFile $RegistryPath
$gates = Read-JsonFile $CapabilityGatePath
$notDeployed = @($gates.gates | Where-Object { $_.deployment_state -eq "NOT_DEPLOYED" } | ForEach-Object { $_.system_id })
$errors = [System.Collections.Generic.List[string]]::new()

foreach ($system in $registry.systems) {
    if ($notDeployed -contains $system.system_id) {
        continue
    }
    if ($system.person_lifecycle_role -eq "governance") {
        continue
    }
    if ([string]::IsNullOrWhiteSpace($system.person_lifecycle_endpoint) -or
        $system.person_lifecycle_endpoint -eq "not-applicable") {
        $errors.Add("$($system.system_id)：没有登记人员状态同步入口")
    }
    if (@($system.sync_capabilities).Count -eq 0 -and $system.person_lifecycle_role -ne "governance") {
        $errors.Add("$($system.system_id)：没有登记同步能力")
    }
}

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Error $_ }
    exit 1
}

Write-Host "登记检查通过：$(@($registry.systems).Count) 个系统，$($notDeployed.Count) 个未部署系统已被明确拦截。"
if (-not $Probe) {
    Write-Host "未执行网络探测。需要探测时请加 -Probe，并在各系统环境变量中提供地址。"
    exit 0
}

$urls = @{}
foreach ($system in $registry.systems) {
    $envName = "AEOS_" + ($system.system_id -replace "[^A-Za-z0-9]", "_") + "_URL"
    $url = [Environment]::GetEnvironmentVariable($envName)
    if ($url) { $urls[$system.system_id] = $url.TrimEnd('/') + $system.person_lifecycle_endpoint }
}

foreach ($system in $registry.systems) {
    if ($notDeployed -contains $system.system_id -or -not $urls.ContainsKey($system.system_id)) { continue }
    try {
        $response = Invoke-WebRequest -Uri $urls[$system.system_id] -Method Options -TimeoutSec $TimeoutSec -UseBasicParsing
        Write-Host "$($system.system_id)：网络可达（$($response.StatusCode)）"
    } catch {
        Write-Warning "$($system.system_id)：未通过网络探测；没有输出密钥或请求内容。"
    }
}

