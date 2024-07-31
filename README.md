# ToDo List API

## Описание

API для ToDo листа, который поддерживает регистрацию пользователей, создание, просмотр, обновление и удаление задач, а также управление правами доступа к задачам.

## Стек технологий

- Язык: Python
- СУБД: PostgreSQL
- Framework: FastAPI

## Установка


# Шаг 1: Установка зависимостей

Создайте виртуальное окружение и установите необходимые зависимости:
```
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary passlib 
```

# Шаг 2: Настройка проекта
Создайте структуру проекта:
```
TODO_API/
├── alembic/
│   ├── versions/
│   └── env.py
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── database.py
│   ├── auth.py
│   ├── dependencies.py
└── alembic.ini
```

# Шаг 3: Настройка базы данных и Alembic
alembic.ini
Настройте файл alembic.ini для подключения к базе данных:
```
[alembic]
script_location = alembic

[alembic:ini]
sqlalchemy.url = postgresql://user:password@localhost/todo_db
```

Настройте файл ```alembic/env.py```


# Шаг 4: Модели данных
models.py
- Создайте модели данных:

# Шаг 5: Схемы данных
schemas.py
- Создайте схемы данных для валидации и сериализации:

# Шаг 6: CRUD операции
crud.py
- Создайте CRUD операции для взаимодействия с базой данных:

# Шаг 7: Аутентификация
auth.py 
- Создайте файл для обработки аутентификации:

# Шаг 8: Зависимости
dependencies.py
- Создайте файл для зависимостей:

# Шаг 9: Основной файл приложения
main.py
- Создайте основной файл приложения:

# Шаг 10: Запуск приложения
Запустите приложение:
```uvicorn app.main:app --reload```
