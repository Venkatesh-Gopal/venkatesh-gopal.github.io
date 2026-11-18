"""Concise renderer for the fracture and bonded-steel case studies."""

from html import escape


def table(headers, rows):
    return (
        '<div class="compact-case-table"><table><thead><tr>'
        + "".join(f'<th scope="col">{escape(value)}</th>' for value in headers)
        + "</tr></thead><tbody>"
        + "".join(
            "<tr>" + "".join(f"<td>{escape(value)}</td>" for value in row) + "</tr>"
            for row in rows
        )
        + "</tbody></table></div>"
    )


def render_project_case_study(lang, data, project, base="{{ site.baseurl }}"):
    c = project["case_study"]
    prefix = "/de" if lang == "de" else ""
    poster_url = f'{base}/assets/portfolio/project-posters/{project["slug"]}.png'
    poster_label = "Poster in voller Größe öffnen" if lang == "de" else "Open full-size poster"
    return (
        f'<a class="back-link" href="{base}{prefix}/projects/">← {escape(data["back"])}</a>'
        '<section class="page-heading compact-case-heading">'
        f'<p class="eyebrow">{escape(project["category"])}</p>'
        f'<h1>{escape(project["title"])}</h1>'
        f'<p class="lead">{escape(c["intro"])}</p></section>'
        '<div class="compact-case"><section class="detail-grid">'
        '<figure class="detail-art project-poster">'
        f'<a href="{poster_url}" target="_blank" rel="noopener" aria-label="{poster_label}">'
        f'<img src="{poster_url}" alt="{escape(c["caption"])}" width="2048" height="1531" decoding="async" /></a>'
        f'<figcaption>{escape(c["caption"])}'
        f'<a class="poster-fullsize" href="{poster_url}" target="_blank" rel="noopener">{poster_label} <span aria-hidden="true">↗</span></a></figcaption></figure>'
        f'<div><h2>{escape(c["focus_title"])}</h2><p>{escape(c["focus"])}</p>'
        '<ul class="tags">'
        + "".join(f"<li>{escape(tag)}</li>" for tag in project["tags"])
        + '</ul></div></section><section class="compact-case-section" id="setup">'
        f'<h2>{escape(c["setup_title"])}</h2>'
        + table(c["setup_headers"], c["setup_rows"])
        + '</section><section class="compact-case-section" id="findings">'
        f'<h2>{escape(c["results_title"])}</h2>'
        + table(c["result_headers"], c["result_rows"])
        + '</section><section class="compact-case-section" id="interpretation">'
        f'<h2>{escape(c["conclusion_title"])}</h2><p>{escape(c["conclusion"])}</p>'
        f'<p class="compact-case-note">{escape(c["note"])}</p></section>'
        '<section class="project-significance">'
        f'<a class="text-link" href="{base}{prefix}/contact/">{escape(data["project_cta"])} ↗</a>'
        "</section></div>"
    )
