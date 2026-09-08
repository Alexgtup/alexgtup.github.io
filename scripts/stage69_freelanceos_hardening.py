#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
js_path = root / 'assets' / 'freelance-os.js'
if not js_path.is_file():
    raise SystemExit('stage69: freelance-os.js missing')

js = js_path.read_text(encoding='utf-8')

old_esc = "  const esc = (value = '') => String(value);"
new_esc = "  const esc = (value = '') => String(value).replace(/[&<>\"']/g, (ch) => ({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',\"'\":'&#39;'}[ch]));"
if old_esc in js:
    js = js.replace(old_esc, new_esc, 1)
elif new_esc not in js:
    raise SystemExit('stage69: escape helper has unexpected shape')

cancel_marker = "  els.taskForm.addEventListener('submit', handleTaskSubmit);\n"
cancel_block = "  $$('[value=\"cancel\"]').forEach((el) => el.addEventListener('click', (event) => { event.preventDefault(); el.closest('dialog')?.close(); }));\n"
if cancel_block not in js:
    if cancel_marker not in js:
        raise SystemExit('stage69: dialog listener marker missing')
    js = js.replace(cancel_marker, cancel_marker + cancel_block, 1)

# Record only coarse product interactions through the existing consent-aware layer.
goal_helper_marker = "  const compact = (value) => new Intl.NumberFormat('ru-RU', { notation: 'compact', maximumFractionDigits: 1 }).format(Number(value) || 0);\n"
goal_helper = "  const goal = (name) => { const analytics = window.alexuysAnalytics; if (analytics && typeof analytics.goal === 'function') analytics.goal(name); };\n"
if goal_helper not in js:
    if goal_helper_marker not in js:
        raise SystemExit('stage69: analytics helper marker missing')
    js = js.replace(goal_helper_marker, goal_helper_marker + goal_helper, 1)

replacements = {
    "    toast('Резервная копия выгружена');": "    goal('freelanceos_export');\n    toast('Резервная копия выгружена');",
    "      toast('Данные импортированы');": "      goal('freelanceos_import');\n      toast('Данные импортированы');",
    "    toast('Demo-данные загружены');": "    goal('freelanceos_demo_loaded');\n    toast('Demo-данные загружены');",
    "    els.leadDialog.close();\n    commit();": "    els.leadDialog.close();\n    goal(existing ? 'freelanceos_lead_updated' : 'freelanceos_lead_created');\n    commit();",
}
for old, new in replacements.items():
    if new in js:
        continue
    if old not in js:
        raise SystemExit(f'stage69: interaction marker missing: {old[:45]}')
    js = js.replace(old, new, 1)

js_path.write_text(js, encoding='utf-8')

body = js_path.read_text(encoding='utf-8')
checks = [
    "replace(/[&<>\"']/g",
    "closest('dialog')?.close()",
    "freelanceos_demo_loaded",
    "freelanceos_lead_created",
    "freelanceos_export",
]
for token in checks:
    if token not in body:
        raise SystemExit(f'stage69: hardening token missing: {token}')
if old_esc in body:
    raise SystemExit('stage69: unsafe escape helper survived')

print('stage69: FreelanceOS XSS/import rendering, dialog controls and consent-aware product goals guarded')