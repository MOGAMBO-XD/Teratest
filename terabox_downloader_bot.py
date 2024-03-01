import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import os

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the token for your bot
TOKEN = "5851945481:AAHejMpNRJFtc1ZtQmkcVZzZUCzw2lYz2Ms"

# Define the API key for Terabox
TERABOX_API_KEY = "0795d6076bmshccea2334ece5a30p1b4e9djsn654ea7e07eb7"

# Define the base URL for Terabox downloader API
TERABOX_API_URL = "https://api.terabox.me"

# Define the /start command handler
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to Terabox Downloader Bot! Send me a link to a file and I will download it for you.")

# Define the function to handle file downloads
def download_file(update, context):
    file_url = update.message.text
    download_url = f"{TERABOX_API_URL}/download?link={file_url}"
    headers = {'Authorization': f'Bearer {TERABOX_API_KEY}'}
    response = requests.get(download_url, headers=headers, stream=True)
    if response.status_code == 200:
        filename = os.path.basename(file_url)
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        update.message.reply_text(f"File downloaded successfully! You can find it as {filename}.")
    else:
        update.message.reply_text("Sorry, I couldn't download the file. Please make sure the link is correct.")

def main():
    # Create the Updater and pass it your bot's token
    updater = Updater(token=TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))

    # Register a handler for regular messages
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_file))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
