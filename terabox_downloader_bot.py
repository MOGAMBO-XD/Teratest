import logging
import os
import requests
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram bot token
TELEGRAM_TOKEN = "5851945481:AAHejMpNRJFtc1ZtQmkcVZzZUCzw2lYz2Ms"

# Terabox API key
TERABOX_API_KEY = "0795d6076bmshccea2334ece5a30p1b4e9djsn654ea7e07eb7"

# Terabox base URL
TERABOX_BASE_URL = "https://api.terabox.me"

# Function to handle /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to Terabox Uploader and Downloader Bot!')

# Function to download files from Terabox
def download_file(update: Update, context: CallbackContext) -> None:
    file_url = update.message.text
    headers = {'Authorization': f'Bearer {TERABOX_API_KEY}'}
    response = requests.get(f"{TERABOX_BASE_URL}/download?link={file_url}", headers=headers, stream=True)
    if response.status_code == 200:
        filename = os.path.basename(file_url)
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        update.message.reply_text(f"File downloaded successfully! You can find it as {filename}.")
    else:
        update.message.reply_text("Sorry, failed to download the file from Terabox.")

# Function to upload files to Telegram
# Function to upload files to Telegram
def upload_file(update: Update, context: CallbackContext) -> None:
    file_id = update.message.document.file_id
    new_file = context.bot.get_file(file_id)
    file_path = new_file.download()
    context.bot.send_document(chat_id=update.effective_chat.id, document=open(file_path, 'rb'))
    os.remove(file_path)

  

def main() -> None:
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'^https?:\/\/.*'), download_file))
    dispatcher.add_handler(MessageHandler(Filters.document.url, upload_file))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
