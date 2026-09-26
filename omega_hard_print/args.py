import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate PDFs from markdown!",
    )

    parser.add_argument(
        "inputs",
        nargs="*",
        type=str,
        help=(
            "Path(s) to the input file(s). "
            "Multiple files are supported (e.g. via bash globs); they are procesed in the order entered."
        ),
    )

    parser.add_argument(
        "--toc",
        help="The level of heading to include in table fo contents, defaults to no table of contents. --toc 1 will create a table of contents including all h1",
    )

    parser.add_argument(
        "-o",
        "--out",
        type=str,
        default="out.pdf",
        help="Path to the output file (default: out.pdf)",
    )

    parser.add_argument(
        "-t",
        "--template",
        type=str,
        default=None,
        help="jinja template to render content",
    )

    parser.add_argument(
        "-u",
        "--base-url",
        type=str,
        default=None,
        help="Base url for loading images and styles",
    )

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
        "-d",
        "--data",
        dest="data",
        default=[],
        action="append",
        help=(
            "Path to a data file. "
            "May be supplied multiple times to add more data."
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

    parser.add_argument(
        "--layout",
        type=str,
        default="A4",
        help="Layout name or layout configuration (default: A4, alternatives: landscape or widescreen)",
    )

    parser.add_argument(
        "--print-html",
        action="store_true",
        help="Whether or not to print html (good for debugging)",
    )

    parser.add_argument(
        "--no-default-style",
        action="store_true",
        help="Whether or not disable default styles.",
    )

    return parser.parse_args()
