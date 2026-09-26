from jinja2 import Template
from pathlib import Path
from .content import parse_content
from jinja2 import Environment, ChoiceLoader, FileSystemLoader, PackageLoader, DictLoader

string_templates = {}

loaders = [
    PackageLoader("omega_hard_print.templating", "templates"),
    DictLoader(string_templates),
]

tpl_dir = Path(".") / "templates"
if tpl_dir.exists() and tpl_dir.is_dir():
    print(f"adding {tpl_dir} to templates")
    loaders.append(FileSystemLoader(tpl_dir))
else:
    print("no template dir!", tpl_dir)

loader = ChoiceLoader(loaders)

env = Environment(loader=loader)

def template(file, html, data):
    text = Path(file).read_text()
    string_templates["tpl"] = text
    tpl = env.get_template("tpl")
    content, toc = parse_content(html)
    return tpl.render(chapters=content, toc=toc, **data)
