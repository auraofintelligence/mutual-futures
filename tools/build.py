#!/usr/bin/env python3
"""Build every page as ordinary HTML; no client framework or API is required."""
from pathlib import Path
from html import escape as esc
from importlib.util import spec_from_file_location,module_from_spec
import json,shutil,hashlib,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'site';OUT.mkdir(exist_ok=True)
spec=spec_from_file_location('mf_content',ROOT/'content/site.py');module=module_from_spec(spec);spec.loader.exec_module(module)
SITE,PAGES,PROJECTS,SOURCES,TIMELINE=module.SITE,module.PAGES,module.PROJECTS,module.SOURCES,module.TIMELINE
DOCS=json.loads((ROOT/'content/documents.json').read_text());ASSETS=json.loads((ROOT/'content/assets.json').read_text())
BYID={x['id']:x for x in PROJECTS+SOURCES+DOCS};BYPAGE={x['slug']:x for x in PAGES}
def external(url): return url.startswith(('https://','http://'))
def link(url,label,cls='',download=False):
 extra=' target="_blank" rel="noopener noreferrer"' if external(url) else ''
 if download: extra+=' download'
 return f'<a href="{esc(url,quote=True)}"'+(f' class="{cls}"' if cls else '')+extra+f'>{label}</a>'
def para(text): return ''.join('<p>'+esc(p)+'</p>' for p in text.split('\n\n') if p)
def refs(ids):
 if not ids:return ''
 items=[]
 for rid in ids:
  target=f'library.html#{rid}' if rid.startswith('D') else f'sources.html#{rid}'
  items.append(link(target,f'{rid} · {esc(BYID[rid]["title"])}'))
 return '<p class="source-line">Source trail: '+' '.join(items)+'</p>'
