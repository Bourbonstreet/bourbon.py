import re

file_path = "task1-ru.txt"

with open(file_path, "r", encoding="utf-8") as file:
    content = file.read()

words_3_to_5 = re.findall(r'\b[А-Яа-яЁё]{3,5}\b', content)

numbers_more_than_3 = re.findall(r'\b\d{4,}\b', content)

print("Words with 3 to 5 letters:", words_3_to_5)
print("Numbers with more than 3 digits:", numbers_more_than_3)


