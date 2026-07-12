import os
import sys
import logging
import requests
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get token
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    logger.error("❌ TELEGRAM_BOT_TOKEN not set!")
    sys.exit(1)

logger.info("✅ Bot token loaded successfully")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    keyboard = [
        [InlineKeyboardButton("📰 Trending News", callback_data='news')],
        [InlineKeyboardButton("📊 Top Reddit Posts", callback_data='reddit')],
        [InlineKeyboardButton("📈 Popular Topics", callback_data='popular')],
        [InlineKeyboardButton("🔄 Refresh", callback_data='refresh')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🤖 *Welcome to TrendBot!*\n\n"
        "I track trending topics from across the web.\n"
        "Select an option below:",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'news':
        await show_trending_news(update, context)
    elif query.data == 'reddit':
        await show_trending_reddit(update, context)
    elif query.data == 'popular':
        await show_popular_topics(update, context)
    elif query.data == 'refresh':
        await query.edit_message_text("🔄 Refreshing data...")
        await show_trending_news(update, context)
    elif query.data == 'menu':
        await show_menu(update, context)

async def show_trending_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display trending news from RSS feeds"""
    query = update.callback_query
    
    try:
        # Try to get real news
        response = requests.get(
            "https://api.rss2json.com/v1/api.json?rss_url=https://feeds.bbci.co.uk/news/rss.xml",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])[:5]
            
            message = "📰 *Trending News*\n\n"
            for i, item in enumerate(items, 1):
                title = item.get('title', 'No title')[:60]
                message += f"{i}. {title}...\n"
            
            if not items:
                message = "📰 *Trending News*\n\nNo news available right now."
        else:
            message = "📰 *Trending News*\n\nUsing fallback data:\n\n1. Global Tech Innovations\n2. Climate Action Updates\n3. Economic Trends\n4. Space Exploration\n5. AI Developments"
            
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        message = "📰 *Trending News*\n\nUsing fallback data:\n\n1. Global Tech Innovations\n2. Climate Action Updates\n3. Economic Trends\n4. Space Exploration\n5. AI Developments"
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def show_trending_reddit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display top Reddit posts"""
    query = update.callback_query
    
    try:
        response = requests.get(
            "https://www.reddit.com/r/all/top.json?limit=5",
            headers={'User-Agent': 'Mozilla/5.0'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            
            message = "📊 *Top Reddit Posts*\n\n"
            for i, post in enumerate(posts[:5], 1):
                post_data = post.get('data', {})
                title = post_data.get('title', 'No title')[:60]
                score = post_data.get('score', 0)
                subreddit = post_data.get('subreddit', 'unknown')
                message += f"{i}. {title}...\n   🔥 {score} | r/{subreddit}\n\n"
            
            if not posts:
                message = "📊 *Top Reddit Posts*\n\nNo posts available right now."
        else:
            message = "📊 *Top Reddit Posts*\n\nUsing fallback data:\n\n1. r/technology - AI Breakthrough\n2. r/science - New Discovery\n3. r/worldnews - Global Update\n4. r/programming - Coding Tips\n5. r/futurism - Future Tech"
            
    except Exception as e:
        logger.error(f"Error fetching Reddit: {e}")
        message = "📊 *Top Reddit Posts*\n\nUsing fallback data:\n\n1. r/technology - AI Breakthrough\n2. r/science - New Discovery\n3. r/worldnews - Global Update\n4. r/programming - Coding Tips\n5. r/futurism - Future Tech"
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def show_popular_topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display popular topics"""
    query = update.callback_query
    
    message = "📈 *Popular Topics This Week*\n\n"
    topics = [
        "🌐 Technology: AI, Machine Learning, Robotics",
        "📱 Social Media: Short-form video, Live streaming",
        "🌍 News: Climate change, Geopolitics",
        "💰 Finance: Cryptocurrency, ESG investing",
        "🎮 Entertainment: Gaming, Streaming, Metaverse"
    ]
    
    for topic in topics:
        message += f"• {topic}\n"
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show main menu"""
    query = update.callback_query
    
    keyboard = [
        [InlineKeyboardButton("📰 Trending News", callback_data='news')],
        [InlineKeyboardButton("📊 Top Reddit Posts", callback_data='reddit')],
        [InlineKeyboardButton("📈 Popular Topics", callback_data='popular')],
        [InlineKeyboardButton("🔄 Refresh", callback_data='refresh')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🤖 *TrendBot Menu*\n\n"
        "Select an option below:",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(
        "📋 *Available Commands*\n\n"
        "/start - Show main menu\n"
        "/help - Show this help\n"
        "/ping - Check if bot is alive\n"
        "/news - Get trending news\n"
        "/reddit - Get top Reddit posts\n"
        "/popular - Show popular topics",
        parse_mode='Markdown'
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ping command"""
    await update.message.reply_text("🏓 Pong! I'm alive and running!")

def main():
    """Main function"""
    logger.info("🚀 Starting TrendBot...")
    
    # Create application
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ping", ping))
    
    # Add callback query handler for buttons
    app.add_handler(CallbackQueryHandler(button_callback))
    
    # Start polling
    logger.info("✅ Bot is running!")
    app.run_polling()

if __name__ == '__main__':
    main()
