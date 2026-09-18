#!/usr/bin/env bash
# Run with GitHub CLI authenticated as an authorised repository administrator.
set -euo pipefail
repo='auraofintelligence/mutual-futures'
command -v gh >/dev/null || { echo 'Install GitHub CLI first.' >&2; exit 1; }
gh auth status
python - <<'PY'
import json
from pathlib import Path
m=json.loads(Path('repository-metadata.json').read_text())
Path('/tmp/mutual-futures-about.json').write_text(json.dumps({'description':m['description'],'homepage':m['homepage']}))
Path('/tmp/mutual-futures-topics.json').write_text(json.dumps({'names':m['topics']}))
PY
gh api --method PATCH "repos/$repo" --input /tmp/mutual-futures-about.json
gh api --method PUT "repos/$repo/topics" --input /tmp/mutual-futures-topics.json
if gh api "repos/$repo/pages" >/dev/null 2>&1; then
  gh api --method PUT "repos/$repo/pages" -f build_type=workflow
else
  gh api --method POST "repos/$repo/pages" -f build_type=workflow
fi
gh workflow run publish.yml --repo "$repo" --ref main
rm -f /tmp/mutual-futures-about.json /tmp/mutual-futures-topics.json
