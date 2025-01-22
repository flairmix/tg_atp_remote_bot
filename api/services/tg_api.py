import os
from contextlib import contextmanager
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, ContextTypes

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

@contextmanager
def temporary_bot(token: str):
    try:
        app = Application.builder().token(token).build()
        yield app
    finally:
        app.stop()

async def send_message(chat_id: int, message_text: str):
    with temporary_bot(TOKEN) as bot:
        await bot.bot.send_message(chat_id=chat_id, text=message_text)