# Thought-to-Mail Telegram Bot

A Telegram bot that captures thoughts from images, corrects grammar, and emails them to you.

## Features

- 📸 Accepts image input from Telegram
- 🔍 Extracts text using OCR (Tesseract)
- ✍️ Corrects grammar using OpenAI GPT
- 📧 Emails the polished thought to your inbox

## Prerequisites

- Python 3.8 or higher
- Tesseract OCR installed on your system
- Telegram Bot Token (from BotFather)
- OpenAI API Key
- Gmail account with App Password

## Installation

1. Clone this repository:

```bash
git clone <repository-url>
cd thought_mail_bot
```

2. Install Tesseract OCR:

- On macOS:

```bash
brew install tesseract
```

- On Ubuntu:

```bash
sudo apt-get install tesseract-ocr
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file:

```bash
cp .env.example .env
```

5. Edit the `.env` file with your credentials:

- Get a Telegram Bot Token from [@BotFather](https://t.me/botfather)
- Get your Telegram User ID from [@userinfobot](https://t.me/userinfobot)
- Get an OpenAI API Key from [OpenAI Platform](https://platform.openai.com)
- For Gmail, create an App Password:
  1. Enable 2-Step Verification
  2. Go to Security → App Passwords
  3. Generate a new app password for "Mail"

## Usage

1. Start the bot:

```bash
python bot.py
```

2. Open your Telegram bot and send `/start`

3. Send an image containing text to the bot

4. The bot will:
   - Extract text using OCR
   - Correct grammar
   - Email the result to your configured email address

## Security Notes

- The bot only responds to authorized users
- Sensitive data is stored in environment variables
- Temporary files are automatically cleaned up
- Gmail App Password is used instead of regular password

## Error Handling

The bot includes comprehensive error handling for:

- Invalid images
- OCR failures
- Grammar correction issues
- Email sending problems

## Contributing

Feel free to submit issues and enhancement requests!
