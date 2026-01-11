#!/usr/bin/env python3
import argparse
from .easy import render
from .md import md_to_html

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process an input file with optional stylesheet, layout, and output file."
    )

    # positional argument
    parser.add_argument(
        "input",
        type=str,
        help="Path to the input file",
    )

    # named / optional arguments
    parser.add_argument(
        "--stylesheet",
        type=str,
        help="Path to the stylesheet file",
    )

    # named / optional arguments
    parser.add_argument(
        "--sections",
        type=bool,
        default=False,
        help="Whether or not to use sections (good for advanced styling)",
    )

    parser.add_argument(
        "--out",
        type=str,
        default="out.pdf",
        help="Path to the output file (default: out.pdf)",
    )

    parser.add_argument(
        "--layout",
        type=str,
        default="A4",
        help="Layout name or layout configuration (default: A4, alternatives: landscape or widescreen)",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Example usage of parsed arguments
    input_file = args.input
    stylesheet = args.stylesheet
    out = args.out
    layout = args.layout
    sections = args.sections

    # TODO: implement your tool's logic here
    print(f"Input file: {input_file}")
    print(f"Stylesheet: {stylesheet}")
    print(f"Output file: {out}")
    print(f"Layout: {layout}")
    print(f"Sections: {sections}")

    with open(input_file, "r") as f:
        md_raw = f.read()

    html = md_to_html(md_raw, sections=sections)
    print(html)
    render(html, out=out,  stylesheet=stylesheet, layout=layout)

if __name__ == "__main__":
    main()
