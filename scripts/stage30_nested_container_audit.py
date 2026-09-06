#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
SHELL_CLASSES = {"container", "intl-container"}

class ContainerAudit(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.nested = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = set((a.get("class") or "").split())
        is_shell = bool(classes & SHELL_CLASSES)
        active = [x for x in self.stack if x[1]]
        if is_shell and active:
            parent_tag, _, parent_classes = active[-1]
            self.nested.append((parent_tag, " ".join(sorted(parent_classes)), tag, " ".join(sorted(classes))))
        self.stack.append((tag, is_shell, classes))

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                return

issues = []
for path in sorted(root.rglob("*.html")):
    html = path.read_text(encoding="utf-8", errors="ignore")
    if "</head>" not in html or path.name.startswith(("google", "yandex_")):
        continue
    parser = ContainerAudit()
    parser.feed(html)
    if parser.nested:
        issues.append((path.relative_to(root).as_posix(), parser.nested))

print(f"stage30 nested shared-shell audit: {len(issues)} pages with nested .container/.intl-container")
for rel, nested in issues:
    print(f"  {rel}")
    for parent_tag, parent_cls, child_tag, child_cls in nested[:12]:
        print(f"    {parent_tag}.{parent_cls} -> {child_tag}.{child_cls}")
