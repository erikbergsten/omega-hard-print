# whats the deal with demos?

---

The  `<hr />` elements (represented by `---` in md) create new `<sections>` in
the rendered html which allows easier layouts of pages in a presentation.

---

```line-chart caption="some important data"
2005,2010,2015,2020,2025
foo,1,2,3,4,5
bar,1,2,1,2,3
baz,4,4,3,4,5
```

# pie chart also

---

Normally you get a new `<article>` with each top level heading and a `<section>`
with each second level heading but in a presentation you might not want so many
subheadings.

---

```pie-chart caption="some important data"
foo,1
bar,2
baz,3
```

# and maybe a table

---

> this page simply has a blockquote and a table

---

|name|default|description|
|-|-|-|
| address | `https://google.com` | the address of the page |
| value | 1 | the value of the page |
| autorization | none | the authorization (of the page) |
| timeout | 5s | the time out, of the page |

# A sick slide with the code on the left

---

```python caption="hello-world.py"
def main():
  print("hello world!")

if __name__ == "__main__":
  main()
```

---

This is some code you can take home and study.
