"""Check rendered local links and archived file integrity before publishing."""
from html.parser import HTMLParser
import hashlib
import json
import re
from pathlib import Path
import sys
from urllib.parse import unquote, urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / '_site'
errors = []

class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=set();self.metadata={}
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag == 'meta' and attrs.get('name'):self.metadata[attrs['name']]=attrs.get('content','')
        if attrs.get('id'): self.ids.add(attrs['id'])
        if tag in ('a','link') and attrs.get('href'):self.links.append(attrs['href'])
        if tag in ('img','script','source') and attrs.get('src'):self.links.append(attrs['src'])

html_files=list(SITE.rglob('*.html'));parsed={}
for file in html_files:
    parser=Links();parser.feed(file.read_text());parsed[file]=parser
    if '{{<' in file.read_text():errors.append(f'Unrendered shortcode in {file.relative_to(SITE)}')

checked=0
for file,parser in parsed.items():
    base='https://local.test/'+str(file.relative_to(SITE))
    for link in parser.links:
        if link.startswith(('mailto:','tel:','data:','javascript:')):continue
        url=urlparse(urljoin(base,link))
        if url.netloc!='local.test':continue
        target=SITE/unquote(url.path).lstrip('/')
        if url.path.endswith('/') or target.is_dir():target=target/'index.html'
        checked+=1
        if not target.is_file():errors.append(f'{file.relative_to(SITE)}: missing {link}');continue
        if url.fragment and target.suffix=='.html' and target in parsed:
            if unquote(url.fragment) not in parsed[target].ids:
                errors.append(f'{file.relative_to(SITE)}: missing anchor {link}')

for source in (ROOT/'papers').glob('*.qmd'):
    match=re.search(r'^year: (\d+)',source.read_text(),re.M)
    if not match:continue
    rendered=SITE/'papers'/(source.stem+'.html')
    metadata=parsed[rendered].metadata if rendered in parsed else {}
    if metadata.get('citation_publication_date') != match[1]:
        errors.append(f'{source.name}: citation year differs from publication year {match[1]}')

manifest=json.loads((ROOT/'migration'/'asset-manifest.json').read_text())
for item in manifest:
    file=SITE/unquote(item['path']).lstrip('/')
    if not file.is_file():errors.append('Archived file missing: '+item['path']);continue
    digest=hashlib.sha256(file.read_bytes()).hexdigest()
    if digest!=item['sha256']:errors.append('Archived file changed: '+item['path'])

routes=json.loads((ROOT/'migration'/'legacy-routes.json').read_text())
for old,new in routes.items():
    file=SITE/old.lstrip('/')
    if old.endswith('/'):file=file/'index.html'
    if not file.is_file() or 'gossner-legacy-redirect' not in file.read_text():errors.append('Legacy route missing: '+old)

size=sum(f.stat().st_size for f in SITE.rglob('*') if f.is_file())
if size>1024**3:errors.append('Published website exceeds the GitHub Pages 1 GiB limit.')
source_large=[str(f.relative_to(ROOT)) for f in ROOT.rglob('*.pdf') if '_site' not in f.parts and f.stat().st_size>25*1024**2]
if source_large:errors.append('PDF exceeds browser upload limit: '+', '.join(source_large))

if errors:
    print('\n'.join(errors));sys.exit(1)
print(f'PASS: {len(html_files)} HTML pages, {checked} local links, {len(manifest)} archived assets with matching hashes, {len(routes)} legacy routes; {size/1024**2:.1f} MiB published.')
