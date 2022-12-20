from loguru import logger
from telebot import types
from create_bot import bot, db, cursor


# Стартовое приветствие
# @bot.message_handler(commands=['start'])
def start(message):
    bot.delete_state(message.from_user.id, message.chat.id)
    user = [message.chat.id, message.from_user.username]
    bot.delete_state(message.from_user.id, message.chat.id)
    try:
        cursor.execute("INSERT INTO users VALUES(?, ?);", user)
        db.commit()
        bot.send_message(message.chat.id, "Привет! Напиши /menu")
        logger.info(f'Новый пользователь: {user}')
    except:
        bot.send_message(message.chat.id, "Привет, вы уже находитесь в базе данных, напишите /menu")
        logger.info(f'Старый пользователь нажал старт: {user}')


# Меню help
# @bot.message_handler(commands=['help'])
def help(message):
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, "Потерялся? Напиши /menu , чтобы перейти в главное меню!")


# Отправка локации корп А при вызове /location
# @bot.message_handler(commands=['location'])
def location(message):
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, text="Местонахождения корпуса А техникума на карте:")
    bot.send_location(message.chat.id, latitude=56.126761, longitude=93.334169)
    bot.send_message(message.chat.id, text="Местонахождения корпуса Б техникума на карте:")
    bot.send_location(message.chat.id, latitude=56.126960, longitude=93.338488)


# Кнопки гл. меню
@bot.message_handler(commands=['menu'])
def main_menu(message):
    bot.delete_state(message.from_user.id, message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🙋🏻‍♂️ ‍Абитуриентам 🙋🏻‍♂️")
    item2 = types.KeyboardButton("📅 Расписание 📅")
    item3 = types.KeyboardButton("👨‍👩‍👦 Родителям 👨‍👩‍👦")
    item4 = types.KeyboardButton("🗓 Графики и планы 🗓")
    item5 = types.KeyboardButton("👨🏻‍🎓 Курсы и доп. образование 👨🏻‍🎓")
    item6 = types.KeyboardButton("💵 Реквизиты для оплаты обучения 💵")
    item7 = types.KeyboardButton("🏞️ Соц. сети и др. 🏞️")
    item8 = types.KeyboardButton("🤖 Написать нам 🤖")
    item9 = types.KeyboardButton("☎ Контакты ☎")
    markup.add(item1)
    markup.add(item2, item3)
    markup.add(item4, item5)
    markup.add(item6, item7)
    markup.add(item8, item9)
    bot.send_message(message.chat.id, 'Выберите один из пунктов меню:', reply_markup=markup)


def register_handlers_client():
    bot.register_message_handler(start, commands=['start'])
    bot.register_message_handler(help, commands=['help'])
    bot.register_message_handler(location, commands=['location'])
    bot.register_message_handler(main_menu, commands=['menu'])
