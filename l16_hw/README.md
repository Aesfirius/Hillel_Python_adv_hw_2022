## Урок 16

### ТЗ

    Знакомство с Django
    Создание пользователя, авторизация

---

### ДЗ

    * Добавить авторизацию в приложение

---

### cmd

Postgres

    docker run --name name_pgsl_docker_container -p 5432:5432 -e POSTGRES_USER=your_postgres_user -e POSTGRES_PASSWORD=your_super_password -e POSTGRES_DB=your_db_name -d postgres

### helpers
    django-admin --version
    django-admin startproject project_name
    
    python manage.py createsuperuser
    python manage.py startapp name
    python manage.py runserver
    
    pip install psycopg2
    pip install psycopg2-binary

    python manage.py makemigrations my_app
    python manage.py migrate

---

open in browser
- 127.0.0.1:8000
