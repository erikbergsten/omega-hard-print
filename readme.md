# Omega Hard Print

Print PDF slides and reports from markdown files.

- Converts markdown to HTML using mistune.
- Renders html with css/images/fonts to PDF using weasyprint.


## Features

- Generate table of contents based on headers (mistune plugin)
- Use HTML file as title page or generate with title and optional subtitle at command line.
- Select document (landscape, widescreen, A4, 16x10)
- Set CSS variable values at command line.
- CSS for paged media (implemented by weasyprint) for page header/footer content and page styling.

### Future Features

- Template complex HTMl documents using jinja and data files.
- Render graphs and tables using pygal (from the creators of weasyprint).
- HTML manipulation for easier CSS styling
  * Grouping into divs based on header levels
  * Assigning ids based on div/page title
  * Previously implemented (in version 0.3) in the markdown parser, will be implemnted as a separate html manipulation module later.
- Syntax highligting for code blocks
  * Previously implemented using pygments.

## Deploying

Install module and run using uv or pip, or use the Containerfile to build a docker image.

For example, this readme was rendered using 

```
docker run -it --rm -v $PWD:/work ohp \
    readme.md \
    --out docs/readme.pdf \
    -s docs/style.css \
    --title "Omega Hard Print"
```
