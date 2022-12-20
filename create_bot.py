import telebot
from loguru import logger
import sqlite3
from telebot.storage import StateMemoryStorage
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup  # States
import os
from dotenv import load_dotenv, find_dotenv


state_storage = StateMemoryStorage()
# Бот и его ключ, бд
load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'), state_storage=state_storage)
yandex_token = os.getenv('YADISK_TOKEN')
logger.add('bot.log', format="{time} {level} {message}", level="DEBUG", rotation="1 MB")
db = sqlite3.connect('bot_db.db', check_same_thread=False)
cursor = db.cursor()
admins = [users[0] for users in cursor.execute("SELECT user_id FROM admins")]


class ScheduleStates(StatesGroup):
    menu = State()
    full_list_changes = State()
    week_in_a_row = State()
    day_of_the_week = State()
    group_select = State()
    raspisanie = State()


class Exams_Schedule(StatesGroup):
    exams_cource_searcher = State()
    exams_date_searcher = State()
    exams_file_sender = State()


class Feedback(StatesGroup):
    feedback = State()
    send_message_to_user = State()
    sending_message_to_user = State()


class Contacts(StatesGroup):
    find_contact = State()


bot.add_custom_filter(custom_filters.StateFilter(bot))
