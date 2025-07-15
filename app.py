import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! I'm your simple schedule bot. Send me events like 'Dinner with Ben 21 July 7pm' "
        "or use /calendar to see your schedule."
    )

async def calendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: Implement calendar display
    await update.message.reply_text("📅 Your calendar feature coming soon!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: Parse and store event
    message = update.message.text
    await update.message.reply_text(f"Got your message: {message}")

def main():
    # Replace with your bot token
    application = Application.builder().token("YOUR_BOT_TOKEN").build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("calendar", calendar))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()