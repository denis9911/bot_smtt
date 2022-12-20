from telebot import types
from create_bot import bot, Exams_Schedule
import os
import docx


@bot.message_handler(state=Exams_Schedule.exams_cource_searcher)
def group_searcher(message):
    user_course = message.text
    if user_course == 'Вернуться в главное меню':
        bot.delete_state(message.from_user.id, message.chat.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Вернуться в главное меню'))
        return bot.send_message(message.chat.id, text='Нажмите на кнопку ещё раз', reply_markup=markup)
    path = r'\\192.168.0.5\pool1\user\Миллер К.М\tgbot\exams' + f'\{user_course}'
    buttons = []
    markup = types.ReplyKeyboardMarkup(row_width=3)
    try:
        for doc in os.listdir(path):
            buttons.append(types.KeyboardButton(doc.split('.')[0]))
    except:
        return bot.send_message(message.chat.id,
                                text='Неправильная команда, нажмите кнопку выбора из представленных вариантов...')
    if len(buttons) > 0:
        markup.add(*buttons)
        bot.send_message(message.chat.id, text='Выберите группу:', reply_markup=markup)
        bot.set_state(message.from_user.id, Exams_Schedule.exams_date_searcher, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as exams_data:
            exams_data['user_course'] = user_course
    else:
        bot.send_message(message.chat.id,
                         text='В выбранном пункте нет файлов...')


@bot.message_handler(state=Exams_Schedule.exams_date_searcher)
def exams_file_sender(message):
    user_group = message.text
    docs = []
    with bot.retrieve_data(message.from_user.id, message.chat.id) as exams_data:
        path = r'\\192.168.0.5\pool1\user\Миллер К.М\tgbot\exams' + f'\{exams_data["user_course"]}'
    for doc in os.listdir(path):
        if doc.split('.')[0] == user_group:
            docs.append(doc)
    try:
        path = path + f'\{docs[0]}'
    except:
        return bot.send_message(message.chat.id,
                                text='Неправильная команда, нажмите кнопку выбора из представленных вариантов...Или в выбранном пункте отсутствуют файлы')
    if len(docs) > 0:
        doc = docx.Document(path)
        exams_dates = []
        date_buttons = []
        rows_list = []
        for tables in doc.tables:
            for row in tables.rows:
                for cell in row.cells:
                    rows_list.append(cell.text)
        del rows_list[0:4]
        for date in range(0, len(rows_list), 4):  # Делаем кнопки по датам
            exams_dates.append(rows_list[date].lstrip('\n'))
            date_buttons.append(types.KeyboardButton(rows_list[date].lstrip('\n')))
        markup = types.ReplyKeyboardMarkup(row_width=3)
        markup.add('Полное расписание экзаменов')
        markup.add(*date_buttons)
        markup.add(types.KeyboardButton('Вернуться в главное меню'))
        bot.send_message(message.chat.id, text='Выберите один из пунктов меню:', reply_markup=markup)
        bot.set_state(message.from_user.id, Exams_Schedule.exams_file_sender, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['rows_list'] = rows_list
            data['exams_dates'] = exams_dates
    else:
        bot.send_message(message.chat.id, text='В выбранном пункте отсутствуют файлы')


@bot.message_handler(state=Exams_Schedule.exams_file_sender)
def exams_file_sender(message):
    copy_rows_list = []
    if message.text == 'Вернуться в главное меню':
        bot.delete_state(message.from_user.id, message.chat.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Вернуться в главное меню')
        return bot.send_message(message.chat.id, text='Нажмите на кнопку еще раз', reply_markup=markup)
    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            copy_rows_list.extend(data['rows_list'])  # Создаём копию списка, так как список нужен будет позже
            if message.text == 'Полное расписание экзаменов':
                for row in range(4, len(data['rows_list']) + 1, 5):  # Для копии полного расписания после каждой 4 ставим "-"
                    copy_rows_list.insert(row, f'{"-" * 30}')
                bot.send_message(message.chat.id, '\n'.join(copy_rows_list))
            elif message.text.lstrip('\n') in data['exams_dates']:
                for row in range(0, len(data['rows_list']), 4):
                    if message.text in data['rows_list'][row]:
                        bot.send_message(message.chat.id, '\n'.join(data['rows_list'][row:row + 4]))

            else:
                bot.send_message(message.chat.id,
                                 text='Неправильная команда, нажмите кнопку выбора из представленных вариантов...')
