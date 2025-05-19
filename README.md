# Telegram Chat Bot

A Telegram bot that simulates connecting with nearby profiles. This bot creates an interactive dating-style interface with simulated profiles that appear to be online and in a user's vicinity. Built with Python and the python-telegram-bot library, it demonstrates modern bot development techniques and engagement strategies.

## Features

- **Interactive User Experience**
  - Simulated profiles with dynamic online/offline status
  - Realistic typing indicators and message timing
  - Human-like interaction patterns with random pauses
  - Responsive button interfaces for profile selection

- **Engagement Optimization**
  - User engagement tracking and analytics
  - Automated follow-ups for inactive users
  - Smart re-engagement with new profile suggestions
  - Click-through rate monitoring and statistics

- **Technical Features**
  - Asynchronous design with python-telegram-bot
  - Environment-based configuration
  - Rate limiting to prevent abuse
  - Comprehensive error handling and logging
  - Modular code organization

## Setup

### Prerequisites

- Python 3.7 or higher
- Telegram Bot Token (get from [@BotFather](https://t.me/botfather))
- Required packages: `python-telegram-bot`, `python-dotenv`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mi2424/tg-chatbot.git
   cd tg-chatbot
   ```

2. Set up a virtual environment (recommended):
   ```bash
   # For Windows
   python -m venv venv
   .\venv\Scripts\activate

   # For Linux/Mac
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your configuration:
   ```
   BOT_TOKEN=your_bot_token_here
   LANDING_PAGE_URL=https://your-landing-page.com
   LOG_FILE=bot.log
   ```

5. Update admin ID in the stats command:
   Edit `bot.py` and replace `ADMIN_ID = 123456789` with your actual Telegram user ID (you can get this from @userinfobot)

6. Ensure profile images are in place:
   The `profiles` directory should contain the following images:
   - sofia.jpg
   - emily.jpg
   - mia.jpg
   - chloe.jpg
   - ava.jpg

7. Run the bot:
   ```bash
   python bot.py
   ```

## Usage

### User Commands
- `/start` - Initiates the bot and displays nearby profiles
- `/help` - Shows available commands and basic instructions
- `/about` - Provides information about the bot and its purpose

### Admin Commands
- `/stats` - Displays engagement metrics and click-through statistics (admin access only)

### User Flow
1. User sends `/start` command
2. Bot "scans the area" (simulated delay)
3. Bot presents a list of nearby profiles with online/offline status
4. User can click on an online profile to initiate a chat
5. Bot simulates a conversation with the chosen profile
6. User is ultimately directed to an external landing page
7. If user doesn't click any profile, a follow-up message is sent after 30 minutes

## Project Structure

```
.
├── bot.py                # Main bot application entry point
├── config.py             # Configuration settings and constants
├── helpers.py            # Helper functions for common operations
├── rate_limiter.py       # Rate limiting implementation to prevent abuse
├── user_tracker.py       # User engagement tracking and re-engagement
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── profiles/             # Directory containing profile images
    ├── sofia.jpg
    ├── emily.jpg
    ├── mia.jpg
    ├── chloe.jpg
    └── ava.jpg
```

## Configuration

Key configuration options are stored in `config.py`:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `DEFAULT_LANDING_PAGE_URL` | URL where users will be directed to | "https://your-prelander-page.com" |
| `DEFAULT_LOG_FILE` | Path to log file | "bot.log" |
| `FOLLOW_UP_MINUTES` | Minutes to wait before sending re-engagement message | 30 |
| `MAX_FOLLOW_UPS` | Maximum number of follow-ups per user | 2 |

### Rate Limiting

The bot implements rate limiting to prevent abuse:
- Default: 5 requests per 60 seconds per user
- Customize in `bot.py` by modifying `RateLimiter` parameters

### Re-engagement Configuration

User tracking and re-engagement settings can be adjusted in `user_tracker.py`:
- Follow-up timing (`FOLLOW_UP_MINUTES` in config.py)
- Follow-up message content (in the `send_follow_up` function)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This bot simulates interactions with fake profiles for educational and demonstration purposes only. All profiles are fictional and no actual matching or dating services are provided. This tool is intended as a demonstration of Telegram bot development techniques including:

- Asynchronous programming with Python
- Telegram Bot API integration
- User engagement tracking and analytics
- Re-engagement strategies
- Rate limiting implementation

**Important**: Do not use this bot for deceptive practices, scams, or any activity that violates Telegram's Terms of Service.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Built with [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- Inspired by modern chatbot engagement patterns
