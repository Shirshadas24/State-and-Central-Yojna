import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)
from langdetect import detect
from query_handler import handle_query
from utils.db_logger import log_conversation

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# 🟩 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! 👋 I can help you understand government schemes.\n\n"
        "Just type your query (in Hindi, English, or Hinglish)!"
    )

# 🟩 Message handler
async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    user_id = update.effective_user.id
    username = update.effective_user.username or "Anonymous"

    # Auto detect language
    try:
        lang_code = detect(user_input)
    except Exception:
        lang_code = "en"

    # Map langdetect codes to your system
    if lang_code in ["hi", "mr", "bn"]:
        language = "Hindi"
    elif lang_code == "en":
        language = "English"
    else:
        language = "Hinglish"

    # 🔁 Call main handler
    response = handle_query(user_input, language)

    # 🧠 Log with user info & language
    log_conversation(
        query=user_input,
        response=response,
        language=language,
        user_id=user_id,
        username=username
    )

    await update.message.reply_text(response)

# 🟩 Main launcher
def run_telegram_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    print("🤖 Telegram bot is running...")
    app.run_polling()

if __name__ == "__main__":
    run_telegram_bot()
