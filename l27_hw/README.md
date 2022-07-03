## Урок 27

### ТЗ

    * Tests часть 2
        - Unittest
        -* RequestFactory

---

### ДЗ

    * Добавить тестировнаие функций в магазине, написанном с Django

    * Задание сложности чуть больше:
        - Написать тесты для эндпоинтов с RequestFactory
---

### cmd

MongoDB

    docker network create mongo-net
    docker run -d --name mongodb_shop -p 27017:27017 -v ~/mongodata:/data/db -e MONGO_INITDB_ROOT_USERNAME='your_mongodb_user' -e MONGO_INITDB_ROOT_PASSWORD='your_mongodb_password' -e MONGO_INITDB_DATABASE='your_db_name' --hostname mongodb_shop --network mongo-net mongo
    docker run -d --name mongo-express -p 8081:8081 -e ME_CONFIG_MONGODB_ADMINUSERNAME='your_mongodb_user' -e ME_CONFIG_MONGODB_ADMINPASSWORD='your_mongodb_password' -e ME_CONFIG_MONGODB_SERVER='mongodb_shop' -e ME_CONFIG_MONGODB_PORT=27017 --hostname mongo-express --network mongo-net mongo-express
    mongodb://your_mongodb_user:your_mongodb_password@mongodb_shop:27017

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
- localhost:8081