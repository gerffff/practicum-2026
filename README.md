# Онлайн Бібліотека API

FastAPI додаток для онлайн бібліотеки з PostgreSQL базою даних.

## Запуск проєкту

1. **Встановлення залежностей:**
```bash
pip install -r requirements.txt
```

2. **Налаштування бази даних:**
- Створіть базу даних PostgreSQL
- Налаштуйте змінні середовища у файлі `.env`:
```
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

3. **Запуск міграцій:**
```bash
alembic upgrade head
```

4. **Запуск сервера:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

5. **Документація API:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Дані для входу

**Адміністратор:**
- Email: `admin@library.com`
- Пароль: `admin`

**Користувачі:**
- Email: `user@library.com` - Пароль: `user`
- Email: `reader1@library.com` - Пароль: `user`
- Email: `reader2@library.com` - Пароль: `user`
- Email: `reader3@library.com` - Пароль: `user`
- Email: `reader4@library.com` - Пароль: `user`
- Email: `reader5@library.com` - Пароль: `user`

## Управління ролями користувачів

Для зміни ролі користувача використовуйте консольну команду:

```bash
# Показати всіх користувачів
python manage_user_role.py list

# Змінити роль
python manage_user_role.py user@example.com admin
python manage_user_role.py user@example.com client
```

## Тестові дані

Для додавання тестових даних виконайте:

```bash
python add_test_data.py
```

Або використовуйте SQL скрипт `insert_test_data.sql` в pgAdmin.

## Структура проєкту

```
online_library/
├── app/
│   ├── __init__.py
│   ├── main.py              # Основне додаток FastAPI
│   ├── database.py           # Налаштування бази даних
│   ├── auth.py              # Аутентифікація та JWT
│   ├── models/              # SQLAlchemy моделі
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── book.py
│   │   ├── author.py
│   │   ├── genre.py
│   │   └── favorite.py
│   ├── schemas/             # Pydantic схеми
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── book.py
│   │   ├── favorite.py
│   │   └── token.py
│   └── routers/             # API роутери
│       ├── __init__.py
│       ├── auth.py
│       ├── books.py
│       ├── favorites.py
│       └── admin.py
├── alembic/                # Міграції бази даних
├── uml/                    # UML діаграми
├── requirements.txt
├── manage_user_role.py       # Консольна команда управління ролями
├── add_test_data.py         # Скрипт додавання тестових даних
└── insert_test_data.sql     # SQL скрипт для pgAdmin
```

## API Ендпоінти

### Авторизація (`/auth`)
- `POST /auth/register` - Реєстрація користувача
- `POST /auth/login` - Вхід користувача

### Книги (`/books`)
- `GET /books/` - Отримати всі книги (без авторизації)
- `GET /books/{book_id}` - Отримати книгу за ID (без авторизації)

### Обрані (`/favorites`)
- `POST /favorites/` - Додати книгу до обраних
- `DELETE /favorites/{book_id}` - Видалити книгу з обраних
- `GET /favorites/` - Отримати обрані книги користувача

### Адміністрування (`/admin`)
- `POST /admin/books` - Додати книгу (тільки адмін)
- `DELETE /admin/books/{book_id}` - Видалити книгу (тільки адмін)
- `GET /admin/export/csv` - Експорт книг в CSV (тільки адмін)
- `PUT /admin/users/{user_id}/role` - Змінити роль користувача (тільки адмін)

## Вимоги до завдання

**Авторизація:**
- Реєстрація з email та паролем
- Вхід з email та паролем
- JWT токени

**Книги:**
- Список всіх книг (без авторизації)
- Інформація по окремій книзі (без авторизації)
- Додавання нової книги (адмін)
- Видалення книги (адмін)

**Обрані:**
- Додавання в обрані
- Видалення з обраних
- Доступ тільки до свого списку

**Ролі:**
- Адміністратор та клієнт
- Консольна команда зміни ролі

**Експорт:**
- Вивантаження списку книг в CSV (адмін)

**База даних:**
- PostgreSQL
- 3-я нормальна форма
- Міграції Alembic

**Документація:**
- UML діаграми (ERD, Class, Sequence)
- Swagger документація

## UML Діаграми

Файли PlantUML знаходяться в директорії `uml/`:
- `entity_relationship_diagram.puml` - ER діаграма
- `class_diagram.puml` - Діаграма класів
- `sequence_diagram.puml` - Діаграма послідовності

## Безпека

- Паролі хешуються з використанням bcrypt
- JWT токени для автентифікації
- Перевірка прав доступу для адмінських функцій
