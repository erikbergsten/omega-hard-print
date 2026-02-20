from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from markdown_it import MarkdownIt
import os
from pygments.formatters import HtmlFormatter

formatter = HtmlFormatter(style='friendly', nobackground=True)
css_definitions = formatter.get_style_defs('.highlight')

code_css = CSS(string=css_definitions)

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

##  every "chapter" is wrappen in an <article /> as per weasyprint examples
breaks_raw = """
article {
    break-before: always;
}
"""
breaks_css = CSS(string=breaks_raw)

watermark_positions = {
    "top-left": "top: 0; left: 0;",
    "top-right": "top: 0; right: 0;",
    "bottom-right": "bottom: 0; right: 0;",
    "bottom-left": "bottom: 0; left: 0;",
}

def watermark_css(position):
    position_str = watermark_positions[position]
    print("position:", position_str)
    style = """
#watermark {
  position: fixed;
  """ + position_str + """
  height: 1cm;
}
    """
    print("style:", style)
    return CSS(string=style)

toc_css = CSS(string="""
#toc {
  page: no-chapter;
  border-color: black;
  font-size: 1rem;
  font-weight: bold;
  ul {
    list-style: none;
    padding-left: 0cm;
    border-color: inherit;
    li {
      padding-top: .25cm;
      ul {
        font-size: 0.9rem;
        a {
          font-weight: normal;
        }
        li {
          ul {
          font-size: 0.8rem;
          }
        }
      }
      border-color: inherit;
      .section {
        break-before: never;
        border-bottom: 1px dashed;
        border-color: inherit;
      }
      a {
        font-weight: bold;
        color: inherit;
        text-decoration: none;
      }
      a::after {
        float: right;
        content: target-counter(attr(href), page);
      }

    }
  }
}
""")

def render(html_raw, out="out.pdf", layout="A4", watermark=None, watermark_position='bottom-left', breaks=True, stylesheet=None, toc=True):
    font_config = FontConfiguration()
    stylesheets = [page_format(layout), code_css]
    base_url = f"file://{os.getcwd()}/"
    html_final = html_raw
    if breaks:
        stylesheets.append(breaks_css)
    if stylesheet:
        stylesheets.append(CSS(stylesheet, font_config=font_config, base_url=base_url))
    if toc:
        stylesheets.append(toc_css)
    if watermark:
        stylesheets.append(watermark_css(watermark_position))
        html_final += f"<img id='watermark' src='{watermark}' />"
    html = HTML(string=html_final, base_url=base_url)
    html.write_pdf(out, stylesheets=stylesheets, font_config=font_config)

