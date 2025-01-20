
from datetime import datetime, timedelta

from telegram import (Update, 
                    InlineKeyboardMarkup,
                    InlineKeyboardButton)
from telegram.ext import (
    CallbackContext
)

import logging

from .states import *
from .date_validation import validate_date


# handle input date from Users 
async def get_complex_date(update: Update, context: CallbackContext) -> int:
        
    date = validate_date(update.message.text)

    if date is not None and type(date) == datetime:

        date_format = date.strftime('%Y-%m-%d')
        context.user_data['request_date'] = date_format
        logging.info(f" context.user_data['request_date'] {context.user_data['request_date']}")

        await update.message.reply_text(f"Выберете статус: <{context.user_data['choice'] }> \n" +
                                    f"Введите свое имя: <{str(context.user_data['name']).upper() }> \n" +
                                    f"Введите дату <{context.user_data['request_date']}> \n" +
                                    f"Опишите причину: ",
                                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data=f"Cancel")]])
                                    )
        return REASON
    
    elif ((date is not None) and (type(date) == str) and date == "Past"):
        await update.message.reply_text(f"Вводимая дата в прошлом, введите корректную дату \n" + 
                                        f"Введите дату в формате: ddmmYYYY (31.12.2024)",
                                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data=f"Cancel")]])
                                        )
        return COMPLEX_DATE
    
    elif ((date is not None) and (type(date) == str) and date == "Weekend"):
        await update.message.reply_text(f"Вводимая дата - выходной день, введите корректную дату \n" + 
                                        f"Введите дату в формате: ddmmYYYY (31.12.2024)",
                                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data=f"Cancel")]])
                                        )
        return COMPLEX_DATE
    
    else:
        await update.message.reply_text(f"Неправильно, попробуй еще раз \n" + 
                                        f"Введите дату в формате: ddmmYYYY (31.12.2024)",
                                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data=f"Cancel")]])
                                        )
        return COMPLEX_DATE