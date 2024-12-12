import os, sys

current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from dotenv import load_dotenv
from datetime import datetime, timedelta
from telegram import (Update, 
                      ReplyKeyboardMarkup, 
                      KeyboardButton, 
                      ForceReply, 
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
from data.database_connection import SessionLocal
from data.users.model import User, Status

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = int(os.getenv('CHAT_ID'))

# Опции для выбора
START_MENU_OPTIONS = ['Start'] 
STATUS_OPTIONS = ['Remote', 'Sick', 'Vacation', 'Cancel']
DATE_MENU_OPTIONS = ['Сегодня', 'Завтра', 'Другой день', 'Выбрать несколько дней', 'Cancel'] 

# Состояния диалога
START, CHOOSING_STATUS, SHORTNAME, REASON = range(4)

# Get chat ID command handler
async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Your chat ID is: {chat_id}")



# Функция для обработки команды /start
async def start(update: Update, context: CallbackContext) -> None:

    keyboard = [[InlineKeyboardButton(option, callback_data=f"{option}") ] for option in START_MENU_OPTIONS]

    await update.message.reply_text(f"Добро пожаловать! Нажмите 'Start' для продолжения. ", 
                                    reply_markup=InlineKeyboardMarkup(keyboard))

    return START


# Функция для обработки выбора опции из второго меню
async def second_menu_choice(update: Update, context: CallbackContext) -> int:
    
    if update.message.text == 'Cancel':
        await update.message.reply_text("Диалог отменен")
        return await start(update, context)


    return SHORTNAME




# Функция для обработки выбора статуса
async def choice(update: Update, context: CallbackContext) -> int:
    user_status_choice = update.message.text
    if user_status_choice in STATUS_OPTIONS:
        context.user_data['choice'] = user_status_choice

        # await update.message.reply_text(f"Введите свое имя:", reply_markup=ForceReply(selective=True))
        status_reply_markup = ReplyKeyboardMarkup(cancel_button, 
                                                  one_time_keyboard=True
                                                  )

        await update.message.reply_text(
            f"Введите свое имя:", reply_markup=status_reply_markup, 
        )
        return SHORTNAME
    elif user_status_choice == 'Cancel':
        await update.message.reply_text("Диалог отменен")
        return await start(update, context)
    else:
        await update.message.reply_text("Неверная команда. Попробуйте еще раз.")
        return CHOOSING_STATUS


# Функция для получения имени
async def get_shortname(update: Update, context: CallbackContext) -> int:
    
    if update.message.text == 'Cancel':
        await update.message.reply_text("Диалог отменен")
        return await start(update, context)

    context.user_data['name'] = update.message.text

    print(f"context.user_data['name'] - {context.user_data['name']}")
    #check if user with this shortname exist 
    session1 = SessionLocal()
    with session1: 
        try:
            user_current = session1.query(User).filter_by(shortname=context.user_data['name']).first()
            if user_current is None:
                await update.message.reply_text(f"Такого пользователя не найдено, введите свой shortname")
                return SHORTNAME
            
        except Exception:
            pass
    
    keyboard = [[InlineKeyboardButton(option, callback_data=f"{option}") ] for option in DATE_MENU_OPTIONS]

    await update.message.reply_text(f"Выберете дату: ", 
                                    reply_markup=InlineKeyboardMarkup(keyboard))

    return REASON


# Функция для получения причины REASON
async def get_reason(update: Update, context: CallbackContext) -> int:

    if update.message.text == 'Cancel':
        await update.message.reply_text("Диалог отменен")
        return await start(update, context)

    # reason = update.message.text
    context.user_data['reason'] = update.message.text

    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message_to_send = (f"{current_datetime}: {context.user_data['name']}" +
        f"находится в статусе {context.user_data['choice']} по причине:" + 
        f"{context.user_data['reason']}")

    session1 = SessionLocal()

    with session1: 
        try:
            user_current = session1.query(User).filter_by(shortname=context.user_data['name']).first()

            if user_current is not None:
                new_status = Status(
                    work_status = context.user_data['choice'],
                    user_id = user_current.id,
                    date_message = datetime.now(),
                    message = context.user_data['reason'],
                    date_for_request = context.user_data['request_date']
                    )
            
            session1.add_all([new_status])
            session1.commit()

        except Exception:
            pass

    # Отправка данных другому пользователю
    await context.bot.send_message(chat_id=CHAT_ID, text=message_to_send)
    await update.message.reply_text("Благодарим вас! Возвращаемся в главное меню.")

    # Возвращаемся в главное меню
    return await start(update, context)



async def button_handler(update: Update, context: CallbackContext) -> int:
    """Обрабатывает нажатие на кнопку."""
    query = update.callback_query
    print(query.data)

    if query.data == "Cancel":
        await query.message.reply_text("Диалог отменен")
        keyboard = [[InlineKeyboardButton(option, callback_data=f"{option}") ] for option in START_MENU_OPTIONS]

        await query.message.reply_text(f"Добро пожаловать! Нажмите 'Start' для продолжения. ", 
                                reply_markup=InlineKeyboardMarkup(keyboard))
    
    
    if query.data in START_MENU_OPTIONS:
        keyboard = [[InlineKeyboardButton(option, callback_data=f"{option}") ] for option in STATUS_OPTIONS]

        await query.message.reply_text(f"Выберете статус: ", 
                                reply_markup=InlineKeyboardMarkup(keyboard))
    
    if query.data in STATUS_OPTIONS:
        context.user_data['choice'] = query.data
        keyboard = [[InlineKeyboardButton(option, callback_data=f"{option}") ] for option in STATUS_OPTIONS]
        
        
        await query.message.reply_text(f"Введите свое имя (shortname): ")
        return SHORTNAME


    if query.data in DATE_MENU_OPTIONS:
        if query.data == "Сегодня":
            context.user_data['request_date'] = datetime.today()
            await query.edit_message_text(f"Выбрано - <{query.data}>")
            
        elif query.data == "Завтра":
            context.user_data['request_date'] = datetime.today() + timedelta(days=1)
            await query.edit_message_text(f"Выбрано - <{query.data}>")
        elif query.data == "Другой день":
            pass
        elif query.data == "Выбрать несколько дней":
            pass
        elif query.data == "Cancel":
            await update.message.reply_text("Диалог отменен")
            return await start(update, context)
        else:
            pass
        
        await query.message.reply_text(f"Опишите причину: ") 
        return REASON
            




if __name__ == "__main__":

    app = Application.builder().token(TOKEN).build()

    callbackhandler = CallbackQueryHandler(button_handler)
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_menu_choice), callbackhandler],
            SHORTNAME: [MessageHandler(filters.TEXT, get_shortname), callbackhandler],
            CHOOSING_STATUS: [MessageHandler(filters.Regex(f'^({"|".join(START_MENU_OPTIONS)})$'), choice), callbackhandler],
            REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_reason), callbackhandler],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("get_chat_id", get_chat_id))


    app.run_polling()




