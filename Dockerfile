# 1. Берем базовый Linux с Python 3.12
FROM python:3.12-slim

# 2. Создаем рабочую папку внутри контейнера
WORKDIR /app

# 3. Копируем список зависимостей
COPY requirements.txt .

# 4. Устанавливаем библиотеки
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копируем весь остальной код проекта
COPY . .

# 6. Команда, которая запустится при старте контейнера
CMD ["uvicorn", "src.api:myapp", "--host", "0.0.0.0", "--port", "8000"]