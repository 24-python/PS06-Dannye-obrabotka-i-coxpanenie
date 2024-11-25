from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import csv
import time

# Настройки веб-драйвера для Firefox
options = Options()
options.add_argument("--headless")  # Запуск в безголовом режиме
service = Service(executable_path="C:\\Users\\ВОВАН\\Documents\\GitHub\\PS06-Dannye-obrabotka-i-coxpanenie\\geckodriver.exe")  # Укажите путь к geckodriver
driver = webdriver.Firefox(service=service, options=options)

# URL страницы с вакансиями
url = "https://tomsk.hh.ru/vacancies/programmist"


# Функция парсинга страницы
def parse_hh():
    driver.get(url)
    time.sleep(5)  # Ждем загрузки страницы

    # Получаем все элементы вакансий
    vacancies = driver.find_elements(By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy"]')

    results = []
    for vacancy in vacancies:
        try:
            title = vacancy.find_element(By.CSS_SELECTOR, '[data-qa="serp-item__title"]').text
            link = vacancy.find_element(By.CSS_SELECTOR, '[data-qa="serp-item__title"]').get_attribute("href")
            salary = vacancy.find_element(By.CSS_SELECTOR,
                                          '[data-qa="vacancy-serp__vacancy-compensation"]').text if len(
                vacancy.find_elements(By.CSS_SELECTOR,
                                      '[data-qa="vacancy-serp__vacancy-compensation"]')) > 0 else "Не указана"
            company = vacancy.find_element(By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy-employer"]').text
            location = vacancy.find_element(By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy-address"]').text

            results.append({
                "Название": title,
                "Компания": company,
                "Зарплата": salary,
                "Локация": location,
                "Ссылка": link
            })
        except Exception as e:
            print(f"Ошибка при обработке вакансии: {e}")

    return results


# Сохраняем данные в CSV
def save_to_csv(data, filename="hh.csv"):
    with open(filename, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Название", "Компания", "Зарплата", "Локация", "Ссылка"])
        writer.writeheader()
        writer.writerows(data)


# Основной код
try:
    print("Начинаем парсинг...")
    data = parse_hh()
    save_to_csv(data)
    print(f"Данные успешно сохранены в файл hh.csv")
finally:
    driver.quit()
