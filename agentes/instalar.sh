#!/usr/bin/env bash
# Copia los subagentes de esta carpeta a ~/.claude/agents (globales en Claude Code). Uso: bash instalar.sh
set -euo pipefail
origen="$(cd "$(dirname "$0")" && pwd)"
destino="$HOME/.claude/agents"
mkdir -p "$destino"
for n in explorador-haiku.md desarrollador-sonnet.md arquitecto-opus.md lider-fable.md; do
  [ -f "$destino/$n" ] && cp "$destino/$n" "$destino/$n.bak" && echo "Respaldo: $destino/$n.bak"
  cp "$origen/$n" "$destino/$n" && echo "Instalado: $destino/$n"
done
echo "Listo. Reinicia Claude Code y comprueba con /agents."
