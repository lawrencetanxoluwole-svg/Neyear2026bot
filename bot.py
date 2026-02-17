import os
import logging
import asyncio
from datetime import timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Use your actual Token from BotFather as an environment variable on Render
TOKEN = os.environ.get("TELEGRAM_TOKEN", "")

# The message content for your 2026 goals
MOTIVATION_TEXT = (
    "🚀 **Goal 2026 Reminder**\n\n"
    "You have a goal to achieve this year 2026! 🏆\n"
    "Stop procrastinating. Focus on success by having a positive mindset.\n\n"
    "Choose your action for this half-hour:"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Initializes the bot and starts the 30-minute timer."""
    chat_id = update.effective_chat.id
    
    # Remove existing jobs for this user if they restart
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in current_jobs:
        job.schedule_removal()

    # Schedule the first reminder in 30 minutes (1800 seconds)
    context.job_queue.run_repeating(
        send_reminder, 
        interval=timedelta(minutes=30), 
        first=1, # Send first message immediately
        chat_id=chat_id, 
        name=str(chat_id)
    )

    await update.message.reply_text(
        "Welcome! Your 2026 Focus Bot is active. I will notify you every 30 minutes to keep you on track."
    )

async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    """The function that sends the notification with buttons."""
    job = context.job
    
    keyboard = [
        [
            InlineKeyboardButton("🧍 Stand", callback_data='stand'),
            InlineKeyboardButton("📦 Contain", callback_data='contain')
        ],
        [InlineKeyboardButton("✅ Continue", callback_data='continue')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=job.chat_id,
        text=MOTIVATION_TEXT,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles button clicks."""
    query = update.callback_query
    await query.answer()

    if query.data == 'continue':
        await query.edit_message_text(
            text="Keep going! Your focus is sharp. See you in 30 minutes for the next check-in. 🎯"
        )
    elif query.data == 'stand':
        await query.edit_message_text(
            text="Good choice! Stand up, stretch, and reset your mind for success. 🧘‍♂️"
        )
    elif query.data == 'contain':
        await query.edit_message_text(
            text="Discipline is key. Stay contained and focused on the task at hand. 🛡️"
        )

def main():
    if not TOKEN:
        print("Error: No TELEGRAM_TOKEN found in environment variables.")
        return

    application = ApplicationBuilder().token(TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Start the Bot
    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
