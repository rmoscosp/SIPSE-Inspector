param(
    [string]$SonarToken = $env:SONAR_TOKEN,
    [string]$JavaHome = "$PSScriptRoot\jdk21tmp\jdk-21.0.11"
)

if (-not $SonarToken) {
    Write-Error 'Debes definir SONAR_TOKEN o pasar -SonarToken'
    exit 1
}

if (-not (Test-Path $JavaHome)) {
    Write-Error "No se encontró JAVA_HOME en '$JavaHome'"
    exit 1
}

$env:JAVA_HOME = $JavaHome
$env:Path = "$env:JAVA_HOME\bin;$env:Path"
$env:SONAR_TOKEN = $SonarToken

Push-Location $PSScriptRoot
& "$PSScriptRoot\sonar-scanner\sonar-scanner-8.0.1.6346\bin\sonar-scanner.bat"
Pop-Location
