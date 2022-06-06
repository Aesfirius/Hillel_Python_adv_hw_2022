## Урок 17

### ТЗ

    * Django
        - Корзина

---

### ДЗ

    * Добавить наполнение корзины в сессии
    * Дописать эндпоинт checkout(/complete_purchase) с сохранением корзины в файл

---

### cmd

MongoDB

    docker run --name mongodb_shop -p 27017:27017 -e DB_NAME=your_db_name -d mongo

### helpers
    django-admin --version
    django-admin startproject project_name
    
    python manage.py createsuperuser
    python manage.py startapp name
    python manage.py runserver

    python manage.py makemigrations shop_app
    python manage.py migrate

---

open in browser
- 127.0.0.1:8000
