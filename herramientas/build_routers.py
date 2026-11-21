"""Construye skills fusionadas (router + modulos) a partir de las skills sincronizadas."""
import glob, os, shutil, sys

COREY = r"D:/Users/jcanchan/AppData/Local/Temp/claude/ac62046613747adb/353b38c1-82b2-4f8f-b911-872b4e2788c7/scratchpad/descargas/corey/skills"
SRC = glob.glob(os.path.expanduser("~/.claude/skills/synced/*/"))[0]
OUT = sys.argv[1]

COMMON = """
## Reglas comunes

- **Contexto primero:** si existe `.agents/product-marketing.md`, `.claude/product-marketing-context.md` o `.agents/marketing-context.md`, léelo antes de empezar. Si no existe y la tarea es de estrategia, sugiere una vez la skill `marketing-context`; para tareas pequeñas, sigue sin él.
- **Carga mínima:** lee solo `modulos/<modulo>/GUIA.md` del módulo elegido (máximo 2 módulos por tarea). Las rutas que aparecen dentro de cada guía (`references/`, `scripts/`, `assets/`, `templates/`) son relativas a la carpeta de ese módulo.
- **Idioma:** responde en el idioma del usuario (español por defecto) aunque la guía esté en inglés. Adapta ejemplos a Colombia/LatAm cuando aplique (COP, WhatsApp, Mercado Libre, Instagram).
- **Datos:** nunca inventes métricas, clientes ni resultados; si falta un número, déjalo como `{{dato}}` y pídelo.
- **Scripts de terceros** (revisados el 2026-11-21: solo librería estándar, sin exfiltración): ejecútalos con `python -I`, con datos ficticios o del proyecto de marketing, nunca con datos de Afinia. Los que aceptan URL solo descargan la URL que se les pasa.
- **Textos finales** que se van a publicar: pásalos por `humanizador` antes de entregarlos.

## Nombres antiguos (las guías pueden citarlos)

Si una guía dice "usa la skill X", traduce X a la skill actual:

| Nombre antiguo | Skill actual |
|---|---|
| page-cro, form-cro, popup-cro, signup-flow-cro, onboarding-cro, paywall-upgrade-cro | `cro` |
| seo-audit, schema-markup, site-architecture, programmatic-seo, competitor-alternatives, aeo, ai-seo, local-seo-manager | `seo` |
| social-content, social-media-manager, social-media-analyzer, x-twitter-growth | `redes-sociales` |
| copywriting, copy-editing | `copywriting` |
| cold-email, email-sequence | `email-marketing` |
| paid-ads, ad-creative | `anuncios` |
| content-strategy, content-production, content-creator, video-content-strategist | `contenido` |
| analytics-tracking, campaign-analytics, ab-test-setup | `analitica-marketing` |
| marketing-strategy-pmm, marketing-demand-acquisition, launch-strategy, marketing-ideas, marketing-psychology, business-name-fit, marketing-ops, ai-decision-authority | `estrategia-marketing` |
| pricing-strategy, churn-prevention, referral-program, free-tool-strategy, webinar-marketing, app-store-optimization | `growth-saas` |
| ads, ad-creative | `anuncios` |
| emails, cold-email, sms, prospecting, lead-magnets | `email-marketing` |
| social, influencer-marketing | `redes-sociales` |
| pricing, offers | `growth-saas` (precios) / `estrategia-marketing` (ofertas) |
| ai-seo, link-building, directory-submissions | `seo` |
| video, image | `contenido` / `optimizador-prompts` |
| conversion-tracking, analytics | `analitica-marketing` |
| marketing-plan, marketing-loops, public-relations, competitor-profiling, marketing-council | `estrategia-marketing` |
| content-humanizer, ai-tells | `humanizador` |
| prompt-engineer-toolkit | `optimizador-prompts` |

Una skill citada que no está en la tabla ni instalada (p. ej. `customer-research`, `sales-enablement`): sigue sin ella.
"""

