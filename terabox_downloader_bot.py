import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
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

# Define the handler for the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to Terabox Video Converter Bot! Send me a Terabox link and I will convert it to a video file for you.')

# Define the handler for regular messages
def convert_to_video(update: Update, context: CallbackContext) -> None:
    file_url = update.message.text
    download_url = f"{TERABOX_API_URL}/download?link={file_url}"
    headers = {'Authorization': f'Bearer {TERABOX_API_KEY}'}
    response = requests.get(download_url, headers=headers, stream=True)
    if response.status_code == 200:
        filename = os.path.basename(file_url)
        # Here you can add your logic to convert the downloaded file to video format
        # For simplicity, let's assume we are just renaming the file with .mp4 extension
        video_filename = f"{filename}.mp4"
        os.rename(filename, video_filename)
        context.bot.send_video(chat_id=update.effective_chat.id, video=open(video_filename, 'rb'))
        os.remove(video_filename)  # Remove the video file after uploading
    else:
        update.message.reply_text("Sorry, I couldn't convert the file. Please make sure the link is correct.")

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Register handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, convert_to_video))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
