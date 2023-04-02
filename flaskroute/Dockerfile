FROM python:3

# Установка зависимостей
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Копирование кода в контейнер
COPY . .

# Открытие порта для доступа к приложению
EXPOSE 5000

# Запуск приложения
CMD [ "python", "main.py" ]