ROUTERS = {
 "cro": {
  "title": "CRO: optimización de conversión",
  "desc": "Optimiza la conversión de cualquier punto del embudo: landing y páginas de venta, formularios, popups, registro, onboarding/activación y paywalls o pantallas de upgrade. Úsala con \"mejora la conversión\", \"mi landing no convierte\", \"revisa este formulario\", \"popup\", \"onboarding\", \"paywall\", CRO, conversion rate. NO usar para escribir copy desde cero (usar copywriting) ni para tests A/B (usar analitica-marketing).",
  "mods": [
   ("page-cro", "Cualquier página de marketing: home, landing, precios, producto, venta.", ""),
   ("form-cro", "Formularios que NO son de registro: leads, contacto, demo, cotización, checkout.", ""),
   ("popup-cro", "Popups, modales, slide-ins, barras, exit-intent.", ""),
   ("signup-flow-cro", "Registro, creación de cuenta, inicio de prueba.", "SaaS"),
   ("onboarding-cro", "Primera experiencia tras registrarse, activación, time-to-value.", "SaaS"),
   ("paywall-upgrade-cro", "Paywalls, upsell dentro de la app, feature gates.", "SaaS"),
  ]},
 "seo": {
  "title": "SEO: posicionamiento orgánico y en IAs",
  "desc": "Todo el SEO en una skill: auditoría técnica y on-page, datos estructurados (schema), arquitectura y enlazado interno, SEO programático, páginas de comparación con competidores, AEO (que ChatGPT/Perplexity/Claude te citen) y SEO local con Google Business Profile. Úsala con \"auditoría SEO\", \"por qué no posiciono\", \"schema\", \"estructura del sitio\", \"páginas alternativa a X\", \"aparecer en ChatGPT\", \"SEO local\", \"Google Maps\", \"backlinks\". NO usar para escribir el artículo en sí (usar contenido).",
  "mods": [
   ("seo-audit", "Auditoría técnica/on-page, Core Web Vitals, E-E-A-T, \"por qué no posiciono\".", ""),
   ("schema-markup", "Implementar o validar datos estructurados JSON-LD.", ""),
   ("site-architecture", "Jerarquía de URLs, navegación, enlazado interno, sitemap.", ""),
   ("programmatic-seo", "Páginas a escala desde plantillas y datos.", ""),
   ("competitor-alternatives", "Páginas \"X vs Y\" y \"alternativas a X\".", ""),
   ("aeo", "Que las IAs (ChatGPT, Perplexity, Claude, Gemini) citen el sitio.", ""),
   ("local-seo-manager", "Negocio local o de servicio a domicilio, Google Business Profile, reseñas, NAP.", ""),
   ("link-building", "Conseguir enlaces entrantes (backlinks) de calidad.", "", COREY),
  ]},
 "redes-sociales": {
  "title": "Redes sociales: estrategia, contenido y métricas",
  "desc": "Estrategia, calendario, publicaciones y métricas para Facebook, TikTok, Instagram (general) y X/Twitter. Úsala con \"plan de redes\", \"calendario de contenido\", \"post para TikTok/Facebook\", \"analiza mis métricas de redes\", \"crecer en X\", engagement, influencers, gifting, embajadores. NO usar para LinkedIn (usar linkedin) ni para piezas concretas de Instagram como reels, carruseles, stories o perfil (usar el plugin instagram-agent: ig-reel, ig-carousel, ig-story, ig-profile).",
  "mods": [
   ("social-media-manager", "Estrategia de redes, comunidad, calendario editorial.", ""),
   ("social-content", "Crear o reciclar publicaciones por plataforma.", ""),
   ("social-media-analyzer", "Calcular engagement, ROI y comparar con benchmarks.", ""),
   ("x-twitter-growth", "Crecer en X/Twitter: hilos, perfil, algoritmo.", ""),
   ("influencer-marketing", "Programas con creadores, afiliados, envío de producto (gifting) y embajadores.", "", COREY),
  ]},
 "copywriting": {
  "title": "Copywriting: escribir y corregir textos de marketing",
  "desc": "Escribe o corrige textos de marketing para páginas (home, landing, precios, producto, \"sobre nosotros\"), titulares, CTAs y perfiles. Dos modos: escribir desde cero y editar/pulir un texto existente. Úsala con \"escribe el copy\", \"mejora este texto de venta\", \"titular\", \"revisa mi copy\", \"copy feedback\". NO usar para anuncios (usar anuncios), correos (usar email-marketing) ni para quitar tono de IA a un texto cualquiera (usar humanizador).",
  "mods": [
   ("copywriting", "Escribir o reescribir copy de una página o pieza.", ""),
   ("copy-editing", "Revisar y pulir un copy existente (claridad, legibilidad, tono).", ""),
  ]},
 "email-marketing": {
  "title": "Email marketing: prospección y secuencias",
  "desc": "Correos en frío B2B para prospectar clientes (freelance, servicios) y secuencias automatizadas: bienvenida, nurturing, carrito abandonado, reactivación, lifecycle. Úsala con \"correo en frío\", \"prospección\", \"secuencia de correos\", \"drip\", \"email de bienvenida\", SMS/WhatsApp de carrito abandonado, listas de prospectos y lead magnets. NO usar para correos de trabajo en Afinia (usar humanizador / internal-comms) ni para DMs de LinkedIn (usar linkedin).",
  "mods": [
   ("cold-email", "Correos en frío a quien no te conoce, y sus seguimientos.", ""),
   ("email-sequence", "Secuencias automatizadas a suscriptores o clientes.", ""),
   ("sms", "Campañas y flujos por SMS/WhatsApp (carrito abandonado, recordatorios) con consentimiento.", "", COREY),
   ("prospecting", "Armar listas de prospectos y enriquecerlas legalmente para el trabajo freelance.", "", COREY),
   ("lead-magnets", "Crear el gancho gratuito (guía, plantilla, checklist) que capta correos.", "", COREY),
  ]},
 "anuncios": {
  "title": "Anuncios pagados: campañas y creatividades",
  "desc": "Campañas pagadas en Meta (Facebook/Instagram), Google Ads, TikTok y LinkedIn: estructura, segmentación, presupuesto y optimización, más el texto y variaciones de los anuncios. Úsala con \"campaña de Meta\", \"Google Ads\", \"textos para anuncios\", \"headlines\", \"ROAS\", \"mis anuncios no venden\". NO usar para medir resultados de varias campañas (usar analitica-marketing).",
  "mods": [
   ("paid-ads", "Estrategia, estructura, segmentación y optimización de campañas.", ""),
   ("ad-creative", "Escribir y escalar textos y conceptos de anuncios.", ""),
  ]},
 "contenido": {
  "title": "Contenido: estrategia, producción y video",
  "desc": "Planifica y produce contenido: estrategia y temas (clusters), artículos/blog/guiones escritos de principio a fin, y estrategia de video para YouTube, Shorts, Reels y TikTok (incluido el canal infantil). Úsala con \"plan de contenidos\", \"sobre qué escribir\", \"escribe un artículo\", \"guion de video\", \"estrategia de YouTube\". NO usar para transcripciones o datos de YouTube (usar youtube-full) ni para posts sueltos de redes (usar redes-sociales).",
  "mods": [
   ("content-strategy", "Decidir qué contenido crear, pilares y clusters de temas.", ""),
   ("content-production", "Llevar una pieza escrita de cero a lista para publicar.", ""),
   ("video-content-strategist", "Estrategia de canal, guiones de video, pipeline de short-form.", ""),
  ]},
 "analitica-marketing": {
  "title": "Analítica de marketing: medición, atribución y experimentos",
  "desc": "Mide marketing: tracking (GA4, Google Tag Manager, eventos, conversiones), atribución multi-touch, ROI/ROAS/CPA por canal y diseño de tests A/B con tamaño de muestra. Úsala con \"configura GA4\", \"Pixel de Meta\", \"API de conversiones\", \"no me cuentan las conversiones\", \"cuál canal rinde más\", \"ROI de campañas\", \"test A/B\". NO usar para análisis de datos de Afinia o genéricos (usar data:analyze).",
  "mods": [
   ("analytics-tracking", "Montar, auditar o depurar tracking (GA4, GTM, eventos).", ""),
   ("campaign-analytics", "Atribución, embudo, ROI y comparación de canales.", ""),
   ("ab-test-setup", "Planificar un experimento A/B y su tamaño de muestra.", ""),
   ("conversion-tracking", "Instalar o auditar Pixel de Meta, API de conversiones (CAPI), GA4 y etiquetas de Google/TikTok para ecommerce y formularios.", "", COREY),
  ]},
 "estrategia-marketing": {
  "title": "Estrategia de marketing: posicionamiento, demanda y lanzamientos",
  "desc": "Estrategia de marketing de punta a punta: posicionamiento y mensajes (PMM), generación de demanda y CAC, lanzamientos, ideas de marketing, psicología de compra, nombre de marca, campañas multicanal y qué decisiones delegar a la IA. Úsala con \"posicionamiento\", \"estrategia de marketing\", \"cómo lanzo\", \"ideas para vender más\", \"nombre para mi marca\", \"plan de campaña\", \"arma la oferta\", \"bonos y garantía\", \"nota de prensa\". NO usar para piezas concretas (usar copywriting, anuncios, contenido) ni para negocios SaaS de precios/churn (usar growth-saas).",
  "mods": [
   ("marketing-strategy-pmm", "Posicionamiento, ICP, mensajes, GTM, inteligencia competitiva.", ""),
   ("marketing-demand-acquisition", "Generación de demanda, mezcla de canales, CAC, partnerships.", ""),
   ("launch-strategy", "Lanzar un producto o funcionalidad.", ""),
   ("marketing-ideas", "Lluvia de ideas y tácticas de marketing.", ""),
   ("marketing-psychology", "Sesgos y modelos mentales aplicados a vender.", ""),
   ("business-name-fit", "Proponer o validar el nombre de un negocio o producto.", ""),
   ("marketing-ops", "Coordinar una campaña que usa varias disciplinas a la vez.", ""),
   ("ai-decision-authority", "Decidir qué decisiones de marketing puede tomar la IA y cuáles no.", ""),
   ("offers", "Diseñar la oferta: ecuación de valor, bonos, garantías, escasez honesta (tienda, servicios freelance).", "", COREY),
   ("marketing-loops", "Rutinas recurrentes de marketing (semanales/mensuales) que se retroalimentan.", "", COREY),
   ("public-relations", "Prensa y medios ganados: pitch a periodistas, newsjacking, notas de prensa.", "", COREY),
  ]},
 "growth-saas": {
  "title": "Growth para software y suscripciones",
  "desc": "Palancas de crecimiento para productos de software o suscripción: precios y planes, reducción de churn y dunning, programas de referidos/afiliados, herramientas gratuitas como marketing, webinars y App Store Optimization. Úsala con \"cuánto cobro\", \"planes de precio\", \"cancelaciones\", \"churn\", \"programa de referidos\", \"webinar\", \"ASO\". Referidos y webinars sirven también para otros negocios. NO usar para dropshipping o el canal infantil salvo referidos/webinars.",
  "mods": [
   ("pricing-strategy", "Estructura de planes, métrica de valor, página de precios, subidas de precio.", "SaaS"),
   ("churn-prevention", "Flujo de cancelación, ofertas de retención, pagos fallidos.", "SaaS"),
   ("referral-program", "Diseñar o mejorar un programa de referidos o afiliados.", ""),
   ("free-tool-strategy", "Crear una herramienta gratis para captar leads o SEO.", ""),
   ("webinar-marketing", "Planear, promover y convertir con un webinar o evento virtual.", ""),
   ("app-store-optimization", "Palabras clave, metadatos y visibilidad en App Store / Google Play.", "SaaS"),
  ]},
}


