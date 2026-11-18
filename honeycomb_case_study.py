"""Render a concise honeycomb case study inside the existing portfolio shell."""

from html import escape


def table(headers, rows):
    return (
        '<div class="honeycomb-table-wrap"><table><thead><tr>'
        + "".join(f'<th scope="col">{escape(label)}</th>' for label in headers)
        + "</tr></thead><tbody>"
        + "".join(
            "<tr>" + "".join(f"<td>{escape(value)}</td>" for value in row) + "</tr>"
            for row in rows
        )
        + "</tbody></table></div>"
    )


def section(anchor, number, title, content):
    return (
        f'<section id="{anchor}" class="honeycomb-section">'
        f'<div class="honeycomb-section-heading"><span class="number" aria-hidden="true">{number:02}</span>'
        f"<h2>{escape(title)}</h2></div>{content}</section>"
    )


def render_honeycomb(lang, data, project, base="{{ site.baseurl }}"):
    c = project["case_study"]
    prefix = "/de" if lang == "de" else ""
    poster_url = f'{base}/assets/portfolio/project-posters/{project["slug"]}.png'
    poster_label = "Poster in voller Größe öffnen" if lang == "de" else "Open full-size poster"
    content = (
        f'<a class="back-link" href="{base}{prefix}/projects/">← {escape(data["back"])}</a>'
        '<section class="page-heading honeycomb-heading">'
        f'<p class="eyebrow">{escape(c["eyebrow"])}</p>'
        f'<h1>{escape(project["title"])}</h1>'
        f'<p class="lead">{escape(c["intro"])}</p></section>'
        '<div class="honeycomb-content">'
        '<section class="detail-grid honeycomb-overview">'
        '<figure class="detail-art project-poster">'
        f'<a href="{poster_url}" target="_blank" rel="noopener" aria-label="{poster_label}">'
        f'<img src="{poster_url}" alt="{escape(c["illustration"])}" width="2048" height="1531" decoding="async" /></a>'
        f'<figcaption>{escape(c["illustration"])}'
        f'<a class="poster-fullsize" href="{poster_url}" target="_blank" rel="noopener">{poster_label} <span aria-hidden="true">↗</span></a></figcaption></figure>'
        f'<div><h2>{escape(c["work_title"])}</h2><p>{escape(c["work"])}</p>'
        '<ul class="tags">'
        + "".join(f"<li>{escape(tag)}</li>" for tag in project["tags"])
        + "</ul></div></section>"
    )
    content += section(
        "setup", 1, c["setup_title"], table(c["setup_headers"], c["setup_rows"])
    )
    content += section(
        "results", 2, c["results_title"],
        table(c["results_headers"], c["results_rows"])
        + f'<p class="honeycomb-note">{escape(c["conclusion"])}</p>',
    )
    content += section(
        "calibration", 3, c["calibration_title"],
        f'<p>{escape(c["calibration"])}</p>'
        f'<p class="honeycomb-note">{escape(c["calibration_limit"])}</p>',
    )
    content += (
        '<section class="project-significance">'
        f'<a class="text-link" href="{base}{prefix}/contact/">{escape(data["project_cta"])} ↗</a>'
        "</section></div>"
    )
    return content
