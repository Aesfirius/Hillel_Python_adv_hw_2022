## Урок 15

### ТЗ

    Знакомство с Django
---

### ДЗ

    * Сделать приложение как на уроке и подключить к нему базу postgress
    * Postgres развернуть в докере
    * Создать модели, сделать миграции и т.д. что-нибудь пописать в базу и почитать из базы

    --------------------------------------------------
    Приложение собирает данные(вводим ручками и отправляем форму) о количестве выпитого кофе за день
    Записываем в БД
    Отображаем список(All/7/30/???) последних записей (дней?)

    в перспективе можно строить графики
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

    python manage.py makemigrations
    python manage.py migrate

---

open in browser
- 127.0.0.1:8000
