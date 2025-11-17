# 1. Берем официальный образ Python 3.12
FROM python:3.12-slim

# 2. Устанавливаем ffmpeg (наконец-то!)
RUN apt-get update && apt-get install -y ffmpeg

# 3. Готовим окружение
WORKDIR /app

# 4. Устанавливаем библиотеки
COPY requirements.txt .
RUN pip install -r requirements.txt

# 5. Копируем всего бота
COPY . .

# 6. Запускаем бота
CMD ["python", "bot.py"]
