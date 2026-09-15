from io import StringIO
from pathlib import Path

def generate_title_page(title, subtitle=None):
    out = StringIO()
    out.write(f'<div id="title-page">\n<h1>{title}</h1>\n')
    if subtitle:
        out.write(f'<h2>{subtitle}</h2>\n')
    out.write('</div>\n')
    return out.getvalue()

def get_title(args):
    if args.title_page:
        return Path(args.title_page).read_text() + "\n"
    elif args.title:
        return generate_title_page(args.title, args.subtitle) + "\n"
    else:
        return ""

