#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration settings for the TelegramChatBot
"""

# Bot Settings
DEFAULT_LANDING_PAGE_URL = "https://your-prelander-page.com"
DEFAULT_LOG_FILE = "bot.log"

# Emojis
EMOJI_ONLINE = "✅"
EMOJI_BUSY = "❌"
EMOJI_OFFLINE = "⚫"
EMOJI_FIRE = "🔥"
EMOJI_WOMAN = "👩"
EMOJI_PIN = "📍"
EMOJI_HEART = "❤️"
EMOJI_SMILE = "😊"
EMOJI_WINK = "😉"

# Profiles data - moved here from main file
FAKE_PROFILES = [
    {"name": "Sofia", "age": 24, "distance": "2.1km", "photo": "sofia.jpg"},
    {"name": "Emily", "age": 22, "distance": "3.4km", "photo": "emily.jpg"},
    {"name": "Mia", "age": 25, "distance": "1.9km", "photo": "mia.jpg"},
    {"name": "Chloe", "age": 23, "distance": "2.7km", "photo": "chloe.jpg"},
    {"name": "Ava", "age": 26, "distance": "3.0km", "photo": "ava.jpg"},
]

# Timing constants
MIN_TYPING_DURATION = 1.5
MAX_TYPING_DURATION = 8.0 
MIN_PAUSE_DURATION = 1.0
MAX_PAUSE_DURATION = 5.0

# Re-engagement settings
FOLLOW_UP_MINUTES = 30   # Time to wait before sending a follow-up
MAX_FOLLOW_UPS = 2       # Maximum number of follow-ups to send
