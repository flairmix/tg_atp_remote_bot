import os

from dotenv import load_dotenv
from datetime import datetime, timedelta
from telegram import (Update, 
                      ReplyKeyboardMarkup, 
                      KeyboardButton, 
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
from database_connection import SessionLocal
from data.users.model import User, Status
from handlers.states import *
from handlers.button_handlers import button_handler_start, button_handler_cancel, button_handler_date
from handlers.date_validation import validate_date

import logging

logger = logging.basicConfig(
    # filename=f'tg_bot/logs/{datetime.now().strftime("%Y-%m-%d__%H-%M-%S")}_log.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)



load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = int(os.getenv('CHAT_ID'))


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


# Функция для обработки выбора опции из второго меню
async def choose_status(update: Update, context: CallbackContext) -> int:

    keyboard = [[InlineKeyboardButton(option, callback_data=f"{option}") ] for option in STATUS_OPTIONS + ["Cancel"]] 

    await update.message.edit_message_text(f"Добро пожаловать! \n"
                                f"Выберете статус: ", 
                                reply_markup=InlineKeyboardMarkup(keyboard))

    return SHORTNAME


# Функция для получения имени
async def get_shortname(update: Update, context: CallbackContext) -> int:
        
    context.user_data['name'] = update.message.text
    message_id_username = update.message.message_id

    #check if user with this shortname exist 
    session1 = SessionLocal()
    with session1: 
        try:
            user_current = session1.query(User).filter_by(shortname=str(context.user_data['name']).upper()).first()
            if user_current is None:
                await update.message.reply_text(f"Такого пользователя не найдено, введите свой shortname")
                return SHORTNAME
            
            context.user_data['name'] = update.message.text
            
        except Exception:
            return START
         
    keyboard = [[InlineKeyboardButton(option, callback_data=f"{option}") ] for option in DATE_MENU_OPTIONS + ["Cancel"]] 

    
    await app.bot.delete_message(chat_id=update.message.chat_id,
                        message_id=message_id_username
        )

    await update.message.reply_text(f"Выберете дату: ", 
                                    reply_markup=InlineKeyboardMarkup(keyboard))

    return REASON


# handle input date from User 
async def get_input_date(update: Update, context: CallbackContext) -> int:
        
    message_id_username = update.message.message_id
    

    if validate_date(update.message.text):
        request_date = datetime.strptime(update.message.text, '%d.%m.%Y')
        context.user_data['request_date'] = datetime.strptime(update.message.text, '%d.%m.%Y')
        
        await update.message.reply_text(f"Выберете статус: <{context.user_data['choice'] }> \n" +
                                    f"Введите свое имя: <{str(context.user_data['name']).upper() }> \n" +
                                    f"Введите дату <{datetime.strptime(update.message.text, '%d.%m.%Y').strftime("%Y-%m-%d")}> \n" +
                                    f"Опишите причину: ",
                                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data=f"Cancel")]])
                                    )
        return REASON
    
    else:
        await app.bot.delete_message(chat_id=update.message.chat_id,
                    message_id=message_id_username
        )
        await update.message.reply_text(f"Неправильно, попробуй еще раз \n" + 
                                        f"Введите дату в формате: ddmmYYYY (31.12.2024)",
                                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data=f"Cancel")]])
                                        )
        return COMPLEX_DATE
    


# Функция для получения причины REASON
async def get_reason(update: Update, context: CallbackContext) -> int:

    context.user_data['reason'] = update.message.text

    message_to_send = (
        f"{context.user_data['date_creation_request']}: User <{str(context.user_data['name']).upper()}> \n" +
        f"отправил запрос на {context.user_data['choice']} на {context.user_data['request_date']} \n"+
        f"с сообщением: \n" + 
        f"{context.user_data['reason']}")

    session1 = SessionLocal()

    with session1: 
        try:
            user_current = session1.query(User).filter_by(shortname=str(context.user_data['name']).upper()).first()

            if user_current is not None:
                new_status = Status(
                    work_status = context.user_data['choice'],
                    user_id = user_current.id,
                    date_message = datetime.now(),
                    message = context.user_data['reason'],
                    date_for_request = context.user_data['request_date'],
                    user=user_current
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

    callbackhandler_start = CallbackQueryHandler(button_handler_start)
    callbackhandler_cancel = CallbackQueryHandler(button_handler_cancel)
    callbackhandler_date = CallbackQueryHandler(button_handler_date)
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START: [MessageHandler(~filters.COMMAND, choose_status), callbackhandler_start],
            SHORTNAME: [MessageHandler(filters.TEXT, get_shortname), callbackhandler_cancel],
            COMPLEX_DATE: [MessageHandler(filters.TEXT, get_input_date), callbackhandler_cancel],
            REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_reason), callbackhandler_date],
        },
        fallbacks=[], 
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get_chat_id", get_chat_id))
    app.add_handler(CommandHandler("help", help))


    app.run_polling()




