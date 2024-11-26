import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Укажите путь к Firefox, если он не найден автоматически
firefox_binary_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"  # Укажите свой путь
geckodriver_path = r"C:\Users\ВОВАН\Documents\GitHub\PS06-Dannye-obrabotka-i-coxpanenie\geckodriver.exe"  # Укажите путь к geckodriver

# Настройки Firefox
options = Options()
options.binary_location = firefox_binary_path  # Указание пути к Firefox
options.add_argument("--start-maximized")

# Настройка сервиса Firefox
service = Service(geckodriver_path)

# Запуск драйвера Firefox
driver = webdriver.Firefox(service=service, options=options)

url = "https://tomsk.hh.ru/vacancies/programmist"
driver.get(url)

# Ожидание загрузки страницы
wait = WebDriverWait(driver, 10)

# Парсинг данных
try:
    vacancies = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.vacancy-serp-item")))
    parsed_data = []

    for vacancy in vacancies:
        try:
            # Название вакансии и ссылка
            title_element = vacancy.find_element(By.CSS_SELECTOR, 'a[data-qa="vacancy-serp__vacancy-title"]')
            title = title_element.text
            link = title_element.get_attribute("href")

            # Компания
            company_element = vacancy.find_element(By.CSS_SELECTOR, 'a[data-qa="vacancy-serp__vacancy-employer"]')
            company = company_element.text

            # Зарплата
            try:
                salary_element = vacancy.find_element(By.CSS_SELECTOR, 'span[data-qa="vacancy-serp__vacancy-compensation"]')
                salary = salary_element.text
            except:
                salary = "Зарплата не указана"

            # Сохранение данных
            parsed_data.append([title, company, salary, link])

        except Exception as e:
            print(f"Ошибка при парсинге одной из вакансий: {e}")
            continue

finally:
    driver.quit()

# Сохранение данных в CSV
with open("hh.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Название вакансии", "Название компании", "Зарплата", "Ссылка на вакансию"])
    writer.writerows(parsed_data)

print("Парсинг завершен. Данные сохранены в файл hh.csv.")
