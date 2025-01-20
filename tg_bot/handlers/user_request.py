from telegram import (Update, 
                    InlineKeyboardMarkup,
                    InlineKeyboardButton
                    )
from telegram.ext import (CallbackContext)

from .states import *

# Функция для обработки выбора опции из второго меню
async def choose_user_request(update: Update, context: CallbackContext) -> int:

    keyboard = [[InlineKeyboardButton(option, callback_data=f"{option}") ] for option in STATUS_OPTIONS + ["Cancel"]] 

    await update.message.edit_message_text(f"Добро пожаловать! \n"
                                f"Выберете статус: ", 
                                reply_markup=InlineKeyboardMarkup(keyboard))

    return ID