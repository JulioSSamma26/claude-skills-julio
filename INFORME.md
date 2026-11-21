# Optimización de skills: informe (2026-11-21)

## Resultado

| | Antes | Después |
|---|---|---|
| Skills tuyas (subidas a claude.ai) | 62 | **24** |
| Grupos de skills que competían por la misma petición | 14 | 0 |
| Contenido perdido | — | ninguno: las skills antiguas viven como módulos |

Cada fusión de marketing usa **carga progresiva**: el `SKILL.md` es un router corto con una tabla "módulo → cuándo usarlo", y solo lee la guía (`modulos/<nombre>/GUIA.md`) que necesita. Así Claude ve 1 descripción en lugar de 6 y gasta menos contexto.

## Fusiones

### Tus skills propias (reescritas)

| Skill nueva | Absorbe | Mejoras |
|---|---|---|
| **linkedin** | li-post, li-dm, li-reply | + modo Perfil (titular, Acerca de, experiencia); voz de Julio o Maillyn; regla de no filtrar datos de Afinia en posts; las 21 fórmulas pasan a `references/ganchos.md` |
| **superpowers** | superpowers + entrevistador-procesos | Una sola skill de definir → construir → verificar; ya no compiten. Frontera clara con subagent-pool |
| **optimizador-prompts** | optimizador-prompts + prompt-engineer-toolkit | Nivel 2 "producción" (prueba A/B, versionado); consejos de XML para Claude; Higgsfield y Power Automate añadidos |
| **humanizador** | (mejorada) | Limpia caracteres invisibles y rayas; frases comodín en inglés; modo redes/marketing; declara precedencia sobre `ig-human` |
| **diseno-web** | referencias-design-md + web-design-guidelines | Modos Inspirar y Revisar; reglas de Vercel en `references/reglas-interfaz.md` |
| **orquestador-skills** | orquestador + marketing-ops | Mapa nuevo con las fusiones, subagent-pool, graphify, arquitec-dev-ia, instagram-agent, replica-skill, Higgsfield, animate, `/code-review`; resultado del escaneo de seguridad |
| **presupuestos-ffpp** | (mejorada) | La descripción no tenía frases de activación ni línea "NO usar" |

### Skills de marketing de terceros (router + módulos)

| Skill nueva | Módulos |
|---|---|
| **cro** | page-cro, form-cro, popup-cro, signup-flow-cro, onboarding-cro, paywall-upgrade-cro |
| **seo** | seo-audit, schema-markup, site-architecture, programmatic-seo, competitor-alternatives, aeo, local-seo-manager |
| **redes-sociales** | social-content, social-media-manager, social-media-analyzer, x-twitter-growth |
| **copywriting** | copywriting, copy-editing |
| **email-marketing** | cold-email, email-sequence |
| **anuncios** | paid-ads, ad-creative |
| **contenido** | content-strategy, content-production, video-content-strategist |
| **analitica-marketing** | analytics-tracking, campaign-analytics, ab-test-setup |
| **estrategia-marketing** | marketing-strategy-pmm, marketing-demand-acquisition, launch-strategy, marketing-ideas, marketing-psychology, business-name-fit, marketing-ops, ai-decision-authority |
| **growth-saas** | pricing-strategy, churn-prevention, referral-program, free-tool-strategy, webinar-marketing, app-store-optimization |

Mejoras comunes a los 10 routers: responden en español aunque la guía esté en inglés; módulos solo SaaS marcados; textos finales pasan por humanizador; tabla de "nombres antiguos" para que las referencias cruzadas entre guías sigan funcionando; leen el contexto de marketing tanto en la ruta actual (`.claude/product-marketing-context.md`) como en la antigua (`.agents/marketing-context.md`).

### Sin cambios (ya estaban bien)

oracle-scada-historian, disponibilidad-soe, power-automate-afinia, verificador-datos, presentaciones-visuales, marketing-context, youtube-full.

## Seguridad (tu protocolo, aplicado)

Escaneé todos los scripts de las skills fusionadas. Veredicto: **Aprobadas**. Todos usan solo la librería estándar. `page-cro`, `seo-audit`, `site-architecture` y `aeo` descargan solo la URL que se les pasa. `prompt_tester.py` ejecuta sin shell el comando que le das. `citation_tracker.py` solo borra su propio archivo de ejemplo en `~/.aeo-data`. No encontré prompt injection en los markdown.

## Cómo aplicarlo en claude.ai

Estas skills se sincronizan desde tu cuenta, así que **los cambios se hacen en claude.ai**. Si edito la copia local, la próxima sincronización la sobrescribe.

