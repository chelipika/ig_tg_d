# 🚀 ReelyFastBot


<p align="center">
  <img src="https://img.shields.io/github/license/chelipika/ig_tg_d" alt="License">
  <img src="https://img.shields.io/github/stars/chelipika/ig_tg_d" alt="Stars">
  <img src="https://img.shields.io/github/forks/chelipika/ig_tg_d" alt="Forks">
  <img src="https://img.shields.io/github/issues/chelipika/ig_tg_d" alt="Issues">
</p>

**ReelyFastBot** is a powerful Telegram bot that allows users to easily download content from Instagram, including Reels, Videos, Photos, and Carousels.

<p align="center">
  <img src="https://raw.githubusercontent.com/chelipika/ig_tg_d/main/assets/demo.gif" alt="Demo GIF" width="600">
</p>

## ✨ Features

- ⚡ **Lightning Fast Downloads**: Get your Instagram content in seconds
- 🎬 **Multiple Format Support**: Download Reels, Videos, Photos, and Carousels
- 📱 **User-Friendly Interface**: Simple paste-and-go functionality
- 🔄 **Channel Subscription System**: Optional channel subscription requirement
- 📊 **User Tracking**: Basic database integration for user management
- 🎁 **Fun Facts**: Displays random Instagram facts during download
- 👥 **Group Support**: Can be added to Telegram groups

## 🎮 Demo

Add [@ReelyFastBot](https://t.me/ReelyFastBot) on Telegram and start downloading your favorite Instagram content instantly!

<p align="center">
  <img src="https://github.com/chelipika/ig_tg_d/blob/master/assets/carousel.jpg" alt="Usage Example" width="300">
</p>
<p align="center">
  <img src="https://github.com/chelipika/ig_tg_d/blob/master/assets/demo.gif" alt="Usage Example gif" width="300">
</p>

## 🔧 Installation

### Prerequisites

- Python 3.8+
- Telegram Bot Token (from [BotFather](https://t.me/BotFather))
- Instagram credentials
- Database setup (see configuration)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/chelipika/ig_tg_d.git
   cd ig_tg_d
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `config.py` file (see [Configuration](#configuration) section)

4. Run the bot:
   ```bash
   python main.py
   ```

## 📝 Configuration

Create a `config.py` file in the project root with the following variables:

```python
# Instagram credentials
USERNAME = "your_instagram_username"
PASSWORD = "your_instagram_password"

# Telegram settings
TOKEN = "your_telegram_bot_token"
CHANNEL_ID = "@your_channel_id"  # Channel users need to subscribe to
CHANNEL_LINK = "https://t.me/your_channel"  # Public link to your channel
```

## 📚 Project Structure

```
ig_tg_d/
├── config.py                 # Configuration variables
├── main.py                   # Bot initialization and startup
├── database/
│   └── requests.py           # Database operations
├── reely/
│   └── keyboards.py          # Telegram inline keyboards
└── requirements.txt          # Python dependencies
```

## 🚀 Usage

Once the bot is running, users can:

1. Start the bot with `/start`
2. Subscribe to the required channel (if enabled)
3. Send any Instagram post/reel URL
4. Receive the downloaded content directly in the chat

### For Developers

The bot uses the following key components:

- **aiogram**: Handling Telegram interactions
- **instaloader**: Processing Instagram content
- **asyncio**: Handling asynchronous operations

## 🙌 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [aiogram](https://github.com/aiogram/aiogram) - Telegram Bot framework
- [instaloader](https://github.com/instaloader/instaloader) - Instagram scraping library
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/chelipika">chelipika</a>
</p>
