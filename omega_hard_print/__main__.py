from .parser import md_to_html
from . import hard_print
from .args import parse_args
from .templating import template
from pathlib import Path
import yaml

def main():
    args = parse_args()
    raw_md = "\n\n".join(map(lambda path: Path(path).read_text(), args.inputs))
    variables = dict(map(lambda x: x.split("="), args.variables))
    data = {}
    for file in args.data:
        print("loading", file)
        text = Path(file).read_text()
        content = yaml.load(text, Loader=yaml.CLoader)
        data |= content
    hard_print(raw_md=raw_md, data=data, template=args.template, path=args.out, base_url=args.base_url, title_page=args.title_page, stylesheets=args.stylesheets, variables=variables, layout=args.layout, default_style=not args.no_default_style, toc=args.toc, print_html=args.print_html)

if __name__ == '__main__':
    main()
