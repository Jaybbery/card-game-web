from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import sqlite3
import random
import logging

# Настройки
TOKEN = "7605688003:AAFXEMP4iRDdSJSqpBBcWU66WWnUQ42Quh8"
DB_NAME = "cards.db"

# Инициализация БД
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    coins INTEGER DEFAULT 100
)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS cards (
    card_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    name TEXT,
    image_url TEXT
)''')
conn.commit()

# Веб-приложение
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        "🎮 Открыть игру",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "Играть", 
                web_app={"url": "https://jaybbery.github.io/card-game-web/"}  # Ссылка на ваше веб-приложение
            )
        ]])
    )

# Обработка данных из Web App
async def handle_web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = json.loads(update.message.web_app_data.data)
    user_id = update.effective_user.id

    if data.get("action") == "open_booster":
        # Логика открытия бустера
        new_card_id = random.randint(1000, 9999)
        cursor.execute('INSERT INTO cards (user_id, name) VALUES (?, ?)', (user_id, f"Карта #{new_card_id}"))
        conn.commit()
        await update.message.reply_text(f"🎉 Вы получили карту #{new_card_id}!")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_web_app_data))
    app.run_polling()

if __name__ == "__main__":
    main()
