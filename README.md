# vibroteh
Задания для должности Помощник системного администратора

1. Был использован API OpenWeatherMap. Были некоторые трудности с работой API, а именно долгое время после создания API ключа он просто не работал, из-за чего данные не получались.
Все данные сохраняются в файл csv для дальнейшего использования данных.
Реализована обработка ошибок на каждом этапе выполнения кода: ошибка подключения к API, ошибка записи в файл (или данные сохранены в {filename}), ошибка при отправке письма (или письмо успешно отправлено), не удалось получить данные о погоде.

Реализована функция отправки готового файла с данными на почту, но в связи с двухфакторной аутентификацией необходимо либо её отключить, либо предоставлять доступ. Я функцию реализовал, но не проверил =)


2. В качестве сайта для парса был выбран известный новостной сайт https://www.rbc.ru, а также фильтрация новостей по тегу "Украина" (https://www.rbc.ru/tags/?tag=Украина), так как именно эти новости являются самыми актуальными )))
В связи с тем, что большая часть сайта догружается с помощью JavaScript было принято решение загружать полностью страницу через браузер Chrome, после чего парсить html шаблон и получать оттуда необходимую информацию через BeautifulSoup.
Все данные выводятся в консоль (для удобства), а также сохраняются в базу данных sqlite3. Также, сначала было реализовано, а позже удалено, функционал того, что будет парситься каждые 6 часов. Данный функционал был реаизован с помощью time.sleep(21600), после чего запускалась функция парсинга и выполнялись все действия и снова возращалось на time.speel().


3. Был реализован простой REST API с использованием Flask для создания API.
Реализованы CRUD-операции: Create, Read, Update, Delete.
Сохранение данных сделал просто в памяти.
Тесты проверок написал через pytest, но также проверил через графический интерфейс Postman.
