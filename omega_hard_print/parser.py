from markdown_it import MarkdownIt
from markdown_it.token import Token
from bs4 import BeautifulSoup
from io import StringIO
import textwrap

md = MarkdownIt()

def slugify(text):
    return text.lower().replace(' ', "-")

def sectionize(tokens):
    sections = []
    section = None

    for token in tokens:
        if token.type == 'heading_open':
            if section:
                sections.append(section)
            section = [token]
        else:
            if not section:
                section = []
            section.append(token)
    sections.append(section)

    return sections

class TocEntry:
    def __init__(self, level, name, children):
        self.level = level
        self.name = name
        self.children = children

class Toc:
    def __init__(self, entries, min_level=1, max_level=2):
        self.entries = entries
        self.min_level = min_level
        self.max_level = max_level

    def render_entry(self, entry, indent="  "):
        if entry.level >= self.min_level:
            slug = slugify(entry.name) + "-header"
            title = entry.name.capitalize()
            self.out.write(f'{indent}<li>\n{indent}  <a href="#{slug}"> {title} </a>\n')
        if entry.level < self.max_level and entry.children:
            self.out.write(f'{indent}  <ul>\n')
            for child in entry.children:
                self.render_entry(child, indent+"    ")
            self.out.write(f'{indent}  </ul>\n')
        if entry.level >= self.min_level:
            self.out.write(f'{indent}</li>\n')

    def render(self):
        self.out = StringIO()
        self.out.write('<ul>\n')
        for entry in self.entries:
            self.render_entry(entry)
        self.out.write('</ul>')
        return self.out.getvalue()


def get_heading_level(token):
    tag = token.tag
    level = int(tag[1:])
    return level

def get_heading_name(section):
    # Convention: the heading text is in the token immediately after
    # the heading_open, usually an 'inline' token with .content
    title_token = section[1] if len(section) > 1 else None
    name = getattr(title_token, "content", "") if title_token else ""
    return name

def build_toc(sections):
    """ GEN AI at its finest """
    toc = []
    stack = []  # will store TocEntry objects representing the current path

    for section in sections:
        if not section:
            continue

        first = section[0]
        if first.type != "heading_open":
            # Skip sections that don't start with a heading
            continue

        level = get_heading_level(first)

        name = get_heading_name(section)

        entry = TocEntry(level=level, name=name, children=[])

        # Find this entry's parent based on level
        # Pop stack until the top has a lower level than current
        while stack and stack[-1].level >= level:
            stack.pop()

        if stack:
            # Current entry is a child of the stack top
            stack[-1].children.append(entry)
        else:
            # Top-level entry
            toc.append(entry)

        # Push current entry to stack
        stack.append(entry)

    return toc

def flatten(xss):
    return [x for xs in xss for x in xs]

def group(sections, tag):
    groups = []
    group = []
    for section in sections:
        if section[0].tag == tag:
            if group:
                groups.append(group)
            group = [section]
        else:
            group.append(section)
    groups.append(group)
    return groups

def parse(text):
    tokens = md.parse(text)
    for i in range(len(tokens)):
        token = tokens[i]
        if token.type == 'heading_open':
            next_token = tokens[i+1]
            title = slugify(next_token.content)
            token.attrPush(["id", title+"-header"])
    sections = sectionize(tokens)
    return sections

def md_to_html(text, article_tag="h1", section_tag="h2", enable_toc=True, toc_min_level = 1, toc_max_level=99):
    sections = parse(text)
    articles = group(sections, article_tag)
    out = StringIO()
    out.write("<html><body>\n")
    if enable_toc:
        toc = Toc(build_toc(sections), min_level=toc_min_level, max_level=toc_max_level)
        out.write('<article id="toc">\n')
        out.write('  <h1> Table of contents </h1>')
        html = textwrap.indent(toc.render(), "  ")
        out.write(html)
        out.write('</article>')
    for article in articles:
        article_name = get_heading_name(article[0])
        article_id = slugify(article_name)
        out.write(f'<article id="{article_id}">\n')
        if section_tag:
            sections = group(article, section_tag)
            for section in sections:
                section_name = get_heading_name(section[0])
                section_id = slugify(section_name)
                out.write(f'  <section id="{section_id}">\n')
                html = textwrap.indent(render(flatten(section)), "    ")
                out.write(html)
                out.write("  </section>\n")
        else:
            html = textwrap.indent(render(flatten(article)), "  ")
            out.write(html)
        out.write("</article>\n")

    out.write("</body></html>")
    return out.getvalue()

def render(tokens):
    html = md.renderer.render(tokens, md.options, {})
    return html

if __name__ == '__main__':
    f = open("groups.md", "r")
    raw = f.read()
    html = md_to_html(raw)
    print(html)
