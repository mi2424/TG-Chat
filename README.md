# Telegram Chat Bot

A Telegram bot that simulates connecting with nearby profiles. This bot is built for educational purposes and demonstration of Telegram bot development techniques.

## Features

- Simulated profiles with online/offline status
- Realistic typing indicators and message timing
- Interactive buttons and chat simulation
- Command handlers for common actions
- Rate limiting to prevent abuse
- Error handling and logging
- User engagement tracking and automated follow-ups
- Click-through analytics and statistics

## Setup

### Prerequisites

- Python 3.7 or higher
- Telegram Bot Token (get from [@BotFather](https://t.me/botfather))
- Required packages: `python-telegram-bot`, `python-dotenv`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tg-chatbot.git
   cd tg-chatbot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your bot token:
   ```
   BOT_TOKEN=your_bot_token_here
   LANDING_PAGE_URL=https://your-landing-page.com
   LOG_FILE=bot.log
   ```

4. Create a `profiles` directory and add profile images:
   ```bash
   mkdir profiles
   # Add images: sofia.jpg, emily.jpg, mia.jpg, chloe.jpg, ava.jpg
   ```

5. Run the bot:
   ```bash
   python bot.py
   ```

## Usage

- `/start` - Start the bot and see profiles
- `/help` - Get help using the bot
- `/about` - Learn more about the bot
- `/stats` - View engagement statistics (admin only)

## Project Structure

- `bot.py` - Main bot code
- `helpers.py` - Helper functions
- `config.py` - Configuration settings
- `rate_limiter.py` - Rate limiting implementation
- `profiles/` - Directory containing profile images

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This bot simulates interactions with fake profiles for demonstration purposes only. All profiles are fictional. Do not use this bot for deceptive practices.
