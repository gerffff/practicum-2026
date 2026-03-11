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
<img width="841" height="147" alt="image" src="https://github.com/user-attachments/assets/1f093c55-d3cf-49d1-9460-0b5805556d59" /><br><br><br>


5. **Документація API за допомогою Swagger:**

`http://localhost:8000/docs`
<br><br>
<img width="1344" height="667" alt="image" src="https://github.com/user-attachments/assets/e16ad3aa-4586-4c5c-b499-dde12601e352" /><br><br>


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
```
<img width="609" height="246" alt="image" src="https://github.com/user-attachments/assets/09ba4a98-d277-4795-a99e-374fbde4009c" />
<br><br>

```bash
# Змінити роль
python manage_user_role.py user@example.com admin
python manage_user_role.py user@example.com client
```

<img width="602" height="76" alt="image" src="https://github.com/user-attachments/assets/8e8e031c-8b4c-4101-a5c7-7940958da798" /><br><br>


## Структура проєкту

```
online_library/
├── app/
│   ├── __init__.py
│   ├── main.py              
│   ├── database.py          
│   ├── auth.py            
│   ├── models/              
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── book.py
│   │   ├── author.py
│   │   ├── genre.py
│   │   └── favorite.py
│   ├── schemas/           
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── book.py
│   │   ├── favorite.py
│   │   └── token.py
│   └── routers/           
│       ├── __init__.py
│       ├── auth.py
│       ├── books.py
│       ├── favorites.py
│       └── admin.py
├── alembic/               
├── uml/                  
├── requirements.txt
└── manage_user_role.py     
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

## Безпека

- Паролі хешуються з використанням bcrypt
- JWT токени для автентифікації
- Перевірка прав доступу для адмінських функцій
