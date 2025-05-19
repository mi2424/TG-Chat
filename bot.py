# -*- coding: utf-8 -*-

import os
import random
import logging
import sys
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import dotenv

# Import helper functions and config
from helpers import assign_status, fake_typing, verify_resource_exists
from config import (
    DEFAULT_LANDING_PAGE_URL, DEFAULT_LOG_FILE, 
    EMOJI_ONLINE, EMOJI_BUSY, EMOJI_OFFLINE, EMOJI_FIRE, 
    EMOJI_WOMAN, EMOJI_PIN, EMOJI_HEART, EMOJI_SMILE, EMOJI_WINK,
    FAKE_PROFILES
)
from rate_limiter import RateLimiter
from user_tracker import user_tracker

# Create a rate limiter instance (5 requests per minute per user)
rate_limiter = RateLimiter(max_calls=5, time_frame=60)

# Ensure proper encoding for emoji support
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        # Python < 3.7 doesn't have reconfigure
        pass

# === Settings ===
# Load environment variables from .env file if it exists
try:
    dotenv.load_dotenv()
except ImportError:
    print("dotenv package not installed. Environment variables must be set manually.")

LANDING_PAGE_URL = os.getenv("LANDING_PAGE_URL", DEFAULT_LANDING_PAGE_URL)
LOG_FILE = os.getenv("LOG_FILE", DEFAULT_LOG_FILE)
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Set this in your environment or .env file