1. claude.ai → Configuración → Capacidades → Skills.
2. **Sube** los 17 ZIP de `zips/`. Si alguna ya existe con el mismo nombre (humanizador, superpowers, optimizador-prompts, orquestador-skills, presupuestos-ffpp, copywriting), reemplázala o bórrala antes de subir la nueva.
3. **Borra o desactiva** estas 49 (ya están dentro de las nuevas):
   - li-post, li-dm, li-reply, entrevistador-procesos, prompt-engineer-toolkit, marketing-ops, referencias-design-md, web-design-guidelines
   - page-cro, form-cro, popup-cro, signup-flow-cro, onboarding-cro, paywall-upgrade-cro
   - seo-audit, schema-markup, site-architecture, programmatic-seo, competitor-alternatives, aeo, local-seo-manager
   - social-content, social-media-manager, social-media-analyzer, x-twitter-growth
   - copy-editing, cold-email, email-sequence, paid-ads, ad-creative
   - content-strategy, content-production, video-content-strategist
   - campaign-analytics, analytics-tracking, ab-test-setup
   - marketing-strategy-pmm, marketing-demand-acquisition, launch-strategy, marketing-ideas, marketing-psychology, business-name-fit, ai-decision-authority
   - pricing-strategy, churn-prevention, referral-program, free-tool-strategy, webinar-marketing, app-store-optimization
4. Prueba de humo en un chat nuevo: "mi landing no convierte" → debería anunciar `cro → page-cro`; "escribe un post de LinkedIn sobre X" → `linkedin`, modo A.

Recomendación: primero **desactiva** las 49 en vez de borrarlas, y bórralas cuando las nuevas lleven una semana funcionando.

## Otras recomendaciones (no aplicadas)

**Skills de Anthropic que puedes desactivar** porque no encajan con tu trabajo y añaden ruido al elegir skill: `brand-guidelines` (aplica la marca de Anthropic, no la tuya), `slack-gif-creator`, `algorithmic-art`, `morning`.

**Plugins con solapamiento que no se pueden fusionar** (son de terceros y se actualizan solos). El orquestador ya decide entre ellos:
- `instagram-agent:ig-human` ↔ humanizador → gana humanizador.
- `instagram-agent:ig-reply` / `ig-dm` ↔ linkedin → linkedin solo para LinkedIn; ig-* para Instagram.
- `engineering:code-review` ↔ `/code-review` integrado → `/code-review` para diffs y PR; engineering para scripts sueltos.
- `data:create-viz` ↔ `data:data-visualization` ↔ `dataviz` → create-viz principal, dataviz de apoyo.

**Skills locales** (subagent-pool, graphify, arquitec-dev-ia). Son paquetes versionados de terceros (elisaul77 / eliflowi), así que no los reescribí: la próxima actualización pisaría los cambios. Ajustes sugeridos:
- `arquitec-dev-ia`: la carpeta se llama `arquitec-dev-ia` pero el `name` es `arquitect-dev-ia`; conviene igualarlos. Además su trigger "create a skill" choca con skill-creator y superpowers: quitarlo.
- `graphify`: la descripción "any question about a codebase" es muy amplia y puede activarse para preguntas simples. Conviene limitarla a cuando existe `graphify-out/` o se pide un mapa del proyecto.
- `subagent-pool` (6.600 palabras) y `graphify` (6.300 palabras) son muy largas para cargarse enteras. Si las mantienes tú, mover secciones a `references/` reduciría el contexto a la mitad.

## Fase 2: lo mejor de GitHub (2026-11-21)

Aplicado en claude.ai el mismo día: 49 skills antiguas desactivadas (reversible), 15 subidas nuevas y 13 reemplazadas con "Subir nueva versión" (cada una conserva su historial).

**Skills nuevas**

| Skill | Módulos (fuente, licencia) |
|---|---|
| desarrollo-codigo | diagnosing-bugs, tdd (mattpocock/skills, MIT) · systematic-debugging, verification-before-completion, receiving-code-review, subagent-driven-development (obra/superpowers, MIT) · doubt-driven-development (addyosmani/agent-skills, MIT) · pr-review-toolkit (Anthropic, Apache-2.0) |
| ahorro-tokens | caveman (Apache-2.0, solo el texto) · writing-for-agents, handoff (mattpocock, MIT) · context-engineering (addyosmani, MIT) · writing-skills (obra, MIT) + reglas oficiales de Anthropic |
| excel-datos | audit-xls, clean-data-xls (anthropics/financial-services, Apache-2.0) · power-bi-dax-optimization (github/awesome-copilot, MIT) |
| tienda-ecommerce | review-reputation, inventory-planner + shared (anthropics/knowledge-work-plugins v1.35.2, Apache-2.0), adaptada a COP, Dropi y dropshipping |

