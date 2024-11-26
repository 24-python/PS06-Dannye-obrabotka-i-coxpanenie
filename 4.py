from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import csv

# Путь к Edge WebDriver
webdriver_path = "C:\\Users\\ВОВАН\\Documents\\GitHub\\PS06-Dannye-obrabotka-i-coxpanenie\\msedgedriver.exe"  # Укажите путь к вашему веб-драйверу

# URL для парсинга
url = "https://tomsk.hh.ru/vacancies/programmist"

# Настройка браузера
options = webdriver.EdgeOptions()
options.add_argument("--start-maximized")
service = EdgeService(webdriver_path)

# Запуск браузера
driver = webdriver.Edge(service=service, options=options)
driver.get(url)

# Задержка для загрузки страницы
time.sleep(5)

# Парсинг данных
vacancies = []
try:
    while True:
        # Находим элементы вакансий
        vacancy_elements = driver.find_elements(By.CSS_SELECTOR, 'vacancy-info--umZA61PpMY07JVJtomBA')
        for vacancy in vacancy_elements:
            try:
                title = vacancy.find_element(By.CSS_SELECTOR, '[data-qa="serp-item__title"]').text
                link = vacancy.find_element(By.CSS_SELECTOR, '[data-qa="serp-item__title"]').get_attribute("href")
                salary = vacancy.find_element(By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy-compensation"]').text
                company = vacancy.find_element(By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy-employer"]').text
                location = vacancy.find_element(By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy-address"]').text

                vacancies.append([title, link, salary, company, location])
            except Exception as e:
                # Пропускаем вакансии с отсутствующими элементами
                continue

        # Переход на следующую страницу
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, '[data-qa="pager-next"]')
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            ActionChains(driver).move_to_element(next_button).click().perform()
            time.sleep(5)  # Ждём загрузки следующей страницы
        except Exception as e:
            # Если кнопка "Далее" отсутствует, выходим из цикла
            break
finally:
    driver.quit()

# Сохранение данных в CSV
csv_file = "hh.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Название", "Ссылка", "Зарплата", "Компания", "Местоположение"])
    writer.writerows(vacancies)

print(f"Данные сохранены в файл {csv_file}")
