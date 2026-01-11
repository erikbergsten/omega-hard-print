from markdown_it import MarkdownIt
from markdown_it.token import Token

def dict_from_code(text):
    out = {}
    for pair in text.split(","):
        try:
            key, val = pair.split("=")
            out[key] = val
        except Exception:
            out[pair] = ""
    return out

md = MarkdownIt()

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

def wrap(tokens, index, tag='article', class_name='page'):
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

def sectionize(tokens):
    sections = group(tokens, headings=["h1", "h2", "h3"])
    for i in range(0, len(sections)):
        sections[i] = wrap(sections[i], i+1, tag="section", class_name="section")
    return flatten(sections)

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

    return md.renderer.render(paged_tokens, {}, {})
