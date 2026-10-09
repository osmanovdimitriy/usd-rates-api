# USD Rates API

Учебный проект: парсер курса ЦБ РФ → PostgreSQL → (далее FastAPI).

## Стек
- Python 3.14
- PostgreSQL 17
- psycopg 3
- requests + BeautifulSoup

## Запуск
1. `pip install -r requirements.txt`
2. Скопируй `.env.example` в `.env` и впиши свой пароль PostgreSQL
3. `python -m src.parser`
4. `python -m src.db`

## Автор

osmanovdimitriy

## Test section