import requests
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Функция для получения данных о погоде из OpenWeatherMap
def get_weather_data(api_key, city='London'):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на статус ответа
        data = response.json()

        # Извлечение необходимых данных о погоде
        weather_data = {
            'city': city,
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'description': data['weather'][0]['description']
        }
        return weather_data

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при подключении к API: {e}")
        return None

# Функция для сохранения данных в CSV
def save_to_csv(weather_data, filename='weather_data.csv'):
    fieldnames = ['city', 'temperature', 'humidity', 'wind_speed', 'description']
    
    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            # Запись заголовков, если файл пустой
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(weather_data)
        print(f"Данные сохранены в {filename}")
    except IOError as e:
        print(f"Ошибка записи в файл: {e}")

# Функция для отправки письма по электронной почте
def send_email(subject, body, to_email, from_email, password):
    try:
        # Настройка сообщения
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Подключение к SMTP серверу и отправка письма
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Защищённое соединение
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
        print("Письмо успешно отправлено")
    
    except smtplib.SMTPException as e:
        print(f"Ошибка при отправке письма: {e}")

# Основная функция
def main():
    api_key = '451ff520e033438ff46683c678ee6483'  # Замените на ваш API-ключ
    city = 'London'  # Можно заменить на любой другой город

    # Получение данных о погоде
    weather_data = get_weather_data(api_key, city)
    
    if weather_data:
        # Сохранение данных в CSV
        save_to_csv(weather_data)

        # Тело письма
        body = (f"Погода в городе {weather_data['city']}:\n"
                f"Температура: {weather_data['temperature']}°C\n"
                f"Влажность: {weather_data['humidity']}%\n"
                f"Скорость ветра: {weather_data['wind_speed']} м/с\n"
                f"Описание: {weather_data['description']}")

        # Отправка данных по электронной почте
        send_email(
            subject="Отчёт о погоде",
            body=body,
            to_email="gleb.vasiliev648@yandex.ru",  # Замените на адрес получателя
            from_email="mamka.negrau@gmail.com",  # Замените на ваш адрес
            password="Ghjnjrjk649"  # Замените на пароль от почты
        )
    else:
        print("Не удалось получить данные о погоде.")

if __name__ == "__main__":
    main()