# === Setup Logger ===
logging.basicConfig(
    filename=LOG_FILE, 
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

# Helper functions moved to helpers.py

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        # Check rate limits
        if not rate_limiter.is_allowed(user.id):
            logging.warning(f"Rate limit exceeded for user_id:{hash(str(user.id)) % 10000}")
            await update.message.reply_text("You're using this bot too frequently. Please try again in a minute.")
            return
            
        assign_status(FAKE_PROFILES, EMOJI_ONLINE, EMOJI_BUSY, EMOJI_OFFLINE)        # Logging only non-identifying information for privacy
        user_id_hash = hash(str(user.id)) % 10000  # Create a hash for privacy
        logging.info(f"/start command received from user_hash:{user_id_hash}")
        
        # Track user start and schedule follow-up
        user_tracker.track_start(user.id)
        user_tracker.schedule_follow_up(user.id, send_follow_up, minutes=30)

        # Show typing indicator before sending first message
        bot = context.bot
        chat_id = update.effective_chat.id
        await fake_typing(bot, chat_id, 3)
        
        # Send the "scanning your area" message
        await update.message.reply_text(f"{EMOJI_PIN} Scanning your area...")
        
        # Add a realistic pause while "scanning"
        scanning_time = 3 + random.random() * 2  # 3-5 seconds of "scanning"
        await asyncio.sleep(scanning_time)
        
        # Create a carousel of profiles
        buttons = []
        for girl in FAKE_PROFILES:
            status = girl["status"]
            label = f"{girl['name']} ({status})"
            if girl["online"]:
                buttons.append([InlineKeyboardButton(f"{EMOJI_FIRE} Chat with {girl['name']}", callback_data=f"chat_{girl['name']}")])
            else:
                buttons.append([InlineKeyboardButton(f"{label}", callback_data="offline")])

        reply_markup = InlineKeyboardMarkup(buttons)
        await update.message.reply_text(
            f"{EMOJI_WOMAN} Girls near you:\nTap to start chatting {EMOJI_FIRE}",
            reply_markup=reply_markup
        )
    except Exception as e:
        logging.error(f"Error in start command: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")

# Handle Button Clicks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()
        user = query.from_user
        chat_id = query.message.chat_id
        bot = context.bot
        if query.data.startswith("chat_"):
            girl_name = query.data.split("_")[1]
            girl = next((g for g in FAKE_PROFILES if g["name"] == girl_name), None)
            if not girl:
                await bot.send_message(chat_id=chat_id, text="Girl not found.")
                return
                
            # Track user click
            user_tracker.track_click(user.id)
            logging.info(f"Chat started with {girl['name']}")
            photo_path = os.path.join("profiles", girl["photo"])
            # Check if file exists before trying to send it
            if not verify_resource_exists(photo_path, f"Photo file not found: {photo_path}"):
                await bot.send_message(chat_id=chat_id, text="Sorry, something went wrong with this profile.")
                return
            
            try:
                with open(photo_path, "rb") as photo:
                    await bot.send_photo(
                        chat_id=chat_id,
                        photo=InputFile(photo),
                        caption=f"{EMOJI_WOMAN} {girl['name']}, {girl['age']}\n{EMOJI_PIN} {girl['distance']} away\n{EMOJI_ONLINE} Online Now"
                    )
            except Exception as e:
                logging.error(f"Error opening photo file {photo_path}: {e}")
                await bot.send_message(chat_id=chat_id, text="Sorry, something went wrong with loading this profile.")

            # Pause realistically before first message - simulate the girl taking time to respond
            await asyncio.sleep(3 + random.random() * 2)
            
            # First message with realistic typing time based on message length
            message1 = f"{girl['name']}: Hey there... {EMOJI_HEART} You look cute {EMOJI_SMILE}"
            await fake_typing(bot, chat_id, 2, len(message1))
            await bot.send_message(chat_id=chat_id, text=message1)
            
            # Pause between messages like a real person would
            await asyncio.sleep(1 + random.random() * 2)
            
            # Second message with realistic typing
            message2 = f"{girl['name']}: I'm just around the corner... Wanna chat?"
            await fake_typing(bot, chat_id, 2, len(message2))
            await bot.send_message(chat_id=chat_id, text=message2)
            
            # Pause before the final CTA
            await asyncio.sleep(2 + random.random() * 1.5)
            
            keyboard = [[InlineKeyboardButton(f"{EMOJI_FIRE} Click to Chat with {girl['name']}", url=LANDING_PAGE_URL)]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Final call-to-action with realistic typing
            final_message = f"{girl['name']}: Click below, I'm waiting for you {EMOJI_WINK}"
            await fake_typing(bot, chat_id, 2, len(final_message))
            await bot.send_message(
                chat_id=chat_id,
                text=final_message,
                reply_markup=reply_markup
            )

            # Log with less personal information
            logging.info(f"Link offered for {girl['name']} profile")

        elif query.data == "offline":
            await bot.send_message(chat_id=chat_id, text=f"{EMOJI_BUSY} This girl is currently busy. Please try another one.")
    except Exception as e:
        logging.error(f"Error in button handler: {e}")
        try:
            await bot.send_message(chat_id=chat_id, text="An error occurred. Please try again later.")
        except:
            pass

# Help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(
            f"Hi! I'm a chat bot that helps you connect with people nearby. 👋\n\n"
            f"Use /start to see people in your area.\n"
            f"Use /about to learn more about this bot."
        )
        logging.info(f"Help command used by user_hash:{hash(str(update.effective_user.id)) % 10000}")
    except Exception as e:
        logging.error(f"Error in help command: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")

# About command handler
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(
            f"This is a demo chat bot that simulates connecting with people nearby.\n\n"
            f"⚠️ Note: All profiles are simulated for demonstration purposes."
        )
        logging.info(f"About command used by user_hash:{hash(str(update.effective_user.id)) % 10000}")
    except Exception as e:
        logging.error(f"Error in about command: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")

# Stats command handler (admin only)
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        # Simple admin check (you should replace this with your actual admin IDs)
        # This is just a placeholder - replace ADMIN_ID with your actual Telegram ID
        ADMIN_ID = 123456789  # Replace with your actual admin ID
        
        if user.id != ADMIN_ID:
            await update.message.reply_text("Sorry, this command is only available to administrators.")
            return
            
        # Calculate statistics
        total_users = len(user_tracker.user_data)
        clicked_users = sum(1 for data in user_tracker.user_data.values() if data['clicked'])
        follow_up_sent = sum(1 for data in user_tracker.user_data.values() if data['follow_up_sent'])
        
        if total_users > 0:
            click_rate = (clicked_users / total_users) * 100
        else:
            click_rate = 0
        
        # Send statistics
        stats_msg = (
            f"📊 *Bot Statistics* 📊\n\n"
            f"Total users: {total_users}\n"
            f"Users who clicked: {clicked_users} ({click_rate:.1f}%)\n"
            f"Follow-ups sent: {follow_up_sent}\n\n"
            f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        await update.message.reply_text(stats_msg, parse_mode='Markdown')
        
    except Exception as e:
        logging.error(f"Error in stats command: {e}")
        await update.message.reply_text("An error occurred retrieving statistics.")

# Handle text messages from users
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        user_id_hash = hash(str(user.id)) % 10000
        message_text = update.message.text
        chat_id = update.effective_chat.id
        bot = context.bot
        
        logging.info(f"Received message from user_hash:{user_id_hash}: '{message_text[:20]}...' if len(message_text) > 20 else message_text")
        
        # Show typing indicator
        await fake_typing(bot, chat_id, 2)
        
        # Respond with suggestion to use commands
        await update.message.reply_text(
            f"👋 Hi there! I'm a bot that helps you connect with people nearby.\n\n"
            f"To get started, try one of these commands:\n"
            f"• /start - See profiles near you\n"
            f"• /help - Get help using this bot\n"
            f"• /about - Learn more about this bot"
        )
    except Exception as e:
        logging.error(f"Error handling message: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")

# Send follow-up to re-engage users who didn't click
async def send_follow_up(user_id):
    """
    Send a follow-up message to users who started the bot but didn't click on any profile
    
    Args:
        user_id: The Telegram user ID to send the follow-up to
    """
    try:
        # Create a new bot instance for sending messages
        bot = ApplicationBuilder().token(BOT_TOKEN).build().bot
        
        # Choose a random girl who will be shown as newly online
        new_online_girl = random.choice(FAKE_PROFILES)
        
        # Simulate typing
        await fake_typing(bot, user_id, 2)
        
        # Send notification about a new match
        await bot.send_message(
            chat_id=user_id,
            text=f"🔥 *New Alert!* 🔥\n\n{EMOJI_WOMAN} *{new_online_girl['name']}* just came online and is looking to chat near you!"
        )
        
        # Pause
        await asyncio.sleep(1.5)
        
        # Create button for the newly online girl
        keyboard = [[InlineKeyboardButton(f"{EMOJI_FIRE} Chat with {new_online_girl['name']}", callback_data=f"chat_{new_online_girl['name']}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send the girl's profile with a button
        await bot.send_message(
            chat_id=user_id,
            text=f"{EMOJI_WOMAN} {new_online_girl['name']}, {new_online_girl['age']} • {new_online_girl['distance']} away\n\n"
                f"She's eager to chat with someone right now! Don't miss your chance!",
            reply_markup=reply_markup
        )
        
        # Log the follow-up
        user_id_hash = hash(str(user_id)) % 10000
        logging.info(f"Follow-up sent to user_hash:{user_id_hash}")
        
    except Exception as e:
        user_id_hash = hash(str(user_id)) % 10000
        logging.error(f"Error sending follow-up to user_hash:{user_id_hash}: {e}")

# === Main Entry Point ===
if __name__ == '__main__':
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN environment variable not set. Please set it in your .env file.")
        sys.exit(1)
    
    try:
        print("Starting bot with emoji support...")
        app = ApplicationBuilder().token(BOT_TOKEN).build()
          # Register command handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("about", about_command))
        app.add_handler(CommandHandler("stats", stats_command))
        app.add_handler(CommandHandler("stats", stats_command))
        
        # Register callback query handler
        app.add_handler(CallbackQueryHandler(button_handler))
        
        # Register message handler (must be last)
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        print("Bot is running...")
        app.run_polling()
    except Exception as e:
        logging.critical(f"Critical error: {e}")
        print(f"Critical error: {e}")
