import logging
import requests

from telegram import (Update, 
                    InlineKeyboardMarkup,
                    InlineKeyboardButton)
from telegram.ext import (
    CallbackContext
)

from .states import *


# Функция для получения имени
async def get_shortname(update: Update, context: CallbackContext) -> int:
        
    context.user_data['name'] = update.message.text.upper()

    #check if Users with this id exist 
    user_db = requests.get(f'http://backend:8000/users/{str(context.user_data['name']).upper()}')
    logging.info(f"user_db.status_code {user_db.status_code}")

    if user_db.status_code == 204:
        await update.message.reply_text(f"Такого пользователя не найдено, введите свой id")
        return ID
                     
    keyboard = [[InlineKeyboardButton(option, callback_data=f"{option}") ] for option in DATE_MENU_OPTIONS + ["Cancel"]] 

    await update.message.reply_text(f"Выберете дату: ", 
                                    reply_markup=InlineKeyboardMarkup(keyboard))

    return REASON