![example workflow](https://github.com/Tchuprow/foodgram-project-react/actions/workflows/main.yml/badge.svg)

# Foodgram - продуктовый помощник.
***

IP 158.160.36.70

### Описание
Здесь представлен проект - "Foodgram", продуктовый помощник.
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
***

### Запуск проекта в Docker контейнере.

+ Склонировать репозиторий на локальную машину:

```
git clone https://github.com/Tchuprow/foodgram-project-react.git
```

+ Перейти в директорию /infra/, создать .env файл и заполнить следующим содержанием:

```
SECRET_KEY=секретный ключ django
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

+ Запустите docker compose:

```
docker-compose up -d --build
```

+ Примените миграции:

```
docker-compose exec backend python manage.py migrate
```

+ Загрузите ингредиенты:

```
docker-compose exec backend python manage.py import_ingredients
```

+ Создайте администратора:

```
docker-compose exec backend python manage.py createsuperuser
```

+ Соберите статику:

```
docker-compose exec backend python manage.py collectstatic --noinput
```
***

### Документация к API 

Документация API будет доступна сразу после поднятия контейнеров по адресу [](localhost/api/docs/)
***

### Тестовые данные:

Подготовлены тестовые данные. Чтобы воспользоваться ими, вместо команд загрузки ингредиентов и создания администратора, выполнить следующую команду:

```
docker-compose exec backend python manage.py loaddata data/fixtures.json
```

В случае использования этой команды, ингредиенты будут загружены и администратор создан, а также добавлены тестовые рецепты и тестовые пользователи.

Данные суперпользователя:

```
email: 111@111
password: admin
```

Данные тестового пользователя:

```
email: 888@888.com
password: 12345+++
```
***