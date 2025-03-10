import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройки WebDriver (добавил headless-режим, если не нужен - удали)
options = webdriver.FirefoxOptions()
options.add_argument("--headless")  # Фоновый режим (убери, если нужно окно)

driver = webdriver.Firefox(options=options)

try:
    # URL страницы
    url = "https://www.divan.ru/category/divany-i-kresla"
    driver.get(url)

    # Устанавливаем ожидание
    wait = WebDriverWait(driver, 20)

    # Ждем загрузки всех карточек с товарами
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[itemprop="itemListElement"]')))

    # Ищем карточки с диванами
    divans = driver.find_elements(By.CSS_SELECTOR, 'div[itemprop="itemListElement"]')

    # Список для хранения данных
    parsed_data = []

    # Парсим данные с каждой карточки
    for divan in divans:
        try:
            # Название дивана
            try:
                name = divan.find_element(By.CSS_SELECTOR, 'a.ui-GPFV8.qUioe.ProductName span[itemprop="name"]').text
            except Exception as e:
                print(f"Ошибка при получении названия: {e}")
                name = 'Название не указано'

            # Цена дивана
            try:
                price = divan.find_element(By.CSS_SELECTOR, 'span.ui-LD-ZU.KIkOH[data-testid="price"]').text
            except Exception as e:
                print(f"Ошибка при получении цены: {e}")
                price = 'Цена не указана'

            # Ссылка на диван
            try:
                link = divan.find_element(By.CSS_SELECTOR, 'a.ui-GPFV8.qUioe.ProductName').get_attribute('href')
            except Exception as e:
                print(f"Ошибка при получении ссылки: {e}")
                link = 'Ссылка не указана'

            # Добавляем данные в список
            parsed_data.append([name, price, link])
        except Exception as e:
            print(f"Ошибка при обработке карточки: {e}")
            continue

    # Сохраняем данные в CSV
    with open("divans.csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Название', 'Цена', 'Ссылка'])
        writer.writerows(parsed_data)

    print(f"Сохранено {len(parsed_data)} записей в divans.csv")

except Exception as e:
    print(f"Ошибка: {e}")

finally:
    # Закрываем браузер в любом случае
    driver.quit()