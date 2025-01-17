from datetime import datetime, timedelta

from telegram import (Update, 
                    InlineKeyboardMarkup,
                    InlineKeyboardButton)
from telegram.ext import (
    CallbackContext
)

from .states import *


async def button_handler_start(update: Update, context: CallbackContext) -> int:
    query = update.callback_query

    if query.data in START_MENU_OPTIONS:
        keyboard = [[InlineKeyboardButton(option, callback_data=f"{option}") ] for option in STATUS_OPTIONS + ["Cancel"]] 

        await query.edit_message_text(f"Выберете статус: ", 
                                    reply_markup=InlineKeyboardMarkup(keyboard))


    if query.data in STATUS_OPTIONS:
        context.user_data['choice'] = query.data
        keyboard = [[InlineKeyboardButton(option, callback_data=f"{option}") ] for option in STATUS_OPTIONS + ["Cancel"]] 
        
        await query.edit_message_text(f"Выберете статус: выбрано <{context.user_data['choice'] }> \n" +
                                    f"Введите свое имя (shortname): ", 
                                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data=f"Cancel")]])
                                    )
        return ID
    
    
async def button_handler_cancel(update: Update, context: CallbackContext) -> int:
    query = update.callback_query

    if query.data == "Cancel":
        await query.message.reply_text("Диалог отменен")
        keyboard = [[InlineKeyboardButton(option, callback_data=f"{option}") ] for option in START_MENU_OPTIONS]

        await query.message.reply_text(f"Добро пожаловать! Нажмите 'Start' для продолжения. ", 
                                reply_markup=InlineKeyboardMarkup(keyboard))
        return START   
    

async def button_handler_date(update: Update, context: CallbackContext) -> int:
    """Обрабатывает нажатие на кнопку."""
    query = update.callback_query

    if query.data == "Cancel":
        await query.message.reply_text("Диалог отменен")
        keyboard = [[InlineKeyboardButton(option, callback_data=f"{option}") ] for option in START_MENU_OPTIONS]

        await query.message.reply_text(f"Добро пожаловать! Нажмите 'Start' для продолжения. ", 
                                reply_markup=InlineKeyboardMarkup(keyboard))
        return START
    

    if query.data in DATE_MENU_OPTIONS:
                            
        context.user_data['date_creation_request'] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

        if query.data == "Сегодня":
            context.user_data['request_date'] = datetime.today()
            
        elif query.data == "Завтра":
            context.user_data['request_date'] = datetime.today() + timedelta(days=1)
            
        elif query.data == "Другой день":
            await query.message.reply_text(
                                        f"Введите дату в формате: ddmmYYYY (31.12.2024):",
                                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data=f"Cancel")]])
                                        )
            return COMPLEX_DATE
            
                                              
        elif query.data == "Выбрать несколько дней":
            await query.message.reply_text(
                                        f"Это пока не работает =) ",
                                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data=f"Cancel")]])
                                        )
        elif query.data == "Cancel":
            await update.message.reply_text("Диалог отменен")
            return START
    
        await query.edit_message_text(f"Выберете статус: выбрано <{context.user_data['choice'] }> \n" +
                                    f"Введите свое имя: <{str(context.user_data['name']).upper() }> \n" +
                                    f"Выбрана дата <{context.user_data['request_date']}>",
                                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data=f"Cancel")]])
                                    )
        

        await query.message.reply_text(f"Опишите причину: ", 
                                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data=f"Cancel")]]))
        return REASON