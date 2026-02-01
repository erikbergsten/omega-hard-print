from markdown_it import MarkdownIt
from markdown_it.token import Token
from . import graphs

def transform_to_dict(kv_array):
    # Dictionary comprehension for a succinct one-liner
    return {
        key: value 
        for item in kv_array 
        for key, value in [item.split("=", 1)]
    }

md = MarkdownIt()
md.enable("table")


def custom_fence_renderer(self, tokens, idx, options, env):
    token = tokens[idx]
    # info contains the string after the backticks (e.g., 'my-special-type')
    infoline = token.info.strip() if token.info else ""
    infos = infoline.split(" ")
    info = infos[0]
    args = transform_to_dict(infos[1:])
    print("my infos:", args)

    if graphs.get_graph(info):
        # Return custom HTML for this specific type
        return graphs.render_graph(info, token.content, args)
    else:
        return f"<pre><code>{token.content}</code></pre>"

md.add_render_rule("fence", custom_fence_renderer)

def group(tokens, headings=["h1", "h2"]):
    groups = []
    group = None
    for token in tokens:
        if token.type == "heading_open" and token.tag in headings:
            # emit old group, start new group
            if group:
                groups.append(group)
            group = [token]
        else:
            group.append(token)
    groups.append(group)
    return groups

def wrap(tokens, index, tag='article', class_name='chapter'):
    open_tag = Token(f'{tag}_open', tag, 1)
    close_tag = Token(f'{tag}_close', tag, -1)
    open_tag.attrPush(["id", f"{class_name}-{index}"])

    """
    if len(page) > 4:
        elem = page[4]
        if len(elem.children) > 0 and elem.children[0].tag == "code":
            content = elem.children[0].content
            params = dict_from_code(content)
            if params.get('layout'):
                open_tag.attrPush(["class", params['layout']])
            if  len(elem.children) == 1:
                del page[4]
            else:
                del page[4].children[0]
    """

    return [open_tag] + tokens + [close_tag]

def flatten(pages):
    out = []
    for page in pages:
        out.extend(page)
    return out

def group_sections(tokens):
    groups = []
    group = []
    for token in tokens:
        if token.type == 'hr':
            groups.append(group)
            group = []
        else:
            group.append(token)
    # add group in prgogress before returning (unless empty!)
    if len(group) > 0:
        groups.append(group)

    return groups

def sectionize(tokens):
    sections = group_sections(tokens)
    for i in range(0, len(sections)):
        sections[i] = wrap(sections[i], i+1, tag="section", class_name="section")
    return flatten(sections)

if __name__=='__main__':
    raw_md = """# hello world

some text

---

and more stuff

## new text

and stuff
"""

    pages = group(md.parse(raw_md))
    print("the first page:", pages[0], "\n")
    sections = sectionize(pages[0])
    print("the first page sections:", sections)

def md_to_html(md_raw, sections=True):
    # get flat tokens
    tokens = md.parse(md_raw)

    # paginate
    pages = group(tokens)

    # sectionize pages if needed
    if sections:
        for i in range(0, len(pages)):
            pages[i] = sectionize(pages[i])

    # add article wrapper tags
    for i in range(0, len(pages)):
        pages[i] = wrap(pages[i], i+1)

    # flatten pages again
    paged_tokens = flatten(pages)

    return md.renderer.render(paged_tokens, md.options, {})
