
# Example FastAPI Project
REST API написанный на FastAPI, с интеграцией [randomuser.me]()

База данных - PostgreSQL, сервис запущен на AWS EC2 с использованием Docker Compose и Caddy (reverse proxy).
## Инструкция для локального запуска
В решении используется контейнеризация, поэтому сначала нужно установить Docker и Docker Compose:

[Docker](https://docs.docker.com/get-started/get-docker/)

[Docker Compose](https://docs.docker.com/compose/install/)

### 1. Склонируйте репозиторий
```
git clone https://github.com/svndor-hub/fastapi-example.git
cd fastapi-example
```

### 2. Настройте переменные окружения
Создайте файл .env в корневой директории и добавьте в него необходимые переменные окружения:
```
# Database Configuration
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_database_name

# FastAPI Settings
DATABASE_URL=postgresql+asyncpg://your_postgres_user:your_postgres_password@localhost:5432/your_database_name
DATABASE_ASYNC_URL=postgresql+asyncpg://your_postgres_user:your_postgres_password@localhost:5432/your_database_name
SECRET_KEY=your_secret_key
```
Необходимо заменить `your_postgres_user`, `your_postgres_password`, `your_database_name`, и `your_secret_key` на свои значения.
SECRET_KEY нужен для аутентификации, его можно сгенерировать разными способами (показаны 2 возможных способа):

Командой в терминале Linux: 
```
openssl rand -hex 32
```
Используя Python:
```
import secrets
hex_key = secrets.token_hex(32)
base64_key = secrets.token_urlsafe(32)
```

### 4. Сборка и запуск приложения
```
docker-compose up --build
```

### 5. Применение миграций базы данных
Приложение использует Alembic для миграций БД. Для создания необходимых таблиц после запуска приложения, нужно применить миграции:
```
docker-compose exec web alembic upgrade head
```

### 6. Доступ к API
`http://localhost:8000`

Документация Swagger:
`http://localhost:8000/docs`

### Остановка приложения
`docker-compose down`
## Описание эндпоинтов и примеры запросов

### Эндпоинты с использованием внешнего API (randomuser.me)

`GET /randomuser/test` - Тестовый эндпоинт, возвращает данные рандомно сгенерированного пользователя. 

Curl:
```
curl -X 'GET' \
  'http://127.0.0.1:8000/randomuser/test' \
  -H 'accept: application/json'
```

`POST /randomuser/save` - Получает рандомного пользователя с randomuser.me, и сохраняет его в базе данных.

Curl:
```
curl -X 'POST' \
  'http://127.0.0.1:8000/randomuser/save' \
  -H 'accept: application/json' \
  -d ''
```

### Авторизация (OAuth2 с JWT)
`POST /token` - Авторизация с username и password, возвращает access token.

Curl:
```
curl -X 'POST' \
  'http://127.0.0.1:8000/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=USERNAME&password=PASSWORD&scope=&client_id=string&client_secret=string'
```

Некоторые защищенные эндпоинты для проверки авторизации:
`GET /users/me` - Возвращает данные авторизованного пользователя.

Curl:
```
curl -X 'GET' \
  'http://127.0.0.1:8000/users/me/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer access_token'
```

### CRUD эндпоинты users
`GET /users` - Получить всех пользователей

`POST /users` - Создать пользователя

```
curl -X 'POST' \
  'http://127.0.0.1:8000/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "string",
  "email": "string",
  "password": "string"
}'
```

`GET /users/{user_id}` - Получить пользователя по id

`PUT /users/{user_id}` - Обновить пользователя

`DELETE /users/{user_id}` - Удалить пользователя
## Ссылка на развернутый сервис

[sanzhar.tech/docs]()