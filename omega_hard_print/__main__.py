from .parser import md_to_html
from .title import get_title
from .rendering import render
from .args import parse_args
from .soup import format, pretty_print
from .templating import template
from pathlib import Path

def main():
    args = parse_args()
    raw_md = "\n\n".join(map(lambda path: Path(path).read_text(), args.inputs))
    variables = dict(map(lambda x: x.split("="), args.variables))
    titlepage = get_title(args)
    if args.template:
        content = format(md_to_html(raw_md, toc=args.toc))
        html = template(args.template, content)
    else:
        html = titlepage + format(md_to_html(raw_md, toc=args.toc))
    if args.print_html:
        pretty_print(html)
    render(html, path=args.out, base_url=args.base_url, input_stylesheets=args.stylesheets, variables=variables, layout=args.layout, default_style=not args.no_default_style)

if __name__ == '__main__':
    main()
