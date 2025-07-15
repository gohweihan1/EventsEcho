import logging
import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! I'm EventEcho 🎯\n\n"
        "Send me events like 'Dinner with Ben 21 July 7pm' "
        "or use /calendar to see your schedule."
    )

async def calendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📅 Your calendar feature coming soon!")

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📅 Your today feature coming soon!")

async def week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📅 Your week feature coming soon!") 

async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📅 Your week feature coming soon!") 

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📅 Your week feature coming soon!") 

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📅 Your week feature coming soon!") 

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    await update.message.reply_text(f"Got your message: {message}")

def main():
    # Get token from environment variable
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        print("Error: TELEGRAM_TOKEN not found in environment variables")
        return
    
    application = ApplicationBuilder().token(token).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("calendar", calendar))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("EventEcho is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()