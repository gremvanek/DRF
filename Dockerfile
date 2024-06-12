# Используем базовый образ Python
FROM python:3.12

# Устанавливает переменную окружения, которая гарантирует, что вывод из python
# будет отправлен прямо в терминал без предварительной буферизации
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию в контейнере
WORKDIR /DRF_Django

# Копируем файлы pyproject.toml и poetry.lock
COPY pyproject.toml poetry.lock /DRF_Django/

# Устанавливаем Poetry и используем его для установки зависимостей
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction

# Копируем остальные файлы приложения
COPY . /DRF_Django/

# Команда для запуска Django-сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
