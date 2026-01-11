from weasyprint import HTML, CSS
from markdown_it import MarkdownIt

html_raw = """
<article id="page-1">
    <h1> hello world </h1>
    <p> an introductory text </p>
</article>
<article id="page-2">
    <h2> a smaller thing </h2>
    <p> a text about other stuff </p>
</article>
"""

sizes = {
    "A4": "A4",
    "landscape": "A4 landscape",
    "widescreen": "320mm 180mm", # Large format 16:9 widescreen
}

def page_format(fmt = "A4"):
    size = sizes[fmt]
    css = "@page { size: %s; }" % (size,)
    print("style:", css)
    return CSS(string=css)

##  every "chapter" is wrappen in an <article /> as per weasyprint examples
breaks_raw = """
article {
    break-before: always;
}
"""
breaks_css = CSS(string=breaks_raw)

def render(html_raw, out="out.pdf", layout="A4", breaks=True, stylesheet=None):
    stylesheets = [page_format(layout)]
    if breaks:
        stylesheets.append(breaks_css)
    if stylesheet:
        stylesheets.append(CSS(stylesheet))
    html = HTML(string=html_raw)
    html.write_pdf(out, stylesheets=stylesheets)

md = MarkdownIt()
def render_md(md_raw, **kwargs):
    html_raw = md.render(md_raw)
    html = HTML(string=html_raw)
    render(html, **kwargs)

md_raw = """
# hello world

a bit of text!

## subheading

more text here!
"""

if __name__ == '__main__':
    render_md(md_raw, out="outmd.pdf")
