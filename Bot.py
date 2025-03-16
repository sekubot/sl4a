import os
import time
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Set environment variables if they are not already set
if "BOT_TOKEN" not in os.environ:
    os.environ["BOT_TOKEN"] = "8190832955:AAFP4RY6TxzI8u-KpnveCvYt2zIS5AhbNmY"  # Replace with your bot token
if "OWNER_USER_ID" not in os.environ:
    os.environ["OWNER_USER_ID"] = "7403487121"  # Replace with your numeric user ID

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_USER_ID = os.getenv("OWNER_USER_ID")

# Validate environment variables
if not BOT_TOKEN or not OWNER_USER_ID:
    raise ValueError("Please set the BOT_TOKEN and OWNER_USER_ID environment variables.")

# Convert OWNER_USER_ID to integer
try:
    OWNER_USER_ID = int(OWNER_USER_ID)
except ValueError:
    raise ValueError("OWNER_USER_ID must be a numeric value.")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me any message, and I'll forward it to the owner.")

# Handler to forward all messages to the owner
async def forward_to_owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.message.from_user
        logger.info(f"Received message from user: {user.username} (ID: {user.id})")

        # Forward the message to the owner
        await context.bot.forward_message(
            chat_id=OWNER_USER_ID,  # Use the owner's user ID
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )
        logger.info("Message forwarded successfully!")
    except Exception as e:
        logger.error(f"Error forwarding message: {e}")

# Main function to set up the bot
def main():
    while True:
        try:
            # Create the Application
            application = Application.builder().token(BOT_TOKEN).build()

            # Add handlers
            application.add_handler(CommandHandler("start", start))  # Handle /start command
            application.add_handler(MessageHandler(filters.ALL, forward_to_owner))  # Handle ALL message types

            # Start the bot
            logger.info("Bot is running...")
            application.run_polling()
        except Exception as e:
            logger.error(f"Bot crashed due to: {e}, restarting in 5 seconds...")
            time.sleep(5)  # Wait before restarting

if __name__ == "__main__":
    main()
