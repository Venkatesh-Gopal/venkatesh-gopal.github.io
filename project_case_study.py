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
    return (
        f'<a class="back-link" href="{base}{prefix}/projects/">← {escape(data["back"])}</a>'
        '<section class="page-heading compact-case-heading">'
        f'<p class="eyebrow">{escape(project["category"])}</p>'
        f'<h1>{escape(project["title"])}</h1>'
        f'<p class="lead">{escape(c["intro"])}</p></section>'
        '<div class="compact-case"><section class="detail-grid">'
        '<figure class="detail-art">'
        f'<img src="{base}/assets/portfolio/{project["slug"]}.svg" alt="{escape(c["caption"])}" width="600" height="360" />'
        f'<figcaption>{escape(c["caption"])}</figcaption></figure>'
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
