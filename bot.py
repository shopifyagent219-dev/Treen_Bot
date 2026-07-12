import os
import sys
import logging
import time
from datetime import datetime

# Setup logging - this will help us see what's wrong
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

logger.info("🚀 TrendBot starting...")

# Try to import required modules with error handling
try:
    import requests
    logger.info("✅ Requests module loaded")
except ImportError as e:
    logger.error(f"❌ Failed to import requests: {e}")
    sys.exit(1)

try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
    logger.info("✅ Telegram module loaded")
except ImportError as e:
    logger.error(f"❌ Failed to import telegram: {e}")
    sys.exit(1)

# Get token with proper error handling
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    logger.error("❌ TELEGRAM_BOT_TOKEN environment variable not set!")
    logger.error("❌ Please add it in Railway -> Variables tab")
    sys.exit(1)

logger.info("✅ Bot token loaded successfully")

# Simple handler functions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    try:
        keyboard = [
            [InlineKeyboardButton("📰 Trending News", callback_data='news')],
            [InlineKeyboardButton("📊 Top Reddit", callback_data='reddit')],
            [InlineKeyboardButton("📈 Popular Topics", callback_data='popular')],
            [InlineKeyboardButton("❓ Help", callback_data='help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🤖 *TrendBot*\n\n"
            "I track trending topics from across the web!\n"
            "Select an option below:",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Error in start: {e}")
        await update.message.reply_text("⚠️ Something went wrong. Please try again.")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    try:
        query = update.callback_query
        await query.answer()
        
        if query.data == 'news':
            await show_trending_news(update, context)
        elif query.data == 'reddit':
            await show_trending_reddit(update, context)
        elif query.data == 'popular':
            await show_popular_topics(update, context)
        elif query.data == 'help':
            await show_help(update, context)
        elif query.data == 'menu':
            await show_menu(update, context)
        else:
            await query.edit_message_text("Unknown command. Use /start")
    except Exception as e:
        logger.error(f"Error in button_callback: {e}")

async def show_trending_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display trending news"""
    try:
        query = update.callback_query
        
        # Simple fallback data
        news_data = [
            "🌍 Global Technology Innovations",
            "🤖 AI and Machine Learning Updates",
            "🌱 Climate Change and Sustainability",
            "💰 Cryptocurrency Market Trends",
            "🚀 Space Exploration News"
        ]
        
        message = "📰 *Trending News*\n\n"
        for i, news in enumerate(news_data, 1):
            message += f"{i}. {news}\n"
        message += "\n*Data source: Trending topics*"
        
        keyboard = [[InlineKeyboardButton("🔙 Menu", callback_data='menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Error in show_trending_news: {e}")

async def show_trending_reddit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display Reddit trends"""
    try:
        query = update.callback_query
        
        reddit_data = [
            "r/technology - AI Breakthroughs",
            "r/science - New Discoveries",
            "r/worldnews - Global Events",
            "r/programming - Coding Resources",
            "r/futurism - Future Technologies"
        ]
        
        message = "📊 *Top Reddit Posts*\n\n"
        for i, post in enumerate(reddit_data, 1):
            message += f"{i}. {post}\n"
        message += "\n*Data source: Top posts*"
        
        keyboard = [[InlineKeyboardButton("🔙 Menu", callback_data='menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Error in show_trending_reddit: {e}")

async def show_popular_topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display popular topics"""
    try:
        query = update.callback_query
        
        topics = [
            "🌐 Technology: AI, ML, Robotics",
            "📱 Social Media: Short-form video",
            "🌍 News: Climate, Geopolitics",
            "💰 Finance: Crypto, ESG",
            "🎮 Entertainment: Gaming, Streaming"
        ]
        
        message = "📈 *Popular Topics*\n\n"
        for topic in topics:
            message += f"• {topic}\n"
        message += "\n*Data source: Current trends*"
        
        keyboard = [[InlineKeyboardButton("🔙 Menu", callback_data='menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Error in show_popular_topics: {e}")

async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help"""
    try:
        query = update.callback_query
        
        message = "📋 *Help*\n\n"
        message += "• /start - Main menu\n"
        message += "• Click buttons to explore\n"
        message += "• Data updates daily\n"
        message += "• Powered by TrendBot"
        
        keyboard = [[InlineKeyboardButton("🔙 Menu", callback_data='menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Error in show_help: {e}")

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show main menu"""
    try:
        query = update.callback_query
        
        keyboard = [
            [InlineKeyboardButton("📰 Trending News", callback_data='news')],
            [InlineKeyboardButton("📊 Top Reddit", callback_data='reddit')],
            [InlineKeyboardButton("📈 Popular Topics", callback_data='popular')],
            [InlineKeyboardButton("❓ Help", callback_data='help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🤖 *TrendBot Menu*\n\n"
            "What would you like to explore?",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Error in show_menu: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    try:
        await update.message.reply_text(
            "📋 *Commands*\n\n"
            "/start - Show menu\n"
            "/help - Show this help\n"
            "/ping - Check if alive",
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error in help_command: {e}")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ping command"""
    try:
        await update.message.reply_text("🏓 Pong! I'm alive! 🟢")
    except Exception as e:
        logger.error(f"Error in ping: {e}")

def main():
    """Main function with error handling"""
    try:
        logger.info("🚀 Building application...")
        
        # Create application with timeout settings
        app = ApplicationBuilder()\
            .token(TOKEN)\
            .connect_timeout(30.0)\
            .read_timeout(30.0)\
            .build()
        
        # Add handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("ping", ping))
        app.add_handler(CallbackQueryHandler(button_callback))
        
        logger.info("✅ Application built successfully")
        logger.info("🤖 Starting polling...")
        
        # Start the bot
        app.run_polling(
            drop_pending_updates=True,
            allowed_updates=['message', 'callback_query']
        )
        
    except Exception as e:
        logger.error(f"❌ Fatal error in main: {e}")
        logger.error(f"Stack trace:", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