def title_plain(p): return re.sub('<[^>]+>',' ',p['title']).replace('  ',' ').strip()
def image(key): return 'assets/images/'+key+Path(ASSETS[key][1]).suffix.lower()
def tools(kind):
 if kind=='capital':
  def inp(name,label,value,minv=0,maxv=None,step=1000):
   return f'<label>{label}<input name="{name}" type="number" value="{value}" min="{minv}"'+(f' max="{maxv}"' if maxv is not None else '')+f' step="{step}" required></label>'
  result=lambda id,label:f'<div class="result"><span'+(' id="gap-label"' if id=='gap' else '')+f'>{label}</span><strong id="{id}-out" data-capital-result>Calculating</strong></div>'
  return '<section class="section" id="tool"><div class="wrap"><span class="tag demo">Interactive illustration</span><h2 style="margin-top:20px">Capital & cash-flow explorer</h2><p class="measure muted">Every amount is in Australian dollars. These sample values are invented, not a market estimate. Nothing is uploaded or automatically saved.</p><div class="tool"><form id="capital-form" onsubmit="return false"><fieldset><legend>Uses of capital</legend><div class="form-grid">'+''.join([inp('price','Negotiated purchase price (A$)',1000000),inp('working','Working capital (A$)',150000),inp('upgrade','Upfront upgrading (A$)',100000),inp('fees','Transaction expenses (A$)',50000)])+'</div></fieldset><fieldset><legend>Finance and deferred consideration</legend><div class="form-grid">'+''.join([inp('senior','Senior loan cash (A$)',500000),inp('seniorRate','Senior interest (% per year)',8,0,40,.1),inp('seniorTerm','Senior repayment term (years)',7,1,30,1),inp('vendor','Deferred seller price (A$)',300000),inp('vendorRate','Seller-note interest (% per year)',5,0,40,.1),inp('vendorTerm','Seller repayment term (years)',5,1,30,1),inp('equity','Outside equity cash (A$)',450000),inp('members','Member capital cash (A$)',50000)])+'</div></fieldset><fieldset><legend>Annual cash and transition</legend><div class="form-grid">'+''.join([inp('cash','Cash before acquisition financing (A$/year)',280000),inp('transition','Added workforce budget (A$/year)',40000),inp('stress','Stress: reduction in annual cash (%)',25,0,100,1)])+'</div></fieldset></form><div class="result-grid" aria-live="polite">'+''.join([result('uses','Total uses of capital'),result('gap','Funding difference'),result('debt','Annual modelled debt service'),result('base','Base cash after debt and workforce budget'),result('stress','Stressed cash after debt and workforce budget'),result('ratio','Stressed cash / debt service')])+'</div><p class="tool-status" id="capital-status" role="status"></p><div class="actions"><button class="button primary-button" id="capital-export" type="button">Download scenario .md</button><button class="button subtle" id="capital-reset" type="button">Restore sample inputs</button></div><p class="consent-note">Level annual repayments are used. Investor distributions, earn-outs, refinancing and tax changes are not forecast. A guarantee is not counted as funding. The ratio is a simple cash comparison, not a lender\'s eligibility test.</p></div></div></section>'
 if kind=='workforce':
  return '''<section class="section" id="tool"><div class="wrap"><span class="tag demo">Browser-local planning tool</span><h2 style="margin-top:20px">My next chapter</h2><p class="measure muted">Sketch preferences, not an approved employment arrangement. Save only when you choose, or download a Markdown copy to keep elsewhere.</p><div class="tool"><form id="life-planner" onsubmit="return false"><label>Plan title<input id="plan-title" maxlength="160" value="My next chapter"></label><fieldset><legend>Phases of work and life</legend><div id="phase-list"></div><button id="phase-add" class="button subtle" type="button">Add a phase</button></fieldset><div class="phase-strip" id="phase-strip" aria-label="Proposed cycle"></div><h3 id="cycle-total"></h3><p class="tool-intro" id="cycle-note"></p><label>What would make this possible?<textarea id="plan-notes" maxlength="5000" placeholder="Funding, care, qualifications, hosts, travel permissions, coverage and return arrangements..."></textarea></label></form><div class="actions"><button id="life-export" class="button primary-button" type="button">Download plan .md</button><button id="life-save" class="button" type="button">Save in this browser</button><button id="life-load" class="button" type="button">Load saved draft</button><button id="life-clear" class="button subtle" type="button">Remove saved copy</button><button id="life-reset" class="button subtle" type="button">Restore example</button></div><p id="life-status" class="tool-status" role="status"></p><p class="consent-note">This tool has no account or remote storage. Browser storage is not encryption. A draft does not create a leave entitlement, employment contract, income guarantee or permission to undertake an activity overseas.</p></div></div></section>'''
 if kind=='permissions':
  opts=lambda name,label,values:'<label>'+label+f'<select name="{name}">'+''.join('<option>'+esc(v)+'</option>' for v in values)+'</select></label>'
  return '<section class="section" id="tool"><div class="wrap"><span class="tag demo">Draft builder, not access control</span><h2 style="margin-top:20px">My permissions, in plain language</h2><p class="measure muted">Express a proposed boundary without submitting personal records. The export is a draft for discussion and implementation, not a legal instrument or cryptographic guarantee.</p><div class="tool"><form id="permissions-form" onsubmit="return false"><div class="form-grid two"><label>Draft name<input name="profileName" maxlength="160" placeholder="A name for this draft"></label>'+opts('scope','Material covered',['Personal preferences','Professional record','Household material','Collective material: authority still to be established'])+opts('inference','Use for inference',['Local use only, as authorised','Specific external service, by separate agreement','Not yet decided'])+opts('training','Use for model training',['Not authorised by this draft','Specific research only, separately agreed','Specific model only, separately agreed','Not yet decided'])+opts('offDevice','Off-device sharing',['No sharing authorised by this draft','Named recipients and purposes only','An agreed public subset only','Not yet decided'])+opts('retention','Retention preference',['For the agreed purpose and period only','Keep my own copy; external retention separately agreed','Not yet decided'])+'<label>Named recipients and purposes<textarea name="recipients" maxlength="3000" placeholder="Describe roles or purposes, without adding private contact details."></textarea></label><label>What should happen when permission changes?<textarea name="revoke" maxlength="3000" placeholder="Future use, access, retention and records each need an actual arrangement."></textarea></label><label class="full-width">Questions and implementation notes<textarea name="notes" maxlength="5000" placeholder="Legal obligations, cultural authority, trained-model effects and technical enforcement remain distinct questions."></textarea></label></div></form><div class="actions"><button id="permissions-export" class="button primary-button" type="button">Download draft .md</button><button id="permissions-json" class="button" type="button">Download draft .json</button><button id="permissions-save" class="button" type="button">Save in this browser</button><button id="permissions-load" class="button" type="button">Load saved draft</button><button id="permissions-clear" class="button subtle" type="button">Remove saved copy</button></div><p id="permissions-status" class="tool-status" role="status"></p><p class="consent-note">No personal data is sent to a model or server by this tool. Applicable retention requirements, collective authority and the limits of revocation need their own treatment in an actual implementation.</p></div></div></section>'
 if kind=='dependencies':
  return '''<section class="section" id="tool"><div class="wrap"><span class="tag demo">Fixed illustrative model</span><h2 style="margin-top:20px">Dependency studio</h2><p class="measure muted">Select an interruption and trace a small service network. A path in this graph is not a prediction of real-world failure.</p><div class="tool" id="dependency-tool"><h3>Which service is unavailable in this sketch?</h3><div id="dependency-inputs" class="check-grid"></div><div class="tag-row"><span class="tag source">Gold: selected interruption</span><span class="tag proposal">Violet: dependency path</span><span class="tag demo">Teal: no path traced</span></div><div id="dependency-grid" class="dependency-grid" aria-live="polite"></div><p id="dependency-status" class="tool-status" role="status"></p><label>Notes, substitutes and questions<textarea id="dependency-notes" maxlength="5000" placeholder="Which real assets, people, tested alternatives or uncertain assumptions would change this sketch?"></textarea></label><div class="actions"><button id="dependency-export" class="button primary-button" type="button">Download scenario .md</button><button id="dependency-reset" class="button subtle" type="button">Clear interruptions</button></div><p class="consent-note">The graph treats an edge as a complete dependency for tracing. It has no live sensors, geography, buffers, capacity, timing, severity or probability model. It is not an emergency instruction or safety assessment.</p></div></div></section>'''
 return ''
