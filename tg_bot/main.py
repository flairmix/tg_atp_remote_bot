import os
from dotenv import load_dotenv
from telegram import (Update, 
                      InlineKeyboardMarkup,
                    InlineKeyboardButton)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackContext,
    ContextTypes,
    filters,
    CallbackQueryHandler,
)
import requests
import logging

from handlers.states import *
from handlers.button_handlers import button_handler_start, button_handler_cancel, button_handler_date
from handlers.user_request import choose_user_request
from handlers.complex_date_handler import get_complex_date, get_interval_date
from handlers.get_reason_handler import get_reason
from handlers.get_shortname_handler import get_shortname


# Get chat ID command handler
async def api_hello_world(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    result = requests.get('http://backend:8000/users/list_users').text
    await update.message.reply_text(result)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await app.bot.send_message(chat_id=update.effective_chat.id, 
                               text=f"Справка по использованию бота.\n" +
                               f"Пишите свои замечания и мысли в канал https://t.me/atp_tlp"
                               )


# Get chat ID command handler
async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Your chat ID is: {chat_id}")


# Функция для обработки команды /start
async def start(update: Update, context: CallbackContext) -> None:

    keyboard = [[InlineKeyboardButton(option, callback_data=f"{option}") ] for option in START_MENU_OPTIONS]

    await update.message.reply_text(f"Добро пожаловать! Нажмите 'Start' для продолжения. ", 
                                    reply_markup=InlineKeyboardMarkup(keyboard))
    
    logging.info(msg="bot succesfully started - state START")
    return START


if __name__ == "__main__":


    logger = logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    load_dotenv()
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    CHAT_ID = int(os.getenv('CHAT_ID'))


    app = Application.builder().token(TOKEN).build()

    messages_ids = set()

    callbackhandler_start = CallbackQueryHandler(button_handler_start)
    callbackhandler_cancel = CallbackQueryHandler(button_handler_cancel)
    callbackhandler_date = CallbackQueryHandler(button_handler_date)
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START: [MessageHandler(~filters.COMMAND, choose_user_request), callbackhandler_start],
            ID: [MessageHandler(filters.TEXT, get_shortname), callbackhandler_cancel],
            COMPLEX_DATE: [MessageHandler(filters.TEXT, get_complex_date), callbackhandler_cancel],
            INTERVAL_DATE: [MessageHandler(filters.TEXT, get_interval_date), callbackhandler_cancel],
            REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_reason), callbackhandler_date],
        },
        fallbacks=[], 
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get_chat_id", get_chat_id))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("hello_api", api_hello_world))


    app.run_polling()




