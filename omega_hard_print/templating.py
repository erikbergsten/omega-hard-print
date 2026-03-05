from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("omega_hard_print"),
    autoescape=select_autoescape()
)

def render(content, data):
    renderable = '{% import "macros.jinja" as m %}\n'+content
    template = env.from_string(renderable)
    return template.render(data)
