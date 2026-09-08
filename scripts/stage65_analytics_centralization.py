#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
check_only = "--check" in sys.argv[2:]
js_path = root / "assets" / "site-enhancements.js"
if not js_path.is_file():
    raise SystemExit(f"stage65: missing {js_path}")

text = js_path.read_text(encoding="utf-8")
original = text

if not check_only:
    # Stage39 lead form: keep the form-specific conversion, but delegate transport
    # and consent handling to the shared analytics layer.
    text = text.replace(
        """    if (typeof window.ym === 'function') {\n      try { window.ym(112290993, 'reachGoal', 'lead_brief_submit', { page: location.pathname, kind, budget }); } catch (_) {}\n    }""",
        """    window.alexuysAnalytics?.goal('lead_brief_submit', { kind, budget });""",
    )
    text = text.replace(
        """    if (window.alexuysAnalytics?.consent === 'accepted' && typeof window.ym === 'function') {\n      try { window.ym(112290993, 'reachGoal', 'lead_brief_submit', { page: location.pathname, kind, budget }); } catch (_) {}\n    }""",
        """    window.alexuysAnalytics?.goal('lead_brief_submit', { kind, budget });""",
    )

    # Stage43 referral funnel: shared analytics owns the generic telegram_click.
    # Keep only referral-specific goals here to avoid double-counting Telegram clicks.
    text = text.replace(
        """  const reach = (goal, params = {}) => {\n    if (typeof window.ym !== 'function') return;\n    try { window.ym(112290993, 'reachGoal', goal, params); } catch (_) {}\n  };""",
        """  const reach = (goal, params = {}) => {\n    window.alexuysAnalytics?.goal(goal, params);\n  };""",
    )
    text = text.replace(
        """  const reach = (goal, params = {}) => {\n    if (window.alexuysAnalytics?.consent !== 'accepted' || typeof window.ym !== 'function') return;\n    try { window.ym(112290993, 'reachGoal', goal, params); } catch (_) {}\n  };""",
        """  const reach = (goal, params = {}) => {\n    window.alexuysAnalytics?.goal(goal, params);\n  };""",
    )
    text = text.replace(
        """      reach('telegram_click', { page: location.pathname, freelance_referral: fromFreelance ? 'yes' : 'no' });\n      if (fromFreelance) reach('freelance_to_telegram', { page: location.pathname });""",
        """      if (fromFreelance) reach('freelance_to_telegram', { source: 'freelance' });""",
    )

    # Stage44 compact brief.
    text = text.replace(
        """  const goal = (name, params = {}) => {\n    if (typeof window.ym !== 'function') return;\n    try { window.ym(112290993, 'reachGoal', name, { page: location.pathname, ...params }); } catch (_) {}\n  };""",
        """  const goal = (name, params = {}) => {\n    window.alexuysAnalytics?.goal(name, params);\n  };""",
    )
    text = text.replace(
        """  const goal = (name, params = {}) => {\n    if (window.alexuysAnalytics?.consent !== 'accepted' || typeof window.ym !== 'function') return;\n    try { window.ym(112290993, 'reachGoal', name, { page: location.pathname, ...params }); } catch (_) {}\n  };""",
        """  const goal = (name, params = {}) => {\n    window.alexuysAnalytics?.goal(name, params);\n  };""",
    )

    if text == original and "reachGoal" in text:
        raise SystemExit("stage65: direct reachGoal found in site-enhancements.js but no known rewrite matched")
    js_path.write_text(text, encoding="utf-8")

    # Pre-stage62 guard: only the shared JS is final enough to validate here.
    # Some source HTML still contains legacy inline snippets that stage62 removes.
    if "reachGoal" in text:
        raise SystemExit("stage65: direct reachGoal remains in site-enhancements.js after patch")
    print("stage65 analytics centralization patch: OK; site-enhancements.js direct reachGoal = 0")
    raise SystemExit(0)

# Final production invariant, intentionally run after stage62/stage64/stage63:
# analytics.js is the only built file allowed to know Yandex reachGoal.
violations = []
for path in sorted(root.rglob("*.js")) + sorted(root.rglob("*.html")):
    if path == root / "assets" / "analytics.js":
        continue
    body = path.read_text(encoding="utf-8", errors="ignore")
    if "reachGoal" in body:
        violations.append(path.relative_to(root).as_posix())

if violations:
    raise SystemExit("stage65: direct reachGoal outside analytics.js: " + ", ".join(violations))

print("stage65 analytics centralization check: OK; direct reachGoal outside analytics.js = 0")
