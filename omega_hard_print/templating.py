from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("omega_hard_print"),
    autoescape=select_autoescape()
)

def render(content, data):
    template = env.from_string(content)
    return template.render(data)