**Skills mejoradas:** verificador-datos (+ modo auditoría de fuentes, alirezarezvani source-audit), orquestador-skills v3 (mapa con las nuevas), y 9 módulos nuevos de coreyhaines31/marketingskills v2.14.25: conversion-tracking → analitica-marketing; offers, marketing-loops, public-relations → estrategia-marketing; influencer-marketing → redes-sociales; link-building → seo; sms, prospecting, lead-magnets → email-marketing.

**Seguridad:** todos los archivos copiados se escanearon (red, ejecución, ofuscación, inyección de instrucciones, caracteres invisibles). Hallazgos legítimos: snippets de GTM para el sitio propio, ejemplos `curl` a RSS públicos, scripts bash locales con git. Descartado a propósito: CLI/hooks/telemetría de caveman, hook de inicio de sesión de obra/superpowers, repos GPL-3.0 o PolyForm (token-optimizer, data-goblin, context-engineering-kit), oracle/skills (licencia UPL, pendiente de tu decisión), wrappers "*-automation" de Composio y registros ClawHub/skills.sh (Snyk encontró 13,4 % con problemas críticos). Tu youtube-full ya es la versión segura.

**No hecho en la fase 2** (resuelto en la fase 3): módulos antiguos de marketing. Las skills de LinkedIn de alirezarezvani (lint de posts, guardián de políticas) quedaron fuera.

## Fase 3: marketing actualizado a Corey Haines v2.14.25 (2026-11-21)

Los módulos antiguos eran Alireza Rezvani v1.0.0 (marzo 2026), casi todos derivados de la v1 de Corey. Ahora **45 de 57 módulos** vienen de Corey v2.14.25 (commit 5b2b400, 2026-11-19). Las 10 skills se subieron con "Subir nueva versión" (cada una guarda su historial).

| Skill | Cambios |
|---|---|
| cro | page-cro + form-cro → `cro`; popup-cro → `popups`; signup-flow-cro → `signup`; onboarding-cro → `onboarding`; paywall-upgrade-cro → `paywalls` |
| seo | seo-audit, schema, site-architecture, programmatic-seo, competitors, link-building (v2); aeo → `ai-seo` (Corey, con preparación para agentes); local-seo-manager se conserva |
| redes-sociales | social-content y social-media-manager → `social`; + `community-marketing`; se conservan social-media-analyzer y x-twitter-growth |
| copywriting | copywriting y copy-editing v2 (incluyen la lista de "AI tells") |
| email-marketing | cold-email v2; email-sequence → `emails` |
| anuncios | paid-ads → `ads`; ad-creative v2 (plantilla de revisión sin imágenes remotas) |
| contenido | content-strategy v2; + `video` y `image` (producción con IA o código); se conservan content-production y video-content-strategist |
| analitica-marketing | analytics-tracking → `analytics`; ab-test-setup → `ab-testing`; + `attribution`; se conserva campaign-analytics (scripts de ROI) |
| estrategia-marketing | launch-strategy → `launch`; marketing-ideas y marketing-psychology v2; + `marketing-plan`, `customer-research`, `competitor-profiling`; se conservan pmm, demand-acquisition, business-name-fit, marketing-ops, ai-decision-authority |
| growth-saas | pricing-strategy → `pricing`; churn-prevention v2; referral-program → `referrals`; free-tool-strategy → `free-tools`; app-store-optimization → `aso`; se conserva webinar-marketing |

**Seguridad:** los módulos de Corey son solo texto (más carpetas `evals/` de pruebas que los routers mandan a ignorar). Algunas guías sugieren ejecutar `npx` (Remotion, Hyperframes, Playwright, is-agentic) o APIs con clave: los routers ahora exigen preguntar antes y revisar el paquete. Sin URLs remotas en plantillas, sin caracteres invisibles ni inyección de instrucciones.

**Descartadas de Corey v2** por no aplicar a tus negocios: sales-enablement, revops, co-marketing, events, directory-submissions, marketing-council, reverse-engineer-marketing, product-marketing (lo cubre la skill marketing-context).

**Verificación:** la sincronización local ya muestra solo tus 28 skills activas (más las 23 de Anthropic), sin las 49 desactivadas. claude.ai muestra cada skill de marketing en su nueva versión, por ejemplo "Cro v2 · actual" con 29 archivos.

## Fase 4: verificación de repositorios mundiales y mejoras aplicadas (2026-11-21)

