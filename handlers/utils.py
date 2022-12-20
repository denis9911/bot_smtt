import os
from create_bot import bot
from create_bot import cursor, db, logger
from bs4 import BeautifulSoup
import requests
from telebot import types
from create_bot import Contacts


def register_new_users(message):
    try:
        user = [message.chat.id, message.from_user.username]
        cursor.execute("INSERT INTO users VALUES(?, ?);", user)
        db.commit()
        logger.info(f'Новый пользователь: {user}')
    except:
        pass


def doc_file_manage(path, message):
    files = []
    for file in os.listdir(path):
        files.append(os.path.join(path, file))
    for doc in files:
        bot.send_document(message.chat.id, document=open(doc, 'rb'))


# Открываем фото в папке и отправляем их
def photo_file_manage(path, message):
    files = []
    for file in os.listdir(path):
        files.append(os.path.join(path, file))
    for doc in files:
        bot.send_photo(message.chat.id, photo=open(doc, 'rb'))

def structure_buttons():
    url = requests.get('http://satehm.ru/sveden/struct/')  # Получаем код страницы
    site_content = BeautifulSoup(url.content, 'lxml')
    structure_table = site_content.find('tbody')  # Получаем таблицу на сайте
    name_and_dolj = structure_table.find_all(
        'h1')  # Получаем информацию о всех хэдерах, в которых хранится имя и должность
    names_row = [name.text for name in name_and_dolj]
    names = [names_row[i] for i in range(0, len(names_row), 2)]
    buttons = [types.KeyboardButton(name) for name in names]
    return buttons

def structure_smtt(message):
    url = requests.get('http://satehm.ru/sveden/struct/')  # Получаем код страницы
    site_content = BeautifulSoup(url.content, 'lxml')
    structure_table = site_content.find('tbody')  # Получаем таблицу на сайте
    name_and_dolj = structure_table.find_all(
        'h1')  # Получаем информацию о всех хэдерах, в которых хранится имя и должность
    peoples_info = structure_table.find_all(
        'address')  # Получаем остальные данные из ячеек, где указаны кабинет, телефон, емаил и день рождения
    names_row = []
    names = []
    telephones_row = []
    telephones = []
    complite_list = []

    for name in name_and_dolj:
        names_row.append(name.text)
    for people in range(len(peoples_info)):
        if 'День рождения' not in peoples_info[people].text and len(
                peoples_info[people].text) > 0:  # Убираем дни рождения и пустые строки
            telephones_row.append(peoples_info[people].text)

    for i in range(0, len(names_row), 2):
        names.append(
            '\n'.join(
                names_row[i:i + 2]))  # Объединяем информацию о человеке и соединяем в 1 строку, помещаем её в список

    for i in range(0, len(telephones_row), 3):
        telephones.append('\n'.join(telephones_row[i:i + 3]))

    prepare_to_join = list(zip(names, telephones))  # Попарно объединяем имя+должность с информацией о человеке
    for i in range(len(prepare_to_join)):
        complite_list.append('\n'.join(prepare_to_join[i]))
    finding_contact = []
    for i in range(len(complite_list)):
        if message.text in complite_list[i]:
            finding_contact.append(complite_list[i])
    if len(finding_contact) > 0:
        bot.send_message(message.chat.id, text=finding_contact)
    else:
        bot.send_message(message.chat.id, text='Неверно введены данные, попробуйте сделать запрос по-другому или вернитесь в главное меню')


@bot.message_handler(state=Contacts.find_contact)
def find_contact(message):
    if message.text == 'Вернуться в главное меню':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Вернуться в главное меню'))
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, text='Нажмите на кнопку ещё раз', reply_markup=markup)
    else:
        structure_smtt(message)
