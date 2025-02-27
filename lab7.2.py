import requests
import json

params = {
    'text': 'Python',
    'area': 1,
    'per_page': 1
}

response = requests.get('https://api.hh.ru/vacancies', params=params)

if response.status_code == 200:
    data = response.json()

    if data['items']:
        vacancy = data['items'][0]

        print(f"Job Title: {vacancy['name']}")
        print(f"Company: {vacancy['employer']['name']}")
        print(f"City: {vacancy['area']['name']}")
        print(f"Date Published: {vacancy['published_at']}")
        print(f"Job Link: {vacancy['alternate_url']}")

        if vacancy['salary']:
            salary = vacancy['salary']
            salary_from = salary['from'] if salary['from'] else 'not specified'
            salary_to = salary['to'] if salary['to'] else 'not specified'
            print(f"Salary: from {salary_from} to {salary_to} {salary['currency']}")
        else:
            print("Salary: not specified")
    else:
        print("No vacancies found.")
else:
    print(f"Request error: {response.status_code}")
