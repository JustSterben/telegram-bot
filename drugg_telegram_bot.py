import os  # Импортируем модуль os

# Получаем API-ключи из переменных окружения
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

import logging
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# 🔑 Вставь свой API-ключ OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 🔑 Вставь свой API-ключ Telegram
TELEGRAM_API_TOKEN = "8076484956:AAFpgyQi_H-uRFo0Oni3Czaox2fdKq2g9UQ"

# Настраиваем OpenAI API
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Команда /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! 😊 Я ChatGPT-бот. Спроси меня о чем угодно!")

# Генерация ответа через OpenAI (ChatGPT)
async def generate_response(update: Update, context):
    user_message = update.message.text.strip()

    try:
        print(f"Отправляю запрос в OpenAI: {user_message}")  # Отладка

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Можно заменить на "gpt-4", если у тебя есть доступ
            messages=[
                {"role": "system", "content": "Ты дружелюбный и умный чат-бот. Отвечай кратко и понятно."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )

        bot_reply = response.choices[0].message.content.strip()
        print(f"Ответ от OpenAI: {bot_reply}")  # Отладка

        await update.message.reply_text(bot_reply)

    except Exception as e:
        logger.error(f"Ошибка OpenAI: {e}")
        await update.message.reply_text("Упс! Что-то пошло не так. Попробуй позже!")

# Запуск бота
def main():
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_response))

    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()
