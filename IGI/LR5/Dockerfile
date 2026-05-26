FROM python:3.12-slim

WORKDIR /app

# Системные зависимости для psycopg2 и других пакетов
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Создаём необходимые директории
RUN mkdir -p staticfiles logs media

# Отключаем сборку статики для локального теста (включим позже)
# RUN python manage.py collectstatic --noinput

# Открываем порт
EXPOSE 8000

# Запускаем gunicorn (для продакшена) или оставим runserver для теста
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]