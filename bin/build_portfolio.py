#!/usr/bin/env python3
"""Generate the bilingual portfolio from _data/portfolio.json (standard library only)."""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / '_data/portfolio.json').read_text())
esc = html.escape
KEYS = ['about', 'projects', 'experience', 'skills', 'contact']
BASE = '{{ site.baseurl }}'

def route(lang, key):
    prefix = '/de' if lang == 'de' else ''
    return prefix + ('/' if key == 'about' else '/' + key + '/')

def link(lang, key):
    return BASE + route(lang, key)

def tags(items):
    return '<ul class="tags">' + ''.join('<li>' + esc(t) + '</li>' for t in items) + '</ul>'

def cards(lang, omitted=None):
    d = DATA[lang]
    output = '<div class="project-grid">'
    for i, p in enumerate(d['projects']):
        if p['slug'] == omitted:
            continue
        output += f'''<a class="project-card" href="{link(lang, 'projects/' + p['slug'])}">
        <div class="card-art art-{i}" aria-hidden="true"><span>0{i+1}</span><img src="{BASE}/assets/portfolio/{p['slug']}.svg" alt="" width="600" height="360" loading="lazy"></div>
        <div class="card-copy"><p class="eyebrow">{esc(p['category'])}</p><h3>{esc(p['title'])}</h3><p>{esc(p['short'])}</p><span class="text-link">{esc(d['read'])} <span aria-hidden="true">↗</span></span></div></a>'''
    return output + '</div>'

def heading(eyebrow, title, description):
    return f'<section class="page-heading"><p class="eyebrow">{esc(eyebrow)}</p><h1>{esc(title)}</h1><p class="lead">{esc(description)}</p></section>'

def body(lang, key):
    d = DATA[lang]
    if key == 'about':
        return f'''<section class="hero"><div class="hero-copy"><p class="eyebrow">{esc(d['eyebrow'])}</p><h1>{d['headline']}</h1><p class="lead">{esc(d['intro'])}</p><div class="actions"><a class="button primary" href="{link(lang,'projects')}">{esc(d['view'])} <span aria-hidden="true">↗</span></a><a class="button secondary" href="{link(lang,'contact')}">{esc(d['contact'])}</a></div><p class="availability"><span aria-hidden="true"></span>{esc(d['availability'])}</p></div><figure class="hero-figure"><div class="figure-heading"><span>VG / 01</span><span>{esc(d['role'])}</span></div><img src="{BASE}/assets/portfolio/mesh.svg" alt="" width="640" height="570"><figcaption>{esc(d['mesh'])}</figcaption></figure></section>
        <div class="focus-strip"><p class="eyebrow">{esc(d['focus'])}</p><p>{esc(d['footer'])}</p></div>
        <section class="section"><div class="section-heading"><div><h2>{esc(d['selected'])}</h2><p>{esc(d['selected_desc'])}</p></div><a class="text-link" href="{link(lang,'projects')}">{esc(d['all'])} <span aria-hidden="true">↗</span></a></div>{cards(lang)}</section>
        <section class="about-block"><p class="eyebrow">{esc(d['nav'][0])} / VENKATESH GOPAL</p><div><h2>{esc(d['about_title'])}</h2><p>{esc(d['about_body'])}</p><p>{esc(d['about_end'])}</p><a class="text-link" href="{link(lang,'experience')}">{esc(d['nav'][2])} <span aria-hidden="true">↗</span></a></div></section>'''
    if key == 'projects':
        return heading(d['eyebrow'], d['projects_title'], d['projects_intro']) + cards(lang)
    if key.startswith('projects/'):
        slug = key.split('/')[1]
        p = next(x for x in d['projects'] if x['slug']==slug)
        return f'''<a class="back-link" href="{link(lang,'projects')}">← {esc(d['back'])}</a>''' + heading(p['category'],p['title'],p['short']) + f'''<section class="detail-grid"><figure class="detail-art"><img src="{BASE}/assets/portfolio/{slug}.svg" alt="" width="600" height="360"><figcaption>{esc(d['mesh'])}</figcaption></figure><div><h2>{esc(d['overview'])}</h2><p>{esc(p['body'])}</p>{tags(p['tags'])}</div></section><section class="focus-panel"><h2>{esc(d['methods'])}</h2><ul>{''.join('<li>'+esc(t)+'</li>' for t in p['focus'])}</ul></section><section class="section"><h2>{esc(d['related'])}</h2>{cards(lang,slug)}</section>'''
    if key == 'experience':
        return heading(d['nav'][2],d['experience_title'],d['experience_intro']) + f'''<div class="timeline"><article><p class="eyebrow">01 / {esc(d['work_label'])}</p><div><h2>{esc(d['work_title'])}</h2><p class="institution">{esc(d['university'])}</p><p>{esc(d['work_body'])}</p></div></article><article><p class="eyebrow">02 / {esc(d['education_label'])}</p><div><h2>{esc(d['degree'])}</h2><p class="institution">{esc(d['university'])}</p><p>{esc(d['education_body'])}</p></div></article></div><section class="callout"><h2>{esc(d['interests_title'])}</h2><p>{esc(d['interests_body'])}</p><a class="button primary" href="{link(lang,'contact')}">{esc(d['contact'])} ↗</a></section>'''
    if key == 'skills':
        groups=''.join(f'<article class="skill-card"><span class="number">{g[0]}</span><h2>{esc(g[1])}</h2><ul>'+''.join('<li>'+esc(s)+'</li>' for s in g[2])+'</ul></article>' for g in d['groups'])
        langs=''.join('<div><dt>'+esc(a)+'</dt><dd>'+esc(b)+'</dd></div>' for a,b in d['language_values'])
        return heading(d['nav'][3],d['skills_title'],d['skills_intro'])+f'<section class="skills-grid">{groups}</section><section class="language-section"><h2>{esc(d["languages"])}</h2><dl class="language-grid">{langs}</dl></section>'
    if key == 'contact':
        return heading(d['nav'][4],d['contact_title'],d['contact_intro'])+f'''<section class="contact-grid"><article class="contact-card"><p class="eyebrow">{esc(d['contact_label'])}</p><h2>Venkatesh Gopal</h2><p>{esc(d['contact_body'])}</p><a class="button primary" href="https://github.com/Venkatesh-Gopal">{esc(d['github'])} ↗</a></article><article class="contact-details"><p class="eyebrow">{esc(d['region'])}</p><h2>{esc(d['opportunities'])}</h2><ul>{''.join('<li>'+esc(t)+'</li>' for t in d['opp_values'])}</ul><p class="availability"><span aria-hidden="true"></span>{esc(d['availability'])}</p></article></section>'''
    return heading('404', d['notfound'],d['notfoundbody'])+f'<a class="button primary" href="{link(lang,"about")}">{esc(d["home"])}</a>'

