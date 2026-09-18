"""After Quarto renders, preserve legacy routes and verify archived assets.

Uses only the Python standard library. No accounts or network access required.
GitHub Pages supports HTML redirect documents, not configurable HTTP 301 rules.
"""
from html import escape
import json
import os
from pathlib import Path
import shutil
from urllib.parse import quote, unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path(os.environ.get('QUARTO_PROJECT_OUTPUT_DIR', ROOT / '_site'))
if not OUTPUT.is_absolute(): OUTPUT = ROOT / OUTPUT
routes = json.loads((ROOT / 'migration' / 'legacy-routes.json').read_text())
assets = json.loads((ROOT / 'migration' / 'asset-manifest.json').read_text())
for entry in assets:
    if entry['status'] != 'saved': raise SystemExit('Unresolved archived file: ' + entry['source_url'])
    relative = unquote(entry['path']).lstrip('/')
    src = ROOT / relative
    dst = OUTPUT / relative
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists(): shutil.copy2(src, dst)

for old, new in routes.items():
    if not old.startswith('/') or not new.startswith('/') or '..' in Path(old).parts:
        raise SystemExit('Invalid local redirect: ' + old)
    target = OUTPUT / new.lstrip('/')
    if new.endswith('/'): target = target / 'index.html'
    if not target.is_file(): raise SystemExit('Redirect target missing: ' + new)
    dest = OUTPUT / old.lstrip('/')
    if old.endswith('/'): dest = dest / 'index.html'
    if dest.exists() and 'gossner-legacy-redirect' not in dest.read_text():
        raise SystemExit('Refusing to overwrite a rendered page: ' + str(dest))
    dest.parent.mkdir(parents=True, exist_ok=True)
    new_html = escape(new, quote=True)
    dest.write_text('<!doctype html>\n<!-- gossner-legacy-redirect -->\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="robots" content="noindex">'
        f'<meta http-equiv="refresh" content="0; url={new_html}">'
        f'<link rel="canonical" href="{new_html}"><title>Page moved — Olivier Gossner</title></head>'
        f'<body><p>This page has moved. <a href="{new_html}">Continue to the page</a>.</p>'
        f'<script>location.replace({json.dumps(new)} + location.hash);</script></body></html>')

(OUTPUT / '.nojekyll').touch()
production = 'production' in os.environ.get('QUARTO_PROFILE', '').split(',')
(OUTPUT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://gossner.me/sitemap.xml\n' if production else 'User-agent: *\nDisallow: /\n')
print(f'Preserved {len(assets)} archived assets and {len(routes)} legacy page routes.')
