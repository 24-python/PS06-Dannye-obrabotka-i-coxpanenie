import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Запуск Firefox
driver = webdriver.Firefox()

# URL страницы
url = "https://tomsk.hh.ru/vacancies/programmist"
driver.get(url)

# Ожидание загрузки вакансий
wait = WebDriverWait(driver, 15)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.vacancy-info--umZA61PpMY07JVJtomBA')))

# Поиск вакансий
vacancies = driver.find_elements(By.CSS_SELECTOR, 'div.vacancy-info--umZA61PpMY07JVJtomBA')

parsed_data = []

for vacancy in vacancies:
    try:
        # Название и ссылка
        title_element = vacancy.find_element(By.CSS_SELECTOR, 'a.magritte-link___b4rEM_4-3-12')
        title = title_element.text
        link = title_element.get_attribute('href')

        # Название компании
        try:
            company = vacancy.find_element(By.CSS_SELECTOR, 'span.magritte-text___tkzIl_4-3-12').text
        except:
            company = "Компания не указана"

        # Зарплата
        try:
            salary = vacancy.find_element(By.CSS_SELECTOR, 'span[data-qa="vacancy-serp__vacancy-compensation"]').text
        except:
            salary = "Не указана"

        # Сохранение данных
        parsed_data.append([title, company, salary, link])

    except Exception as e:
        print(f"Произошла ошибка при обработке вакансии: {e}")
        continue

# Закрытие драйвера
driver.quit()

# Сохранение данных в CSV
with open("hh.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название вакансии', 'Название компании', 'Зарплата', 'Ссылка на вакансию'])
    writer.writerows(parsed_data)

print(f"Парсинг завершён. Сохранено {len(parsed_data)} вакансий.")
