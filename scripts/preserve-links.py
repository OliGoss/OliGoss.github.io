"""After Quarto renders, preserve legacy routes and verify archived assets.

Uses only the Python standard library. No accounts or network access required.
GitHub Pages supports HTML redirect documents, not configurable HTTP 301 rules.
"""
from html import escape
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import shutil
import xml.etree.ElementTree as ET
from urllib.parse import quote, unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path(os.environ.get('QUARTO_PROJECT_OUTPUT_DIR', ROOT / '_site'))
if not OUTPUT.is_absolute(): OUTPUT = ROOT / OUTPUT
routes = json.loads((ROOT / 'migration' / 'legacy-routes.json').read_text())
assets = json.loads((ROOT / 'migration' / 'asset-manifest.json').read_text())

SITE_URL = 'https://gossner.me'


class HeadMetadata(HTMLParser):
    """Collect the standard citation metadata emitted by Quarto/Pandoc."""
    def __init__(self):
        super().__init__()
        self.values = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'meta' and attrs.get('name') and attrs.get('content'):
            self.values.setdefault(attrs['name'], []).append(attrs['content'])


def insert_head(html, markup):
    marker = '</head>'
    if marker not in html:
        raise SystemExit('Rendered HTML has no closing head element.')
    return html.replace(marker, markup + '\n' + marker, 1)


def canonical_url(file):
    relative = file.relative_to(OUTPUT).as_posix()
    if relative == 'index.html':
        return SITE_URL + '/'
    if relative.endswith('/index.html'):
        return SITE_URL + '/' + relative[:-10]
    return SITE_URL + '/' + relative


def add_search_metadata():
    """Add canonical, identity and scholarly metadata to rendered pages."""
    home = OUTPUT / 'index.html'
    if home.is_file():
        identity = {
            '@context': 'https://schema.org',
            '@graph': [
                {
                    '@type': 'WebSite',
                    '@id': SITE_URL + '/#website',
                    'url': SITE_URL + '/',
                    'name': 'Olivier Gossner',
                    'description': 'Research, publications and teaching by Olivier Gossner.',
                    'inLanguage': ['en', 'fr'],
                    'publisher': {'@id': SITE_URL + '/#person'},
                },
                {
                    '@type': 'Person',
                    '@id': SITE_URL + '/#person',
                    'name': 'Olivier Gossner',
                    'url': SITE_URL + '/',
                    'image': SITE_URL + '/assets/olivier-gossner.jpeg',
                    'jobTitle': ['CNRS Research Director', 'Professor of Economics'],
                    'affiliation': [
                        {'@type': 'Organization', 'name': 'CNRS'},
                        {'@type': 'Organization', 'name': 'CREST', 'url': 'https://crest.science/'},
                        {'@type': 'CollegeOrUniversity', 'name': 'École polytechnique', 'url': 'https://www.polytechnique.edu/'},
                        {'@type': 'CollegeOrUniversity', 'name': 'London School of Economics and Political Science', 'url': 'https://www.lse.ac.uk/'},
                    ],
                    'knowsAbout': [
                        'Game theory', 'Economics of information',
                        'Bounded rationality', 'Finance', 'Insurance',
                    ],
                    'sameAs': [
                        'https://orcid.org/0000-0003-3950-0208',
                        'https://ideas.repec.org/e/pgo39.html',
                        'https://crest.science/user/olivier-gossner/',
                        'https://www.polytechnique.edu/annuaire/gossner-olivier',
                        'https://www.lse.ac.uk/people/olivier-gossner',
                    ],
                },
            ],
        }
        html = home.read_text()
        html = insert_head(html, '<script type="application/ld+json">' +
                           json.dumps(identity, ensure_ascii=False, separators=(',', ':')) +
                           '</script>')
        home.write_text(html)

    for source in (ROOT / 'papers').glob('*.qmd'):
        rendered = OUTPUT / 'papers' / (source.stem + '.html')
        if not rendered.is_file():
            continue
        source_text = source.read_text()
        pdf_match = re.search(r'^pdf:\s*["\']?([^"\'\n]+)', source_text, re.M)
        pdf_url = None
        if pdf_match:
            pdf = pdf_match.group(1).strip()
            pdf_url = pdf if urlparse(pdf).scheme else SITE_URL + '/' + pdf.lstrip('/')

        html = rendered.read_text()
        parsed = HeadMetadata()
        parsed.feed(html)
        meta = parsed.values
        title = (meta.get('citation_title') or [source.stem.replace('-', ' ')])[0]
        authors = meta.get('citation_author', ['Olivier Gossner'])
        year = (meta.get('citation_publication_date') or meta.get('citation_year') or [None])[0]
        abstract = (meta.get('citation_abstract') or [None])[0]
        journal = (meta.get('citation_journal_title') or [None])[0]
        article_url = canonical_url(rendered)
        scholarly = {
            '@context': 'https://schema.org',
            '@type': 'ScholarlyArticle',
            '@id': article_url + '#article',
            'url': article_url,
            'headline': title,
            'author': [
                ({'@id': SITE_URL + '/#person'} if name == 'Olivier Gossner'
                 else {'@type': 'Person', 'name': name})
                for name in authors
            ],
        }
        if year:
            scholarly['datePublished'] = year
        if abstract:
            scholarly['abstract'] = abstract
        if journal:
            scholarly['isPartOf'] = {'@type': 'Periodical', 'name': journal}
        if pdf_url:
            scholarly['encoding'] = {
                '@type': 'MediaObject', 'contentUrl': pdf_url,
                'encodingFormat': 'application/pdf',
            }
            if 'name="citation_pdf_url"' not in html:
                html = insert_head(html, '<meta name="citation_pdf_url" content="' +
                                   escape(pdf_url, quote=True) + '">')
        html = insert_head(html, '<script type="application/ld+json">' +
                           json.dumps(scholarly, ensure_ascii=False, separators=(',', ':')) +
                           '</script>')
        rendered.write_text(html)

    for file in OUTPUT.rglob('*.html'):
        html = file.read_text()
        if 'gossner-legacy-redirect' in html or 'rel="canonical"' in html:
            continue
        html = insert_head(html, '<link rel="canonical" href="' +
                           escape(canonical_url(file), quote=True) + '">')
        file.write_text(html)
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

add_search_metadata()
# Quarto lists directory indexes explicitly; use the same URLs as our canonicals.
sitemap = OUTPUT / 'sitemap.xml'
if sitemap.is_file():
    namespace = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', namespace)
    tree = ET.parse(sitemap)
    for location in tree.findall(f'.//{{{namespace}}}loc'):
        url = location.text or ''
        if url.startswith(SITE_URL + '/') and url.endswith('/index.html'):
            location.text = url[:-10]
    tree.write(sitemap, encoding='utf-8', xml_declaration=True)
(OUTPUT / '.nojekyll').touch()
production = 'production' in os.environ.get('QUARTO_PROFILE', '').split(',')
(OUTPUT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://gossner.me/sitemap.xml\n' if production else 'User-agent: *\nDisallow: /\n')
print(f'Preserved {len(assets)} archived assets and {len(routes)} legacy page routes.')
