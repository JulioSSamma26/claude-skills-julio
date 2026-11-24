# Deja un equipo Windows listo para Claude Code con la configuración de Julio:
#   1) los 5 subagentes con modelo fijo (incluido Explore) en %USERPROFILE%\.claude\agents
#   2) la regla de zona horaria al final de %USERPROFILE%\.claude\CLAUDE.md (solo si no está)
# Las skills NO se instalan aquí: llegan solas a cada equipo desde la cuenta de claude.ai.
# Uso, desde la raíz del repo:  powershell -ExecutionPolicy Bypass -File .\instalar-equipo.ps1
# Se puede repetir sin riesgo.
$ErrorActionPreference = "Stop"
$repo = $PSScriptRoot
$claude = Join-Path $env:USERPROFILE ".claude"

& (Join-Path $repo "agentes\instalar.ps1")

$personal = Join-Path $claude "CLAUDE.md"
$utf8 = New-Object Text.UTF8Encoding $false
$actual = if (Test-Path $personal) { [IO.File]::ReadAllText($personal) } else { "" }
if ($actual -match '(?m)^## Zona horaria') {
    Write-Host "Zona horaria: ya estaba en $personal"
} else {
    $lineas = [IO.File]::ReadAllLines((Join-Path $repo "CLAUDE.md"), $utf8)
    $i = [array]::IndexOf($lineas, "## Zona horaria")
    if ($i -lt 0) { throw "No encontré '## Zona horaria' en el CLAUDE.md del repo" }
    $seccion = @($lineas[$i])
    for ($j = $i + 1; $j -lt $lineas.Count -and $lineas[$j] -notmatch '^#'; $j++) { $seccion += $lineas[$j] }
    $seccion = ($seccion -join "`r`n").TrimEnd()
    if (Test-Path $personal) { Copy-Item $personal "$personal.bak" -Force; Write-Host "Respaldo: $personal.bak" }
    $prefijo = if ($actual -and -not $actual.EndsWith("`n")) { "`r`n`r`n" } elseif ($actual) { "`r`n" } else { "" }
    New-Item -ItemType Directory -Force -Path $claude | Out-Null
    [IO.File]::AppendAllText($personal, $prefijo + $seccion + "`r`n", $utf8)
    Write-Host "Zona horaria: agregada a $personal"
}
Write-Host "Listo. Reinicia Claude Code y revisa /agents."
