from .rendering import render
from .parser import md_to_html
from . import graphs
from .title import get_title
from .soup import format, pretty_print
from . import templating

def hard_print(raw_md="", data={}, path="out.pdf", layout="A4", variables={}, base_url=None, stylesheets=[], title_page=None, title=None, subtitle=None, default_style=True, template=None, toc=None, print_html=False):
    titlepage = get_title(title_page, title, subtitle)
    if template:
        content = format(md_to_html(raw_md, toc=toc))
        html = templating.template(template, content, data)
    else:
        html = titlepage + format(md_to_html(raw_md, toc=toc))

    if print_html:
        pretty_print(html)

    render(html, path=path, layout=layout, variables=variables, base_url=base_url, input_stylesheets=stylesheets, default_style=default_style)
