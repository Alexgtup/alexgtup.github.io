#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re, sys

ROOT = Path(sys.argv[1] if len(sys.argv)>1 else '_site')
MARKER='stage158-sitewide-editorial-cleanup'
STYLE=r'''<style id="stage158-sitewide-editorial-cleanup">
/* Final normalization for legacy Russian hub/service/guide pages. */
body[data-ux-family="hub"],body[data-ux-family="service"],body[data-ux-family="guide"]{overflow-x:clip;background:#070a0c;color:#f5f7f4}

/* HUBS */
body[data-ux-family="hub"] .p130-hero{position:relative!important;min-height:0!important;padding:clamp(72px,7vw,116px) 0 clamp(84px,8vw,132px)!important;background:transparent!important;overflow:visible!important;border:0!important;}
body[data-ux-family="hub"] .p130-hero::before{content:""!important;position:absolute!important;z-index:-1!important;right:-8%!important;top:42%!important;width:min(700px,48vw)!important;aspect-ratio:1!important;border-radius:50%!important;transform:translateY(-50%)!important;background:radial-gradient(circle,rgba(98,129,255,.10),rgba(83,137,103,.05) 40%,transparent 72%)!important;filter:blur(18px)!important;pointer-events:none!important;}
body[data-ux-family="hub"] .p130-hero::after{content:none!important;display:none!important;}
body[data-ux-family="hub"] .p130-shell.p130-hero-grid{display:grid!important;grid-template-columns:minmax(0,1.22fr) minmax(300px,.58fr)!important;align-items:center!important;gap:clamp(48px,6vw,96px)!important;width:min(1480px,calc(100% - 64px))!important;max-width:1480px!important;margin:0 auto!important;padding:0!important;transform:none!important;}
body[data-ux-family="hub"] .p130-hero-grid>div:first-child{grid-column:1!important;position:relative!important;width:100%!important;max-width:none!important;min-width:0!important;min-height:0!important;margin:0!important;padding:0!important;border:0!important;border-radius:0!important;background:transparent!important;box-shadow:none!important;backdrop-filter:none!important;-webkit-backdrop-filter:none!important;overflow:visible!important;}
body[data-ux-family="hub"] .p130-hero-grid>div:first-child::before,body[data-ux-family="hub"] .p130-hero-grid>div:first-child::after{content:none!important;display:none!important;}
body[data-ux-family="hub"] .p130-kicker{margin:0 0 22px!important;color:rgba(226,233,228,.55)!important;font-size:12px!important;letter-spacing:.19em!important;text-transform:uppercase!important;}
body[data-ux-family="hub"] .p130-hero h1{width:100%!important;max-width:none!important;margin:0 0 30px!important;font-size:clamp(72px,6.6vw,122px)!important;line-height:.88!important;letter-spacing:-.07em!important;text-wrap:pretty!important;overflow-wrap:normal!important;word-break:normal!important;color:#f5f7f4!important;}
body[data-ux-family="hub"] .p130-hero h1 span{color:#ff765e!important;font-family:Georgia,serif!important;font-weight:500!important;letter-spacing:-.055em!important;}
body[data-ux-family="hub"] .p130-lead{width:100%!important;max-width:72ch!important;margin:0!important;color:rgba(234,239,236,.74)!important;font-size:clamp(18px,1.22vw,22px)!important;line-height:1.72!important;text-wrap:pretty!important;}
body[data-ux-family="hub"] .p130-hero-side{grid-column:2!important;position:relative!important;width:100%!important;max-width:390px!important;min-width:0!important;min-height:0!important;margin:0!important;padding:clamp(24px,2.7vw,34px)!important;justify-self:end!important;align-self:center!important;border:1px solid rgba(255,255,255,.10)!important;border-radius:26px!important;background:linear-gradient(145deg,rgba(255,255,255,.055),rgba(255,255,255,.018)),rgba(12,16,20,.50)!important;backdrop-filter:blur(20px) saturate(125%)!important;-webkit-backdrop-filter:blur(20px) saturate(125%)!important;box-shadow:0 24px 72px rgba(0,0,0,.28),inset 0 1px 0 rgba(255,255,255,.045)!important;color:rgba(224,231,235,.72)!important;font-size:15px!important;line-height:1.72!important;}
body[data-ux-family="hub"] .p130-hero-side strong{display:block!important;margin:0 0 10px!important;color:#f5f7f4!important;font-size:clamp(19px,1.55vw,24px)!important;line-height:1.15!important;}
body[data-ux-family="hub"] .p130-list-section,body[data-ux-family="hub"] .p130-editorial,body[data-ux-family="hub"] .p130-footer-cta{position:relative!important;}
body[data-ux-family="hub"] .p130-list-section>.p130-shell,body[data-ux-family="hub"] .p130-editorial>.p130-shell,body[data-ux-family="hub"] .p130-footer-cta>.p130-shell{width:min(1480px,calc(100% - 64px))!important;max-width:1480px!important;}

/* SERVICES */
body[data-ux-family="service"] .p155-service-hero{position:relative!important;display:grid!important;grid-template-columns:minmax(0,1.18fr) minmax(360px,.62fr)!important;align-items:center!important;gap:clamp(56px,6vw,104px)!important;width:min(1480px,calc(100% - 64px))!important;max-width:1480px!important;min-height:clamp(620px,52vw,820px)!important;margin:clamp(56px,6vw,96px) auto clamp(88px,8vw,132px)!important;padding:clamp(18px,2vw,32px) 0!important;overflow:visible!important;isolation:isolate!important;border:0!important;border-radius:0!important;background:transparent!important;box-shadow:none!important;}
body[data-ux-family="service"] .p155-service-hero::before{content:""!important;position:absolute!important;z-index:-1!important;right:-7%!important;top:50%!important;width:min(720px,50vw)!important;aspect-ratio:1!important;transform:translateY(-50%)!important;border-radius:50%!important;background:radial-gradient(circle,rgba(255,107,93,.095),rgba(109,128,255,.05) 42%,transparent 72%)!important;filter:blur(18px)!important;pointer-events:none!important;}
body[data-ux-family="service"] .p155-service-hero::after{content:none!important;display:none!important;}
body[data-ux-family="service"] .p155-service-band,body[data-ux-family="service"] .p155-service-band .p129-svc-copy{position:relative!important;inset:auto!important;transform:none!important;translate:none!important;width:100%!important;max-width:none!important;min-width:0!important;min-height:0!important;height:auto!important;margin:0!important;padding:0!important;display:block!important;border:0!important;border-radius:0!important;background:transparent!important;box-shadow:none!important;backdrop-filter:none!important;-webkit-backdrop-filter:none!important;overflow:visible!important;}
body[data-ux-family="service"] .p155-service-band::before,body[data-ux-family="service"] .p155-service-band::after,body[data-ux-family="service"] .p129-svc-copy::before,body[data-ux-family="service"] .p129-svc-copy::after{content:none!important;display:none!important;}
body[data-ux-family="service"] .p129-kicker{margin:0 0 22px!important;color:rgba(226,233,228,.55)!important;font-size:12px!important;letter-spacing:.19em!important;text-transform:uppercase!important;}
body[data-ux-family="service"] .p129-svc-copy h1{width:100%!important;max-width:none!important;margin:0 0 30px!important;font-size:clamp(70px,6.25vw,116px)!important;line-height:.89!important;letter-spacing:-.068em!important;text-wrap:pretty!important;overflow-wrap:normal!important;word-break:normal!important;color:#f5f7f4!important;}
body[data-ux-family="service"] .p129-svc-copy h1 em{color:#ff765e!important;font-family:Georgia,serif!important;font-weight:500!important;}
body[data-ux-family="service"] .p129-lead{width:100%!important;max-width:70ch!important;margin:0!important;color:rgba(234,239,236,.74)!important;font-size:clamp(18px,1.2vw,21px)!important;line-height:1.72!important;text-wrap:pretty!important;}
body[data-ux-family="service"] .p129-svc-actions{margin-top:36px!important;display:flex!important;flex-wrap:wrap!important;align-items:center!important;gap:14px 22px!important;}
body[data-ux-family="service"] .p155-service-preview{position:relative!important;inset:auto!important;transform:none!important;translate:none!important;width:100%!important;max-width:460px!important;min-width:0!important;margin:0!important;align-self:center!important;justify-self:end!important;}
body[data-ux-family="service"] .p155-service-preview::before{content:""!important;position:absolute!important;z-index:-1!important;inset:8% 4% -10% 4%!important;border-radius:36px!important;background:linear-gradient(135deg,rgba(255,118,94,.12),rgba(103,127,255,.08))!important;filter:blur(48px)!important;opacity:.8!important;pointer-events:none!important;}
body[data-ux-family="service"] .p155-service-preview .p129-svc-board{position:relative!important;inset:auto!important;transform:none!important;translate:none!important;width:100%!important;max-width:none!important;min-width:0!important;min-height:0!important;margin:0!important;padding:clamp(28px,3vw,42px)!important;border:1px solid rgba(255,255,255,.09)!important;border-radius:28px!important;background:linear-gradient(145deg,rgba(255,255,255,.055),rgba(255,255,255,.018)),rgba(12,16,20,.52)!important;box-shadow:0 34px 90px rgba(0,0,0,.34),inset 0 1px 0 rgba(255,255,255,.04)!important;backdrop-filter:blur(20px) saturate(125%)!important;-webkit-backdrop-filter:blur(20px) saturate(125%)!important;}
body[data-ux-family="service"] .p129-outcomes>.p129-shell,body[data-ux-family="service"] .p129-process>.p129-shell,body[data-ux-family="service"] .p129-cases>.p129-shell,body[data-ux-family="service"] .p129-faq>.p129-shell,body[data-ux-family="service"] .p129-final>.p129-shell{width:min(1480px,calc(100% - 64px))!important;max-width:1480px!important;}

/* GUIDES */
body[data-ux-family="guide"] .ux-guide-main{background:#070a0c!important;color:#f5f7f4!important;}
body[data-ux-family="guide"] .ux-guide-main>.crumbs{width:min(1320px,calc(100% - 64px))!important;max-width:1320px!important;margin:0 auto!important;padding:28px 0 0!important;color:#7f898f!important;}
body[data-ux-family="guide"] .ux-guide-main>.hero{position:relative!important;width:min(1320px,calc(100% - 64px))!important;max-width:1320px!important;min-height:0!important;margin:0 auto!important;padding:clamp(64px,7vw,110px) 0 clamp(72px,7vw,112px)!important;display:block!important;overflow:visible!important;background:transparent!important;}
body[data-ux-family="guide"] .ux-guide-main>.hero::before,body[data-ux-family="guide"] .ux-guide-main>.hero::after{content:none!important;display:none!important;}
body[data-ux-family="guide"] .ux-guide-main>.hero h1{width:100%!important;max-width:none!important;margin:18px 0 28px!important;font-size:clamp(70px,7vw,118px)!important;line-height:.89!important;letter-spacing:-.07em!important;text-wrap:pretty!important;color:#f5f7f4!important;}
body[data-ux-family="guide"] .ux-guide-main>.hero h1 em{color:#ff765e!important;font-family:Georgia,serif!important;font-weight:500!important;}
body[data-ux-family="guide"] .ux-guide-main>.hero .lead{width:100%!important;max-width:76ch!important;color:rgba(234,239,236,.72)!important;font-size:clamp(18px,1.25vw,22px)!important;line-height:1.72!important;}
body[data-ux-family="guide"] .ux-guide-main>.hero .meta{margin-top:26px!important;color:#7f898f!important;}
body[data-ux-family="guide"] .ux-guide-main>.layout{width:min(1320px,calc(100% - 64px))!important;max-width:1320px!important;margin:0 auto clamp(90px,9vw,150px)!important;padding:0!important;display:grid!important;grid-template-columns:minmax(0,1fr) minmax(240px,300px)!important;gap:clamp(44px,6vw,84px)!important;background:transparent!important;color:#f5f7f4!important;}
body[data-ux-family="guide"] .ux-guide-main .article{min-width:0!important;padding:0!important;}
body[data-ux-family="guide"] .ux-guide-main .article>section{padding:clamp(46px,5vw,76px) 0!important;border-top:1px solid rgba(255,255,255,.09)!important;}
body[data-ux-family="guide"] .ux-guide-main .article>section:first-child{border-top:0!important;padding-top:0!important;}
body[data-ux-family="guide"] .ux-guide-main .article h2{max-width:none!important;color:#f5f7f4!important;font-size:clamp(38px,4vw,64px)!important;line-height:.98!important;letter-spacing:-.045em!important;}
body[data-ux-family="guide"] .ux-guide-main .article h3{color:#f5f7f4!important;}
body[data-ux-family="guide"] .ux-guide-main .article p,body[data-ux-family="guide"] .ux-guide-main .article li{color:rgba(226,233,236,.74)!important;font-size:clamp(16px,1.15vw,19px)!important;line-height:1.75!important;}
body[data-ux-family="guide"] .ux-guide-main .answer{background:rgba(255,255,255,.045)!important;color:#f5f7f4!important;border:1px solid rgba(255,255,255,.09)!important;border-radius:22px!important;padding:clamp(24px,3vw,40px)!important;box-shadow:none!important;}
body[data-ux-family="guide"] .ux-guide-main .layout>aside{position:sticky!important;top:88px!important;height:auto!important;align-self:start!important;padding:24px!important;background:rgba(255,255,255,.035)!important;border:1px solid rgba(255,255,255,.08)!important;border-radius:22px!important;color:#f5f7f4!important;}
body[data-ux-family="guide"] .ux-guide-main .layout>aside a{color:#aab3b8!important;border-bottom:1px solid rgba(255,255,255,.07)!important;padding:12px 0!important;}

@media(max-width:980px){
 body[data-ux-family="hub"] .p130-shell.p130-hero-grid,body[data-ux-family="service"] .p155-service-hero{grid-template-columns:1fr!important;gap:42px!important;width:min(100% - 28px,860px)!important;min-height:0!important;}
 body[data-ux-family="hub"] .p130-hero-side,body[data-ux-family="service"] .p155-service-preview{grid-column:1!important;justify-self:start!important;max-width:640px!important;}
 body[data-ux-family="hub"] .p130-hero h1,body[data-ux-family="service"] .p129-svc-copy h1,body[data-ux-family="guide"] .ux-guide-main>.hero h1{font-size:clamp(52px,11vw,82px)!important;max-width:none!important;}
 body[data-ux-family="guide"] .ux-guide-main>.crumbs,body[data-ux-family="guide"] .ux-guide-main>.hero,body[data-ux-family="guide"] .ux-guide-main>.layout{width:min(100% - 28px,860px)!important;}
 body[data-ux-family="guide"] .ux-guide-main>.layout{grid-template-columns:1fr!important;gap:28px!important;}
 body[data-ux-family="guide"] .ux-guide-main .layout>aside{position:relative!important;top:auto!important;}
}
@media(max-width:600px){
 body[data-ux-family="hub"] .p130-shell.p130-hero-grid,body[data-ux-family="service"] .p155-service-hero,body[data-ux-family="guide"] .ux-guide-main>.crumbs,body[data-ux-family="guide"] .ux-guide-main>.hero,body[data-ux-family="guide"] .ux-guide-main>.layout{width:calc(100% - 24px)!important;}
 body[data-ux-family="hub"] .p130-hero,body[data-ux-family="service"] .p155-service-hero{margin-top:0!important;padding-top:42px!important;}
 body[data-ux-family="hub"] .p130-hero h1,body[data-ux-family="service"] .p129-svc-copy h1,body[data-ux-family="guide"] .ux-guide-main>.hero h1{font-size:clamp(46px,13.5vw,68px)!important;}
}
</style>'''

