
import os 
import json
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

from telegram import (Update, 
                    InlineKeyboardMarkup,
                    InlineKeyboardButton)
from telegram.ext import (
    CallbackContext
)

from .states import *


load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = int(os.getenv('CHAT_ID_MID'))

# Функция для получения причины REASON
async def get_reason(update: Update, context: CallbackContext) -> int:

    context.user_data['reason'] = update.message.text

    message_to_send = (
        f"{context.user_data['date_creation_request']}: User <{str(context.user_data['name']).upper()}> \n" +
        f"отправил запрос на {context.user_data['choice']} на <{context.user_data['request_date']}> \n"+
        f"с сообщением: \n" + 
        f"<{context.user_data['reason']}>")


    try:
        user_id = str(context.user_data['name']).upper()
        
        url_user = f'http://backend:8000/users/{user_id}'
        url_post = f'http://backend:8000/users/create_user_request/{user_id}'

        user_db = requests.get(url_user)

        if user_db.status_code != 204:

            for date in context.user_data['request_date']:

                payload = {
                    "work_status": context.user_data['choice'],
                    "user_id": user_id,
                    "date_for_request": date,
                    "message": context.user_data['reason']
                }
                headers = {'Content-Type': 'application/json'}
                
                requests.post(url_post, data=json.dumps(payload), headers=headers)

    except Exception:
        pass


    # Отправка данных другому пользователю
    await context.bot.send_message(chat_id=CHAT_ID, text=message_to_send)
    await update.message.reply_text(message_to_send +"\n\n Благодарим вас! Возвращаемся в главное меню.")

    # Возвращаемся в главное меню
    return START  