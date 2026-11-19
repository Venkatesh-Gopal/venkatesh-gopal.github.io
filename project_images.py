"""Responsive poster images shared by project cards and detail pages."""

from html import escape


def poster_paths(project, base):
    stem = f'{base}/assets/portfolio/{project["slug"]}'
    return stem + '-card.png', stem + '-card-2x.png'


def card_image(project, base):
    small, large = poster_paths(project, base)
    return (
        f'<img src="{small}" srcset="{small} 718w, {large} 1436w" '
        'sizes="(max-width: 650px) calc(100vw - 40px), (max-width: 1000px) 50vw, 33vw" '
        'alt="" width="718" height="537" loading="lazy" decoding="async">'
    )


def project_poster(project, lang, base):
    small, large = poster_paths(project, base)
    caption = escape(project['case_study']['caption'], quote=True)
    label = 'Poster in voller Größe öffnen' if lang == 'de' else 'Open full-size poster'
    return (
        '<figure class="detail-art project-poster">'
        f'<a href="{large}" target="_blank" rel="noopener" aria-label="{label}">'
        f'<img src="{small}" srcset="{small} 718w, {large} 1436w" '
        'sizes="(max-width: 900px) calc(100vw - 40px), 50vw" '
        f'alt="{caption}" width="718" height="537" decoding="async"></a>'
        f'<figcaption>{caption}<a class="poster-fullsize" href="{large}" '
        f'target="_blank" rel="noopener">{label}</a></figcaption></figure>'
    )
