import sys
from pytube import YouTube
import os
import webbrowser
from pytube.exceptions import VideoUnavailable, RegexMatchError
from telegram.ext import *

API_KEY = 'ENTER KEY HERE'
words_list = ['youtube', 'youtu', 'yt']


def get_file_name(input_link):
    yt = YouTube(input_link)
    file_name = yt.title
    return file_name


def youtube_download(input_link, update, context):  # separate this function to download, video details and print
    if any(word in input_link for word in words_list):
        yt = YouTube(input_link)

        audio = yt.streams.get_audio_only()
        download_name = audio.default_filename.replace("mp4", "mp3")

        if os.path.exists(download_name):
            already_exist(update, context)

        out_file = audio.download(output_path="")
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'

        update.message.reply_text(f"Downloading now {get_file_name(input_link)}")
        os.rename(out_file, new_file)
        update.message.reply_text(f"Download {get_file_name(input_link)} finished!")
        update.message.reply_text(yt.thumbnail_url)
        update.message.reply_text("--------------------------------------------\n"
                                  "--------------------------------------------\n"
                                  "--------------------------------------------\n"
                                  "--------------------------------------------\n"
                                  "--------------------------------------------\n"
                                  "Past any link to start a new download!\n"
                                  "--------------------------------------------\n"
                                  "--------------------------------------------\n"
                                  "--------------------------------------------\n"
                                  "--------------------------------------------\n"
                                  "--------------------------------------------\n")
        webbrowser.open(get_file_name(input_link) + '.mp3')
        update.message.reply_text(os.getcwd() + get_file_name(input_link) + '.mp3')
        # add telegram link to the path of the file


def already_exist(update, context):
    update.message.reply_text("File already exist!!\n"
                              "Please run the program again")
    os.execl(sys.executable, sys.executable, *sys.argv)


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
