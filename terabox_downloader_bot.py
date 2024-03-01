import requests
from telegram.ext import Updater, CommandHandler

API_KEY = '0795d6076bmshccea2334ece5a30p1b4e9djsn654ea7e07eb7'
TOKEN = '5851945481:AAHejMpNRJFtc1ZtQmkcVZzZUCzw2lYz2Ms'

def download_video(update, context):
    video_url = context.args[0]
    url = f"https://api.terabox.com/download?video_url={video_url}&api_key={API_KEY}"

    response = requests.get(url)

    if response.status_code == 200:
        with open("downloaded_video.mp4", "wb") as file:
            file.write(response.content)
        update.message.reply_text("Video downloaded successfully!")
    else:
        update.message.reply_text("Failed to download video. Please check the URL and API key.")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("download", download_video))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

if __name__ == '__main__':
    main()