def document(lang,key):
    d=DATA[lang]
    nav=''.join(f'<a href="{link(lang,k)}"'+(' aria-current="page"' if key==k or (k=='projects' and key.startswith('projects/')) else '')+f'>{esc(label)}</a>' for k,label in zip(KEYS,d['nav']))
    switches=''.join(f'<a href="{link(l,key if key!="404" else "about")}" lang="{l}" hreflang="{l}" aria-label="'+('English' if l=='en' else 'Deutsch')+'"'+(' aria-current="true"' if l==lang else '')+'>'+l.upper()+'</a>' for l in ['en','de'])
    title=d['nav'][KEYS.index(key)] if key in KEYS else next((p['title'] for p in d['projects'] if key=='projects/'+p['slug']),d['notfound'])
    description=d['intro'] if key=='about' else d.get(key+'_intro',title+' · '+d['footer'])
    url=route(lang,key) if key!='404' else '/404.html'
    alternate=''.join(f'<link rel="alternate" hreflang="{l}" href="{{{{ site.url }}}}{link(l,key)}">' for l in ['en','de']) if key!='404' else ''
    return f'''---
layout: null
title: {json.dumps(title,ensure_ascii=False)}
permalink: {url}
lang: {lang}
sitemap: {'false' if key=='404' else 'true'}
---
<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Venkatesh Gopal · {esc(d['role'])}</title>
<meta name="description" content="{esc(description,quote=True)}">
<meta name="color-scheme" content="light dark">
<link rel="canonical" href="{{{{ site.url }}}}{BASE}{url}">{alternate}
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)} · Venkatesh Gopal"><meta property="og:description" content="{esc(description,quote=True)}"><meta property="og:url" content="{{{{ site.url }}}}{BASE}{url}">
<link rel="icon" href="{BASE}/assets/portfolio/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{BASE}/assets/portfolio/portfolio.css">
<script src="{BASE}/assets/portfolio/portfolio.js" defer></script>
</head>
<body>
<a class="skip-link" href="#main">{esc(d['skip'])}</a>
<header class="site-header"><div class="header-inner"><a class="brand" href="{link(lang,'about')}"><span class="brand-mark" aria-hidden="true">VG<span>.</span></span><span>Venkatesh Gopal<small>{esc(d['role'])}</small></span></a><nav class="main-nav" aria-label="{'Hauptnavigation' if lang=='de' else 'Main navigation'}">{nav}</nav><div class="header-tools"><nav class="language-switch" aria-label="{'Sprache' if lang=='de' else 'Language'}">{switches}</nav><button class="theme-toggle" type="button" aria-label="{esc(d['theme'])}" aria-pressed="false" hidden><svg aria-hidden="true" viewBox="0 0 24 24" width="18" height="18"><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M12 2v3m0 14v3M2 12h3m14 0h3M5 5l2 2m10 10 2 2M5 19l2-2M17 7l2-2" stroke="currentColor" stroke-width="1.5"/></svg></button></div></div></header>
<main id="main" tabindex="-1" class="container">{body(lang,key)}</main>
<footer class="site-footer"><div class="container footer-inner"><div><strong>Venkatesh Gopal</strong><p>{esc(d['footer'])}</p></div><a href="{link(lang,'contact')}">{esc(d['contact'])} <span aria-hidden="true">↗</span></a></div></footer>
</body></html>
'''

if __name__=='__main__':
    pages=ROOT/'_pages'
    for lang in DATA:
        for key in KEYS+['projects/'+p['slug'] for p in DATA[lang]['projects']]:
            (pages/f'portfolio-{lang}-{key.replace("/","-")}.html').write_text(document(lang,key))
    (pages/'404.md').write_text(document('en','404'))
    print('Generated 16 bilingual pages and the 404 page.')
