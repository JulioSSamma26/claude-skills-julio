# Verificación de repositorios mundiales para potenciar tu Claude (2026-11-21)

**Fuentes revisadas:** directorio oficial de Claude (3.779 plugins; solo 468 revisados: 94 por Anthropic y 374 por socios), registro oficial de MCP, GitHub, VoltAgent, awesome-claude-code, skillsmp, marketplaces en otros idiomas, y documentación de Microsoft, Oracle, Meta, Google, Astronomer y Docker. Los datos críticos los verifiqué yo mismo en la fuente original.

**Tu situación hoy:** 28 skills propias + 23 de Anthropic + unas 60 de plugins + 3 locales; 14 conectores activos.

---

## 1. Hacer ya: bajo riesgo, alto impacto

### 1.1 Ajustes de Claude Code (no instalan nada)
Verificado en la documentación oficial (code.claude.com/docs/en/skills):

- Por defecto, la lista de skills solo ocupa **1 % del contexto**. Con más de 110 skills, las descripciones probablemente se están recortando, y Claude elige peor.
  - **`skillListingBudgetFraction: 0.02`** (sube ese tope al 2 %).
- **`skillOverrides`** → `"name-only"` para las skills que casi no usas. Se listan sin descripción y liberan espacio para las importantes.
- **Desactivar plugins cuando no los uses:** open-higgsfield (~40 skills de video), animate y replica-skill. Se reactivan con `/plugin`.
- Un **hook PreToolUse** que recorte salidas largas de comandos (últimas 100 líneas) es el ejemplo oficial de la página "costs".

### 1.2 Conectores nuevos (solo datos personales o públicos)
| Conector | Para qué te sirve | Estado |
|---|---|---|
| **Microsoft Learn** | Documentación al día de Power Automate, SharePoint, Excel/VBA, WSL | Oficial de Microsoft, sin login |
| **Context7** | Documentación al día de Airflow, python-oracledb, pandas, Docker | Revisado por socio (Upstash) |
| **Meta Ads** (`mcp.facebook.com/ads`) | Reportes y campañas de Mascotas Seguras | **Oficial de Meta, verificado**. Puede gastar dinero: aprueba cada cambio |
| **TikTok for Business** | Campañas de TikTok | Oficial, en el directorio |
| **vidIQ** | Palabras clave y videos que destacan para el canal infantil | Revisado por socio |
| **Typefully** | Programar posts de LinkedIn (LinkedIn no tiene conector oficial) | En el directorio |

### 1.3 Plugins revisados por Anthropic
| Plugin | Para qué | Nota |
|---|---|---|
| **session-report** | Informe local de dónde se van tus tokens: subagentes, skills, prompts más caros | Lee solo archivos locales |
| **security-guidance** | Avisos de seguridad al editar código (inyección, secretos en código, etc.) | Deja solo la capa regex (`ENABLE_CODE_SECURITY_REVIEW=0`) para no gastar tokens |
| **claude-md-management** | Mantener tus CLAUDE.md cortos y al día | Complementa a arquitec-dev-ia |
| **hookify** | Convertir reglas ("no tocar .env", "no editar DAGs de producción") en hooks | Tú revisas cada hook |
| **pyright-lsp** | Revisión de tipos en Python; menos idas y vueltas | |

### 1.4 Skills para fusionar en las tuyas
| Fuente (licencia) | Qué aporta | Dónde va |
|---|---|---|
| **oracle/skills** (UPL-1.0, permisiva) | Ajuste de SQL y PL/SQL: plan de ejecución, índices, cursores, manejo de errores | Referencias de **oracle-scada-historian**, marcadas "solo 12c+" (no aplica a 9i) |
| **astronomer/agents** + **docker/skills** (Apache-2.0, oficiales) | Escribir, probar y depurar DAGs; Docker Compose; protecciones contra comandos destructivos | Nueva skill **airflow-docker** |
| **github/awesome-copilot** + **microsoft/skills-for-fabric** (MIT) | Revisión de modelos, rendimiento y diseño de reportes en Power BI | Módulos de **excel-datos** |
| **mukul975/Anthropic-Cybersecurity-Skills** (Apache-2.0, 36k ⭐) | Seguridad OT: zonas IEC 62443, detección de ataques a SCADA, respuesta a incidentes | Nueva skill **ot-ciberseguridad** (solo texto, sin sus scripts) |
| **rondoflow** (MIT) | Propuestas, contratos y NDA para freelance | Nueva skill **freelance-propuestas**, adaptada a COP y Colombia |
| **microsoft/power-platform-skills** (MIT) | Patrones de flujos ("nunca adivinar parámetros del conector") | Reglas para **power-automate-afinia** |
| **alirezarezvani skill-security-auditor** (MIT) + **Cisco skill-scanner** (Apache-2.0, modo offline) | Escanear skills antes de instalarlas | Herramienta del **orquestador** |

