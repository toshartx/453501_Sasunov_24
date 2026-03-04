# FROM python
# WORKDIR /app
# COPY geometric_lib/ ./geometric_lib/
# COPY script.py .
# RUN chmod +x script.py
# VOLUME ["/config"]
# CMD python script.py 
FROM python:3.9-slim

WORKDIR /app

# Копируем библиотеку
COPY geometric_lib/ ./geometric_lib/

# Копируем скрипт
COPY script.py .

# Делаем скрипт исполняемым
RUN chmod +x script.py

# Создаем точку монтирования
VOLUME ["/config"]

# Запускаем с отладкой
CMD ["python", "script.py"]