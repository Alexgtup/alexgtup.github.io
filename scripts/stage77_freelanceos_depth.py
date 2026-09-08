#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
p = root / "freelance-os" / "index.html"
if not p.is_file():
    raise SystemExit("stage77-fos: /freelance-os/ missing")

text = p.read_text(encoding="utf-8")
MARK = 'data-stage77-product-depth="true"'
if MARK not in text:
    block = '''<section class="s77-section" data-stage77-product-depth="true"><h2>Когда local-first CRM подходит, а когда нужен сервер</h2><p>Local-first вариант удобен для одного специалиста или небольшой личной воронки: данные остаются на устройстве, CRM запускается без аккаунта и серверной инфраструктуры, а резервную копию можно сохранить через JSON export. Если нужен одновременный доступ команды, синхронизация между устройствами, роли, история изменений или централизованные резервные копии, следующий этап — авторизация, серверная база данных и cloud-sync.</p><div class="s77-links"><a href="/cases/freelance-os/">Технический кейс FreelanceOS</a><a href="/crm-development/">Разработка CRM</a></div></section>'''
    text, n = re.subn(r'</main>', block + '</main>', text, count=1, flags=re.I)
    if n != 1:
        raise SystemExit("stage77-fos: </main> not found exactly once")
    p.write_text(text, encoding="utf-8")

final = p.read_text(encoding="utf-8")
for token in (MARK, "Local-first вариант удобен", 'href="/cases/freelance-os/"', 'href="/crm-development/"'):
    if token not in final:
        raise SystemExit(f"stage77-fos: invariant failed: {token}")
print("stage77-fos: product depth block guarded")
