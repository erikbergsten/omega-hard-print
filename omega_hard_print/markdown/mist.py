import mistune
from mistune.plugins.table import table
from io import StringIO
from . import block_code

def slugify(text):
    return '-'.join(text.lower().split(' '))

def link(text, level):
    slug = slugify(text)
    return f'<li class="level-{level}"><a href="#{slug}">{text}</a></li>\n'

def generate_toc(ast, title="table of contents"):
    out = StringIO()
    out.write(f'<article id="toc">\n<h1> { title }</h1>\n<ul>\n')
    last_h1 = "none"
    for token in ast:
        if token['type'] != 'heading':
            continue
        level = token['attrs']['level']
        text = token['children'][0]['raw']
        if level == 1:
            last_h1 = text
            out.write(link(text, level))
        elif level == 2:
            out.write(link(last_h1 + " " + text, level))
    out.write('</ul>\n</article>')
    return out.getvalue()

def generate_title_page(title, subtitle=None):
    out = StringIO()
    out.write(f'<article id="title-page">\n<h1>{title}</h1>\n')
    if subtitle:
        out.write(f'<h2>{subtitle}</h2>\n')
    out.write('</article>\n')
    return out.getvalue()

class OmegaRenderer(mistune.HTMLRenderer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def block_code(self, code, info=None):
        return block_code.render(code, info=info)

    def heading(self, text, level, **attrs):
        slug = slugify(text)
        if level == self.last_level:
            self.heading_prefix[level-1] = slug
        elif level > self.last_level:
            self.heading_prefix.append(slug)
        else:
            self.heading_prefix = self.heading_prefix[:level]
            self.heading_prefix[level-1] = slug
        self.last_level = level
        heading_id = "-".join(self.heading_prefix)
        res = super().heading(text, level, **{"id":heading_id})
        if level == 1:
            res = f"<article id='{heading_id}'>\n<section>\n"+res
            if not self.first:
                res = "</section>\n</article>\n"+ res
            self.first = False
        if level == 2:
            res = f"</section>\n<section id='{ heading_id }'>\n"+ res

        return res

    def thematic_break(self):
        return "</section>\n<section>\n"

    def __call__(self, tokens, state):
        self.first = True
        self.last_level = 0
        self.heading_prefix = []
        res = super().__call__(tokens, state)
        if self.first:
            return res
        else:
            return res + "</section>\n</article>"

md = mistune.create_markdown(renderer=None, escape=False, plugins=[table])
html = mistune.create_markdown(renderer=OmegaRenderer(escape=False), escape=False, plugins=[table])

def get_pages_style(ast):
    filtered = filter(lambda token: token['type'] == 'heading' and token['attrs']['level'] == 1, ast)
    texts = map(lambda token: token['children'][0]['raw'], filtered)
    out = StringIO()
    out.write("<style>\n")
    for text in texts:
        slug = slugify(text)
        out.write("#" + slug + "{ page: " + slug + "; }\n")
    out.write("</style>\n")
    return out.getvalue()

def md_to_html(raw, toc=False, title=None, subtitle=None, title_page=None, toc_title="table of contents"):
    ast = md(raw)
    pages_style = get_pages_style(ast)
    rendered = html(raw)
    if toc:
        toc = generate_toc(ast, title=toc_title)
        rendered = toc + rendered
    if title_page:
        content = Path(title_page).read_text()
        rendered = content + rendered
    elif title:
        titlepage = generate_title_page(title, subtitle)
        rendered = titlepage + rendered
    return f"""<html>
<head>
{ pages_style }
</head>
<body>
{rendered}
</body>
</html>
"""
