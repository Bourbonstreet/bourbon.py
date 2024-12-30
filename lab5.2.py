import re

file_path = "task2.html"

with open(file_path, "r", encoding="utf-8") as file:
    content = file.read()

opening_tags = re.findall(r"<([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>", content)

unique_tags = set(opening_tags)

print("Unique opening tags:", unique_tags)