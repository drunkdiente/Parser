from flask import Flask, request, render_template, jsonify
from parse import parse_vacancies
import mysql.connector
import json

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="mysql-db",
        user="ddientee",
        password="pass",
        database="hh_ru"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    area = request.form.get('area')
    per_page = int(request.form.get('per_page'))
    pages = int(request.form.get('pages'))
    filename = request.form.get('filename')

    vacancies = parse_vacancies(query, area, per_page, pages)
    with open(f"{filename}.json", 'w', encoding='utf-8') as f:
        json.dump(vacancies, f, ensure_ascii=False, indent=4)

    connection = get_db_connection()
    cursor = connection.cursor()

    for vacancy in vacancies:
        cursor.execute("""
            INSERT INTO vacancies (name, alternate_url, salary, employer, requirement)
            VALUES (%s, %s, %s, %s, %s)
        """, (vacancy['name'], vacancy['alternate_url'], vacancy['salary'], vacancy['employer'], vacancy['requirement']))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify(vacancies[:20])

@app.route('/database')
def database():
    filters = {
        'name': request.args.get('name'),
        'employer': request.args.get('employer'),
        'salary': request.args.get('salary')
    }
    vacancies = fetch_vacancies_from_db(filters)
    if request.headers.get('Accept') == 'application/json':
        return jsonify(vacancies)
    return render_template('results.html', vacancies=vacancies)

def fetch_vacancies_from_db(filters=None):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM vacancies"
    conditions = []
    values = []

    if filters:
        if filters.get('name'):
            conditions.append("name LIKE %s")
            values.append(f"%{filters['name']}%")
        if filters.get('employer'):
            conditions.append("employer LIKE %s")
            values.append(f"%{filters['employer']}%")
        if filters.get('salary'):
            conditions.append("salary LIKE %s")
            values.append(f"%{filters['salary']}%")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, values)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
