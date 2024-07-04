import requests

def parse_vacancies(query, area, per_page, pages):
    url = "https://api.hh.ru/vacancies"
    vacancies = []

    for page in range(pages):
        params = {
            'text': query,
            'area': area,
            'per_page': per_page,
            'page': page
        }
        response = requests.get(url, params=params)
        data = response.json()
        for item in data.get('items', []):
            salary = None
            if item.get('salary'):
                salary_from = item['salary'].get('from')
                salary_to = item['salary'].get('to')
                salary_currency = item['salary'].get('currency')
                salary = f"{salary_from}-{salary_to} {salary_currency}" if salary_from and salary_to else f"{salary_from or salary_to} {salary_currency}"
                
            vacancy = {
                'name': item.get('name'),
                'alternate_url': item.get('alternate_url'),
                'salary': salary,
                'employer': item['employer']['name'] if item.get('employer') else None,
                'requirement': item.get('snippet', {}).get('requirement')
            }
            vacancies.append(vacancy)
    return vacancies
