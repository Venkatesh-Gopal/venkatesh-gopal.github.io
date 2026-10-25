#!/usr/bin/env python3
"""Render portfolio-only HTML for local review without Ruby/Jekyll.

This is not a replacement for the production Jekyll build.
Usage: python bin/preview_portfolio.py [output-directory]
"""
import re
import shutil
import sys
from pathlib import Path
from build_portfolio import DATA, KEYS, ROOT, document, route


def build(destination):
    destination = Path(destination).resolve()
    if destination == ROOT or ROOT in destination.parents and destination.name not in ('.preview', '_site'):
        raise ValueError('Use .preview, _site, or an output directory outside the source tree.')
    destination.mkdir(parents=True, exist_ok=True)
    for lang, data in DATA.items():
        for key in KEYS + ['projects/' + p['slug'] for p in data['projects']]:
            target = destination / route(lang, key).strip('/') / 'index.html'
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render(document(lang, key)))
    (destination / '404.html').write_text(render(document('en', '404')))
    shutil.copytree(ROOT / 'assets/portfolio', destination / 'assets/portfolio', dirs_exist_ok=True)
    print(f'Portfolio-only preview: {destination}')


def render(source):
    source = re.sub(r'^---\n.*?\n---\n', '', source, count=1, flags=re.S)
    return source.replace('{{ site.baseurl }}', '').replace('{{ site.url }}', 'https://venkatesh-gopal.github.io')


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else ROOT / '.preview')
