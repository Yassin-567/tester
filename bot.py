import logging
import os
from telegram import Update, Video
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from moviepy.editor import VideoFileClip

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the function to handle /start command
def start(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! Send me a video, and I'll compress it for you.")

# Define the function to handle video messages
def handle_video(update: Update, context):
    video = update.message.video

    if isinstance(video, Video):
        # Get the file path of the video on Telegram's servers
        file_path = context.bot.get_file(video.file_id).file_path

        # Perform video compression using MoviePy
        clip = VideoFileClip(file_path)

        # Adjust the compression settings
        compressed_file = "compressed_video.mp4"
        codec = 'libx265'  # Change the codec to 'libvpx-vp9' for VP9 compression
        bitrate = '250k'  # Adjust the bitrate as desired (e.g., '1M' for 1 Mbps)

        # Compress the video with the specified codec and bitrate
        clip.write_videofile(compressed_file, codec=codec, bitrate=bitrate)

        # Send the compressed video
        context.bot.send_video(chat_id=update.effective_chat.id, video=open(compressed_file, 'rb'))

        # Clean up the temporary files
        clip.close()
        os.remove(compressed_file)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please send a video file.")

# Set up the Telegram bot
def create_app():
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    bot_token = '5909482823:AAHEtxgzV9LJ0bhXzwYldhqqliRw0iufJIA'

    # Initialize the bot
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    # Add command handlers
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # Add message handlers
    video_handler = MessageHandler(Filters.video, handle_video)
    dispatcher.add_handler(video_handler)

    # Start the bot
    updater.start_polling()
    logger.info("Bot started!")

    return updater

app = create_app()

if __name__ == '__main__':
    import os
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=PORT)
