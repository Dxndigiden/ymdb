### YAMDB
YaMDb — это приложение для сайта агрегатора критики, которая собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

### Авторы проекта:

Zardigal - Сергей Лончаков  
Dxndigiden - Денис Смирнов  
KonovalovEvgeniy - Евгений Коновалов  

### Используемые технологии:

Python  
Django  
DjangoRestFramework  

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone <web URL/SSH key>
```
```
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Примеры запросов к API
С полным списком запросов к api можно озанкомится по эндпоинту redoc/.  
Примеры некоторых запросов:

| Тип запроса | Url | Параметры | Ответ | Описание |
| --- | --- | --- | --- | --- |
| POST | api/v1/auth/signup/ | {"email": "user@example.com", "username": "string"} | {"email": "string","username": "string"} | Регистрация нового пользователя, на почту придет код подтвеждения для получения JWT токена. |
| GET | api/v1/titles/ | None | {"count": 0, "next": "string", "previous": "string", "results": [{"name": "string", "year": 0, "description": "string", "genre": ["string"],"category": "string"}]} | Получить список всех произведений. |
| POST | api/v1/titles/ | {"name": "string", "year": 0, "description": "string", "genre": ["string"],"category": "string"} | { "id": 0, "name": "string", "year": 0, "rating": 0, "description": "string", "genre": [{"string"}], "category": {"name": "string", "slug": "string"}} | Добавление нового произведения (для администраторов). |
| POST | api/v1/titles/{title_id}/reviews/ | {"text": "string", "score": 1} | {"id": 0, "text": "string", "author": "string", "score": 1, "pub_date": "2019-08-24T14:15:22Z"} | Добавление нового к отзыва к произведению (для аутентифицированного пользователя). |
| PATCH | api/v1/users/me/ | {"username": "string", "email": "user@example.com", "first_name": "string", "last_name": "string", "bio": "string"} | {"username": "string", "email": "user@example.com", "first_name": "string", "last_name": "string", "bio": "string", "role": "user"} | Изменить данные своей учетной записи (любой авторизованный пользователь) |
