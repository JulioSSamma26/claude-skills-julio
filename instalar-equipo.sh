#!/usr/bin/env bash
# Deja un equipo macOS/Linux listo para Claude Code con la configuración de Julio:
#   1) los 4 subagentes con modelo fijo en ~/.claude/agents
#   2) la regla de zona horaria al final de ~/.claude/CLAUDE.md (solo si no está)
# Las skills NO se instalan aquí: llegan solas a cada equipo desde la cuenta de claude.ai.
# Uso, desde la raíz del repo: bash instalar-equipo.sh   (se puede repetir sin riesgo)
set -euo pipefail
repo="$(cd "$(dirname "$0")" && pwd)"
personal="$HOME/.claude/CLAUDE.md"

bash "$repo/agentes/instalar.sh"

mkdir -p "$HOME/.claude"
touch "$personal"
if grep -q '^## Zona horaria' "$personal"; then
  echo "Zona horaria: ya estaba en $personal"
else
  [ -s "$personal" ] && cp "$personal" "$personal.bak" && echo "Respaldo: $personal.bak"
  seccion="$(awk '/^## Zona horaria/{f=1; print; next} f && /^#/{exit} f' "$repo/CLAUDE.md" | tr -d '\r' | sed -e :a -e '/^\n*$/{$d;N;ba' -e '}')"
  [ -n "$seccion" ] || { echo "No encontré '## Zona horaria' en $repo/CLAUDE.md" >&2; exit 1; }
  { [ -s "$personal" ] && printf '\n'; printf '%s\n' "$seccion"; } >> "$personal"
  echo "Zona horaria: agregada a $personal"
fi
echo "Listo. Reinicia Claude Code y revisa /agents."