OLD_STYLE_IDS_RE=re.compile(r'<style\b[^>]*id="(?:stage153-case-left-panel|stage154-text-into-existing-band|stage154-case-left-band|stage155-case-dom-scene|stage156-stable-hero-layout(?:-v2)?|stage151-hub-layout-polish)"[^>]*>.*?</style>',re.I|re.S)
RUNTIME_SCRIPT_RE=re.compile(r'<script\b[^>]*src="/assets/(?:stage134-experimental-web|stage135-world-system)\.js[^\"]*"[^>]*>\s*</script>',re.I|re.S)
BODY_RE=re.compile(r'<body\b([^>]*)>',re.I)

def target(html:str)->bool:
 m=BODY_RE.search(html)
 if not m:return False
 attrs=m.group(1)
 ux=re.search(r'data-ux-family="([^"]+)"',attrs)
 fam=re.search(r'data-x135-family="([^"]+)"',attrs)
 if not ux or ux.group(1) not in {'hub','service','guide'}: return False
 # Russian legacy worlds only; leave international/tool/demo/product untouched.
 return not fam or fam.group(1) in {'cinematic','guide'}

def clean(html:str)->str:
 html=OLD_STYLE_IDS_RE.sub('',html)
 html=RUNTIME_SCRIPT_RE.sub('',html)
 html=re.sub(r'\sdata-x134="[^"]*"','',html,count=1)
 html=re.sub(r'\sdata-x135="[^"]*"','',html,count=1)
 html=re.sub(r'\sdata-x135-family="[^"]*"','',html,count=1)
 return html

changed=[]
for p in sorted(ROOT.rglob('index.html')):
 s=p.read_text(encoding='utf-8',errors='ignore')
 if not target(s): continue
 s=clean(s)
 if '</head>' not in s: raise SystemExit(f'head missing: {p}')
 s=s.replace('</head>',STYLE+'</head>',1)
 p.write_text(s,encoding='utf-8')
 changed.append(p)

if len(changed)<10: raise SystemExit(f'stage158: too few pages: {len(changed)}')
for p in changed:
 s=p.read_text(encoding='utf-8')
 if s.count(f'id="{MARKER}"')!=1: raise SystemExit(f'marker guard: {p}')
 if 'stage134-experimental-web.js' in s or 'stage135-world-system.js' in s: raise SystemExit(f'runtime remains: {p}')
 body=BODY_RE.search(s).group(0)
 if 'data-x134=' in body or 'data-x135=' in body or 'data-x135-family=' in body: raise SystemExit(f'flags remain: {p}')
print(f'stage158 normalized legacy pages: {len(changed)}')