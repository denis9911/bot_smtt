# Импорты
from telebot import types
import os
from loguru import logger
from create_bot import bot, ScheduleStates, Exams_Schedule, Feedback, Contacts
from handlers import admin, utils, client, schedule, exams_schedule

admin.register_handlers_admin()
client.register_handlers_client()


# Меню
@bot.message_handler(content_types=['text'])
def message_reply(message):
    utils.register_new_users(message)  # В главном меню пробуем регистрировать каждого юзера, так как остались старые пользователи бота, которые не проходили через /start
    try:
        if message.text == "🙋🏻‍♂️ ‍Абитуриентам 🙋🏻‍♂️":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton("Приказы о зачислении 2022")
            btn2 = types.KeyboardButton("Правила приёма")
            btn3 = types.KeyboardButton("Контакты приёмной комиссии")
            btn4 = types.KeyboardButton("Вступительные экзамены")
            btn5 = types.KeyboardButton("Перечень необходимых документов")
            btn6 = types.KeyboardButton("Специальности, профессии и срок обучения")
            btn7 = types.KeyboardButton("Информация об обеспечении возможности получения"
                                        " образования инвалидами и лицами с ОВЗ")
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, back)
            bot.send_message(message.chat.id, text="Выберите один из пунктов меню:", reply_markup=markup)

        # Нажатие на кнопку Приказы о зачислении отправляет документы, в имени которых есть месяц приказа из папки
        elif message.text == 'Приказы о зачислении 2022':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            btn1 = types.KeyboardButton("Очное (бюджет)")
            btn2 = types.KeyboardButton("Очное (внебюджет)")
            btn3 = types.KeyboardButton("Заочное (бюджет)")
            btn4 = types.KeyboardButton("Заочное (внебюджет)")
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, btn3, btn2, btn4, back)
            bot.send_message(message.chat.id, text="Выберите один из пунктов меню:", reply_markup=markup)

        elif message.text == "Очное (бюджет)":
            path = r'abiturienty\prikazy_o_zachislenii_2022'  # Отправляем папку
            files = []
            for root, d, folder in os.walk(path):
                for orders in folder:
                    if 'очное бюджет' in orders:
                        files.append(os.path.join(root, orders))
            for pdf in files:
                bot.send_document(message.chat.id, document=open(pdf, 'rb'))

        elif message.text == "Очное (внебюджет)":
            path = r'abiturienty\prikazy_o_zachislenii_2022'  # Отправляем папку
            files = []
            for root, d, folder in os.walk(path):
                for orders in folder:
                    if 'очное внебюджет' in orders:
                        files.append(os.path.join(root, orders))
            for pdf in files:
                bot.send_document(message.chat.id, document=open(pdf, 'rb'))

        elif message.text == "Заочное (бюджет)":
            path = r'abiturienty\prikazy_o_zachislenii_2022'  # Отправляем папку
            files = []
            for root, d, folder in os.walk(path):
                for orders in folder:
                    if 'заоч бюджет' in orders:
                        files.append(os.path.join(root, orders))
            for pdf in files:
                bot.send_document(message.chat.id, document=open(pdf, 'rb'))

        elif message.text == "Заочное (внебюджет)":
            path = r'abiturienty\prikazy_o_zachislenii_2022'  # Отправляем папку
            files = []
            for root, d, folder in os.walk(path):
                for orders in folder:
                    if 'заоч внебюджет' in orders:
                        files.append(os.path.join(root, orders))
            for pdf in files:
                bot.send_document(message.chat.id, document=open(pdf, 'rb'))

        elif message.text == 'Правила приёма':
            path = r'abiturienty\pravila_priyoma'
            utils.doc_file_manage(path, message)

        elif message.text == 'Контакты приёмной комиссии':
            bot.send_message(message.chat.id,
                             text="Адрес: 662500, Красноярский край, г. Сосновоборск, ул. Юности, 7 (Корпус А)"
                                  "\nТел.: 8 (39131) 2-16-93 (доб. 111)\ne-mail: priemsmtt@smtt24.ru; сайт: www.satehm.ru")

        elif message.text == 'Вступительные экзамены':
            bot.send_message(message.chat.id, text="ПРИЁМ В ТЕХНИКУМ - БЕЗ ВСТУПИТЕЛЬНЫХ ЭКЗАМЕНОВ\n"
                                                   "\nПри поступлении учитывается средний балл аттестата, а при конкурсе "
                                                   "больше одного поступающего на место рассматривается средний балл по "
                                                   "профильным предметам из таблицы ниже:")
            path = r'abiturienty\vstupitelnye_ekzameny'
            utils.photo_file_manage(path, message)

        elif message.text == 'Перечень необходимых документов':
            bot.send_message(message.chat.id, 'Приём документов от НЕСОВЕРШЕННОЛЕТНИХ абитуриентов осуществляется в '
                                              'присутствии законных представителей (родителей, усыновителей, попечителей '
                                              '(опекунов), которые представляют следующие документы (оригинал и копию): '
                                              'паспорт, свидетельство о рождении абитуриента, акт органа опеки и '
                                              'попечительства о назначении опекуна или попечителя.Законные представители '
                                              'несовершеннолетних вправе оформить нотариально удостоверенную доверенность '
                                              'на другое физическое лицо для представления своих интересов.')
            path = r'abiturienty\perechen_neobhodimyh_dokumentov'
            utils.photo_file_manage(path, message)

        elif message.text == 'Специальности, профессии и срок обучения':
            path = r'abiturienty\specialnosti_professii_i_srok_obucheniya'
            utils.photo_file_manage(path, message)

        elif message.text == 'Информация об обеспечении возможности получения образования инвалидами и лицами с ОВЗ':
            bot.send_message(message.chat.id, text='http://www.satehm.ru/sveden/ovz/')


        # Меню внутри Расписание
        elif message.text == "📅 Расписание 📅":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Расписание" + '\n' + "очное")
            btn2 = types.KeyboardButton("Полный список изменений")
            btn3 = types.KeyboardButton("Расписание" + '\n' + "экзаменов")
            btn4 = types.KeyboardButton("Ссылка на полное расписание")
            btn5 = types.KeyboardButton("Расписание звонков")
            btn6 = types.KeyboardButton("Заочникам")
            btn7 = types.KeyboardButton("Расписание кружков и секций")
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, btn2)
            markup.add(btn3, btn4)
            markup.add(btn5)
            markup.add(btn6, btn7)
            markup.add(back)
            bot.send_message(message.chat.id, text="Выберите один из пунктов меню:", reply_markup=markup)
        elif message.text == "Расписание" + '\n' + "очное":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton('Текущая неделя')
            btn2 = types.KeyboardButton('Следующая неделя')
            cancel = types.KeyboardButton('Вернуться в главное меню')
            markup.add(btn1, btn2, cancel)
            bot.set_state(user_id=message.from_user.id, state=ScheduleStates.week_in_a_row, chat_id=message.chat.id)
            bot.send_message(message.chat.id, text='Расписание для текущей или следующей недели?',
                             reply_markup=markup)
        elif message.text == 'Полный список изменений':
            path = r'\\192.168.0.5\pool1\user\Миллер К.М\tgbot'  # Отправляем папку
            file_buttons = []
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            for folder in os.listdir(path):
                if 'doc' in folder:
                    file_buttons.append(types.KeyboardButton(folder[:-5].title()))
            if len(file_buttons) < 1:
                return bot.send_message(message.chat.id, text='Изменений нет')
            markup.add(*file_buttons)
            markup.add(types.KeyboardButton('Вернуться в главное меню'))
            bot.send_message(message.chat.id, 'Выберите день недели:', reply_markup=markup)
            bot.set_state(message.from_user.id, ScheduleStates.full_list_changes, message.chat.id)

        elif message.text == "Расписание" + '\n' + "экзаменов":
            path = r'\\192.168.0.5\pool1\user\Миллер К.М\tgbot\exams'
            buttons = []
            markup = types.ReplyKeyboardMarkup(row_width=2)
            btn1 = types.KeyboardButton('1 курс')
            btn2 = types.KeyboardButton('2 курс')
            btn3 = types.KeyboardButton('3 курс')
            btn4 = types.KeyboardButton('4 курс')
            btn5 = types.KeyboardButton('ГИА 2022')
            back = types.KeyboardButton('Вернуться в главное меню')
            markup.add(btn1, btn2, btn3, btn4, btn5)
            markup.add(back)
            bot.set_state(user_id=message.from_user.id, state=Exams_Schedule.exams_cource_searcher,
                          chat_id=message.chat.id)
            bot.send_message(message.chat.id, text="Выберите курс:", reply_markup=markup)
        elif message.text == 'Ссылка на полное расписание':
            bot.send_message(message.chat.id, text="https://disk.yandex.ru/d/-o2yqSzfbytH6A")
        elif message.text == 'Расписание звонков':
            path = r"raspisanie\raspisanie zvonkov"
            utils.photo_file_manage(path, message)
        elif message.text == 'Заочникам':
            bot.send_message(message.chat.id, text="http://www.satehm.ru/studentam/zaochnoe-otdelenie/")
        elif message.text == 'Расписание кружков и секций':
            path = r"raspisanie\raspisanie kruzhkov i sekcij"
            utils.photo_file_manage(path, message)


        elif message.text == "👨‍👩‍👦 Родителям 👨‍👩‍👦":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            btn1 = types.KeyboardButton("Навигатор дополнительного образования")
            btn2 = types.KeyboardButton("Памятки")
            btn3 = types.KeyboardButton("Родительские собрания")
            btn4 = types.KeyboardButton("Классные часы")
            btn5 = types.KeyboardButton("Задолженности")
            btn6 = types.KeyboardButton("Условия питания")
            btn7 = types.KeyboardButton("Информация о волонтерском отряде")
            back = types.KeyboardButton("Вернуться в главное меню")
            button_list = [btn1, btn2, btn3, btn4, btn5, btn6, btn7, back]
            markup.add(button_list[0])
            markup.add(*button_list[1:-1])
            markup.add(button_list[-1])
            bot.send_message(message.chat.id, text="Выберите один из пунктов меню:", reply_markup=markup)
        elif message.text == "Навигатор дополнительного образования":
            markup = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton(
                url='https://navigator.krao.ru/program/26555-dobrovolcheskii-volonterskii-otryad-prodobro',
                text='Волонтерский отряд «PROДОБРО»')
            btn2 = types.InlineKeyboardButton(
                url='https://navigator.krao.ru/program/26567-golos-smtt',
                text='Вокальная студия «Голос СМТТ»')
            btn3 = types.InlineKeyboardButton(
                url='https://navigator.krao.ru/program/26577-kaleidoskop',
                text='Театральная студия «Калейдоскоп»')
            btn4 = types.InlineKeyboardButton(
                url='https://navigator.krao.ru/program/30935-mini-futbol',
                text='Cекция «Мини-футбол»')
            btn5 = types.InlineKeyboardButton(
                url='https://navigator.krao.ru/program/30941-fitnes-dlya-devushek',
                text='Студия фитнеса «Флексио»')
            btn6 = types.InlineKeyboardButton(
                url='https://navigator.krao.ru/program/30969-psikhologicheskii-klub',
                text='Психологический клуб «Луч»')
            btn7 = types.InlineKeyboardButton(
                url='https://navigator.krao.ru/program/31286-komanda-kvn-baldezh',
                text='Команда КВН « Балдеж»')
            btn8 = types.InlineKeyboardButton(
                url='https://navigator.krao.ru/program/31289-sektsiya-voleibol',
                text='Спортивная секция «Волейбол»')
            btn9 = types.InlineKeyboardButton(
                url='https://navigator.krao.ru/program/30924-voenno-sportivnyi-klub-bars',
                text='Военно-спортивный клуб «Барс»')
            btn10 = types.InlineKeyboardButton(
                url='https://navigator.krao.ru/program/31291-3d-masterskaya',
                text='3Д-моделирование')
            btn11 = types.InlineKeyboardButton(
                url='https://navigator.krao.ru/program/31292-azbuka-svarki',
                text='Азбука сварки')
            button_list = [btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, ]
            markup.add(*button_list)
            bot.send_message(message.chat.id, text="Выберите один из пунктов меню:", reply_markup=markup)
        elif message.text == "Памятки":
            path = r'roditelyam\pamyatki'
            button_list = []
            for doc in os.listdir(path):
                button_list.append(types.KeyboardButton(f'{doc.split(".")[0]}'))
            markup = types.ReplyKeyboardMarkup(row_width=1)
            markup.add(*button_list)
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(back)
            bot.send_message(message.chat.id, text="Выберите один из пунктов меню:", reply_markup=markup)
        elif message.text + '.jpg' in os.listdir(r'roditelyam\pamyatki'):
            for doc in os.listdir(r'roditelyam\pamyatki'):
                if message.text + '.jpg' in doc:
                    print(r'roditelyam\pamyatki' + '\\' + doc)
                    bot.send_message(message.chat.id, text=f'Загружаю памятку на тему "{message.text}"...')
                    bot.send_photo(message.chat.id, photo=open((r'roditelyam\pamyatki' + '\\' + doc), 'rb'))
        elif message.text == 'Родительские собрания':
            path = r'roditelyam\sobrania'
            utils.photo_file_manage(path, message)
        elif message.text == 'Классные часы':
            inline_markup = types.InlineKeyboardMarkup()
            inline_markup.add(types.InlineKeyboardButton('Разговоры о важном', url='https://razgovor.edsoo.ru/'))
            bot.send_message(message.chat.id,
                             text='Каждый понедельник в техникуме проводятся классные часы по темам внеурочных занятий «Разговоры о важном»',
                             reply_markup=inline_markup)
        elif message.text == 'Задолженности':
            path = 'roditelyam\zadoljennosti'
            utils.photo_file_manage(path, message)
        elif message.text == 'Условия питания':
            path = r'roditelyam\uslovia_pitania'
            utils.photo_file_manage(path, message)
        elif message.text == 'Информация о волонтерском отряде':
            path = r'roditelyam\volonterskiy_otryad'
            utils.photo_file_manage(path, message)
        # Меню внутри Соц. Сети
        elif message.text == "🏞️ Соц. сети и др. 🏞️":
            socialkb = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton(text="Новости на сайте", url="http://www.satehm.ru/news/")
            btn2 = types.InlineKeyboardButton(text="Вконтакте", url="https://vk.com/smtt24")
            btn3 = types.InlineKeyboardButton(text="Youtube", url="https://www.youtube.com/c/SMTT24")
            socialkb.add(btn1, btn2, btn3)
            bot.send_message(message.chat.id, "Выберите один из пунктов меню:", reply_markup=socialkb)


        # Меню внутри графики и планы
        elif message.text == "🗓 Графики и планы 🗓":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton("Календарный учебный график 22-23 уч.г (очное)")
            btn2 = types.KeyboardButton("Календарный учебный график 22-23 уч.г (заочное)")
            btn3 = types.KeyboardButton("График дежурств")
            btn4 = types.KeyboardButton("План работы СМТТ")
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, btn2, btn3, btn4, back)
            bot.send_message(message.chat.id, text="Выберите один из пунктов меню:", reply_markup=markup)
        elif message.text == 'Календарный учебный график 22-23 уч.г (очное)':
            path = r'grafiki_and_plani\kalendarnyj_uchebnyj_grafik_ochnoe'
            utils.photo_file_manage(path, message)
        elif message.text == 'Календарный учебный график 22-23 уч.г (заочное)':
            path = r'grafiki_and_plani\kalendarnyj_uchebnyj_grafik_zaochnoe'
            utils.photo_file_manage(path, message)
        elif message.text == 'График дежурств':
            path = r'grafiki_and_plani\grafik_dezhurstv'
            utils.photo_file_manage(path, message)
        elif message.text == 'План работы СМТТ':
            path = r'grafiki_and_plani\plan_raboty_SMTT'
            utils.doc_file_manage(path, message)


        # Меню внутри Курсы и доп. образование
        elif message.text == "👨🏻‍🎓 Курсы и доп. образование 👨🏻‍🎓":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton("Автокурсы")
            btn2 = types.KeyboardButton("Платные образовательные услуги")
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, btn2, back)
            bot.send_message(message.chat.id, text="Выберите один из пунктов меню:", reply_markup=markup)


        # Меню внутри Автокурсы
        elif message.text == 'Автокурсы':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Автокурсы - Контакты")
            btn2 = types.KeyboardButton("Автокурсы - Необходимые документы")
            btn3 = types.KeyboardButton("Автокурсы - Реквизиты для оплаты автокурсов")
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1)
            markup.add(btn2)
            markup.add(btn3)
            markup.add(back)
            bot.send_message(message.chat.id,
                             text="Автошкола Сосновоборского техникума ведет набор на курсы подготовки "
                                  "водителей категории «В».\nНачало занятий по мере комплектации "
                                  "групп.\nТеоретические занятия проводятся в вечернее время. Вождение "
                                  "автомобиля - по отдельному графику, учитывающему пожелания "
                                  "обучающихся.\nСтоимость обучения – 31 тысяча рублей, возможна оплата "
                                  "помесячно. Для студентов СМТТ предусмотрены скидки.",
                             reply_markup=markup)
        elif message.text == 'Автокурсы - Контакты':
            bot.send_message(message.chat.id,
                             text='Контакты:\nмоб. +7(983)201-0973\nтел. 8(39131)2-16-93, доб. 116\nкаб. '
                                  'А-11, корпус А, Юности, 7\nАржаников Владимир Владимирович\n\nмоб. +7('
                                  '950)997-3838 \nтел. 8(39131)2-16-93, доб. 114\nкаб. 108 корпус А, '
                                  'Юности, 7\nКарабарина Лариса Юрьевна')
        elif message.text == 'Автокурсы - Необходимые документы':
            bot.send_message(message.chat.id, text='Для записи в автошколу необходимо предоставить документы:\n- '
                                                   'паспорт;\n- документ об образовании (аттестат, диплом);\n- СНИЛС;\n- '
                                                   'медицинская справка;\n- 1 фото 3х4 (ч/б или цв).')
        elif message.text == 'Автокурсы - Реквизиты для оплаты автокурсов':
            bot.send_message(message.chat.id, text='http://www.satehm.ru/studentam/rekvizity-dlya-oplaty/')


        # Меню внутри Платные образовательные услуги
        elif message.text == 'Платные образовательные услуги':
            bot.send_message(message.chat.id, text='http://www.satehm.ru/sveden/paid_edu/')

        # Меню внутри Написать нам
        elif message.text == '🤖 Написать нам 🤖':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(back)
            bot.send_message(message.chat.id, text="Напишите свой вопрос или предложение:", reply_markup=markup)
            bot.set_state(message.from_user.id, state=Feedback.feedback, chat_id=message.chat.id)


        # Кнопка показывает реквизиты для оплаты обучения
        elif message.text == '💵 Реквизиты для оплаты обучения 💵':
            bot.send_message(message.chat.id, text="http://www.satehm.ru/studentam/rekvizity-dlya-oplaty/:")


        # Кнопка показывает Контакты
        elif message.text == "☎ Контакты ☎":
            markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            markup.add(*utils.structure_buttons())
            markup.add(types.KeyboardButton('Вернуться в главное меню'))
            bot.send_message(message.chat.id,
                             "662500 Красноярский край г. Сосновоборск, ул. Юности, зд. 7"
                             "\nТелефон очного отделения:+7 (39131)21693 (доб. 122)"
                             "\nТелефон заочного отделения: +7 (39131) 21693 (доб. 109)"
                             "\nЭл. почта секретаря директора: secret@smtt24.ru\n"
                             "\nСайт: http://www.satehm.ru", reply_markup=markup)
            bot.send_message(message.chat.id,
                             text='Выберите один из пунктов меню или напишите 1 ключевое слово для поиска (Фамилия/Имя/Отчество/Должность/Кабинет)')
            bot.set_state(message.from_user.id, Contacts.find_contact, message.chat.id)

        # Вернуться в меню - дублирует меню
        elif message.text == 'Вернуться в главное меню':
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
        else:
            bot.send_message(message.chat.id, text='Я тебя не понимаю, напиши /menu если потерялся')
    except FileNotFoundError:
        logger.warning(f'В пункте {message.text} отсутствуют файлы')
        bot.send_message(message.chat.id,
                         f'В пункте {message.text} отсутствуют файлы, администрация уже решает эту проблему')


bot.infinity_polling()
