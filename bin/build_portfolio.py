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

def bullet_list(items):
    return '<ul>' + ''.join('<li>' + esc(t) + '</li>' for t in items) + '</ul>'

def callout(lang, title, text):
    d = DATA[lang]
    return f'<section class="callout"><h2>{esc(title)}</h2><p>{esc(text)}</p><a class="button primary" href="{link(lang,"contact")}">{esc(d["contact"])} <span aria-hidden="true">↗</span></a></section>'

def training(d):
    return '<section class="language-section"><h2>'+esc(d['certifications_title'])+'</h2><div class="training-grid">'+''.join(f'<article><p class="eyebrow">{esc(year)}</p><h3>{esc(title)}</h3><p>{esc(provider)}</p></article>' for year,title,provider in d['certifications'])+'</div></section>'

def body(lang, key):
    d = DATA[lang]
    if key == 'about':
        capabilities=''.join(f'<article class="capability"><span class="number">0{i+1}</span><h3>{esc(title)}</h3><p>{esc(text)}</p></article>' for i,(title,text) in enumerate(d['capabilities']))
        return f'''<section class="hero"><div class="hero-copy"><p class="eyebrow">{esc(d['hero_eyebrow'])}</p><h1>{d['headline']}</h1><p class="lead">{esc(d['intro'])}</p><p class="hero-context">{esc(d['intro_more'])}</p><p class="hero-context">{esc(d['hero_evidence'])}</p><div class="hero-expertise">{tags(d['hero_expertise'])}</div><p class="hero-domains">{esc(d['hero_domains'])}</p><p class="hero-approach">{esc(d['hero_approach'])}</p><div class="actions"><a class="button primary" href="{link(lang,'projects')}">{esc(d['view'])} <span aria-hidden="true">↗</span></a><a class="button secondary" href="{link(lang,'contact')}">{esc(d['hero_contact'])}</a></div></div><figure class="hero-figure"><div class="figure-heading"><span>VG / 01</span><span>{esc(d['role'])}</span></div><p class="figure-note">{esc(d['figure_note'])}</p><img src="{BASE}/assets/portfolio/mesh.svg" alt="" width="640" height="570"><figcaption>{esc(d['mesh'])}</figcaption></figure></section>
        <div class="focus-strip"><p class="eyebrow">{esc(d['focus'])}</p><p>{esc(d['focus_values'])}</p></div>
        <section class="section"><h2>{esc(d['capabilities_title'])}</h2><div class="capability-grid">{capabilities}</div></section>
        <section class="section"><div class="section-heading"><div><h2>{esc(d['selected'])}</h2><p>{esc(d['selected_desc'])}</p></div><a class="text-link" href="{link(lang,'projects')}">{esc(d['all'])} <span aria-hidden="true">↗</span></a></div>{cards(lang)}</section>
        <section class="about-block"><p class="eyebrow">VENKATESH GOPAL</p><div><h2>{esc(d['about_title'])}</h2><p>{esc(d['about_body'])}</p><p>{esc(d['about_more'])}</p><p>{esc(d['about_values'])}</p><p>{esc(d['about_end'])}</p><a class="text-link" href="{link(lang,'experience')}">{esc(d['nav'][2])} <span aria-hidden="true">↗</span></a></div></section>''' + callout(lang,d['closing_title'],d['closing_body'])
    if key == 'projects':
        return heading(d['eyebrow'],d['projects_title'],d['projects_intro'])+cards(lang)+f'''<section class="about-block"><p class="eyebrow">{esc(d['nav'][2])}</p><div><h2>{esc(d['project_broad_title'])}</h2><p>{esc(d['project_broad_body'])}</p><a class="text-link" href="{link(lang,'experience')}">{esc(d['nav'][2])} ↗</a></div></section>'''
    if key.startswith('projects/'):
        slug=key.split('/')[1]
        p=next(x for x in d['projects'] if x['slug']==slug)
        contribution=f'<section class="focus-panel"><h2>{esc(d["contribution_label"])}</h2>{bullet_list(p["contributions"])}</section>' if p.get('contributions') else ''
        return f'<a class="back-link" href="{link(lang,"projects")}">← {esc(d["back"])}</a>'+heading(p['category'],p['title'],p['short'])+f'''<section class="question-panel"><p class="eyebrow">{esc(d['question_label'])}</p><h2>{esc(p['question'])}</h2></section><section class="detail-grid"><figure class="detail-art"><img src="{BASE}/assets/portfolio/{slug}.svg" alt="" width="600" height="360"><figcaption>{esc(d['mesh'])}</figcaption></figure><div><h2>{esc(d['overview'])}</h2><p>{esc(p['body'])}</p>{tags(p['tags'])}</div></section>'''+contribution+f'''<section class="focus-panel"><h2>{esc(d['methods'])}</h2>{bullet_list(p['focus'])}</section><section class="project-significance"><h2>{esc(d['significance_label'])}</h2><p>{esc(p['significance'])}</p><a class="text-link" href="{link(lang,'contact')}">{esc(d['project_cta'])} ↗</a></section><section class="section"><h2>{esc(d['related'])}</h2>{cards(lang,slug)}</section>'''
    if key == 'experience':
        jobs=''.join(f'''<article><p class="eyebrow">{esc(j['dates'])}</p><div><h2>{esc(j['title'])}</h2><p class="institution">{esc(j['company'])}</p>{bullet_list(j['bullets'])}</div></article>''' for j in d['jobs'])
        education=''.join(f'<article><p class="eyebrow">{esc(year)}</p><div><h3>{esc(title)}</h3><p class="institution">{esc(place)}</p></div></article>' for year,title,place in d['education'])
        return heading(d['nav'][2],d['experience_title'],d['experience_intro'])+f'''<section aria-labelledby="work-heading"><h2 class="section-label" id="work-heading">{esc(d['work_label'])}</h2><div class="timeline">{jobs}</div></section><section class="professional-development"><p class="eyebrow">{esc(d['development_date'])}</p><h2>{esc(d['development_label'])}</h2><p>{esc(d['development_body'])}</p></section><section class="section" aria-labelledby="education-heading"><h2 class="section-label" id="education-heading">{esc(d['education_label'])}</h2><div class="timeline">{education}</div></section><section class="working-method"><h2>{esc(d['working_title'])}</h2><ol>{''.join('<li>'+esc(t)+'</li>' for t in d['working_values'])}</ol></section>'''+callout(lang,d['interests_title'],d['interests_body'])
    if key == 'skills':
        cards_html=[]
        for card in d['skill_cards']:
            tools=('<div class="skill-group"><h3>'+esc(d['skills_tools_label'])+'</h3>'+tags(card['tools'])+'</div>') if card['tools'] else ''
            methods='<div class="skill-group"><h3>'+esc(d['skills_methods_label'])+'</h3>'+tags(card['methods'])+'</div>'
            cards_html.append(f'<article class="skill-card skill-chip-card"><span class="number">{esc(card["number"])}</span><h2>{esc(card["title"])}</h2><p class="skill-description">{esc(card["description"])}</p>{tools}{methods}</article>')
        languages=''.join('<li><span>'+esc(name)+'</span><strong>'+esc(level)+'</strong></li>' for name,level in d['language_values'])
        cards_html.append('<article class="skill-card skill-chip-card language-card"><span class="number">'+str(len(d['skill_cards'])+1).zfill(2)+'</span><h2>'+esc(d['languages'])+'</h2><ul class="skill-language-list">'+languages+'</ul></article>')
        return heading(d['nav'][3],d['skills_title'],d['skills_intro'])+'<section class="skills-grid skills-chip-grid">'+''.join(cards_html)+'</section>'+training(d)
    if key == 'contact':
        return heading(d['nav'][4],d['contact_title'],d['contact_intro'])+f'''<section class="contact-grid"><article class="contact-card"><p class="eyebrow">{esc(d['contact_label'])}</p><h2>Venkatesh Gopal</h2><p>{esc(d['contact_body'])}</p><a class="email-address" href="mailto:gopal92.venkatesh@gmail.com">gopal92.venkatesh@gmail.com</a><div class="contact-actions"><a class="button primary" href="mailto:gopal92.venkatesh@gmail.com">{esc(d['email_label'])} ↗</a><a class="text-link" href="https://www.linkedin.com/in/venkatesh-gopal/">{esc(d['linkedin_label'])} ↗</a><a class="text-link" href="https://github.com/venkatesh-gopal">{esc(d['github'])} ↗</a></div></article><article class="contact-details"><p class="eyebrow">{esc(d['region'])}</p><p class="region-description">{esc(d['region_body'])}</p><h2>{esc(d['opportunities'])}</h2>{bullet_list(d['opp_values'])}<p class="availability"><span aria-hidden="true"></span>{esc(d['availability'])}</p></article></section>'''
    return heading('404',d['notfound'],d['notfoundbody'])+f'<a class="button primary" href="{link(lang,"about")}">{esc(d["home"])}</a>'

