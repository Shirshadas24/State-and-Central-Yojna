# import os
# from dotenv import load_dotenv
# from telegram import Update
# from telegram.ext import (
#     ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
# )
# from langdetect import detect
# from query_handler import handle_query
# from utils.db_logger import log_conversation

# load_dotenv()
# BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(
#         "Hello! 👋 I can help you understand government schemes.\n\n"
#         "Just type your query (in Hindi, English, or Hinglish)!"
#     )


# async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_input = update.message.text
#     user_id = update.effective_user.id
#     username = update.effective_user.username or "Anonymous"

#     try:
#         lang_code = detect(user_input)
#     except Exception:
#         lang_code = "en"

    
#     if lang_code in ["hi", "mr", "bn"]:
#         language = "Hindi"
#     elif lang_code == "en":
#         language = "English"
#     else:
#         language = "Hinglish"

#     response = handle_query(user_input, language)

#     log_conversation(
#         query=user_input,
#         response=response,
#         language=language,
#         user_id=user_id,
#         username=username
#     )

#     await update.message.reply_text(response)

# def run_telegram_bot():
#     app = ApplicationBuilder().token(BOT_TOKEN).build()

#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

#     print("🤖 Telegram bot is running...")
#     app.run_polling()

# if __name__ == "__main__":
#     run_telegram_bot()




# import os
# from dotenv import load_dotenv
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import (
#     ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes,
#     CallbackQueryHandler, filters
# )
# from langdetect import detect
# from query_handler import handle_query
# from utils.db_logger import log_conversation

# load_dotenv()
# BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# # /start command handler
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [InlineKeyboardButton("Ayushman Bharat", callback_data="Ayushman Bharat")],
#         [InlineKeyboardButton("Atal Pension Yojana", callback_data="Atal Pension Yojana")],
#         [InlineKeyboardButton("Beti Bachao, Beti Padhao", callback_data="Beti Bachao")],
#         [InlineKeyboardButton("PM Kisan", callback_data="PM Kisan")],
#         [InlineKeyboardButton("Jal Jeevan Mission", callback_data="Jal Jeevan")],
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)

#     await update.message.reply_text(
#         "👋 Welcome! Type your question or select a scheme below to know more:",
#         reply_markup=reply_markup
#     )

# # Button click handler
# async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()
#     selected_scheme = query.data

#     # Run it as a normal query through your handler
#     response = handle_query(selected_scheme, language="English")

#     # Optional: Log it
#     log_conversation(
#         query=selected_scheme,
#         response=response,
#         language="English",
#         user_id=query.from_user.id,
#         username=query.from_user.username or "Anonymous"
#     )

#     await query.edit_message_text(text=response)

# # Free text message handler
# async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_input = update.message.text
#     user_id = update.effective_user.id
#     username = update.effective_user.username or "Anonymous"

#     try:
#         lang_code = detect(user_input)
#     except Exception:
#         lang_code = "en"

#     if lang_code in ["hi", "mr", "bn"]:
#         language = "Hindi"
#     elif lang_code == "en":
#         language = "English"
#     else:
#         language = "Hinglish"

#     response = handle_query(user_input, language)

#     log_conversation(
#         query=user_input,
#         response=response,
#         language=language,
#         user_id=user_id,
#         username=username
#     )

#     await update.message.reply_text(response)

# # Run bot
# def run_telegram_bot():
#     app = ApplicationBuilder().token(BOT_TOKEN).build()

#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(CallbackQueryHandler(button_click))
#     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

#     print("🤖 Telegram bot is running...")
#     app.run_polling()

# if __name__ == "__main__":
#     run_telegram_bot()


# import os
# from dotenv import load_dotenv
# from telegram import Update
# from telegram.ext import (
#     ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
# )
# from langdetect import detect
# from query_handler import handle_query
# from utils.db_logger import log_conversation

# load_dotenv()
# BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# # Standard welcome message
# WELCOME_MESSAGE = (
#     "Hello! 👋 I can help you understand government schemes.\n\n"
#     "Just type your query (in Hindi, English, or Hinglish)!"
# )

