import requests
from bs4 import BeautifulSoup as BS
import time
import mysql.connector

# Параметры подключения к БД
db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='18021973564378988PpP',
    database='Work'
)
db_cursor = db_connection.cursor()


page = 1
city = "Чернігів"

while True: 
    url = f"https://www.work.ua/jobs-chernihiv/?page={page}"
    response = requests.get(url)
    soup = BS(response.content, 'html.parser')
    vacancies = soup.select("div.card.card-hover")  

    if not vacancies:
        break

    if page == 20:
        break

    for works in vacancies:
        # Название вакансии 
        title_tag = works.select_one("h2.my-0 a")
        Work_name = title_tag.text.strip() if title_tag else "Невідомо"

        # Зарплата
        salary_tag = works.select_one(".strong-600") 
        salary = salary_tag.text.strip() if salary_tag else "Не вказано"

        # Інформація про вакансію
        info_tag = works.select_one("p.ellipsis.ellipsis-line.ellipsis-line-3.text-default-7.mb-0")
        info = info_tag.text.strip() if info_tag else "Немає опису"

        # Вставка в БД
        db_cursor.execute('''
            INSERT INTO work_chernigiv (Work_name, salary, city, info)
            VALUES (%s, %s, %s, %s)
        ''', (Work_name, salary, city, info))

    print(f"Сторінка {page} оброблена.")
    page += 1
    time.sleep(1)


db_connection.commit()
db_connection.close()
