#!/usr/bin/env python3
import argparse
import yaml
from . import print_pdf
import sys
import frontmatter
from pathlib import Path

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process one or more input files with optional stylesheet(s), layout, and output file.",
    )

    # positional argument(s)
    parser.add_argument(
        "inputs",
        nargs="+",
        type=str,
        help=(
            "Path(s) to the input file(s). "
            "Multiple files are supported (e.g. via bash globs); they are processed in alphabetical order."
        ),
    )

    # stylesheet(s)
    parser.add_argument(
        "-s",
        "--stylesheet",
        dest="stylesheets",
        default=[],
        action="append",
        help=(
            "Path to a stylesheet file. "
            "May be supplied multiple times to apply multiple stylesheets in order."
        ),
    )

    parser.add_argument(
        "-v",
        "--variable",
        dest="variables",
        default=[],
        action="append",
        help=(
            "variables"
            "provide any number of key value pairs which will be set as css variables (-v foo=bar will make var(--foo) available in css)"
        ),
    )

    parser.add_argument(
        "--print-html",
        action="store_true",
        help="Whether or not to print html (good for debugging)",
    )

    parser.add_argument(
        "--print-data",
        action="store_true",
        help="Whether or not to print template data",
    )

    parser.add_argument(
        "-t",
        "--template",
        action="store_true",
        help="Whether or not to treat input as a template.",
    )

    parser.add_argument(
        "-d",
        "--data",
        dest="data",
        default=[],
        action="append",
        help="Data file(s) (yaml or json) to template content with.",
    )

    parser.add_argument(
        "--toc",
        action="store_true",
        help="Whether or not to add a table of contents",
    )

    parser.add_argument(
        "-o",
        "--out",
        type=str,
        default="out.pdf",
        help="Path to the output file (default: out.pdf)",
    )

    parser.add_argument(
        "-u",
        "--base-url",
        type=str,
        default=None,
        help="Base url for loading images and styles",
    )

    parser.add_argument(
        "--layout",
        type=str,
        default="A4",
        help="Layout name or layout configuration (default: A4, alternatives: landscape or widescreen)",
    )

    parser.add_argument(
        "--title",
        type=str,
        default=None,
        help="Title for the front page",
    )

    parser.add_argument(
        "--toc-title",
        type=str,
        default="table of contents",
        help="Title for the table of contents page",
    )

    parser.add_argument(
        "--subtitle",
        type=str,
        default=None,
        help="Subtitle for the front page",
    )

    parser.add_argument(
        "--title-page",
        type=str,
        default=None,
        help="Path to an HTML page to use as titlepage.",
    )

    return parser.parse_args()

def main() -> None:
    args = parse_args()

    # Sort input files alphabetically for deterministic, filename-based ordering
    input_files = sorted(args.inputs)

    toc = args.toc

    # Concatenate all input markdown files in sorted order
    md_parts = []
    for path in input_files:
        content = frontmatter.load(path)
        md_parts.append(content.content)

    md_raw = "\n\n".join(md_parts)
    data = {}
    for data_entry in args.data:
        if "=" in data_entry:
            key, path = data_entry.split('=')
            data_file = Path(path)
            if data_file.exists():
                data[key] = yaml.safe_load(data_file.read_text())
            else:
                print(f"ERROR: no such file: {path}")
        else:
            data_file = Path(data_entry)
            if data_file.exists():
                data = data | yaml.safe_load(data_file.read_text())
            else:
                print(f"ERROR: no such file: {data}")
    if args.print_data:
        print("DATA:\n---")
        print(yaml.dump(data) + "---")

    variables = dict(map(lambda x: x.split("="), args.variables))

    print_pdf(md_raw, toc=toc, toc_title=args.toc_title, title=args.title, subtitle=args.subtitle, title_page=args.title_page, stylesheets=args.stylesheets, base_url=args.base_url, data=data, layout=args.layout, print_html=args.print_html, out=args.out, template=args.template, variables=variables)

if __name__ == "__main__":
    main()
