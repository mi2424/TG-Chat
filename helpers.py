#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import os
import random
import logging
from telegram.constants import ChatAction

# === Helper Functions ===

# Add fake availability logic (randomly select 1 online)
def assign_status(profiles, emoji_online, emoji_busy, emoji_offline):
    """
    Assigns online/offline status to profiles with appropriate emojis.
    
    Args:
        profiles: List of profile dictionaries
        emoji_online, emoji_busy, emoji_offline: Status emojis
    """
    online_girl = random.choice(profiles)
    for girl in profiles:
        girl["online"] = (girl == online_girl)
        girl["status"] = f"{emoji_online} Online" if girl["online"] else random.choice(
            [f"{emoji_busy} Busy", f"{emoji_offline} Offline"]
        )

# Simulate typing with more realistic timing
async def fake_typing(bot, chat_id, duration=2, message_length=None):
    """
    Simulate human typing with more realistic timing.
    
    Args:
        bot: The bot instance
        chat_id: The chat ID to send typing action to
        duration: Minimum duration for typing
        message_length: If provided, calculate typing time based on message length
    """
    try:
        # If message length is provided, calculate a more realistic typing time
        if message_length:
            # Average human types 40-60 WPM, we'll use 40 WPM = ~200 chars per minute
            # = ~3.33 chars per second, plus some randomness
            typing_speed = 3.33  # chars per second
            calculated_duration = (message_length / typing_speed) * (0.8 + 0.4 * random.random())
            
            # Ensure minimum and maximum reasonable times
            duration = max(duration, min(calculated_duration, 8))
            
        # Add small random variation to make it more human-like
        human_duration = duration * (0.9 + 0.3 * random.random())
        
        # Send typing indicator in chunks to keep it active for the whole duration
        chunks = max(1, int(human_duration / 4))  # Telegram typing indicator lasts ~5 seconds
        chunk_duration = human_duration / chunks
        
        for _ in range(chunks):
            await bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
            await asyncio.sleep(chunk_duration)
            
    except Exception as e:
        logging.error(f"Error during fake_typing: {e}")

# Function to check if a file exists and handle errors gracefully
def verify_resource_exists(filepath, error_message=None):
    """
    Verifies if a resource file exists
    
    Args:
        filepath: Path to the file to check
        error_message: Custom error message
        
    Returns:
        bool: True if file exists, False otherwise
    """
    if not os.path.exists(filepath):
        if error_message:
            logging.error(error_message)
        else:
            logging.error(f"Resource not found: {filepath}")
        return False
    return True
