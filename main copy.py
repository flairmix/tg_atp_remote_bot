import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Retrieve the bot token and admin chat ID from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

# Check if BOT_TOKEN and ADMIN_CHAT_ID are set
if not BOT_TOKEN or not ADMIN_CHAT_ID:
    raise ValueError("BOT_TOKEN and ADMIN_CHAT_ID must be set in the .env file.")

# Define states for ConversationHandler
SELECT_OPTION, GET_REASON, GET_SHORTNAME = range(3)

# Menu options
menu_options = [
    [KeyboardButton("start")],
    [KeyboardButton("Remote"), KeyboardButton("Sick")],
    [KeyboardButton("Vacation"), KeyboardButton("Emergency")],
]

# Start command handler
async def start():
    # reply_markup = ReplyKeyboardMarkup(
    #     keyboard=menu_options, one_time_keyboard=True, resize_keyboard=True
    # )
    # await update.message.reply_text("Please choose an option:", reply_markup=reply_markup)
    return SELECT_OPTION

# Handle menu selection
async def select_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    selected_option = update.message.text
    context.user_data["selected_option"] = selected_option

    if selected_option == "Start":
        await start(update, context)
    elif selected_option == "Shortname":
        await update.message.reply_text("Please provide your shortname:")
        return GET_SHORTNAME
    else:
        await update.message.reply_text("Please provide a reason or message:")
        return GET_REASON

# Handle shortname input
async def get_shortname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    shortname = update.message.text
    user = update.message.from_user
    username = f"@{user.username}" if user.username else user.full_name
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Message to admin
    admin_message = (
        f"**Notification**\n\n"
        f"**User**: {username}"
        f"**Shortname**: {shortname}"
        f"**Date and Time**: {current_time}"
    )

    # Send message to admin
    await context.bot.send_message(
        chat_id=int(ADMIN_CHAT_ID),
        text=admin_message,
        parse_mode="Markdown",
    )

    # Acknowledge user
    await update.message.reply_text("Your shortname has been sent to the admin. Thank you!")
    return ConversationHandler.END

# Handle reason input
async def get_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reason = update.message.text
    user = update.message.from_user
    username = f"@{user.username}" if user.username else user.full_name
    selected_option = context.user_data.get("selected_option")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Message to admin
    admin_message = (
        f"**Notification**\n\n"
        f"**User**: {username}\n"
        f"**Option**: {selected_option}\n"
        f"**Message**: {reason}\n"
        f"**Date and Time**: {current_time}"
    )

    # Send message to admin
    await context.bot.send_message(
        chat_id=int(ADMIN_CHAT_ID),
        text=admin_message,
        parse_mode="Markdown",
    )

    # Acknowledge user
    await update.message.reply_text("Your message has been sent to the admin. Thank you!")

    return ConversationHandler.END

# Cancel handler
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operation cancelled. You can start again by sending /start.")
    return ConversationHandler.END

# Get chat ID command handler
async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Your chat ID is: {chat_id}")

# Main function to run the bot
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    # Create a conversation handler with the states SELECT_OPTION, GET_REASON, and GET_SHORTNAME
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECT_OPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_option)],
            GET_REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_reason)],
            GET_SHORTNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_shortname)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add the conversation handler and get_chat_id handler to the application
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("get_chat_id", get_chat_id))

    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()