# # List of common greetings
# GREETINGS = {"hi", "hello", "hey", "yo", "namaste", "namaskar", "hii", "helloo", "heyy"}

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(WELCOME_MESSAGE)

# async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_input = update.message.text.strip().lower()
#     user_id = update.effective_user.id
#     username = update.effective_user.username or "Anonymous"

#     # If it's a greeting, reply with welcome message
#     if user_input in GREETINGS:
#         await update.message.reply_text(WELCOME_MESSAGE)
#         return

#     try:
#         lang_code = detect(user_input)
#     except Exception:
#         lang_code = "en"

#     if lang_code in ["hi", "mr", "bn"]:
#         language = "Hindi"
#     elif lang_code == "en":
#         language = "English"
#     else:
#         language = "Hinglish"

#     response = handle_query(user_input, language)

#     log_conversation(
#         query=user_input,
#         response=response,
#         language=language,
#         user_id=user_id,
#         username=username
#     )

#     await update.message.reply_text(response)

# def run_telegram_bot():
#     app = ApplicationBuilder().token(BOT_TOKEN).build()

#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

#     print("🤖 Telegram bot is running...")
#     app.run_polling()

# if __name__ == "__main__":
#     run_telegram_bot()


import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)
from langdetect import detect
from query_handler import handle_query
from utils.db_logger import log_conversation
import re
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
def detect_input_language(text):
    # Simple check for Hinglish: mix of Hindi words in Latin script
    HINGLISH_HINTS = ["kya", "kaise", "hai", "ladki", "laabh", "milta", "ham",  "kaise", "kahan", "kab", "kyun","karna"]

    if any(hint in text.lower() for hint in HINGLISH_HINTS):
        return "Hinglish"

    try:
        lang_code = detect(text)
    except Exception:
        lang_code = "en"

    if lang_code in ["hi", "mr", "bn"]:
        return "Hindi"
    elif lang_code == "en":
        return "English"
    else:
        return "Hinglish"


# 🔘 Inline buttons for popular schemes
keyboard = [
    [InlineKeyboardButton("Ayushman Bharat", callback_data="Ayushman Bharat")],
    [InlineKeyboardButton("Atal Pension Yojana", callback_data="Atal Pension Yojana")],
    [InlineKeyboardButton("Beti Bachao, Beti Padhao", callback_data="Beti Bachao")],
    [InlineKeyboardButton("PM Kisan", callback_data="PM Kisan")],
]

reply_markup = InlineKeyboardMarkup(keyboard)

# 👋 Welcome message
WELCOME_MESSAGE = (
    "Hello! 👋 I can help you understand government schemes.\n\n"
    "Just type your query (in Hindi, English, or Hinglish)!"
)

# 🎯 Recognized greetings
GREETINGS = {"hi", "hello", "hey", "yo", "namaste", "namaskar", "hii", "helloo", "heyy"}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup)

async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip().lower()
    user_id = update.effective_user.id
    username = update.effective_user.username or "Anonymous"

    # Handle greetings
    if user_input in GREETINGS:
        await update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup)
        return

    # try:
    #     lang_code = detect(user_input)
    # except Exception:
    #     lang_code = "en"

    # if lang_code in ["hi", "mr", "bn"]:
    #     language = "Hindi"
    # elif lang_code == "en":
    #     language = "English"
    # else:
    #     language = "Hinglish"


    # Set language explicitly
    language = "Hinglish"
    response = handle_query(user_input)

    log_conversation(
        query=user_input,
        response=response,
        language=language,
        user_id=user_id,
        username=username
    )

    await update.message.reply_text(response)

# 🔘 Handle button clicks
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    scheme_name = query.data
    response = handle_query(scheme_name, language="English")  # default to English for button clicks

    await query.edit_message_text(response)

def run_telegram_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))
    app.add_handler(CallbackQueryHandler(handle_button))

    print("🤖 Telegram bot is running...")
    app.run_polling()

if __name__ == "__main__":
    run_telegram_bot()
