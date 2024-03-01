import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import os

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the token for your bot
TOKEN = "5851945481:AAHejMpNRJFtc1ZtQmkcVZzZUCzw2lYz2Ms"

# Define the base URL for Terabox downloader API
TERABOX_API_URL = "https://api.terabox.me"

# Define the handler for the /start command
def start(update: Update, context: CallbackContext) -> None:
    if update.effective_chat.type == "private":
        update.message.reply_text('Welcome to Terabox Downloader Bot! Send me a link to a file and I will download it for you.')
    else:
        context.bot.send_message(update.effective_chat.id, text='Welcome to Terabox Downloader Bot! Send me a link to a file and I will download it for you.')

# Define the handler for regular messages
def download_file(update: Update, context: CallbackContext) -> None:
    file_url = update.message.text
    download_url = f"{TERABOX_API_URL}/download?link={file_url}"
    response = requests.get(download_url, stream=True)
    if response.status_code == 200:
        filename = os.path.basename(file_url)
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        update.message.reply_text(f"File downloaded successfully! You can find it as {filename}.")
    else:
        update.message.reply_text("Sorry, I couldn't download the file. Please make sure the link is correct.")

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Register handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_file))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