def document(lang,key):
    d=DATA[lang]
    nav=''.join(f'<a href="{link(lang,k)}"'+(' aria-current="page"' if key==k or (k=='projects' and key.startswith('projects/')) else '')+f'>{esc(label)}</a>' for k,label in zip(KEYS,d['nav']))
    switches=''.join(f'<a href="{link(l,key if key!="404" else "about")}" lang="{l}" hreflang="{l}" aria-label="'+('English' if l=='en' else 'Deutsch')+'"'+(' aria-current="true"' if l==lang else '')+'>'+l.upper()+'</a>' for l in ['en','de'])
    title=d['nav'][KEYS.index(key)] if key in KEYS else next((p['title'] for p in d['projects'] if key=='projects/'+p['slug']),d['notfound'])
    description=d['meta_description'] if key=='about' else (next(p['short'] for p in d['projects'] if key=='projects/'+p['slug']) if key.startswith('projects/') else d.get(key+'_intro',title+' · '+d['footer']))
    browser_title=d['browser_titles'].get(key,title+' · Venkatesh Gopal')
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
<title>{esc(browser_title)}</title>
<meta name="description" content="{esc(description,quote=True)}">
<meta name="color-scheme" content="light dark">
<link rel="canonical" href="{{{{ site.url }}}}{BASE}{url}">{alternate}
<meta property="og:type" content="website"><meta property="og:title" content="{esc(browser_title)}"><meta property="og:description" content="{esc(description,quote=True)}"><meta property="og:url" content="{{{{ site.url }}}}{BASE}{url}">
<link rel="icon" href="{BASE}/assets/portfolio/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{BASE}/assets/portfolio/portfolio.css">
<script src="{BASE}/assets/portfolio/portfolio.js" defer></script>
</head>
<body>
<a class="skip-link" href="#main">{esc(d['skip'])}</a>
<header class="site-header"><div class="header-inner"><a class="brand" href="{link(lang,'about')}"><span class="brand-mark" aria-hidden="true">VG<span>.</span></span><span>Venkatesh Gopal<small>{esc(d['role'])}</small></span></a><nav class="main-nav" aria-label="{'Hauptnavigation' if lang=='de' else 'Main navigation'}">{nav}</nav><div class="header-tools"><nav class="language-switch" aria-label="{'Sprache' if lang=='de' else 'Language'}">{switches}</nav><button class="theme-toggle" type="button" aria-label="{esc(d['theme'])}" aria-pressed="false" hidden><svg aria-hidden="true" viewBox="0 0 24 24" width="18" height="18"><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M12 2v3m0 14v3M2 12h3m14 0h3M5 5l2 2m10 10 2 2M5 19l2-2M17 7l2-2" stroke="currentColor" stroke-width="1.5"/></svg></button></div></div></header>
<main id="main" tabindex="-1" class="container">{body(lang,key)}</main>
<footer class="site-footer"><div class="container footer-inner"><div><strong>Venkatesh Gopal</strong><p>{esc(d['footer'])}</p></div><div class="footer-links"><a href="https://github.com/venkatesh-gopal">GitHub ↗</a><a href="https://www.linkedin.com/in/venkatesh-gopal/">LinkedIn ↗</a><a href="{link(lang,'contact')}">{esc(d['contact'])} ↗</a><p>{esc(d['footer_note'])} · © 2026</p></div></div></footer>
</body></html>
'''

if __name__=='__main__':
    pages=ROOT/'_pages'
    for lang in DATA:
        for key in KEYS+['projects/'+p['slug'] for p in DATA[lang]['projects']]:
            (pages/f'portfolio-{lang}-{key.replace("/","-")}.html').write_text(document(lang,key))
    (pages/'404.md').write_text(document('en','404'))
    print('Generated 16 bilingual pages and the 404 page.')
