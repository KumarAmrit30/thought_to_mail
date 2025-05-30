import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from ocr_utils import extract_text_from_image
from grammar_utils import correct_grammar
from email_utils import send_email, format_thought_email

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
ALLOWED_USERS = [int(os.getenv('AUTHORIZED_USER_ID'))]  # List of authorized user IDs
TARGET_EMAIL = os.getenv('TARGET_EMAIL')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("Sorry, you are not authorized to use this bot.")
        return
    
    await update.message.reply_text(
        "Welcome to Thought-to-Mail Bot! 📝\n\n"
        "Send me an image containing text, and I'll:\n"
        "1. Extract the text using OCR\n"
        "2. Correct any grammar issues\n"
        "3. Email the polished thought to you\n\n"
        "Just send an image to get started!"
    )

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming images."""
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("Sorry, you are not authorized to use this bot.")
        return

    # Get the photo file
    photo = update.message.photo[-1]  # Get the largest photo
    file = await context.bot.get_file(photo.file_id)
    
    # Create a temporary directory if it doesn't exist
    os.makedirs('temp', exist_ok=True)
    
    # Download the photo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"temp/image_{timestamp}.jpg"
    await file.download_to_drive(file_path)
    
    await update.message.reply_text("Processing your image... Please wait.")
    
    try:
        # Extract text using OCR
        original_text = extract_text_from_image(file_path)
        if not original_text.strip():
            raise ValueError("No text could be extracted from the image. Please ensure the image contains clear, readable text.")
            
        await update.message.reply_text("Text extracted successfully! Now correcting grammar...")
        
        # Correct grammar
        try:
            corrected_text = await correct_grammar(original_text)
        except Exception as e:
            await update.message.reply_text(f"Error in grammar correction: {str(e)}")
            return
            
        await update.message.reply_text("Grammar correction complete! Sending email...")
        
        # Format and send email
        try:
            subject, body = format_thought_email(original_text, corrected_text)
            send_email(subject, body, TARGET_EMAIL)
        except Exception as e:
            await update.message.reply_text(f"Error sending email: {str(e)}")
            return
        
        await update.message.reply_text("Your thought has been processed and emailed to you!")
        
    except ValueError as e:
        logger.error(f"Value Error: {str(e)}")
        await update.message.reply_text(str(e))
    except Exception as e:
        logger.error(f"Unexpected error processing image: {str(e)}")
        await update.message.reply_text("Sorry, there was an unexpected error processing your image. Please try again.")
    finally:
        # Clean up temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))

    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 