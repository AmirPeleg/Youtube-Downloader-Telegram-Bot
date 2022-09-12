import sys

from pytube import YouTube
import os


def already_exist(update, context):
    update.message.reply_text("File already exist!!\n"
                              "Please try another link")
    os.execl(sys.executable, sys.executable, *sys.argv)


def get_file_name(input_link):
    yt = YouTube(input_link)
    file_name = yt.title
    return file_name


def print_message(input_link, update, context, file_format):
    yt = YouTube(input_link)
    update.message.reply_text(f"Downloading now {get_file_name(input_link)}")
    update.message.reply_text(f"Download {get_file_name(input_link)} finished!")
    update.message.reply_text(yt.thumbnail_url)
    update.message.reply_text(os.getcwd() + get_file_name(input_link) + file_format)
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
