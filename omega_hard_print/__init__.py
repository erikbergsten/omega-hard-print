from .markdown import md_to_html
from . import templating
from .rendering import render

def print_pdf(raw, toc=False, toc_title="table of contents", title=None, title_page=None, subtitle=None, data=None, stylesheets=[], layout="A4", base_url=None, print_html=False, print_md=False, out="out.pdf", template=False, variables={}):

    if data or template:
        raw = templating.render(raw, data)

    if print_md:
        print(raw)

    html = md_to_html(
        raw,
        toc=toc,
        toc_title=toc_title,
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
        base_url=base_url,
        variables=variables
    )
