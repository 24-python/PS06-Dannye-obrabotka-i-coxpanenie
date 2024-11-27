import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Запускаем браузер Firefox
driver = webdriver.Firefox()

# URL страницы
url = "https://www.divan.ru/krasnoyarsk/category/divany-i-kresla"
driver.get(url)

# Устанавливаем ожидание
wait = WebDriverWait(driver, 20)

# Ожидаем загрузки всех элементов с диванами
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.WdR1o')))  # Измените селектор на актуальный

# Ищем все карточки с диванами
divans = driver.find_elements(By.CSS_SELECTOR, 'div.WdR1o')  # Измените селектор на актуальный

# Список для хранения данных
parsed_data = []

# Парсим данные с каждой карточки
for divan in divans:
    try:
        # Название дивана
        try:
            name = divan.find_element(By.CSS_SELECTOR, 'a.ui-GPFV8').text  # Измените селектор на актуальный
        except:
            name = 'Название не указано'

        # Цена дивана
        try:
            price = divan.find_element(By.CSS_SELECTOR, 'div.pY3d2').text  # Измените селектор на актуальный
        except:
            price = 'Цена не указана'

         #Ссылка на диван
        try:
            link = divan.find_element(By.CSS_SELECTOR, 'a.ui-GPFV8').get_attribute('href')  # Измените селектор на актуальный
        except:
            link = 'Ссылка не указана'

        # Добавляем данные в список
        parsed_data.append([name, price, link])
    except Exception as e:
        print(f"Ошибка при обработке дивана: {e}")
        continue

# Закрываем браузер
driver.quit()
print(parsed_data)
# # Сохраняем данные в CSV
# with open("divans.csv", 'w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Название', 'Цена', 'Ссылка'])
#     writer.writerows(parsed_data)
#
# print(f"Сохранено {len(parsed_data)} записей в файл divans.csv.")