
# Example FastAPI Project




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