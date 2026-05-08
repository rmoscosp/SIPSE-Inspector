param(
    [string]$ProjectKey = 'SIPSE-Inspector',
    [string]$SonarHostUrl = 'http://localhost:9000',
    [string]$SonarToken = $env:SONAR_TOKEN,
    [string]$OutputFile = 'sonar-report.json'
)

if (-not $SonarToken) {
    Write-Error 'Debes definir SONAR_TOKEN o pasar -SonarToken'
    exit 1
}

$auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("$SonarToken:"))
$headers = @{ Authorization = "Basic $auth" }

$metrics = 'coverage,lines_to_cover,uncovered_lines,bugs,vulnerabilities,code_smells,duplicated_lines_density,sqale_debt_ratio'
$measuresUrl = "$SonarHostUrl/api/measures/component?component=$ProjectKey&metricKeys=$metrics"
$analysisUrl = "$SonarHostUrl/api/project_analyses/search?project=$ProjectKey&size=5"

try {
    $measures = Invoke-RestMethod -Uri $measuresUrl -Headers $headers
    $analyses = Invoke-RestMethod -Uri $analysisUrl -Headers $headers
} catch {
    Write-Error "Error al consultar la API de SonarQube: $_"
    exit 1
}

$report = [PSCustomObject]@{
    timestamp = (Get-Date).ToString('o')
    projectKey = $ProjectKey
    measures = $measures
    analyses = $analyses
}

$report | ConvertTo-Json -Depth 5 | Out-File -FilePath $OutputFile -Encoding utf8
Write-Host "Reporte Sonar exportado en $OutputFile"
