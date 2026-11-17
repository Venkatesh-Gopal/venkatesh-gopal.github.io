"""Render the honeycomb case study using the portfolio's existing page shell."""

from html import escape


def paragraphs(items, class_name=""):
    attr = f' class="{class_name}"' if class_name else ""
    return "".join(f"<p{attr}>{escape(item)}</p>" for item in items)


def bullets(items):
    return "<ul>" + "".join(f"<li>{escape(item)}</li>" for item in items) + "</ul>"


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
    """Return main content only; the caller retains navigation and related cards."""
    c = project["case_study"]
    prefix = "/de" if lang == "de" else ""
    overview = escape(data["overview"])
    content = (
        f'<a class="back-link" href="{base}{prefix}/projects/">← {escape(data["back"])}</a>'
        '<section class="page-heading honeycomb-heading">'
        f'<p class="eyebrow">{escape(c["eyebrow"])}</p>'
        f'<h1>{escape(project["title"])}</h1>'
        f'<p class="lead">{escape(project["short"])}</p></section>'
        '<div class="honeycomb-content">'
        f'<p class="honeycomb-scope">{escape(c["scope"])}</p>'
        '<dl class="honeycomb-snapshot">'
        + "".join(
            f"<div><dt>{escape(label)}</dt><dd>{escape(value)}</dd></div>"
            for label, value in c["snapshot"]
        )
        + '</dl><section class="detail-grid honeycomb-overview">'
        '<figure class="detail-art">'
        f'<img src="{base}/assets/portfolio/honeycomb.svg" alt="{escape(c["illustration"])}" width="600" height="360" />'
        f'<figcaption>{escape(c["illustration"])}</figcaption></figure>'
        f"<div><h2>{overview}</h2><p>{escape(project['body'])}</p>"
        '<ul class="tags">'
        + "".join(f"<li>{escape(tag)}</li>" for tag in project["tags"])
        + '</ul></div></section><section class="question-panel">'
        f'<p class="eyebrow">{escape(data["question_label"])}</p>'
        f'<h2>{escape(project["question"])}</h2></section>'
        f'<nav class="honeycomb-jump" aria-label="{escape(c["jump_label"])}">'
        + "".join(f'<a href="#{anchor}">{escape(label)}</a>' for anchor, label in c["jump"])
        + "</nav>"
    )
    content += section("challenge", 1, c["challenge_title"], paragraphs(c["challenge"]))
    content += section("contribution", 2, c["contribution_title"], bullets(project["contributions"]))
    content += section(
        "tests", 3, c["tests_title"],
        table(c["test_headers"], c["test_rows"]) + paragraphs([c["test_note"]], "honeycomb-note"),
    )
    content += section(
        "models", 4, c["models_title"],
        paragraphs([c["models_intro"]]) + table(c["model_headers"], c["model_rows"]),
    )
    results = paragraphs([c["results_intro"]])
    for result in c["results"]:
        results += (
            '<article class="honeycomb-result">'
            f'<h3>{escape(result["title"])}</h3><dl class="honeycomb-reading">'
            + "".join(
                f"<div><dt>{escape(label)}</dt><dd>{escape(value)}</dd></div>"
                for label, value in result["reading"]
            )
            + "</dl>"
            + paragraphs([result["source"]], "honeycomb-source")
            + "</article>"
        )
    content += section(
        "results", 5, c["results_title"],
        results + paragraphs([c["result_note"]], "honeycomb-note"),
    )
    process = '<ol class="honeycomb-process">' + "".join(
        f"<li><h3>{escape(title)}</h3><p>{escape(text)}</p></li>"
        for title, text in c["steps"]
    ) + "</ol>"
    content += section(
        "calibration", 6, c["calibration_title"],
        paragraphs([c["calibration_intro"]]) + process
        + paragraphs([c["calibration_explanation"]])
        + paragraphs([c["calibration_limit"]], "honeycomb-note"),
    )
    content += section(
        "limits", 7, c["limits_title"],
        bullets(c["conclusions"]) + paragraphs([c["limits"]], "honeycomb-note"),
    )
    content += (
        '<details class="honeycomb-sources">'
        f'<summary>{escape(c["source_summary"])}</summary>'
        + bullets(c["sources"]) + "</details>"
        '<section class="project-significance">'
        f'<h2>{escape(data["significance_label"])}</h2>'
        f'<p>{escape(project["significance"])}</p>'
        f'<a class="text-link" href="{base}{prefix}/contact/">{escape(data["project_cta"])} ↗</a>'
        "</section></div>"
    )
    return content
