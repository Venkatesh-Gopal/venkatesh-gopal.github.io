"""Check built portfolio routes, translations, links and demo-content exclusion."""
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import urlsplit, unquote

root=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(); self.links=[]; self.lang=None; self.ids=set(); self.alternates={}; self.h1=0; self.nav=[]; self.switches={}; self.nav_kind=None; self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html': self.lang=a.get('lang')
        if tag=='nav': self.nav_kind=a.get('class')
        if tag=='a' and self.nav_kind=='main-nav': self.nav.append((a.get('href'),a.get('aria-current')))
        if tag=='a' and self.nav_kind=='language-switch': self.switches[a.get('lang')]=a.get('href')
        if tag=='h1': self.h1+=1
        if 'id' in a: self.ids.add(a['id'])
        if tag in ('a','link','script','img'):
            u=a.get('href',a.get('src',''))
            if u: self.links.append(u)
        if tag=='link' and a.get('rel')=='alternate': self.alternates[a.get('hreflang')]=a.get('href')

    def handle_endtag(self,tag):
        if tag=='nav': self.nav_kind=None

paths=['','projects','experience','skills','contact','projects/steel-repair','projects/adhesive-fracture','projects/honeycomb']
count=0
for lang,prefix in [('en',''),('de','de/')]:
    for path in paths:
        f=root/prefix/path/'index.html'
        text=f.read_text(); page=Page(text)
        assert page.lang==lang,(f,'wrong language')
        assert page.h1==1,(f,'expected one main heading')
        expected_nav=['/'+prefix+x+('/' if x else '') for x in paths[:5]]
        assert [url for url,_ in page.nav]==expected_nav,(f,'main menu must contain only the five agreed pages')
        assert sum(current=='page' for _,current in page.nav)==1,(f,'one active menu item required')
        for target_lang,target_prefix in [('en',''),('de','de/')]:
            expected='/'+target_prefix+path+('/' if path else '')
            assert page.switches[target_lang]==expected,(f,'language switch must retain current page')
            assert urlsplit(page.alternates[target_lang]).path==expected,(f,'alternate must match page')
        if path=='contact':
            assert 'mailto:gopal92.venkatesh@gmail.com' in page.links,(f,'missing email link')
            assert 'https://www.linkedin.com/in/venkatesh-gopal/' in page.links,(f,'missing LinkedIn link')
        if path=='experience':
            for employer in ['Aurora','BSH','Maruti','Braunschweig']:
                assert employer in text,(f,'missing experience',employer)
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
print(f'Passed: {count} bilingual pages, internal links, five-item menus, active navigation, paired language routes, contact links, work history and demo exclusion.')
