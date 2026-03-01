#!/usr/bin/env python3
import argparse
from yaml import load, CLoader
from . import print_pdf
import sys

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
        "--print-html",
        action="store_true",
        help="Whether or not to print html (good for debugging)",
    )

    parser.add_argument(
        "-t",
        "--template",
        action="store_true",
        help="Whether or not to treat input as a template. Data must be provided on stdin.",
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
        with open(path, "r") as f:
            md_parts.append(f.read())

    md_raw = "\n\n".join(md_parts)

    if args.template:
        data = load(sys.stdin.read(), Loader=CLoader)
    else:
        data = None

    print_pdf(md_raw, toc=toc, title=args.title, subtitle=args.subtitle, title_page=args.title_page, stylesheets=args.stylesheets, base_url=args.base_url, data=data, layout=args.layout, print_html=args.print_html, out=args.out)

if __name__ == "__main__":
    main()
