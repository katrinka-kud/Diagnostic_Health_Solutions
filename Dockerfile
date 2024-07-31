# Используем базовый образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем зависимости в контейнер
COPY /requirements.txt /

# Устанавливаем зависимости
RUN pip install -r /requirements.txt --no-cache-dir

# Копируем код приложения в контейнер
COPY config .

# Команда для запуска приложения при старте контейнера
#CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0.:8000"]
