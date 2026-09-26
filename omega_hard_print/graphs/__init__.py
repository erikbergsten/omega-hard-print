from .. import templating
import pygal
from pygal.style import Style
import sys

default_style = Style(
    title_font_size=24,
    label_font_size=18,
    major_label_font_size=18,
    legend_font_size=20,
    background='transparent',
    plot_background='transparent',
    stroke_width=2,
)

def line_chart(title, labels, lines):
    line_chart = pygal.Line(style=default_style)
    line_chart.title = title
    line_chart.x_labels = map(str, labels)
    for key, value in lines.items():
        line_chart.add(key, value)
    return line_chart.render().decode('utf-8')

def pie_chart(title, data, inner_radius=0):
    pie_chart = pygal.Pie(style=default_style, inner_radius=inner_radius)
    pie_chart.title = title
    for key, value in data.items():
        pie_chart.add(key, value)
    return pie_chart.render().decode('utf-8')

def bar_chart(title, data):
    bar_chart = pygal.Bar(style=default_style)
    bar_chart.title = title
    for key, value in data.items():
        bar_chart.add(key, value)
    return bar_chart.render().decode('utf-8')

print("adding lineggraph")
templating.env.globals['graphs'] = sys.modules[__name__]
