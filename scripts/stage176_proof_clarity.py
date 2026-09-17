from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
SLUGS=['personal-cabinet-development','admin-panel-development','saas-development','ecommerce-development','excel-google-sheets-automation','python-scripts','web-scraping-parsers','1c-integration','payment-integration','crm-integration','api-development','automation-services','site-repair','ai-chatbot-development','tilda-development','bitrix-development']
changed=0
for slug in SLUGS:
    fp=ROOT/slug/'index.html'
    if not fp.exists(): continue
    x=fp.read_text(encoding='utf-8')
    # Secondary landing pages use a nearby real project as architectural proof; label it honestly.
    x,n=re.subn(r'<span class="p129-kicker"><i></i>REAL WORK</span>','<span class="p129-kicker"><i></i>RELATED CASE / REAL WORK</span>',x,count=1)
    changed+=n
    # Keep the case bridge explicit instead of implying the case was built on the exact same platform.
    x=x.replace('<span class="p129-textlink">Открыть кейс ↗</span>','<span class="p129-textlink">Посмотреть связанный кейс ↗</span>',1)
    fp.write_text(x,encoding='utf-8')
print(f'stage176 proof clarity: pages={len(SLUGS)}, relabeled={changed}')
