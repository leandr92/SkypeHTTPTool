# SkypeHTTPTool

Приложение для управления чатами в скайпе через HTTP-API

Приложение стартует по адресу 127.0.0.1:5000

Приложение использует встроенные веб-сервер Flask, потому использовать строго внутри защищенного контура.

После этого можно в него слать запросы. Примеры запросов можно посмотреть в postman-коллекции 
[SkypeTool.postman_collection.json](SkypeTool.postman_collection.json). Для этого нужно будет импортировать коллекцию в Postman

## Возможности
!Не поддерживает двухфакторная авторизация

Методы:
- POST utils/ping - проверка работы сервиса
- POST utils/auth - авторизация
- POST utils/exit - завершение работы приложения

- GET chats - список последних групповых чатов с подгрузкой (ограничение скайпа). С каждым новым запросом подгружается новая порция
- GET chatUsers - список пользователей чата по id чата
- POST chatUsers - добавить пользователя в чат (поддерживается тихий режим без вывода сообщения в чат)
- DELETE chatUsers - удалить пользователя из чата (поддерживается тихий режим без вывода сообщения в чат)

## Зависимости 
FLask
    
```sh 
pip install flask-restful
```
Библиотека работы со скайпом
```sh 
pip install skpy
```

## Сборка в exe
Для сборки приложения в exe необходимо установить pyinstaller 

```sh
pip install pyinstaller
```
перейти в каталог приложения и запустить сборку скриптом

```sh
pyinstaller --windowed --onefile SkypeTool.py
```