Detalle de la investigación en `VERIFICACION-REPOSITORIOS.md`.

**Skills nuevas:**
- **airflow-docker:** astronomer/agents y docker/skills, ambos Apache-2.0.
- **ot-ciberseguridad:** mukul975, Apache-2.0. Solo el texto; los scripts se omitieron.
- **freelance-propuestas:** rondoflow, MIT, adaptada a COP y Colombia.
- **edicion-fotos:** propia. La idea viene de un reel de @academiaagentica; los comandos son /identitylock, /studioquality, /upscale, /cleanup, /fondoblanco, /lifestyle y /miniatura, sobre Higgsfield y Canva.

**Skills mejoradas:**
- **oracle-scada-historian v3:** suma las guías oficiales de Oracle (UPL-1.0) de rendimiento y PL/SQL, cada una marcada según si aplica o no a la 9i.
- **power-automate-afinia v3:** suma las reglas de Microsoft para construir y depurar flujos (MIT).
- **excel-datos v2:** suma tres módulos de Power BI: modelo, rendimiento y diseño (MIT).
- **orquestador-skills v8:** mapa actualizado y skill-security-auditor (MIT) integrado en el protocolo de seguridad.

**Plugins agregados**, todos revisados por Anthropic: session-report, security-guidance (en `settings.json` quedó `ENABLE_CODE_SECURITY_REVIEW=0` para conservar solo la capa de regex), claude-md-management, hookify y pyright-lsp.

**Conectores:**
- Agregados: Microsoft Learn y Context7.
- Pendientes de que inicies sesión tú: Meta Ads (oficial, `https://mcp.facebook.com/ads`), TikTok for Business, vidIQ y Typefully.
- TradingNote quedó desconectado; se puede volver a conectar.

**Ajustes de Claude Code (`~/.claude/settings.json`)**, con respaldo en `settings.json.bak-20261121`:
- `skillListingBudgetFraction` 0.02.
- `skillOverrides` en `"name-only"` para 7 skills de poco uso.
- `bashOutputMaxChars` en 15000.
- `deniedMcpServers` bloquea 10 conectores sin autenticar o que fallan: BigQuery, Hex, Amplitude EU, Atlassian, Definite, Slack, Asana, PagerDuty, Datadog y el GitHub duplicado.

**Pendiente de tu decisión:** otra sesión habilitó el plugin de terceros `cc-safety-net` (marketplace `kenryu42/cc-safety-net`, MIT). Tiene un hook PreToolUse que bloquea comandos destructivos. No está revisado por Anthropic ni por un socio.

## Fase 5: fusiones desde ECC (2026-11-21)

El análisis completo está en `ecc-fusion.md` (affaan-m/ECC v2.2.3, MIT, commit 4adeee6). **ECC no se instaló.** Se tomaron 9 ideas, reescritas en español y adaptadas al entorno de Julio, con referencia a la fuente en cada skill.

| Skill (versión en claude.ai) | Qué se añadió |
|---|---|
| desarrollo-codigo v2 | Portón de hechos antes de editar un archivo (quién lo usa, qué cambia hacia fuera, esquema real de los datos, instrucción citada), una línea de vuelta atrás antes de comandos destructivos, línea "Destino: VERIFICADO / FALLÓ / NO REALIZADO / NO APLICA" y revisión rápida de Python |
| ahorro-tokens v2 | Traspaso con callejones sin salida, lo no probado y el siguiente paso exacto; cuándo compactar y guardar el plan en un archivo antes de hacerlo |
| superpowers v4 | Buscar antes de construir; línea de verificación en el destino |
| orquestador-skills v9 | En el protocolo: versiones e imágenes sin fijar, `ANTHROPIC_BASE_URL`, `enableAllProjectMcpServers`, caracteres invisibles, contenido externo tratado como dato y auditoría trimestral de skills |
| airflow-docker v2 | Seguridad de contenedores |
| oracle-scada-historian v4 | Reglas de calidad SQL: bind, sin `SELECT *`, paginación por clave en 9i |
| contenido v3, redes-sociales v4 | Antes de publicar un video: divulgación de contenido hecho con IA, promoción pagada y "contenido para niños" (COPPA) |

**Pendiente, a confirmar con Julio:** las 3 reglas de hookify (bloquear SQL de escritura contra Oracle, credenciales escritas en el código y edición de configuraciones de linters) y las filas 7 a 19 de `ecc-fusion.md` que no se aplicaron.

**Nota:** cc-safety-net bloqueó la primera escritura por un falso positivo (el texto mencionaba el nombre del archivo de variables de entorno). Se resolvió cambiando la redacción, sin desactivar el plugin.
