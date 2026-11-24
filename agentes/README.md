# Subagentes con modelo fijo (enrutamiento de modelos)

| Subagente | Modelo | Para qué | Herramientas |
|---|---|---|---|
| explorador-haiku | `haiku` | Logs, búsquedas, grep, resumir salidas largas | Read, Grep, Glob (solo lectura) |
| Explore | `haiku` | Reemplaza al Explore de fábrica (que usa el modelo de la sesión); lo llaman el modo Plan y la delegación automática | Read, Grep, Glob (solo lectura) |
| desarrollador-sonnet | `sonnet` | Python, SQL Oracle, VBA, flujos, DAGs | Read, Edit, Write, Grep, Glob, Bash |
| arquitecto-opus | `opus` | Diseño, bug difícil, revisión crítica | Read, Grep, Glob, Bash, Edit |
| lider-fable | `fable` | Proyectos largos que coordinan a los otros tres | Agent(los tres), Read, Grep, Glob, Bash, Edit, Write, TodoWrite |

Regla de uso: skill `ahorro-tokens`, sección "Enrutamiento de modelos". Modelos verificados el 2026-11-23 en platform.claude.com/docs y code.claude.com/docs/en/sub-agents.

## Instalar
- Windows: `powershell -ExecutionPolicy Bypass -File .\instalar.ps1`
- macOS/Linux: `bash instalar.sh`

Luego reinicia Claude Code (los subagentes se cargan al iniciar sesión) y revisa `/agents`. Durante una tarea, `/tasks` muestra el modelo de cada subagente.

## Prueba hecha (2026-11-23, Claude Code 2.1.330, datos ficticios)
| Subagente | Tarea | Modelo real en el registro |
|---|---|---|
| explorador-haiku | Resumir 3 líneas ERROR de un log de 500 | claude-haiku-5-5 ✔ |
| desarrollador-sonnet | suma.py + 2 pruebas unittest (pasan) | claude-sonnet-5-5 ✔ |
| arquitecto-opus | Revisar SQL con f-string: detectó la inyección (`consulta.py:4`) | claude-opus-5-5 ✔ |
| lider-fable (`claude --agent lider-fable`) | Delegó lectura a Haiku y código a Sonnet; tests pasan | claude-fable-5-2 → haiku-5-5 + sonnet-5-5 ✔ |

## Prueba de Explore (2026-11-24, Claude Code 2.1.322, datos ficticios)
Misma tarea (resumir las líneas ERROR de un log de 50), llamando a `Explore` sin el parámetro `model`:

| Sesión principal | Explore de fábrica | Explore propio (`Explore.md`) |
|---|---|---|
| Opus | claude-opus-5-5 (1,18 USD) | claude-haiku-5-5 (0,58 USD) |
| Sonnet | claude-sonnet-5-5 (0,58 USD) | claude-haiku-5-5 (0,29 USD) |

`explorador-haiku` no reemplaza al de fábrica porque tiene otro nombre; por eso existen los dos.

Nota: como subagente, lider-fable solo puede delegar si `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` es ≥ 2 (por defecto 3). Las sesiones en la nube de Claude Code lo fijan en 1; ahí úsalo como agente principal.
