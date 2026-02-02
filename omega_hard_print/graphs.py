import pygal
from pygal.style import Style, NeonStyle

import csv
from io import StringIO
import base64

default_style = Style(
    label_font_size=18,
    major_label_font_size=18,
    legend_font_size=20,
    background='transparent',
    plot_background='transparent',
    stroke_width=2,
)
styles = {
    "neon": NeonStyle(background="transparent", plot_background="transparent"),
}

def make_image_from_str(svg_str):
    return make_image_from_bytes(svg_str.encode("utf-8"))

def make_image_from_bytes(svg_bytes):
    encoded = base64.b64encode(svg_bytes).decode("utf-8")
    return f"""
        <img
            src="data:image/svg+xml;base64,{encoded}"
            alt="auto generated graph"
        />
    """

def read_csv(text):
    f = StringIO(text)
    reader = csv.reader(f)
    rows = []

    for row in reader:
        rows.append(row)

    return rows

def get_style(args):
    if args.get('style'):
        return styles.get(args['style'])
    else:
        return default_style

def horizontal_bars(text, args):
    rows = read_csv(text)
    style = get_style(args)

    bar_chart = pygal.HorizontalBar(height=len(rows)*75, style=style)

    for row in rows:
        bar_chart.add(row[0], int(row[1]))

    rendered = bar_chart.render()
    return make_image_from_bytes(rendered)


def pie_chart(text, args):
    rows = read_csv(text)
    style = get_style(args)

    pie_chart = pygal.Pie(style=style)
    if args.get('title'):
        pie_chart.title = args['title']

    for row in rows:
        pie_chart.add(row[0], int(row[1]))

    return make_image_from_bytes(pie_chart.render())

def line_chart(text, args):
    rows = read_csv(text)
    style = get_style(args)

    line_chart = pygal.Line(style=style)
    if args.get('title'):
        line_chart.title = args['title']
    line_chart.x_labels = rows[0]
    for row in rows[1:]:
        data = list(map(int, row[1:]))
        print(f"adding data for {row[0]}:", data)
        line_chart.add(row[0], data)

    return make_image_from_bytes(line_chart.render())

graph_table = {
    "horizontal-bars": horizontal_bars,
    "pie-chart": pie_chart,
    "line-chart": line_chart,
}

def get_graph(name):
    return graph_table.get(name)

def render_graph(name, text, args):
    f = get_graph(name)
    return f(text, args)
