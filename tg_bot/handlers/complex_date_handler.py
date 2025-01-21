
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
        context.user_data['request_date'] = [date_format]
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
    

# handle interval date from User input TODO
async def get_interval_date(update: Update, context: CallbackContext) -> list:
    
    try:
        interval_date = update.message.text.split(' - ')
        # context.user_data['request_dates_interval'] = []
        context.user_data['request_date'] = []

        dates = []
        start_date = validate_date(interval_date[0])
        end_date = validate_date(interval_date[1])
    except:
        await update.message.reply_text(f"Неправильно, попробуй еще раз \n" + 
                                        f"Введите несколько дней подряд в формате: (31.12.2024 - 07.01.2025):",
                                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data=f"Cancel")]])
                                        )
        return INTERVAL_DATE        
        
    if ((type(start_date) == datetime) 
        and (type(end_date) == datetime) 
        and ((end_date - start_date).days <= 5)
        ):

        current_day = start_date

        while current_day <= end_date:
            if current_day.weekday() not in {5, 6}:
                # dates.append(current_day.strftime('%Y-%m-%d'))
                context.user_data['request_date'].append(current_day.strftime('%Y-%m-%d'))
            current_day += timedelta(days=1)

        # context.user_data['request_dates_interval'] = dates
        await update.message.reply_text(f"Опишите причину: ", 
                                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data=f"Cancel")]]))
        return REASON
    
    else:
        await update.message.reply_text(f"Неправильно, попробуй еще раз \n" + 
                                        f"Введите несколько дней подряд в формате: (31.12.2024 - 07.01.2025): \n" +
                                        f"(Выбрать не более 5 дней подряд, исключая выходные)",
                                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data=f"Cancel")]])
                                        )
        return INTERVAL_DATE

    