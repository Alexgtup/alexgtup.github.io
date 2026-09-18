#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html,json,re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'; TODAY='2026-09-18'
PERSON_ID=BASE+'/#person'
FULL_NAME='Александр Александров'
ALT_NAME='Alexuys'
JOB='Разработчик сайтов, программного обеспечения и автоматизации'
SAME_AS=['https://github.com/Alexgtup','https://freelance.ru/gglalex','https://t.me/Alexuys']
KNOWS=['веб-разработка','разработка программного обеспечения','Python','REST API','Telegram Bot API','CRM','автоматизация бизнес-процессов','искусственный интеллект']

def walk(x,fn):
    if isinstance(x,dict):
        fn(x)
        for v in x.values(): walk(v,fn)
    elif isinstance(x,list):
        for v in x: walk(v,fn)

def patch_jsonld(s:str):
    def repl(m):
        try:o=json.loads(m.group(2))
        except Exception:return m.group(0)
        def cb(x):
            if x.get('@type')=='Person' and x.get('@id')==PERSON_ID:
                x['name']=FULL_NAME
                x['alternateName']=ALT_NAME
                x['givenName']='Александр'
                x['familyName']='Александров'
                x['url']=BASE+'/about/'
                x['jobTitle']=JOB
                x['sameAs']=SAME_AS
                x['knowsAbout']=KNOWS
            if x.get('@type')=='WebSite' and x.get('url')==BASE+'/':
                x['publisher']={'@id':PERSON_ID}
                x['author']={'@id':PERSON_ID}
        walk(o,cb)
        return m.group(1)+json.dumps(o,ensure_ascii=False,separators=(',',':'))+m.group(3)
    return re.sub(r'(<script[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',repl,s,flags=re.I|re.S)

changed=[];persons=0; websites=0
for p in ROOT.rglob('index.html'):
    s=p.read_text(encoding='utf-8',errors='ignore')
    before=s
    s=patch_jsonld(s)
    if s!=before:
        persons += s.count('"@id":"'+PERSON_ID+'"') - before.count('"@id":"'+PERSON_ID+'"') + before.count('"@type":"Person"')
        p.write_text(s,encoding='utf-8')
        rel=p.relative_to(ROOT)
        route='/' if str(rel)=='index.html' else '/'+str(rel.parent).replace('\\','/')+'/'
        changed.append(route)

# Visible identity evidence on About; structured data should not claim a fuller identity than the page itself shows.
p=ROOT/'about'/'index.html'
s=p.read_text(encoding='utf-8')
if 'data-stage202-person-name' not in s:
    needle='<p class="p130-kicker"><i></i>ABOUT</p>'
    if needle not in s: raise SystemExit('stage202 about kicker missing')
    s=s.replace(needle,needle+'<p class="p130-person-name" data-stage202-person-name="true">Александр Александров <span>· Alexuys</span></p>',1)
    style='<style id="stage202-person-style">.p130-person-name{margin:14px 0 10px;color:rgba(238,243,240,.78);font-size:14px;font-weight:750;letter-spacing:.01em}.p130-person-name span{color:rgba(238,243,240,.48);font-weight:650}@media(max-width:600px){.p130-person-name{font-size:13px;margin-top:12px}}</style>'
    s=s.replace('</head>',style+'</head>',1)
# Align About SERP identity with the public profile without changing the positioning H1.
s=re.sub(r'<title[^>]*>.*?</title>',f'<title>{FULL_NAME} — разработчик | Alexuys</title>',s,count=1,flags=re.I|re.S)
for attr,key,val in [
 ('property','og:title',f'{FULL_NAME} — разработчик | Alexuys'),
 ('name','twitter:title',f'{FULL_NAME} — разработчик | Alexuys'),
]:
    pat=rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(key)}["\'])[^>]*>'
    repl=f'<meta {attr}="{key}" content="{html.escape(val,quote=True)}"/>'
    if re.search(pat,s,re.I): s=re.sub(pat,repl,s,count=1,flags=re.I)
p.write_text(s,encoding='utf-8')
if '/about/' not in changed: changed.append('/about/')

# Refresh dates only for pages whose built output changed.
for name in ('sitemap.xml','sitemap-google.xml'):
    sp=ROOT/name
    if not sp.exists(): continue
    text=sp.read_text(encoding='utf-8')
    for route in sorted(set(changed)):
        text=re.sub(r'(<loc>'+re.escape(BASE+route)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',text,count=1)
    sp.write_text(text,encoding='utf-8')

# Strict consistency audit.
seen=[]
for p in ROOT.rglob('index.html'):
    s=p.read_text(encoding='utf-8',errors='ignore')
    for m in re.finditer(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',s,re.I|re.S):
        try:o=json.loads(m.group(1))
        except Exception:continue
        def audit(x):
            if x.get('@type')=='Person' and x.get('@id')==PERSON_ID:
                seen.append((p,x))
                expected={'name':FULL_NAME,'alternateName':ALT_NAME,'givenName':'Александр','familyName':'Александров','url':BASE+'/about/','jobTitle':JOB,'sameAs':SAME_AS,'knowsAbout':KNOWS}
                for k,v in expected.items():
                    if x.get(k)!=v: raise SystemExit(f'stage202 inconsistency {p}: {k}={x.get(k)!r}')
        walk(o,audit)
if len(seen)<20: raise SystemExit(f'stage202 suspicious Person count {len(seen)}')
a=(ROOT/'about'/'index.html').read_text(encoding='utf-8')
for needle in [FULL_NAME,'data-stage202-person-name="true"',f'<title>{FULL_NAME} — разработчик | Alexuys</title>']:
    if needle not in a: raise SystemExit(f'stage202 about guard: {needle}')
print(f'stage202 person entity consistency: person_nodes={len(seen)}, changed_pages={len(set(changed))}')
