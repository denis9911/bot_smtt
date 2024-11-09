import sqlite3
import time

from apscheduler.schedulers.background import BackgroundScheduler
from telebot import types
from bs4 import BeautifulSoup
import requests
from datetime import datetime as dt
from loguru import logger
from create_bot import bot, cursor, db, admins, Feedback, yandex_token
import yadisk

send_rss = True


def admin_notification():
    dtnow = dt.now().strftime('%d-%m-%Y, %H:%M:%S')
    bot.send_message(765860654, text='Бот был перезапущен ' + dtnow)
    logger.info('Бот был перезапущен ' + dtnow)


admin_notification()


# @bot.message_handler(commands=['admin'])
def admin_menu(message):
    if message.chat.id in admins:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        item1 = types.KeyboardButton("/send_message")
        item2 = types.KeyboardButton("/send_rss")
        item3 = types.KeyboardButton("/send_log")
        item4 = types.KeyboardButton("/send_feedback")
        item5 = types.KeyboardButton("/reg_send_message_to_user")
        item6 = types.KeyboardButton("Вернуться в главное меню")
        markup.add(item1, item2, item3, item4, item5, item6)
        bot.send_message(message.chat.id, "Выбери админ. команду:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Это команда для администратора, Вы - им не являетесь 👀")


# @bot.message_handler(commands=['send_log'])
def sending_log(message):
    if message.chat.id in admins:
        bot.send_document(message.chat.id, document=open(r'bot.log', 'rb'))


# Рассылка пользователям
# @bot.message_handler(commands=['send_message'])
def sending_command(message):
    if message.chat.id in admins:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Вернуться в главное меню")
        markup.add(item1)
        bot.send_message(message.chat.id, "Что отправить всем пользователям бота?", reply_markup=markup)
        bot.register_next_step_handler(message, sending_message)
    else:
        bot.send_message(message.chat.id, "Это команда для администратора, Вы - им не являетесь 👀")


def sending_message(message):
    if message.text == "Вернуться в главное меню":
        bot.send_message(message.chat.id, 'Задание отменено, нажмите кнопку ещё раз')
    else:
        bot.send_message(message.chat.id, 'Начал отправку сообщения')
        cursor.execute("SELECT user_id FROM users")
        for users in cursor.fetchall():
            try:
                bot.copy_message(message_id=message.id, from_chat_id=message.chat.id, *users)
                time.sleep(0.25)
            except:
                logger.info(f'Не смог отправить {users[0]}')
                time.sleep(0.25)
        bot.send_message(message.chat.id, 'Сообщение доставлено всем пользователям')
        logger.info(f'Пользователь {message.chat.id} отправил подписчикам {message.text}')


# @bot.message_handler(commands=['send_message_to_user'])
def reg_send_message_to_user(message):
    if message.chat.id in admins:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Вернуться в главное меню")
        markup.add(item1)
        bot.send_message(message.chat.id, "Напишите id пользователя", reply_markup=markup)
        bot.set_state(message.from_user.id, Feedback.send_message_to_user, message.chat.id)
    else:
        bot.send_message(message.chat.id, "Это команда для администратора, Вы - им не являетесь 👀")


@bot.message_handler(state=Feedback.send_message_to_user)
def send_message_to_user(message):
    if message.text == "Вернуться в главное меню":
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, 'Задание отменено, нажмите кнопку ещё раз')
    else:
        bot.send_message(message.chat.id, text='Напишите сообщение, которое хотите отправить')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['sending_user_id'] = message.text
        bot.set_state(message.from_user.id, Feedback.sending_message_to_user, message.chat.id)


