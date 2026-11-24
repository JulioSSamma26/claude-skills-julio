# Copia los subagentes de esta carpeta a %USERPROFILE%\.claude\agents (globales en Claude Code).
# Uso (PowerShell, desde la carpeta agentes):  powershell -ExecutionPolicy Bypass -File .\instalar.ps1
$origen  = $PSScriptRoot
$destino = Join-Path $env:USERPROFILE ".claude\agents"
New-Item -ItemType Directory -Force -Path $destino | Out-Null
$nombres = "explorador-haiku.md","Explore.md","desarrollador-sonnet.md","arquitecto-opus.md","lider-fable.md"
foreach ($n in $nombres) {
    $dst = Join-Path $destino $n
    if (Test-Path $dst) { Copy-Item $dst "$dst.bak" -Force; Write-Host "Respaldo: $dst.bak" }
    Copy-Item (Join-Path $origen $n) $dst -Force
    Write-Host "Instalado: $dst"
}
Write-Host "Listo. Reinicia Claude Code y comprueba con /agents."
