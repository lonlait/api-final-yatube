# API для проекта Yatube

API для социальной сети Yatube, где пользователи могут публиковать посты, подписываться на других пользователей и комментировать записи.

## Описание

API предоставляет следующие возможности:
- Регистрация и аутентификация пользователей
- Создание, редактирование и удаление постов
- Добавление и редактирование комментариев
- Подписка на других пользователей
- JWT-аутентификация

## Технологии

- Python 3.11
- Django 5.1.1
- Django REST Framework 3.15.2
- Djoser 2.3.1
- Simple JWT 5.4.0

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/api-final-yatube.git
cd api-final-yatube
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Выполните миграции:
```bash
python yatube_api/manage.py migrate
```

5. Запустите сервер:
```bash
python yatube_api/manage.py runserver
```

## Примеры запросов к API

### Аутентификация

Получение токена:
```bash
POST /api/v1/jwt/create/
{
    "username": "your_username",
    "password": "your_password"
}
```

### Работа с постами

Получение списка постов:
```bash
GET /api/v1/posts/
```

Создание поста:
```bash
POST /api/v1/posts/
{
    "text": "Текст нового поста"
}
```

### Работа с комментариями

Получение комментариев к посту:
```bash
GET /api/v1/posts/{post_id}/comments/
```

Добавление комментария:
```bash
POST /api/v1/posts/{post_id}/comments/
{
    "text": "Текст комментария"
}
```

### Подписки

Получение списка подписок:
```bash
GET /api/v1/follow/
```

Подписка на пользователя:
```bash
POST /api/v1/follow/
{
    "following": "username"
}
```

## Документация API

После запуска проекта документация доступна по адресу:
```
http://127.0.0.1:8000/redoc/
```

## Автор

Ваше имя - [GitHub](https://github.com/lonlait)
