import os, sys

current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from dotenv import load_dotenv
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ForceReply
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackContext,
    ContextTypes,
    filters,
)
from typing import Generator
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
STATUS_OPTIONS = ['Remote', 'Sick', 'Vacation', 'Emergency']
SECOND_MENU_OPTIONS = STATUS_OPTIONS + ['Cancel']

# Состояния диалога
START, CHOOSING, NAME, REASON = range(4)


# Функция для обработки команды /start
async def start(update: Update, context: CallbackContext) -> int:
    # Создаем клавиатуру с одной кнопкой: Start
    menu_keyboard = [[KeyboardButton('Start')]]
    menu_reply_markup = ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "Добро пожаловать! Нажмите 'Start' для продолжения.",
        reply_markup=menu_reply_markup
    )

    return START

# Функция для обработки выбора опции из второго меню
async def second_menu_choice(update: Update, context: CallbackContext) -> int:
    user_second_menu_choice = update.message.text
    if user_second_menu_choice == 'Start':
        # Переходим к выбору статуса
        status_keyboard = [[KeyboardButton(option)] for option in STATUS_OPTIONS]
        cancel_button = [[KeyboardButton('Cancel')]]
        status_reply_markup = ReplyKeyboardMarkup(status_keyboard + cancel_button, one_time_keyboard=True)

        await update.message.reply_text(
            "Выберите статус:", reply_markup=status_reply_markup
        )

        return CHOOSING
    else:
        await update.message.reply_text("Неверная команда. Попробуйте еще раз.")
        return START

# Функция для обработки выбора статуса
async def choice(update: Update, context: CallbackContext) -> int:
    user_status_choice = update.message.text
    if user_status_choice in STATUS_OPTIONS:
        context.user_data['choice'] = user_status_choice
        await update.message.reply_text(f"Введите свое имя:", reply_markup=ForceReply(selective=True))
        return NAME
    elif user_status_choice == 'Cancel':
        await update.message.reply_text("Диалог отменен")
        return await start(update, context)
    else:
        await update.message.reply_text("Неверная команда. Попробуйте еще раз.")
        return CHOOSING

# Get chat ID command handler
async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Your chat ID is: {chat_id}")


# Функция для получения имени
async def get_name(update: Update, context: CallbackContext) -> int:
    
    if update.message.text == 'Cancel':
        await update.message.reply_text("Диалог отменен")
        return await start(update, context)

    context.user_data['name'] = update.message.text

    session1 = SessionLocal()
    
    with session1: 
        try:
            user_current = session1.query(User).filter_by(shortname=context.user_data['name']).first()

            if user_current is None:
                await update.message.reply_text(f"Такого пользователя не найдено, введите свой shortname")
                return NAME
            
        except Exception:
            pass
    
    await update.message.reply_text(f"Пожалуйста, объясните почему вы выбрали '{context.user_data['choice']}'.")
    return REASON

# Функция для получения причины
async def get_reason(update: Update, context: CallbackContext) -> int:

    if update.message.text == 'Cancel':
        await update.message.reply_text("Диалог отменен")
        return await start(update, context)

    reason = update.message.text
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message_to_send = f"{current_datetime}: {context.user_data['name']} находится в статусе {context.user_data['choice']} по причине: {reason}"

    session1 = SessionLocal()

    with session1: 
        try:
            user_current = session1.query(User).filter_by(shortname=context.user_data['name']).first()

            if user_current is not None:
                new_status = Status(
                    work_status = context.user_data['choice'],
                    user_id = user_current.id,
                    date_status = datetime.now(),
                    message = reason
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


if __name__ == "__main__":

    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START: [MessageHandler(filters.Regex(f'^({"|".join(['Start'])})$'), second_menu_choice)],
            NAME: [MessageHandler(filters.TEXT, get_name)],
            CHOOSING: [MessageHandler(filters.Regex(f'^({"|".join(SECOND_MENU_OPTIONS)})$'), choice)],
            REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_reason)]
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("get_chat_id", get_chat_id))
    app.run_polling()




