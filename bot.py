import os
import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Get token from environment variable
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

if TOKEN is None:
    print("❌ Error: TELEGRAM_BOT_TOKEN environment variable not set!")
    sys.exit(1)

print(f"✅ Bot token loaded successfully!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Hello! I am TrendBot!\n"
        "Send /help to see available commands."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/ping - Check if bot is alive"
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Pong! I'm alive!")

def main():
    print("🚀 Starting TrendBot...")
    
    # Create application
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ping", ping))
    
    # Start polling
    print("✅ Bot is running! Press Ctrl+C to stop.")
    application.run_polling()

if __name__ == '__main__':
    main()
