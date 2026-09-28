"""Check built portfolio routes, translations, links and demo-content exclusion."""
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import urlsplit, unquote

root=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(); self.links=[]; self.lang=None; self.ids=set(); self.alternates={}; self.h1=0; self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html': self.lang=a.get('lang')
        if tag=='h1': self.h1+=1
        if 'id' in a: self.ids.add(a['id'])
        if tag in ('a','link','script','img'):
            u=a.get('href',a.get('src',''))
            if u: self.links.append(u)
        if tag=='link' and a.get('rel')=='alternate': self.alternates[a.get('hreflang')]=a.get('href')

paths=['','projects','experience','skills','contact','projects/steel-repair','projects/adhesive-fracture','projects/honeycomb']
count=0
for lang,prefix in [('en',''),('de','de/')]:
    for path in paths:
        f=root/prefix/path/'index.html'
        text=f.read_text(); page=Page(text)
        assert page.lang==lang,(f,'wrong language')
        assert page.h1==1,(f,'expected one main heading')
        assert set(page.alternates)=={'en','de'},(f,'missing alternate language')
        assert 'Albert Einstein' not in text and 'you@example.com' not in text,(f,'demo content')
        for target in page.links:
            parts=urlsplit(target)
            if parts.scheme or parts.netloc: continue
            dest=(root/unquote(parts.path.lstrip('/'))) if parts.path.startswith('/') else f.parent/parts.path
            if parts.path.endswith('/'): dest=dest/'index.html'
            if not parts.path: dest=f
            assert dest.exists(),(f,'missing target',target)
            if parts.fragment and dest.suffix=='.html':
                assert parts.fragment in Page(dest.read_text()).ids,(f,'missing anchor',target)
        count+=1
assert not (root/'people/index.html').exists(),'demo profiles published'
assert not (root/'blog/2022/giscus-comments/index.html').exists(),'demo posts published'
print(f'Passed: {count} bilingual pages, internal links, language metadata and demo exclusion.')
