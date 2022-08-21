import messages
from pytube import YouTube
import os
from pytube.exceptions import VideoUnavailable, RegexMatchError
from telegram.ext import *

API_KEY = 'ENTER KEY HERE'
words_list = ['youtube', 'youtu', 'yt']


def youtube_download(input_link, update, context):
    if any(word in input_link for word in words_list):
        file_format = input_link[-3:]
        input_link = input_link[:-3]
        yt = YouTube(input_link)
        if file_format == 'vid':
            video = yt.streams.get_highest_resolution()
            file_format = '.mp4'
            download_name = video.default_filename
            check_dup(download_name, update, context)
            out_file = video.download(output_path="")
            messages.print_message(input_link, update, context, file_format)

        else:
            audio = yt.streams.get_audio_only()
            file_format = '.mp3'
            download_name = audio.default_filename
            check_dup(download_name,update,context)
            download_name = audio.default_filename.replace("mp4", "mp3")
            out_file = audio.download(output_path="")
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'

            os.rename(out_file, new_file)
            messages.print_message(input_link, update, context, file_format)


        # add telegram link to the path of the file

def check_dup(download_name, update,context):
    if os.path.exists(download_name):
        messages.already_exist(update, context)
    if os.path.exists(download_name+'.mp4'):
        messages.already_exist(update, context)
def youtube_error(update, context):
    update.message.reply_text("Please use only youtube video links!")


def reply(update, context):
    input_link = update.message.text
    try:
        youtube_download(input_link, update, context)
    except VideoUnavailable:
        youtube_error(update, context)
        # Add here exception for unavailable video
    except RegexMatchError:
        youtube_error(update, context)
    # add exception handler file
    # add message and reply file


def main():
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, reply))
    updater.start_polling()
    updater.idle()


main()
