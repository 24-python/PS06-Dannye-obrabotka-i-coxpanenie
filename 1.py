import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Функция для рекурсивного парсинга ссылок
def parse_links(url, base_url, max_depth, current_depth=0, visited=None):
    if visited is None:
        visited = set()

    # Проверяем, достигнут ли максимальный уровень вложенности или URL уже посещен
    if current_depth > max_depth or url in visited:
        return

    visited.add(url)
    print(f"{'  ' * current_depth}URL: {url}")  # Выводим текущий URL с отступами по уровню

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка при запросе {url}: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)

    # Проходимся по всем ссылкам на текущей странице
    for link in links:
        href = link['href']
        full_url = urljoin(base_url, href)
        # Проверяем, что ссылка начинается с базового URL и не была ранее посещена
        if full_url.startswith(base_url) and full_url not in visited:
            parse_links(full_url, base_url, max_depth, current_depth + 1, visited)

# Начальный URL и базовый URL
start_url = "https://www.shokonat.ru/product/"
base_url = "https://www.shokonat.ru"

# Максимальный уровень вложенности
max_depth = 3  # Изменено на 3 для большей глубины

# Запуск рекурсивного парсинга
parse_links(start_url, base_url, max_depth)