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
from handlers.states import *
from handlers.button_handlers import button_handler_start, button_handler_cancel, button_handler_date
from handlers.date_validation import validate_date

import requests
import json
import logging



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


# Функция для обработки выбора опции из второго меню
async def choose_User_requests(update: Update, context: CallbackContext) -> int:

    keyboard = [[InlineKeyboardButton(option, callback_data=f"{option}") ] for option in STATUS_OPTIONS + ["Cancel"]] 

    await update.message.edit_message_text(f"Добро пожаловать! \n"
                                f"Выберете статус: ", 
                                reply_markup=InlineKeyboardMarkup(keyboard))

    return ID


# Функция для получения имени
async def get_shortname(update: Update, context: CallbackContext) -> int:
        
    context.user_data['name'] = update.message.text.upper()
    message_id_username = update.message.message_id

    #check if Users with this id exist 
    user_db = requests.get(f'http://backend:8000/users/{str(context.user_data['name']).upper()}')
    logging.info(f"user_db.status_code {user_db.status_code}")

    if user_db.status_code == 204:
        await update.message.reply_text(f"Такого пользователя не найдено, введите свой id")
        return ID
                     
    keyboard = [[InlineKeyboardButton(option, callback_data=f"{option}") ] for option in DATE_MENU_OPTIONS + ["Cancel"]] 

    
    await app.bot.delete_message(chat_id=update.message.chat_id,
                        message_id=message_id_username
        )

    await update.message.reply_text(f"Выберете дату: ", 
                                    reply_markup=InlineKeyboardMarkup(keyboard))

    return REASON


# # handle input date from Users 
async def get_input_date(update: Update, context: CallbackContext) -> int:
        
    message_id_username = update.message.message_id
    

    if validate_date(update.message.text):

        date = datetime(update.message.text)

        context.user_data['request_date'] = date.strftime('%Y-%m-%d')
        logging.info(f" context.user_data['request_date'] {context.user_data['request_date']}")

        await update.message.reply_text(f"Выберете статус: <{context.user_data['choice'] }> \n" +
                                    f"Введите свое имя: <{str(context.user_data['name']).upper() }> \n" +
                                    f"Введите дату <{context.user_data['request_date']}> \n" +
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
        f"{context.user_data['date_creation_request']}: Users <{str(context.user_data['name']).upper()}> \n" +
        f"отправил запрос на {context.user_data['choice']} на {context.user_data['request_date']} \n"+
        f"с сообщением: \n" + 
        f"{context.user_data['reason']}")


    try:
        user_id = str(context.user_data['name']).upper()
        
        url_user = f'http://backend:8000/users/{user_id}'
        url_post = f'http://backend:8000/users/create_user_request/{user_id}'


        user_db = requests.get(url_user)

        if user_db.status_code != 204:
            logging.info(f'''user_db.status_code {user_db.status_code},
                        work_status: context.user_data['choice'] {context.user_data['choice']},
                         user_id {user_id}, 
                         context.user_data['reason'] {context.user_data['reason']}"
                         date {context.user_data['request_date']}'''
                         )


            payload = {
                "work_status": context.user_data['choice'],
                "user_id": user_id,
                "date_for_request": context.user_data['request_date'],
                "message": context.user_data['reason']
            }
            headers = {'Content-Type': 'application/json'}
            
            requests.post(url_post, data=json.dumps(payload), headers=headers)

                          
            
    except Exception:
        pass


    # Отправка данных другому пользователю
    await context.bot.send_message(chat_id=CHAT_ID, text=message_to_send)
    await update.message.reply_text("Благодарим вас! Возвращаемся в главное меню.")

    # Возвращаемся в главное меню
    return await start(update, context)



if __name__ == "__main__":


    logger = logging.basicConfig(
        # filename=f'tg_bot/logs/{datetime.now().strftime("%Y-%m-%d__%H-%M-%S")}_log.log',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    load_dotenv()
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    CHAT_ID = int(os.getenv('CHAT_ID'))


    app = Application.builder().token(TOKEN).build()

    callbackhandler_start = CallbackQueryHandler(button_handler_start)
    callbackhandler_cancel = CallbackQueryHandler(button_handler_cancel)
    callbackhandler_date = CallbackQueryHandler(button_handler_date)
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START: [MessageHandler(~filters.COMMAND, choose_User_requests), callbackhandler_start],
            ID: [MessageHandler(filters.TEXT, get_shortname), callbackhandler_cancel],
            COMPLEX_DATE: [MessageHandler(filters.TEXT, get_input_date), callbackhandler_cancel],
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




