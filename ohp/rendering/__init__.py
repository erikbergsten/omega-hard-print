from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from io import StringIO
import os

from .styles import default_css, page_format, variable_css

font_config = FontConfiguration()

def render(html, path="out.pdf", layout="A4", variables={}, base_url=None, input_stylesheets=[], title=None, subtitle=None):
    if not base_url:
        base_url = f"file://{os.getcwd()}/"

    stylesheets = [
        variable_css(variables),
        default_css,
        page_format(layout),
    ]

    for stylesheet in input_stylesheets:
        stylesheets.append(CSS(stylesheet, font_config=font_config, base_url=base_url))

    html = HTML(string=html, base_url=base_url)
    html.write_pdf(
        path,
        stylesheets=stylesheets,
        font_config=font_config
    )