---

## 2. Requiere aprobación de TI de Afinia (no lo hagas por tu cuenta)

| Conector | Por qué es delicado |
|---|---|
| **Microsoft 365** (Outlook, Teams, SharePoint) | Necesita consentimiento del administrador del tenant; todo lo que ves pasa por Anthropic |
| **Oracle SQLcl MCP** | Los resultados del historiador saldrían del entorno. **No funciona con Oracle 9i (SGDPROD)**. Desde la versión 26.1.2 arranca sin restricciones |
| **Power BI remoto** | Datos corporativos |
| **Airflow MCP (Astronomer)** | Las conexiones guardan credenciales Oracle; solo con usuario de lectura |

Mientras tanto, sigue con tu skill **oracle-scada-historian** en Python local y comparte con Claude solo resultados agregados o anonimizados.

---

## 3. Limpiar (gastan contexto sin aportar)

- **TradingNote:** tu plan gratuito no expone datos. Quitarlo.
- **9 conectores de plugins sin autenticar** en Claude Code: Amplitude, BigQuery, Hex, Atlassian, Asana, Datadog, PagerDuty, Slack, Linear. **definite** falla al conectar.
- **Duplicados:** GitHub y Notion están en el plugin engineering y además como conector. Deja uno de cada uno.
- **n8n-mcp** (comunitario): tuvo 4 avisos de seguridad en 2026 (SSRF, secretos en logs). Usa el MCP oficial integrado de n8n, o al menos la versión 2.57.4 o superior.
- **Higgsfield:** úsalo solo para video. Para anuncios usa los conectores oficiales de Meta y TikTok, así tu cuenta publicitaria no pasa por un tercero.

---

## 4. Evitar

- **claude-mem:** licencia AGPL más no comercial, y telemetría activa por defecto.
- **Plugins de "ahorro de tokens" no revisados** (token-saver, AgentOne, Token Shield): prometen 60–90 % sin pruebas. Un benchmark independiente midió 8,5 % para caveman.
- **Registros ClawHub y skills.sh:** Snyk encontró problemas críticos en el 13,4 % de las skills.
- **Servidores MCP comunitarios de Oracle o de WhatsApp Web:** sacan datos o violan los términos de WhatsApp (riesgo de que bloqueen el número).
- **data-goblin (Power BI):** GPL-3.0 y hooks automáticos. Solo como ideas.
- **FlowStudio (Power Automate):** los flujos de Afinia pasarían por un servidor pago de terceros.
- **Blaze SQL, Desktop Commander, agregadores de anuncios** (Adspirer, Windsor): demasiado acceso o redundantes.
- **Incidentes documentados:** postmark-mcp falso (copiaba correos), typosquat de mcp-server-github, gusano SANDWORM_MODE, CVE-2025-6514 en mcp-remote (usa la versión 0.1.16 o superior).

**Alerta verificada (29 oct 2026):** una copia troyanizada de la extensión de Claude Code (2.1.312/313) se publicó en el marketplace de **Cursor** e instalaba una puerta trasera SSH. **Tu PC no está afectado:** no tienes Cursor, no existe `authorized_keys` y tu extensión de VS Code es la 2.1.328–2.1.330. Instala Claude Code solo desde canales oficiales.

---

## 5. Huecos donde no existe nada bueno: construir en casa

- Índices **SAIDI/SAIFI** e indicadores CREG (sobre disponibilidad-soe).
- Ingeniería de protocolos **IEC 60870-5-104 / 61850 / DNP3**: listas de puntos, calidad del time-stamp, mapeo a Spectrum Power 7.
- Racionalización de alarmas **ISA-18.2** con datos del historiador: avalanchas, alarmas que se repiten, alarmas permanentes.
- Detalles de **Oracle 9i** (todo lo público empieza en 19c).
- **Facturación electrónica DIAN** e impuestos en Colombia.
- **Dropshipping contraentrega con Dropi** y comercio por WhatsApp cumpliendo las reglas.
- **Cumplimiento de canal infantil** en YouTube (madeForKids / COPPA).