@bot.message_handler(state=Feedback.sending_message_to_user, content_types=types.util.content_type_media)
def sending_message_to_user(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        bot.copy_message(message_id=message.id, from_chat_id=message.chat.id, chat_id=data['sending_user_id'])
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Вернуться в главное меню'))
    for admin in admins:
        bot.send_message(admin, text=f'Сообщение "{message.text}" отправлено пользователю', reply_markup=markup)
    bot.delete_state(message.from_user.id, message.chat.id)


# @bot.message_handler(commands=['send_feedback'])
def send_feedback(message):
    if message.chat.id in admins:
        cursor.execute('SELECT user_id, user_name, message, date, link FROM feedback')
        feedback_message = cursor.fetchall()
        for user_id, user_name, user_message, date, link in feedback_message:
            bot.send_message(message.chat.id, link, parse_mode='html')
    else:
        bot.send_message(message.chat.id, "Это команда для администратора, Вы - им не являетесь 👀")


# Отправка новостей с сайта
# @bot.message_handler(commands=['send_rss'])
def rss_command(message):
    if message.chat.id in admins:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Включить")
        item2 = types.KeyboardButton("Выключить")
        item3 = types.KeyboardButton("Отмена")
        markup.add(item1), markup.add(item2), markup.add(item3)
        bot.send_message(message.chat.id,
                         f"Текущий статус отправки новостей: {send_rss} \n\nВключить или выключить рассылку?",
                         reply_markup=markup)
        bot.register_next_step_handler(message, rss_switch)
    else:
        bot.send_message(message.chat.id, "Это команда для администратора, Вы - им не являетесь 👀")


# Переключаем тумблер на включении и выключении отправки новостей
def rss_switch(message):
    global send_rss
    if message.text == "Включить":
        if send_rss:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Вернуться в главное меню")
            markup.add(item1)
            bot.send_message(message.chat.id, "Рассылка новостей была включена ранее", reply_markup=markup)
        else:
            send_rss = True
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Вернуться в главное меню")
            markup.add(item1)
            bot.send_message(message.chat.id, text='Рассылка новостей успешно включена', reply_markup=markup)
            logger.info(f'Пользователь {message.chat.id} включил рассылку новостей с сайта')
    elif message.text == "Выключить":
        if send_rss:
            send_rss = False
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Вернуться в главное меню")
            markup.add(item1)
            bot.send_message(message.chat.id, text='Рассылка новостей успешно выключена', reply_markup=markup)
            logger.info(f'Пользователь {message.chat.id} выключил рассылку новостей с сайта')
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Вернуться в главное меню")
            markup.add(item1)
            bot.send_message(message.chat.id, "Рассылка новостей была выключена ранее", reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Вернуться в главное меню")
        markup.add(item1)
        bot.send_message(message.chat.id, "Задание отменено, выберите пункт меню:", reply_markup=markup)


def rss_sending():
    if send_rss:
        url = requests.get("http://satehm.ru/news/rss")
        site_content = BeautifulSoup(url.content, 'xml')
        site_items = site_content.find_all('item')
        for item in site_items[:5]:
            site_date = item.pubDate.text[:-5]
            news_name = item.title.text
            news_link = item.link.text
            news_date = dt.strptime(site_date, '%a, %d %B %Y %H:%S:%M')
            news = [news_name, news_date, news_link]
            cursor.execute("SELECT news_name FROM site_news WHERE news_name=?", (news_name,))
            if len(cursor.fetchall()) == 0:
                cursor.execute("INSERT INTO site_news VALUES(?, ?, ?);", news)
                db.commit()
                bot.send_message(765860654, f'Вышла новая новость {news_name}, начинаю отправку пользователям', parse_mode='html')
                logger.info(f'Вышла новая новость, отправляю всем подписчикам: {news_name} - {news_link}')
                cursor.execute("SELECT user_id FROM users")
                success_send = 0
                unsuccess_send = 0
                for user_id in cursor.fetchall():
                    try:
                        bot.send_message(*user_id, text=f'{news_name} \n\n{news_link}', parse_mode='html')
                        logger.info(f'Отправил новость {user_id[0]}')
                        success_send += 1
                        time.sleep(0.25)
                    except:
                        logger.info(f'Не смог отправить {user_id[0]}')
                        unsuccess_send += 1
                        time.sleep(0.25)
                bot.send_message(765860654, f'Новость {news_name} удачно доставлена {success_send} челам и неудачно {unsuccess_send} челам', parse_mode='html')
            else:
                logger.info('Последняя новость:'+news_name)
    else:
        logger.info('Отправка новостей с сайта отключена')


# Получаем филдбек
@bot.message_handler(state=Feedback.feedback)
def feedback(message):
    temp = f"<a href='tg://user?id={message.chat.id}'>Этот пользователь оставил сообщение: {message.text}</a>"
    if message.text == "Вернуться в главное меню":
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, 'Нажмите на кнопку ещё раз')
    else:
        message_date = dt.now()
        feedback_list = [message.chat.id, message.from_user.username,
                         message.text, message_date.strftime('%d %B %Y %H:%M:%S'), temp]
        logger.info(f'Пользователь @{feedback_list[1]} оставил сообщение: {feedback_list[2]}')
        db.execute("INSERT INTO feedback VALUES(?, ?, ?, ?, ?)", feedback_list)
        db.commit()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1)
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, text="Спасибо за обратную связь! Можете вернуться в главное меню:",
                         reply_markup=markup)
        for admin in admins:
            bot.send_message(admin, temp + '\n' + 'Его id - ' + str(message.chat.id), parse_mode='html')
            bot.send_message(admin, f'`{str(message.chat.id)}`', parse_mode='Markdown')


def izmenenia_yadisk():
    file_format = '.docx'
    y = yadisk.YaDisk(token='*') #Токен папки с изменениями на яндекс диске
    a = y.public_listdir('*') #Папка с файлами изменения на я.диске
    path_izmenenia = r'\\192.168.0.5\pool1\user\Миллер К.М\tgbot'
    count = 0
    for file in a:
        if file_format in file.name:
            y.download_public(public_key=file.public_key, path=file.path,
                              file_or_path=path_izmenenia + f'\\' + file.name)
            count += 1
    if count > 0:
        logger.info('Обновил изменения в папке')
    else:
        logger.info('В папке на я.диске нет файлов')


def register_handlers_admin():
    bot.register_message_handler(admin_menu, commands=['admin'])
    bot.register_message_handler(sending_log, commands=['send_log'])
    bot.register_message_handler(sending_command, commands=['send_message'])
    bot.register_message_handler(send_feedback, commands=['send_feedback'])
    bot.register_message_handler(rss_command, commands=['send_rss'])
    bot.register_message_handler(reg_send_message_to_user, commands=['reg_send_message_to_user'])


# Каждые 10 минут срабатывает проверка на
scheduler = BackgroundScheduler()
scheduler.add_job(rss_sending, "interval", minutes=10)
scheduler.add_job(izmenenia_yadisk, "interval", minutes=60)
scheduler.start()
