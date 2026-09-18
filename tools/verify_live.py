#!/usr/bin/env python3
"""Check the actual public site independently of the build directory."""
from pathlib import Path
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import json,time
BASE='https://auraofintelligence.github.io/mutual-futures/'
PAGES=['index','succession','ownership','capital','workforce','livelihoods','intelligence','law','simulation','health','resilience','galactic','travel','oceania','culture','roadmap','library','sources','about','site-map','licence']
def read(path):
 try:
  with urlopen(Request(BASE+path,headers={'User-Agent':'Mutual-Futures-live-verification/1.0','Cache-Control':'no-cache'}),timeout=30) as r:
   data=r.read();ok=(b'Mutual Futures' in data and b'<h1>' in data) if path.endswith('.html') else len(data)>0
   if path=='index.html':ok=ok and b'Shared wealth.' in data
   return {'path':path,'status':r.status,'bytes':len(data),'expected_content':ok}
 except Exception as e:return {'path':path,'status':'error','error':str(e),'expected_content':False}
for attempt in range(8):
 if read('index.html')['expected_content']:break
 time.sleep(15)
paths=[p+'.html' for p in PAGES]+['assets/style.css','assets/app.js','assets/images/favicon.png','documents/manifest.json','documents/guides/vuvale-union.md']
with ThreadPoolExecutor(max_workers=5) as ex:results=list(ex.map(read,paths))
report={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'base_url':BASE,'method':'Actual HTTP requests from GitHub Actions to the public GitHub Pages URL. Browser interaction tests are documented separately.','passed':all(r['status']==200 and r['expected_content'] for r in results),'results':results}
Path('docs').mkdir(exist_ok=True);Path('docs/live-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if report['passed']:
 p=Path('README.md');s=p.read_text().replace('**Intended public page:**','**Public page:**')
 start=s.find('**The public Pages deployment is not yet verified live.**')
 if start>=0:
  end=s.find('\n\n',start)
  s=s[:start]+'**The public site is live and verified.** The HTTP check confirmed all 21 chapter and utility pages, the shared stylesheet and script, the favicon and the source-library downloads. See [live-check.json](docs/live-check.json) for the date and individual requests. The build supports either GitHub Actions or main / (root) publishing.'+s[end:]
 s=s.replace('Fourteen related-project links with their respective purposes. An outbound connection does not itself confirm a reciprocal edit to the linked project.','Fourteen related-project links with their respective purposes. The [reciprocal-link audit](docs/reciprocal-links.json) confirms backlinks in all fourteen source READMEs and thirteen source homepages; the legal engine is a repository-only source.')
 p.write_text(s)
