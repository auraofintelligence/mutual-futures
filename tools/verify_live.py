#!/usr/bin/env python3
"""Compare the public Pages site to the checked build, not just its HTTP status."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit
from urllib.request import Request, urlopen
import json
import os
import time

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
BASE = 'https://auraofintelligence.github.io/mutual-futures/'

class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = set()
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        attr = 'href' if tag in ('a', 'link') else 'src' if tag in ('img', 'script') else None
        if not attr or not values.get(attr):
            return
        url = urlsplit(values[attr])
        if url.scheme or url.netloc or not url.path:
            return
        path = unquote(url.path)
        target = (SITE / path).resolve()
        if target.is_relative_to(SITE.resolve()) and target.is_file():
            self.paths.add(path)

def expected_files():
    paths = {'assets/style.css', 'assets/app.js', 'documents/manifest.json', 'sitemap.xml', 'robots.txt'}
    for page in sorted(SITE.glob('*.html')):
        paths.add(page.name)
        refs = References()
        refs.feed(page.read_text(encoding='utf-8'))
        paths.update(refs.paths)
    for document in json.loads((SITE / 'documents/manifest.json').read_text()):
        paths.add(document['guide_path'])
        if document['original_available']:
            paths.add(document['original_path'])
    return {path: sha256((SITE / path).read_bytes()).hexdigest() for path in sorted(paths)}

def check(path, expected_hash):
    url = BASE + quote(path, safe='/') + '?mf-check=' + expected_hash[:12]
    result = {'path': path or '/', 'expected_sha256': expected_hash}
    try:
        request = Request(url, headers={'User-Agent': 'Mutual-Futures-site-verifier/2.0', 'Cache-Control': 'no-cache'})
        with urlopen(request, timeout=30) as response:
            data = response.read()
            actual_hash = sha256(data).hexdigest()
            result.update(status=response.status, bytes=len(data), actual_sha256=actual_hash,
                          passed=response.status == 200 and actual_hash == expected_hash)
    except Exception as error:
        result.update(status='error', error=str(error), passed=False)
    return result

def main():
    expected = expected_files()
    # A rendered README also has an h1 and the project name: compare actual bytes.
    expected[''] = expected['index.html']
    for attempt in range(1, 7):
        with ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(lambda item: check(*item), expected.items()))
        failed = [r for r in results if not r['passed']]
        print(f'Public check {attempt}: {len(results)-len(failed)}/{len(results)} exact file matches', flush=True)
        if not failed or attempt == 6:
            break
        print('Waiting for publishing: ' + ', '.join(r['path'] for r in failed), flush=True)
        time.sleep(15)
    report = {
        'checked_at_utc': datetime.now(timezone.utc).isoformat(),
        'base_url': BASE,
        'source_commit': os.environ.get('GITHUB_SHA', 'local'),
        'method': 'HTTP GET of the public directory, every generated page and locally linked resource; exact SHA-256 comparison with site/. No browser interaction is implied.',
        'passed': not failed,
        'request_count': len(results),
        'results': results,
    }
    (ROOT / 'docs').mkdir(exist_ok=True)
    (ROOT / 'docs/live-check.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return 0 if report['passed'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
