# Проект YaMDb
### Проект YaMDb собирает отзывы пользователей на произведения.
# API для проекта YaMDB в контейнере Docker
[![yamdb project workflow](https://github.com/drgreey/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?branch=main)](https://github.com/drgreey/yamdb_final/actions/workflows/yamdb_workflow.yml)
### Шаблон наполнения env-файла:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
### Описание команд для запуска приложения в контейнерах:
```
Пересоберите контейнеры и запустите docker-compose 
из ./infra_sp2/infra командой: 
docker-compose up --build

Остановить запущенные контейнеры:
docker-compose down -v 

Для входа в контейнер выполните команду:
docker exec -it <CONTAINER ID> bash

Проверьте работоспособность приложения:
http://localhost
```
### Описание команды для заполнения базы данными
```
Запуск миграций:
docker-compose exec web python manage.py migrate

Создание супер пользователя:
docker-compose exec web python manage.py createsuperuser

Подгрузка статики:
docker-compose exec web python manage.py collectstatic --no-input 
```
## Используемые технологии:
```
python 3.9.13
requests 2.26.0
Django 3.2
djangorestframework 3.12.4
PyJWT 2.1.0
pytest 6.2.4
pytest-django 4.4.0
pytest-pythonpath 0.7.3
gunicorn==20.0.4
psycopg2-binary==2.8.6
```
### Авторы: Зацарин Игорь, Таначев Антон, Носков Денис


