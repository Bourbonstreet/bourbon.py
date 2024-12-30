import re

file_path = "task_add.txt"

with open(file_path, "r", encoding="utf-8") as file:
    content = file.read()

date_pattern = r"\b(?:\d{2}[-/.]\d{2}[-/.]\d{4}|\d{4}[-/.]\d{2}[-/.]\d{2})\b"
email_pattern = r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"
website_pattern = r"\bhttps?://[^\s]+\b"

dates = re.findall(date_pattern, content)
emails = re.findall(email_pattern, content)
websites = re.findall(website_pattern, content)

dates = dates[:5]
emails = emails[:5]
websites = websites[:5]

print("Dates:", dates)
print("Emails:", emails)
print("Websites:", websites)