def build():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    for name, r in ROUTERS.items():
        assert len(r["desc"]) <= 1024, (name, len(r["desc"]))
        root = os.path.join(OUT, name)
        rows = []
        for m in r["mods"]:
            mod, when, tag = m[:3]
            base = m[3] if len(m) > 3 else SRC
            src = os.path.join(base, mod)
            dst = os.path.join(root, "modulos", mod)
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".claude-plugin"))
            os.rename(os.path.join(dst, "SKILL.md"), os.path.join(dst, "GUIA.md"))
            if base == COREY:
                shutil.copy(os.path.join(COREY, "..", "LICENSE"), os.path.join(dst, "LICENSE"))
                open(os.path.join(dst, "FUENTE.md"), "w", encoding="utf-8").write("Fuente: github.com/coreyhaines31/marketingskills (MIT), v2.14.25, commit 5b2b400, descargado y escaneado el 2026-11-21.\n")
            label_src = " *(nuevo 2026-11)*" if base == COREY else ""
            label = f"{when} **(solo SaaS/suscripción)**" if tag == "SaaS" else when
            rows.append(f"| `{mod}`{label_src} | {label} | `modulos/{mod}/GUIA.md` |")
        desc_esc = r["desc"].replace('"', '\\"')
        body = f"""---
name: {name}
description: "{desc_esc}"
---

# {r['title']}

Skill fusionada: reúne {len(r['mods'])} skills que antes competían entre sí. Este archivo solo enruta; el método completo de cada caso está en su módulo.

## Paso 1: elegir el módulo

| Módulo | Úsalo cuando | Leer |
|---|---|---|
""" + "\n".join(rows) + f"""

Si la petición toca dos módulos, empieza por el que produce el entregable y usa el segundo solo como apoyo. Si ninguno encaja, dilo y sugiere la skill correcta (ver `orquestador-skills`).

## Paso 2: ejecutar

Lee el `GUIA.md` del módulo y sigue su proceso y formato de salida. Anuncia en una línea el módulo usado, por ejemplo: "Uso {name} → `{r['mods'][0][0]}`".
{COMMON}"""
        with open(os.path.join(root, "SKILL.md"), "w", encoding="utf-8", newline="\n") as f:
            f.write(body)
        print(f"{name:22} {len(r['mods'])} módulos, desc {len(r['desc'])} chars")


if __name__ == "__main__":
    build()
