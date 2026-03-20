import shlex
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html
from io import StringIO
import pandas
from . import graphs

def highlight_code(code, lang, attrs):
    """Syntax highlighting function for markdown-it-py."""
    try:
        # Look up the lexer for the specified language
        lexer = get_lexer_by_name(lang)
        # Generate highlighted HTML (without the outer <pre> wrapper)
        return highlight(code, lexer, html.HtmlFormatter(nowrap=True))
    except Exception as e:
        # Fallback for unknown languages: return None to use default escaping
        raise Exception(f"code highlighting exception {e}")

def transform_to_dict(kv_array):
    out = {}
    for item in kv_array:
        if "=" not in item:
            # Skip tokens that are not key=value
            continue
        key, value = item.split("=", 1)
        # Strip surrounding matching quotes if present
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        out[key] = value
    return out

def parse_info(infoline):
    if not infoline:
        return None, {}
    parts = shlex.split(infoline)
    if not parts:
        info = ""
        args = {}
    else:
        info = parts[0]
        args = transform_to_dict(parts[1:])
    return info, args

def render_table(code, args):
    df = pandas.read_csv(StringIO(code))
    return df.to_html(index=False, justify='start')

def render(code, info):
    lang, args = parse_info(info)
    out = StringIO()
    if lang == 'graph':
        # Return custom HTML for this specific type
        graph_html = graphs.render_graph(code, args)
        out.write(f'<div class="graph-container {info}">{graph_html}')
    elif lang == 'table':
        table = render_table(code, args)
        out.write(table)
    else:
        high_code = highlight_code(code, lang, args) if lang else code
        out.write(f'<div class="code-container"><pre><code class="highlight">{high_code}</code></pre>')
    if args.get('caption'):
        out.write(f'<span>{args["caption"]}</span>')
    out.write('</div>')
    return out.getvalue()
