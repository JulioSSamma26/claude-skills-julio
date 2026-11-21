# claude-skills-julio

Respaldo privado de las skills de Claude de Julio, consolidadas el 2026-11-21: 62 skills sueltas pasaron a 24, y se sumaron las mejores skills públicas de GitHub (filtradas por licencia y escaneadas).

Cada ZIP es una skill lista para subir en claude.ai → Personalizar → Plugins → Agregar → Subir plugin (o, si ya existe, ⋯ → Subir nueva versión con el mismo ZIP renombrado a `.skill`).

## Skills

| Skill | Qué hace | Origen |
|---|---|---|
| orquestador-skills | Mapa central: elige la skill correcta y aplica el protocolo de seguridad | Propia |
| superpowers | Definir → construir → verificar (incluye la entrevista de requisitos) | Propia |
| desarrollo-codigo | Depurar, TDD, verificar antes de terminar, revisión de PR por pasadas, un subagente por tarea | obra/superpowers, mattpocock/skills, addyosmani/agent-skills, Anthropic |
| ahorro-tokens | Modo conciso, traspaso de sesión, higiene de contexto, escribir skills cortas | caveman, mattpocock/skills, addyosmani, obra + docs de Anthropic |
| excel-datos | Auditar fórmulas, limpiar datos, optimizar DAX | Anthropic financial-services, github/awesome-copilot |
| tienda-ecommerce | Reseñas y reputación, inventario y reabastecimiento | Anthropic knowledge-work-plugins |
| humanizador | Quitar tono de IA conservando datos exactos | Propia |
| verificador-datos | Verificar afirmaciones y auditar fuentes citadas | Propia + alirezarezvani source-audit |
| optimizador-prompts | Prompts listos para usar; prueba A/B y versionado | Propia + alirezarezvani |
| linkedin | Posts, conexiones y DM, comentarios, perfil | Propia (base aldushmedia, MIT) |
| diseno-web | Inspiración de sistemas de diseño y revisión de interfaz | Propia (VoltAgent, Vercel) |
| presupuestos-ffpp | Formularios de precios FF PP de subestaciones | Propia |
| cro, seo, redes-sociales, copywriting, email-marketing, anuncios, contenido, analitica-marketing, estrategia-marketing, growth-saas | Marketing por dominio, cada una con sus módulos | coreyhaines31/marketingskills (v2.14.25) y alirezarezvani/claude-skills |

Sin cambios y solo en claude.ai: oracle-scada-historian, disponibilidad-soe, power-automate-afinia, presentaciones-visuales, marketing-context, youtube-full.

## Diseño para ahorrar tokens

Cada skill fusionada es un **router corto** (`SKILL.md` < 200 líneas) con una tabla "situación → módulo". El método completo vive en `modulos/<nombre>/GUIA.md` y solo se lee el módulo necesario. Así Claude ve una descripción por dominio en vez de varias que compiten.

## Licencias

Todo el contenido de terceros es MIT o Apache-2.0. Cada módulo trae su `LICENSE` y un `FUENTE.md` con repositorio, commit y fecha de escaneo. No se copiaron hooks, CLIs ni componentes con telemetría.

## Archivos

- `zips/` — un ZIP por skill (estructura completa dentro).
- `INFORME.md` — análisis, fusiones, seguridad y pasos aplicados.
- `herramientas/` — scripts que generaron los paquetes.
