import requests

from bs4 import BeautifulSoup

url = "https://"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
rows = soup.find_all("tr")
# tr - каждый ряд таблицы
# td - каждая ячейка внутри ряда таблицы
data = []

for row in rows:
    cols = row.find_all("td")
    cleaned_cols = [col.text.strip() for col in cols]
    data.append(cleaned_cols)

print(data)
