# Используем базовый образ Python
FROM python:3.12

# Устанавливает переменную окружения, которая гарантирует, что вывод из python
# будет отправлен прямо в терминал без предварительной буферизации
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию в контейнере
WORKDIR /OnlineTraining

# Копируем зависимости и код приложения
COPY ./requirements.txt /OnlineTraining/
RUN pip install -r /OnlineTraining/requirements.txt
COPY . .

# Команда для запуска Django-сервера
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]