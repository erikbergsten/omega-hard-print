from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from markdown_it import MarkdownIt
import os
from pygments.formatters import HtmlFormatter
from importlib import resources

formatter = HtmlFormatter(style='friendly', nobackground=True)
css_definitions = formatter.get_style_defs('.highlight')

code_css = CSS(string=css_definitions)
default_css_path = resources.files(__package__).joinpath("default.css")
print("default css path:", default_css_path)
default_css = CSS(default_css_path)

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
    "1610": "320mm 200mm", # Large format 16:0 widescreen
}

dimensions = {
    "A4": [210, 297],
    "landscape": [297, 210],
    "widescreen": [320, 180],
    "1610": [320, 200],
}

def page_format(fmt = "A4"):
    size = sizes[fmt]
    width, height = dimensions[fmt]
    css = """
@page {
    size: %s;
}

:root {
    --page-width: %dmm;
    --page-height: %dmm;
}

""" % (size, width, height)
    print("style:", css)
    return CSS(string=css)


def render(html_raw, out="out.pdf", layout="A4", stylesheets=[], use_default_css=True, base_url=None):
    font_config = FontConfiguration()
    css = [page_format(layout), code_css]
    if use_default_css:
        css.append(default_css)
    if not base_url:
        base_url = f"file://{os.getcwd()}/"
    html_final = html_raw
    for stylesheet in stylesheets:
        css.append(CSS(stylesheet, font_config=font_config, base_url=base_url))
    html = HTML(string=html_final, base_url=base_url)
    html.write_pdf(out, stylesheets=css, font_config=font_config)

