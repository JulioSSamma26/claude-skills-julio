"""Copia los módulos de terceros (con licencia y fuente) para las skills nuevas."""
import os, shutil, sys

DL = r"D:/Users/jcanchan/AppData/Local/Temp/claude/ac62046613747adb/353b38c1-82b2-4f8f-b911-872b4e2788c7/scratchpad/descargas"
OUT = sys.argv[1]

REPOS = {  # clave: (licencia, url, commit, ruta del archivo LICENSE)
 "caveman": ("Apache-2.0", "github.com/JuliusBrussee/caveman", "a192894", "JuliusBrussee_caveman/LICENSE"),
 "matt": ("MIT", "github.com/mattpocock/skills", "abeeaf9", "mattpocock_skills/LICENSE"),
 "addy": ("MIT", "github.com/addyosmani/agent-skills", "8c99fa3", "addyosmani_agent-skills/LICENSE"),
 "obra": ("MIT", "github.com/obra/superpowers", "22f0b46", "obra_superpowers/LICENSE"),
 "cpo": ("Apache-2.0", "github.com/anthropics/claude-plugins-official", "73c8cf3", "anthropics_cpo/LICENSE"),
 "fin": ("Apache-2.0", "github.com/anthropics/financial-services", "3e32c22", "anth_fin/x/LICENSE"),
 "kwp": ("Apache-2.0", "github.com/anthropics/knowledge-work-plugins", "0e0fcac", "anth_kwp/x/LICENSE"),
 "copilot": ("MIT", "github.com/github/awesome-copilot", "f10fdb8", "copilot/x/LICENSE"),
 "alireza": ("MIT", "github.com/alirezarezvani/claude-skills", "5909a72", "alireza/x/LICENSE"),
}

SKILLS = {
 "ahorro-tokens": [
  ("caveman", "caveman", "JuliusBrussee_caveman/skills/caveman"),
  ("writing-for-agents", "matt", "mattpocock_skills/skills/productivity/writing-for-agents"),
  ("handoff", "matt", "mattpocock_skills/skills/productivity/handoff"),
  ("context-engineering", "addy", "addyosmani_agent-skills/skills/context-engineering"),
  ("writing-skills", "obra", "obra_superpowers/skills/writing-skills"),
 ],
 "desarrollo-codigo": [
  ("diagnosing-bugs", "matt", "mattpocock_skills/skills/engineering/diagnosing-bugs"),
  ("systematic-debugging", "obra", "obra_superpowers/skills/systematic-debugging"),
  ("tdd", "matt", "mattpocock_skills/skills/engineering/tdd"),
  ("verification-before-completion", "obra", "obra_superpowers/skills/verification-before-completion"),
  ("receiving-code-review", "obra", "obra_superpowers/skills/receiving-code-review"),
  ("doubt-driven-development", "addy", "addyosmani_agent-skills/skills/doubt-driven-development"),
  ("subagent-driven-development", "obra", "obra_superpowers/skills/subagent-driven-development"),
  ("pr-review-toolkit", "cpo", "anthropics_cpo/plugins/pr-review-toolkit/agents"),
 ],
 "excel-datos": [
  ("audit-xls", "fin", "anth_fin/x/plugins/vertical-plugins/financial-analysis/skills/audit-xls"),
  ("clean-data-xls", "fin", "anth_fin/x/plugins/vertical-plugins/financial-analysis/skills/clean-data-xls"),
  ("power-bi-dax-optimization", "copilot", "copilot/x/skills/power-bi-dax-optimization"),
 ],
 "tienda-ecommerce": [
  ("review-reputation", "kwp", "anth_kwp/x/small-business/skills/review-reputation"),
  ("inventory-planner", "kwp", "anth_kwp/x/small-business/skills/inventory-planner"),
 ],
 "verificador-datos": [
  ("source-audit", "alireza", "alireza/x/marketing-skill/skills/source-audit"),
 ],
}

IGN = shutil.ignore_patterns(".claude-plugin", "agents", "__pycache__", "*.pyc", ".git")

for skill, mods in SKILLS.items():
    root = os.path.join(OUT, skill)
    os.makedirs(os.path.join(root, "modulos"), exist_ok=True)
    for name, rk, rel in mods:
        lic, url, commit, licpath = REPOS[rk]
        src = os.path.join(DL, rel)
        dst = os.path.join(root, "modulos", name)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        # pr-review-toolkit: la carpeta fuente ES "agents", no se debe ignorar
        shutil.copytree(src, dst, ignore=None if name == "pr-review-toolkit" else IGN)
        if os.path.exists(os.path.join(dst, "SKILL.md")):
            os.rename(os.path.join(dst, "SKILL.md"), os.path.join(dst, "GUIA.md"))
        shutil.copy(os.path.join(DL, licpath), os.path.join(dst, "LICENSE"))
        with open(os.path.join(dst, "FUENTE.md"), "w", encoding="utf-8") as f:
            f.write(f"Fuente: {url} ({lic}), commit {commit}, ruta `{rel.split('/', 1)[1]}`. "
                    f"Descargado y escaneado el 2026-11-21 (sin red, sin inyección de instrucciones). "
                    f"Texto original sin modificar; solo SKILL.md se renombró a GUIA.md.\n")
    print(skill, [m[0] for m in mods])

# tienda: las guías citan ../../shared/ → va en la raíz de la skill
sh = os.path.join(OUT, "tienda-ecommerce", "shared")
if os.path.exists(sh):
    shutil.rmtree(sh)
shutil.copytree(os.path.join(DL, "anth_kwp/x/small-business/shared"), sh)
shutil.copy(os.path.join(DL, "anth_kwp/x/LICENSE"), os.path.join(sh, "LICENSE"))

# pr-review-toolkit no trae SKILL.md: índice propio
idx = os.path.join(OUT, "desarrollo-codigo", "modulos", "pr-review-toolkit", "GUIA.md")
with open(idx, "w", encoding="utf-8") as f:
    f.write("""# Revisión de PR por pasadas especializadas

Seis prompts de revisor de Anthropic (pr-review-toolkit). Cada archivo es el prompt de un subagente: léelo y úsalo como instrucción para un subagente (o aplícalo tú mismo) sobre el diff.

| Archivo | Pasada |
|---|---|
| `silent-failure-hunter.md` | Errores tragados, catch vacíos, fallbacks que ocultan fallas |
| `pr-test-analyzer.md` | Huecos de cobertura y calidad de las pruebas |
| `type-design-analyzer.md` | Diseño de tipos e invariantes |
| `comment-analyzer.md` | Comentarios falsos, obsoletos o que sobran |
| `code-reviewer.md` | Revisión general contra las convenciones del proyecto |
| `code-simplifier.md` | Simplificar sin cambiar comportamiento |

Elige solo las pasadas que aplican al cambio; no las seis siempre.
""")
print("listo")
