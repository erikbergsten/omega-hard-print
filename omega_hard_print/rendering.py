from . import graphs
from markdown_it import MarkdownIt
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html
from io import StringIO
import shlex


def highlight_code(code, lang, attrs):
    """Syntax highlighting function for markdown-it-py."""
    try:
        # Look up the lexer for the specified language
        lexer = get_lexer_by_name(lang)
        # Generate highlighted HTML (without the outer <pre> wrapper)
        return highlight(code, lexer, html.HtmlFormatter(nowrap=True))
    except Exception as e:
        # Fallback for unknown languages: return None to use default escaping
        print("code highlighting exception", e)
        return None


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


def custom_fence_renderer(self, tokens, idx, options, env):
    token = tokens[idx]
    # info contains the string after the backticks (e.g., 'my-special-type')
    infoline = token.info.strip() if token.info else ""
    # Use shlex to respect quoted strings
    parts = shlex.split(infoline)
    if not parts:
        info = ""
        args = {}
    else:
        info = parts[0]
        args = transform_to_dict(parts[1:])
    print("my infos:", args)
    out = StringIO()
    if graphs.get_graph(info):
        # Return custom HTML for this specific type
        graph_html = graphs.render_graph(info, token.content, args)
        out.write(f'<div class="graph-container {info}">{graph_html}')
    else:
        code = highlight_code(token.content, info, args)
        out.write(f'<div class="code-container"><pre><code class="highlight">{code}</code></pre>')
    if args.get('caption'):
        out.write(f'<span>{args["caption"]}</span>')
    out.write('</div>')
    return out.getvalue()


md = MarkdownIt()
md.enable("table")
md.add_render_rule("fence", custom_fence_renderer)


def render(tokens):
    html = md.renderer.render(tokens, md.options, {})
    return html
