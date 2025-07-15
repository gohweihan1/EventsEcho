import logging
import os
import asyncio
from database import db
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
    """Handle /calendar command - show all upcoming events"""
    try:
        username = f"@{update.effective_user.username}" if update.effective_user.username else f"user_{update.effective_user.id}"
        events = db.get_upcoming_events(username)
        
        if not events:
            await update.message.reply_text(f"📅 <b>Your Calendar</b>\n\nYour calendar is empty.\n\nSend me a message to add your first event!", parse_mode='HTML')
            return
        
        # Format events grouped by date
        response = f"📅 <b>Your Calendar</b>\n"
        current_date = None
        
        for event in events:
            response += "\n"
            event_date = event['date']
            
            # Add date header if it's a new date
            if current_date != event_date:
                current_date = event_date
                
                # Parse date and format nicely
                from datetime import datetime
                date_obj = datetime.strptime(event_date, '%Y-%m-%d')
                day = date_obj.strftime('%d').lstrip('0')  # Remove leading zero
                month = date_obj.strftime('%B')
                weekday = date_obj.strftime('%A')
                
                response += f"<b>{day} {month} [{weekday}]</b>\n"
            
            # Format time
            time_str = ""
            if event['time']:
                # Convert 19:00 to 7pm format
                time_obj = datetime.strptime(event['time'], '%H:%M')
                hour = time_obj.hour
                if hour == 0:
                    time_str = "12am"
                elif hour < 12:
                    time_str = f"{hour}am"
                elif hour == 12:
                    time_str = "12pm"
                else:
                    time_str = f"{hour-12}pm"
            
            # Add event
            response += f"{time_str} - {event['event']}\n"
        
        await update.message.reply_text(response, parse_mode='HTML')
        
    except Exception as e:
        logger.error(f"Error in calendar command: {e}")
        await update.message.reply_text("❌ Sorry, I had trouble getting your calendar. Please try again.")

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

async def clear_calendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /clear command - delete all events"""
    try:
        username = f"@{update.effective_user.username}" if update.effective_user.username else f"user_{update.effective_user.id}"
        
        # Get count of events first
        events = db.get_upcoming_events(username)
        event_count = len(events)
        
        if event_count == 0:
            await update.message.reply_text("🗑️ **Clear Calendar**\n\nYour calendar is already empty!")
            return
        
        # Delete all events for this user
        success = db.clear_all_events(username)
        
        if success:
            await update.message.reply_text(f"✅ **Calendar Cleared**\n\nDeleted {event_count} event(s) successfully!")
        else:
            await update.message.reply_text("❌ **Error**\n\nFailed to clear calendar. Please try again.")
            
    except Exception as e:
        logger.error(f"Error in clear command: {e}")
        await update.message.reply_text("❌ Sorry, I had trouble clearing your calendar. Please try again.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # message = update.message.text
    # await update.message.reply_text(f"Got your message: {message}")
    try:
        # Test database insertion
        username = f"@{update.effective_user.username}" if update.effective_user.username else f"user_{update.effective_user.id}"
        event_id = db.add_event(username, "Therapy", "2025-07-19", "16:00")
        await update.message.reply_text(f"✅ Test event added with ID: {event_id}")
        
    except Exception as e:
        logger.error(f"Error adding test event: {e}")
        await update.message.reply_text(f"❌ Error adding event: {e}")


def main():
    # Get token from environment variable
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        print("Error: TELEGRAM_TOKEN not found in environment variables")
        return
    
    try:
        from database import db
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return
    
    application = ApplicationBuilder().token(token).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("calendar", calendar))
    application.add_handler(CommandHandler("today", today))
    application.add_handler(CommandHandler("week", week))
    application.add_handler(CommandHandler("delete", delete))
    application.add_handler(CommandHandler("settings", settings))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("clear", clear_calendar))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("EventEcho is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()