def section(s,n):
 h='<section class="section'+(' tint' if n%2 else '')+f'"><div class="wrap"><div class="section-head reveal"><div><span class="section-number">{n:02d} / EXPLORE</span><h2>{s["title"]}</h2></div></div>'
 if s.get('text'):h+='<div class="prose measure reveal">'+para(s['text'])+'</div>'
 if s.get('statement'):h+='<p class="statement reveal">'+esc(s['statement'])+'</p>'
 if s.get('cards'):
  cards=s['cards'];cl='four-col' if len(cards)==4 else 'three-col' if len(cards)%3==0 else 'two-col'
  h+=f'<div class="{cl}">'
  for i,c in enumerate(cards):
   inside=f'<span class="card-num">{i+1:02d}</span><h3>{esc(c["title"])}</h3><p>{esc(c["text"])}</p>'
   h+=link(c['href'],inside+'<span class="arrow" aria-hidden="true">↗</span>','card card-link reveal') if c.get('href') else '<article class="card reveal">'+inside+'</article>'
  h+='</div>'
 if s.get('flow'):h+='<div class="flow reveal">'+''.join('<span><strong>'+esc(a)+'</strong>'+esc(b)+'</span>' for a,b in s['flow'])+'</div>'
 if s.get('table'):
  t=s['table'];h+='<div class="table-scroll reveal"><table class="info-table"><thead><tr>'+''.join('<th scope="col">'+esc(x)+'</th>' for x in t['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(x)+'</td>' for x in row)+'</tr>' for row in t['rows'])+'</tbody></table></div>'
 if s.get('callout'):h+='<aside class="callout reveal">'+para(s['callout'])+'</aside>'
 h+=refs(s.get('refs',[]))+'</div></section>';return h

def guide(d):
 return f'''# {d['title']}: source reading guide\n\nSource ID: {d['id']}\nOriginal filename: {d['original_name']}\nType: {d['kind']}\nExtent: {d['pages']}\nSupplied: {d['supplied']}\nOriginal SHA-256: {d['sha256']}\n\n## Relationship to Mutual Futures\n\n{d['summary']}\n\n## Selected source locations\n\n{d['locations']}\n\n## Source status and open questions\n\n{d['caution']}\n\n## Guide and original are different\n\nThis is a reading guide, not a full transcription or replacement for the original. The public library reports whether the unchanged original is actually present in the repository. Original files in the handover bundle retain their original bytes. A proposal, an archived claim, a calculation and an independently verified fact are distinct.\n\nMutual Futures: {SITE['url']}\nRepository: {SITE['repo']}\n\nSource by Luke Nathan Hayes and the collaborators identified in the original. Guide prepared for Mutual Futures with ChatGPT, September 2026. Strange But True Public Source Licence; third-party rights remain with their holders.\n'''

for folder in ['assets','documents/guides','documents/originals']:(OUT/folder).mkdir(parents=True,exist_ok=True)
for name in ['style.css','app.js']:shutil.copy2(ROOT/'assets'/name,OUT/'assets'/name)
if (ROOT/'assets/images').exists():shutil.copytree(ROOT/'assets/images',OUT/'assets/images',dirs_exist_ok=True)
if (ROOT/'assets/asset-manifest.json').exists():shutil.copy2(ROOT/'assets/asset-manifest.json',OUT/'assets/asset-manifest.json')
for d in DOCS:
 (OUT/d['guide_path']).write_text(guide(d));orig=ROOT/d['original_path'];d['original_available']=False
 if orig.exists():
  if hashlib.sha256(orig.read_bytes()).hexdigest()!=d['sha256']:raise ValueError('Original checksum mismatch: '+d['original_name'])
  shutil.copy2(orig,OUT/d['original_path']);d['original_available']=True
(OUT/'documents/manifest.json').write_text(json.dumps(DOCS,indent=2,ensure_ascii=False)+'\n')
shutil.copy2(ROOT/'LICENCE.md',OUT/'LICENCE.md')

def extra(p):
 typ=p.get('type');h=''
 if typ=='library':
  h='<section class="section"><div class="wrap" data-filter-scope><label for="library-search" class="kicker">Search the source shelf</label><input class="search-box" id="library-search" data-search type="search" placeholder="Search titles, themes or source status"><div class="filter-row">'+''.join(f'<button class="filter {"active" if v=="all" else ""}" data-filter="{v}" aria-pressed="{str(v=="all").lower()}">{t}</button>' for v,t in [('all','All sources'),('working','Working papers'),('submission','Submissions'),('discussion','Discussion')])+'</div><p data-count class="small muted" role="status"></p><div class="library-grid">'
  for d in DOCS:
   category='working' if d['kind']=='Working paper' or d['kind']=='Specification working paper' else 'discussion' if d['kind']=='Discussion paper' else 'submission'
   h+=f'<article class="document" id="{d["id"]}" data-item data-category="{category}"><p class="doc-meta">{d["id"]} / {esc(d["kind"])} / {esc(d["pages"])}</p><h3>{esc(d["title"])}</h3><p>{esc(d["summary"])}</p><div class="tag-row"><span class="tag archived">Author source, not independent verification</span></div><div class="actions">'+link(d['guide_path'],'Download reading guide .md','button download',True)
   if d['original_available']:h+=link(d['original_path'],'Download unchanged original','button download',True)
   h+='</div>'
   if not d['original_available']:h+='<p class="original-pending">The unchanged original is not yet published in this repository. The downloadable guide is not the original document.</p>'
   h+='<details><summary>Source locations, status and provenance</summary><p>'+esc(d['locations'])+'</p><p>'+esc(d['caution'])+'</p><p>Original filename: '+esc(d['original_name'])+'</p><p>Original checksum: <code>'+d['sha256']+'</code></p></details></article>'
  h+='</div><p hidden data-no-results class="no-results">No sources match this search.</p></div></section>'
 elif typ=='sources':
  h='<section class="section"><div class="wrap" data-filter-scope><label for="source-search" class="kicker">Search references and connections</label><input id="source-search" class="search-box" data-search type="search" placeholder="A project, source or subject"><div class="filter-row"><button class="filter active" data-filter="all" aria-pressed="true">All references</button><button class="filter" data-filter="project" aria-pressed="false">Project family</button><button class="filter" data-filter="external" aria-pressed="false">External sources</button></div><p data-count class="small muted" role="status"></p>'
  for r in PROJECTS+SOURCES:
   isproj=r in PROJECTS;h+=f'<article class="reference" id="{r["id"]}" data-item data-category="{"project" if isproj else "external"}"><span class="ref-code">{r["id"]}</span><div><h3>{esc(r["title"])}</h3><p>{esc(r["text"])}</p><p class="small">'+esc(r['role'] if isproj else r['kind']+' · '+r['checked'])+'</p>'+link(r['url'],'Open source ↗')
   if isproj:h+=' &nbsp; '+link('https://github.com/auraofintelligence/'+r['repo'],'Repository ↗')
   h+='</div></article>'
  h+='<p hidden data-no-results class="no-results">No references match this search.</p></div></section>'
 elif typ=='roadmap':
  h='<section class="section tint"><div class="wrap"><div class="timeline">'
  for year,title,text,status in TIMELINE:h+='<article class="reveal"><span class="year">'+esc(year)+'</span><h3>'+esc(title)+'</h3><p>'+esc(text)+'</p><span class="tag proposal">'+esc(status)+'</span></article>'
  h+='</div>'+refs(['P03','P10','D04','S03'])+'</div></section>'
 elif typ=='sitemap':
  h='<section class="section"><div class="wrap"><ol class="page-map">'+''.join('<li>'+link(q['slug']+'.html#top','<strong>'+esc(q['label'])+'</strong><span>'+esc(q['intro'])+'</span>')+'</li>' for q in PAGES)+'</ol></div></section>'
 elif typ=='about':
  h='<section class="section tint"><div class="wrap"><h2>Project links and tags</h2><div class="actions">'+link(SITE['repo'],'Open the standalone repository','button')+link('LICENCE.md','Read the source licence','button download',True)+'</div><p class="source-line">Public page: '+link(SITE['url'],esc(SITE['url']))+'</p><div class="tag-row">'+''.join('<span class="tag">'+esc(t)+'</span>' for t in SITE['topics'])+'</div></div></section>'
 elif typ=='licence':
  text=(ROOT/'LICENCE.md').read_text();h='<section class="section"><div class="wrap prose measure">'
  for block in text.strip().split('\n\n'):
   if block.startswith('# '):continue
   if block.startswith('## '):h+='<h2 style="font-size:1.65rem;margin-top:38px">'+esc(block[3:])+'</h2>'
   else:h+='<p>'+esc(block).replace('\n','<br>')+'</p>'
  h+='<div class="actions">'+link('LICENCE.md','Download the licence .md','button download',True)+'</div></div></section>'
 return h

def build_page(p,index):
 plain=title_plain(p);base=SITE['url'];slug=p['slug'];home=slug=='index';accent={'gold':'var(--gold)','mint':'var(--mint)','violet':'var(--violet)'}[p['accent']]
 out=f'<!doctype html>\n<html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(p["label"])} | Mutual Futures</title><meta name="description" content="{esc(p["intro"],quote=True)}"><meta name="theme-color" content="#080d16"><link rel="canonical" href="{base}{"" if home else slug+".html"}"><meta property="og:type" content="website"><meta property="og:site_name" content="Mutual Futures"><meta property="og:title" content="{esc(plain,quote=True)}"><meta property="og:description" content="{esc(p["intro"],quote=True)}"><meta property="og:image" content="{base+image(p["image"])}"><meta property="og:url" content="{base}{"" if home else slug+".html"}"><meta name="twitter:card" content="summary_large_image"><link rel="icon" type="image/png" href="assets/images/favicon.png"><link rel="apple-touch-icon" href="assets/images/favicon.png"><link rel="stylesheet" href="assets/style.css"><script defer src="assets/app.js"></script></head><body id="top" style="--accent:{accent}"><a class="skip" href="#main">Skip to content</a>'
 out+='<header class="site-head"><div class="wrap head-inner"><a class="brand" href="index.html#top"><span class="brand-mark" aria-hidden="true"></span><span>Mutual Futures<small>Strange but True</small></span></a><nav class="primary" aria-label="Primary">'
 for s,l in [('succession','Succession'),('workforce','Work & life'),('intelligence','Intelligence'),('resilience','Long game'),('library','Library')]:out+=f'<a href="{s}.html"'+(' aria-current="page"' if s==slug else '')+'>'+l+'</a>'
 out+='</nav><button class="index-toggle" data-open-index aria-expanded="false" aria-controls="site-index" type="button"><span>All chapters</span><span aria-hidden="true">+</span></button></div><div class="reading-progress" aria-hidden="true"></div></header>'
 out+='<dialog class="index-dialog" id="site-index" aria-labelledby="index-heading"><div class="dialog-inner"><div class="dialog-top"><h2 id="index-heading">Your own route.</h2><button data-close-index class="close-menu" aria-label="Close chapter index" type="button">×</button></div><label for="index-search" class="kicker">Find a chapter</label><input id="index-search" class="search-box" type="search" placeholder="Search the workbench"><p id="index-count" class="small muted" role="status">'+str(len(PAGES))+' pages</p><nav class="menu-grid" aria-label="All chapters">'+''.join(link(q['slug']+'.html#top',f'<small>{j:02d}</small>'+esc(q['label'])) for j,q in enumerate(PAGES))+'</nav></div></dialog>'
 out+='<main id="main"><section class="hero'+(' home' if home else '')+'"><img class="hero-image" src="'+image(p['image'])+'" alt="'+esc(ASSETS[p['image']][2],quote=True)+'" fetchpriority="high"><div class="hero-orbit" aria-hidden="true"></div><div class="wrap hero-content">'
 if not home:out+='<div class="breadcrumb">'+link('index.html','Mutual Futures')+' / '+esc(p['label'])+'</div>'
 out+='<p class="kicker eyeline">'+esc(p['kicker'])+'</p><h1>'+p['title']+'</h1><p class="lede">'+esc(p['intro'])+'</p><div class="actions">'
 if home:out+=link('succession.html','Explore the proposal','button primary-button')+link('site-map.html','Find your own route','button')
 elif p.get('tool'):out+=link('#tool','Open the interactive tool','button primary-button')+link('sources.html','Follow the sources','button')
 else:out+=link('#chapter','Explore this chapter','button primary-button')+link('site-map.html','All chapters','button')
 out+='</div></div><div class="wrap hero-foot"><span>Minjerribah / Queensland / outward</span><a href="assets/asset-manifest.json" target="_blank" rel="noopener">Source concept artwork · provenance ↗</a><span>September 2026 / public workbench</span></div></section><div class="intro-strip" id="chapter"><div class="wrap"><p><strong>Explore, compare, question.</strong> Luke\'s proposed architecture, source records and bounded tools. No purchase, sign-up or agreement is required.</p><span class="tag proposal">Public proposal</span></div></div>'
 for n,s in enumerate(p['sections'],1):
  out+=section(s,n)
  if n==2 and p.get('tool'):out+=tools(p['tool'])
 out+=extra(p)
 prev=PAGES[index-1] if index else None;nextp=PAGES[index+1] if index<len(PAGES)-1 else PAGES[0]
 out+='<nav class="wrap chapter-nav" aria-label="Previous and next chapters">'
 out+=link((prev['slug'] if prev else 'site-map')+'.html#top','<span><small>'+('Previous chapter' if prev else 'Choose a path')+'</small><strong>'+esc(prev['label'] if prev else 'Full site map')+'</strong></span><span aria-hidden="true">↖</span>')
 out+=link(nextp['slug']+'.html#top','<span aria-hidden="true">↗</span><span><small>'+('Next chapter' if index<len(PAGES)-1 else 'Back to the beginning')+'</small><strong>'+esc(nextp['label'])+'</strong></span>')+'</nav></main>'
 out+='<footer class="site-footer"><div class="wrap"><div class="footer-top"><div><a class="brand" href="index.html#top"><span class="brand-mark" aria-hidden="true"></span><span>Mutual Futures<small>A wider field of choice</small></span></a><p>Business succession, shared capability and more possible lives. A public workbench by Luke Nathan Hayes / Strange But True / Aura of Intelligence. Proposals remain open to examination and change.</p></div><nav class="footer-links" aria-label="Workbench links"><h3>The workbench</h3>'+link('site-map.html','Every chapter')+link('library.html','Document library')+link('sources.html','Sources and connections')+link('about.html','About and contact')+'</nav><nav class="footer-links" aria-label="Related project links"><h3>Connected, not absorbed</h3>'+link('https://auraofintelligence.github.io/','Aura of Intelligence ↗')+link('https://auraofintelligence.github.io/strange-but-true/','Strange but True ↗')+link('https://auraofintelligence.github.io/GAJRA-earth-infinity/','GAJRA Earth ↗')+link(SITE['repo'],'GitHub repository ↗')+'</nav></div><div class="footer-bottom"><span>© 2026 Luke Nathan Hayes · '+link('licence.html','Strange But True Public Source Licence')+'</span><span>Browser-local tools · No account · <button type="button" data-print class="print-button">Print this page</button></span></div></div></footer><a href="#top" class="to-top" aria-label="Back to top">↑</a></body></html>\n'
 return out
for i,p in enumerate(PAGES):(OUT/(p['slug']+'.html')).write_text(build_page(p,i))
(OUT/'.nojekyll').write_text('')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+SITE['url']+'sitemap.xml\n')
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+SITE['url']+('' if p['slug']=='index' else p['slug']+'.html')+'</loc></url>' for p in PAGES)+'</urlset>\n')
(OUT/'404.html').write_text('<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | Mutual Futures</title><link rel="stylesheet" href="'+SITE['url']+'assets/style.css"></head><body><main class="wrap section"><p class="kicker">Mutual Futures / 404</p><h1>A different route.</h1><p>This address does not point to a page in the workbench.</p>'+link(SITE['url']+'site-map.html','Open the complete site map','button primary-button')+'</main></body></html>')
originals=sum(d['original_available'] for d in DOCS)
report=f'- {len(PAGES)} chapter and utility pages, plus a custom 404.\n- Four browser-local tools.\n- {len(DOCS)} source reading guides.\n- {originals} unchanged original documents present in this build.\n- {len(PROJECTS)} project connections and {len(SOURCES)} external source records.\n- Raster illustrations, no bundled fonts, no SVG.\n- Standalone public URL: {SITE["url"]}\n'
(OUT/'build-report.md').write_text(report)
(ROOT/'repository-metadata.json').write_text(json.dumps(dict(name='mutual-futures',description=SITE['description'][:350],homepage=SITE['url'],topics=SITE['topics']),indent=2)+'\n')
print(report)
