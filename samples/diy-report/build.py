from omega_hard_print import print_pdf
from pathlib import Path
import yaml

data = yaml.safe_load(Path("data.yaml").read_text())

report_dir = Path("./docs")
content = ""

for file in report_dir.iterdir():
    content += file.read_text()

content += """
# Configuration reference

A list of all config parameters

{{ m.table(configuration, ["name", "default", "description"]) }}

"""

#print(content)

print_pdf(content, out="report.pdf", toc=True, title="The report", subtitle="of doom", print_md=True, stylesheets=['style.css'], data=data)
