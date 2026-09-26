from bs4 import BeautifulSoup as BS

class ContentMap:

    def __init__(self, content, raw, id=None):
        self.content = content
        self.raw = raw
        self.id = id
        self.item_dict = {}
        for item in self.content:
            self.item_dict[item['id']] = item

    def __getitem__(self, name):
        if name == 'id':
            return self.id
        else:
            return self.item_dict.get(name)

    def __iter__(self):
        for item in self.content:
            yield item

    def __str__(self):
        return self.raw

def parse_content(html):
    soup = BS(html, "html.parser")
    def parse_element(element, current_level):
        if current_level >= 6:
            return []
        next_level = current_level + 1
        children_maps = []
        for sub_element in element.select(f"div.h{next_level}"):
            nested_children = parse_element(sub_element, next_level)
            children_maps.append(ContentMap(
                nested_children,
                str(sub_element),
                id=sub_element.get('id')
            ))
        return children_maps

    top_level_chapters = parse_element(soup, current_level=0)
    soup2 = BS(html, "html.parser")
    content = ContentMap(top_level_chapters, "\n".join(str(div) for div in soup.select("div.h1")))
    toc = str(soup.select_one("details.toc"))
    return [content, toc]
