from weasyprint import CSS
from importlib import resources
from io import StringIO

default_css_path = resources.files(__package__).joinpath("default.css")
default_css = CSS(default_css_path)

sizes = {
    "A4": "A4",
    "landscape": "A4 landscape",
    "widescreen": "320mm 180mm",
    "1610": "320mm 200mm",
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
    return CSS(string=css)

def variable_css(variables):
    """
    Format a dictionary into css variables so users can adjust styles at the
    command line.
    """
    out = StringIO()
    out.write(":root {\n")
    for k, v in variables.items():
        out.write(f'--{k}: {v};\n')
    out.write("}\n")
    css = out.getvalue()
    return CSS(string=css)
