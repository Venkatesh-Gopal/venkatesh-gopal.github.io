"""Use real web-size poster files and retain the original scientific figures."""

from html import escape


def poster_paths(project, base):
    stem = f'{base}/assets/portfolio/{project["slug"]}'
    return stem + '-card.png', stem + '-card-2x.png', stem + '-full.png'


def card_image(project, base):
    small, retina, _ = poster_paths(project, base)
    return (
        f'<img src="{small}" srcset="{small} 718w, {retina} 1436w" '
        'sizes="(max-width: 650px) calc(100vw - 40px), (max-width: 1000px) 50vw, 33vw" '
        'alt="" width="718" height="537" loading="lazy" decoding="async" />'
    )


def project_poster(project, caption, lang, base):
    small, retina, full = poster_paths(project, base)
    label = 'Poster in voller Größe öffnen' if lang == 'de' else 'Open full-size poster'
    return (
        '<figure class="detail-art project-poster">'
        f'<a href="{full}" target="_blank" rel="noopener" aria-label="{label}">'
        f'<img src="{small}" srcset="{small} 718w, {retina} 1436w" '
        'sizes="(max-width: 780px) calc(100vw - 40px), (max-width: 900px) 718px, 50vw" '
        f'alt="{escape(caption, quote=True)}" width="718" height="537" decoding="async" /></a>'
        f'<figcaption>{escape(caption)}'
        f'<a class="poster-fullsize" href="{full}" target="_blank" rel="noopener">{label} '
        '<span aria-hidden="true">↗</span></a></figcaption></figure>'
    )
