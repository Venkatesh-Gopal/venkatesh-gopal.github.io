"""Check built portfolio routes, translations, links and demo-content exclusion."""
from html.parser import HTMLParser
from pathlib import Path
import struct
import sys
from urllib.parse import urlsplit, unquote

root=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(); self.links=[]; self.images=[]; self.lang=None; self.ids=set(); self.alternates={}; self.h1=0; self.nav=[]; self.switches={}; self.nav_kind=None; self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html': self.lang=a.get('lang')
        if tag=='nav': self.nav_kind=a.get('class')
        if tag=='a' and self.nav_kind=='main-nav': self.nav.append((a.get('href'),a.get('aria-current')))
        if tag=='a' and self.nav_kind=='language-switch': self.switches[a.get('lang')]=a.get('href')
        if tag=='h1': self.h1+=1
        if tag=='img':
            self.images.append(a)
            for candidate in a.get('srcset','').split(','):
                if candidate.strip(): self.links.append(candidate.strip().split()[0])
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
        if path=='projects' or path.startswith('projects/'):
            expected={slug+'-card.png' for slug in ['adhesive-fracture','honeycomb','steel-repair']}
            previews=[img for img in page.images if urlsplit(img.get('src','')).path.endswith('-card.png')]
            assert {Path(urlsplit(img['src']).path).name for img in previews}==expected,(f,'missing project preview')
            for img in previews:
                assert (img.get('width'),img.get('height'))==('718','537'),(f,'wrong preview display dimensions')
                image_path=root/urlsplit(img['src']).path.lstrip('/')
                retina_path=image_path.with_name(image_path.stem+'-2x.png')
                assert any(urlsplit(candidate.strip().split()[0]).path.endswith(retina_path.name) for candidate in img.get('srcset','').split(',') if candidate.strip()),(f,'missing high-resolution preview')
                for candidate,dimensions in [(image_path,(718,537)),(retina_path,(1436,1074))]:
                    with candidate.open('rb') as stream: header=stream.read(24)
                    assert header[:8]==b'\x89PNG\r\n\x1a\n',(f,'preview must be PNG',candidate)
                    assert struct.unpack('>II',header[16:24])==dimensions,(f,'wrong physical PNG dimensions',candidate)
            if path.startswith('projects/'):
                slug=path.split('/')[1]
                assert '/assets/portfolio/'+slug+'-full.png' in page.links,(f,'missing original full-size poster')
        count+=1
assert not (root/'people/index.html').exists(),'demo profiles published'
assert not (root/'blog/2022/giscus-comments/index.html').exists(),'demo posts published'
print(f'Passed: {count} bilingual pages, internal links, navigation, paired language routes, contact links, work history, demo exclusion, physical 718x537 previews, 1436x1074 srcset assets and full-size poster links.')
