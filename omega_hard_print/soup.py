from bs4 import BeautifulSoup as BS
from pathlib import Path
from .parser import md_to_html
import re

def slugify(text):
    return text.lower().replace(" ", "-")

def get_heading_level(tag, max_level):
    """Returns the integer level of a heading tag (e.g., 1 for <h1>), or 0 if not a heading."""
    regex = re.compile(f"^h[1-{max_level}]$")
    if tag.name and re.match(regex, tag.name):
        return int(tag.name[1])
    return 0

def group(html_str, max_level=6):
    # Use 'html.parser' or 'lxml'
    soup = BS(html_str, "html.parser")

    # Create a root wrapper to hold everything temporarily
    root = soup.new_tag("div", attrs={"class": "root"})

    # Extract all top-level children from the initial soup to iterate over them safely
    children = [child for child in soup.contents if child.name or str(child).strip()]
    for child in children:
        child.extract()

    # The stack keeps track of tuple: (heading_level, container_element)
    # Level 0 represents the outermost root container
    stack = [(0, root)]

    for child in children:
        current_level = get_heading_level(child, max_level)

        if current_level > 0:
            # Pop elements from the stack until we find a container with a lower heading level
            while stack and stack[-1][0] >= current_level:
                stack.pop()

            # Create the new wrapper div for this heading hierarchy
            attributes = {
                "class": f"h{current_level}",
                "id": slugify(child.text)
            }
            wrapper = soup.new_tag("div", attrs=attributes)

            # Append the wrapper to the current active container (the last item left on stack)
            stack[-1][1].append(wrapper)

            # Append the heading tag inside its own wrapper
            wrapper.append(child)

            # Push this new container onto the stack
            stack.append((current_level, wrapper))
        else:
            # For non-heading elements (like <p>, <span>, text strings),
            # append them directly to the currently active container on top of the stack
            stack[-1][1].append(child)

    # Return the inner HTML of our temporary root container, beautifully formatted
    return "".join(str(node) for node in root.contents)

def wrap_code(html):
    soup = BS(html, "html.parser")
    for pre_tag in soup.find_all("pre"):
        wrapper = soup.new_tag("div", attrs={"class": "code-wrapper"})
        pre_tag.wrap(wrapper)
    return str(soup)

def fix_toc(html):
    soup = BS(html, "html.parser")
    toc_links = soup.select("details a")
    for a_tag in toc_links:
        wrapper = soup.new_tag("div")
        a_tag.wrap(wrapper)
    return str(soup)

def format(html, max_level=6):
    return fix_toc(wrap_code(group(html, max_level)))

def pretty_print(html):
    print(BS(html, "html.parser").prettify())

if __name__ == '__main__':
    md = Path("readme.md").read_text()
    html = md_to_html(md)

    grouped = group(html, max_level=3)
    print(BS(grouped).prettify())
