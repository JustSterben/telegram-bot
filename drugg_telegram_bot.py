import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext
import openai

# Логирование (для отладки)
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Получаем токены из переменных окружения
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Словарь для хранения обработанных update_id
processed_updates = set()

async def handle_message(update: Update, context: CallbackContext) -> None:
    """Обрабатываем входящее сообщение"""
    message = update.message.text
    chat_id = update.message.chat_id

    # Проверяем, если update_id уже обработан – игнорируем
    if update.update_id in processed_updates:
        logging.info(f"Пропускаем дубликат update_id: {update.update_id}")
        return
    processed_updates.add(update.update_id)  # Добавляем обработанный update_id

    logging.info(f"Получено сообщение: {message}")

    try:
        response = get_chatgpt_response(message)  # Функция для запроса в OpenAI
        await update.message.reply_text(response)
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await update.message.reply_text("Упс! Что-то пошло не так. Попробуй позже!")

def get_chatgpt_response(text):
    """Отправляет запрос в OpenAI и возвращает ответ"""
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Ошибка OpenAI: {e}")
        return "Ошибка запроса к ChatGPT."

def main():
    """Запускаем бота"""
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logging.info("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()
