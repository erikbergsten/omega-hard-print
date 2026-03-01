from .parser import md_to_html
from . import templating
from .easy import render

def print_pdf(raw, toc=False, title=None, title_page=None, subtitle=None, data=None, stylesheets=[], layout="A4", base_url=None, print_html=False, out="out.pdf"):

    if data:
        raw = templating.render(raw, data)

    html = md_to_html(
        raw,
        article_tag="h1",
        section_tag="h2",
        enable_toc=toc,
        toc_max_level=3,
        title=title,
        title_page=title_page,
        subtitle=subtitle,
    )

    if print_html:
        print(html)

    render(
        html,
        out=out,
        stylesheets=stylesheets,
        layout=layout,
        base_url=base_url
    )


