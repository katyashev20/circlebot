import os
import uuid
import asyncio
import subprocess
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart

# 🔑 Твой токен
TOKEN = "8466847169:AAHiFvi86o9XnL_YiqBlFrkPeMZHmFwY-Hw"

# 🔧 Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 🚀 Команда /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Отправь мне видео, и я сделаю из него кружочек 🎬")

# 🎬 Обработка видео
@dp.message(F.video)
async def handle_video(message: Message):
    await message.answer("🎥 Обрабатываю видео, подожди немного...")

    file = await bot.get_file(message.video.file_id)
    input_path = f"temp_{uuid.uuid4().hex}.mp4"
    output_path = f"circle_{uuid.uuid4().hex}.mp4"

    await bot.download_file(file.file_path, input_path)

    # Используем ffmpeg для обрезки и конвертации в квадрат
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-vf", "crop='min(iw,ih)':'min(iw,ih)',scale=480:480,setsar=1,format=yuv420p",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", output_path
    ]

    # subprocess.run заменим на asyncio для надёжности
    process = await asyncio.create_subprocess_exec(*cmd)
    await process.communicate()

    video = FSInputFile(output_path)
    await message.answer_video_note(video_note=video)
    await message.answer("✅ Готово! Вот твой кружочек 😊")

    os.remove(input_path)
    os.remove(output_path)

# 🧠 Основная функция
async def main():
    print("🤖 Бот запущен и ждёт сообщений...")
    await dp.start_polling(bot)

# ▶️ Запуск
if __name__ == "__main__":
    asyncio.run(main())
