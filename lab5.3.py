import re
import csv

# Path to the input and output files
input_file = "task3.txt"
output_file = "output.csv"

# Read the content of the file
with open(input_file, "r", encoding="utf-8") as file:
    content = file.readlines()

# Define regex patterns for each field
id_pattern = r"\b\d+\b"
last_name_pattern = r"\b[A-Z][a-z]+\b"
email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
date_pattern = r"\b\d{4}-\d{2}-\d{2}\b"
website_pattern = r"https?://[^\s]+"

# Process each line and extract data
rows = []
for line in content:
    _id = re.search(id_pattern, line)
    last_name = re.search(last_name_pattern, line)
    email = re.search(email_pattern, line)
    reg_date = re.search(date_pattern, line)
    website = re.search(website_pattern, line)

    # Append data in the correct order
    rows.append([
        _id.group(0) if _id else "",
        last_name.group(0) if last_name else "",
        email.group(0) if email else "",
        reg_date.group(0) if reg_date else "",
        website.group(0) if website else ""
    ])

# Write the normalized data to a CSV file
with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["ID", "Last Name", "Email", "Registration Date", "Website"])  # Header
    writer.writerows(rows)

print(f"Normalized data has been saved to {output_file}.")
