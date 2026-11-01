Замени на:

```markdown
# USD Rates API

Учебный проект: парсер курса ЦБ РФ → PostgreSQL → FastAPI.

## Стек
- Python 3.12 (в Docker), 3.14 локально
- FastAPI, Pydantic
- SQLAlchemy (async), asyncpg
- PostgreSQL 17
- Alembic, Pytest
- Docker, docker-compose

## Быстрый старт (Docker)

1. Скопируй `.env.example` → `.env`, укажи пароль:
   ```
   POSTGRES_PASSWORD=ваш_пароль
   DATABASE_URL=postgresql://postgres:ваш_пароль@localhost:5432/usd_rates
   ```

2. Подними контейнеры:
   ```
   docker compose up -d --build
   ```

3. Примени миграции:
   ```
   docker compose exec api alembic upgrade head
   ```

4. Открой документацию: http://localhost:8000/docs

## Локально (без Docker)

1. `pip install -r requirements.txt`
2. Скопируй `.env.example` в `.env`, впиши пароль PostgreSQL
3. `uvicorn src.api:myapp --reload`

## Эндпоинты

- `GET /rates/{currency}` — курс валюты
- `POST /rates/db` — сохранить курс в БД
- `PUT /rates/db/{id}` — обновить
- `DELETE /rates/db/{id}` — удалить
- `GET /currencies` — список валют
- `GET /history?currency=USD&limit=10` — история

## Парсер

- `python -m src.parser` — обновить курсы
- `python -m src.db` — инициализировать схему

## Тесты

```
pytest tests/ -v
```

## Автор

osmanovdimitriy
```