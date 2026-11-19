"""Brief project summaries using the existing portfolio page design."""

from html import escape
from project_images import project_poster


def bullets(items):
    return '<ul>' + ''.join(f'<li>{escape(item)}</li>' for item in items) + '</ul>'


def render_project_case_study(lang, data, project, base='{{ site.baseurl }}'):
    case = project['case_study']
    prefix = '/de' if lang == 'de' else ''
    return (
        f'<a class="back-link" href="{base}{prefix}/projects/">← {escape(data["back"])}</a>'
        '<section class="page-heading compact-case-heading">'
        f'<p class="eyebrow">{escape(project["category"])}</p>'
        f'<h1>{escape(project["title"])}</h1>'
        f'<p class="lead">{escape(project["short"])}</p></section>'
        '<div class="compact-case"><section class="detail-grid">'
        + project_poster(project, lang, base)
        + f'<div><h2>{escape(data["overview"])}</h2><p>{escape(project["body"])}</p>'
        '<ul class="tags">'
        + ''.join(f'<li>{escape(tag)}</li>' for tag in project['tags'])
        + '</ul></div></section><section class="compact-case-points">'
        f'<div><h2>{escape(case["approach_title"])}</h2>'
        + bullets(case['approach'])
        + f'</div><div><h2>{escape(case["findings_title"])}</h2>'
        + bullets(case['findings'])
        + '</div></section>'
        + (f'<p class="compact-case-note">{escape(case["note"])}</p>' if case.get('note') else '')
        + '</div>'
    )
