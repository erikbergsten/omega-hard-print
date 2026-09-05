import mistune
from mistune.directives import RSTDirective, TableOfContents
from mistune.plugins.table import table

markdown = mistune.create_markdown(
    plugins=[
        # ...
        RSTDirective([TableOfContents()]),
        table
    ]
)

def md_to_html(raw, toc=0):
    """
    Converts markdown to html and injects a table of contents if toc is set.
    The level of header included in the toc is determined by the value of toc.
    The format of the toc directive in mistune is as follows:
    ```
    .. toc:: Table of Contents
       :max-level: <level>
    ```
    Is is compressed into a one-liner and prepended to the input markdown if
    toc is set.
    """
    if toc:
        raw = f".. toc::\n   :max-level: {toc}\n{raw}"
    return markdown(raw)
