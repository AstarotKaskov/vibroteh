from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import sqlite3

# Функция для сохранения данных в БД
def save_to_db(title, text, image_url):
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            text TEXT,
            image_url TEXT
        )
    ''')
    cursor.execute('INSERT INTO news (title, text, image_url) VALUES (?, ?, ?)', (title, text, image_url))
    conn.commit()
    conn.close()

# Основная функция для парсинга
def scrape_and_save():
    # Настройка Selenium для работы с браузером
    chrome_options = Options()
    chrome_options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Путь к Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Открытие страницы
    driver.get('https://www.rbc.ru/tags/?tag=Украина')

    # Получение исходного HTML-кода страницы
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Поиск всех элементов новостей
    news_items = soup.find_all('div', class_='search-item')

    # Проход по каждому элементу
    for item in news_items:
        # Извлечение заголовка
        title_tag = item.find('span', class_='search-item__title')
        title = title_tag.text.strip() if title_tag else 'Без заголовка'

        # Извлечение текста
        text_tag = item.find('span', class_='search-item__text')
        text = text_tag.text.strip() if text_tag else 'Текст отсутствует'

        # Извлечение URL изображения
        image_tag = item.find('span', class_='search-item__image-block')
        image_url = None
        if image_tag:
            img_tag = image_tag.find('img')
            if img_tag and img_tag.has_attr('src'):
                image_url = img_tag['src']

        # Сохранение данных в БД
        save_to_db(title, text, image_url)

    # Закрытие браузера
    driver.quit()

if __name__ == '__main__':
    scrape_and_save()
