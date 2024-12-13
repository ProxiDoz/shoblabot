#!/usr/bin/python3.8.9
# -*- coding: utf-8 -*-

# Тексты при командах /start и /help
help_text_light = '⛔ Вы не участник чата Шобла - ReBorn'
help_text = '🤖 *Shobla Bo* может многое:\n\n' \
            '1) ✅❌ Создание опросов - /who\n' \
            '2) 🎧 Формирование ежемесячных созвонов - /meeting\n' \
            '3) 🛍 Вывод скидок - /discount\n' \
            '4) 💁‍♀️🚗 Встроенная девка за рулём\n' \
            '5) 👩🏻‍⚕️ Встроенный вызов врача\n' \
            '6) 📌 Пин сообщения - просто ответь на необходимое сообщение ником бота @shoblabot\n' \
            '7) ✅ Сохранение гос.номера зеленого Rapida - /rapid\n' \
            '8) 💵 Вывод курса рубля - /usd\n' \
            '9) 🧐 Задай свой вопрос ИИ - /yapoznaumir\n\n' \
            '⭐ А также доступны следующие команды:\n' \
            '/log - вывод лога по состоянию бота\n' \
            '/stat - вывод статистики по командам и функциям бота\n\n' \
            '🌐 По кнопкам ниже доступны полезные ссылки'

# Девка
dvk = ['а', 'аа', 'a', 'aa']
devka = ['aaa', 'aaaa', 'aaaaa', 'aaaaaa', 'aaaaaaa', 'aaaaaaaa', 'aaaaaaaaa', 'aaaaaaaaaa', 'aaaaaaaaaaa', 'aaaaaaaaaaaa', 'aaaaaaaaaaaaa', 'aaaaaaaaaaaaaa', 'aaaaaaaaaaaaaaa',
         'ааа', 'аааа', 'ааааа', 'аааааа', 'ааааааа', 'аааааааа', 'ааааааааа', 'аааааааааа', 'ааааааааааа', 'аааааааааааа', 'ааааааааааааа', 'аааааааааааааа', 'ааааааааааааааа']

# ВРАЧА
hey_doc_gif_id = 'CgADAgADRgIAAkbDcEn-Ox-uqrgsHgI'
hey_doc = ['врача', 'врачаа', 'врачааа', 'врачаааа', 'врачааааа', 'врачаааааа', 'врачааааааа', 'врачаааааааа',
           'враача', 'враачаа', 'враачааа', 'враачаааа', 'враачааааа', 'враачаааааа', 'враачааааааа', 'враачаааааааа',
           'врааача', 'врааачаа', 'врааачааа', 'врааачаааа', 'врааачааааа', 'врааачаааааа', 'врааачааааааа', 'врааачаааааааа',
           'враааача', 'враааачаа', 'враааачааа', 'враааачаааа', 'враааачааааа', 'враааачаааааа', 'враааачааааааа', 'враааачаааааааа',
           'врааааача', 'врааааачаа', 'врааааачааа', 'врааааачаааа', 'врааааачааааа', 'врааааачаааааа', 'врааааачааааааа', 'врааааачаааааааа',
           'враааааача', 'враааааачаа', 'враааааачааа', 'врааааачаааа', 'враааааачааааа', 'враааааачаааааа', 'враааааачааааааа', 'враааааачаааааааа']

# РАСИЯ
russia = ['расия', 'расея', 'раися', 'раеся',
          'рассия', 'рассея', 'раисся', 'раесся',
          'росия', 'росея', 'роися', 'роеся',
          'россия', 'россея', 'роисся', 'роесся',
          'русия', 'русея', 'руися', 'руеся',
          'руссия', 'руссея', 'руисся', 'руесся', '🫡']
anthem = 'AwACAgIAAxkBAAJDIWLGyK15Ym3bMc0u5PU9YXtDDxHnAALtHAACbJI4SiCUtXmDfvoxKQQ'

annet_kek = ['кек', 'лол', 'kek', 'lol']
annet_video = 'BAACAgIAAxkBAAJJN2db5z1qIArBysw7nbB5ZPot5ldBAAK1YgACPaLYSsTy2CPcnhfENgQ'

kirov = ['киров', 'Киров', 'кирове', 'кировский', 'кировское', 'кировчане', 'кировчанское', 'кирова', 'кирову']

mammamia = '🤌️️️️️️'

damage = '🥺'
emotional_damage_voice_id = 'BAACAgIAAxkBAAJGdmPsjA5d_xkOhjrnmm6YYnkRPRx_AAJCJAAClVdoS2h9XwZuAAF-QS4E'

bayan_day_pic = 'AgACAgIAAxkBAAJFzWLeYTbQ2ENcXEwoPOrRZprGCCUUAALHuTEb6BT4ShJZvIDQxNjZAQADAgADcwADKQQ'

faggot_list = ['гей', 'пидор', 'пидр', 'педик', 'гомо', 'гомосек', 'глиномес', 'пидераст', 'леша', 'путин', 'путен', 'путейн', 'маргарин', 'путена']

# team
team = '@team'
team_text = '⚠️ *Внимание, Шобла*\n\n' \
            '[Тарс](t.me/shackoor), [Апол](t.me/apoll), [Ивановский](t.me/ivanovmm), [Конатик](t.me/KanatoF), [Кир](t.me/zhuykovkb), [Катя](tg://user?id=434756061), ' \
            '[Максон](t.me/MrGogu), [Носик](tg://user?id=51994109), [Окз](t.me/oxy_genium), [Паузеньк](t.me/Pausenk), [НТЩ](t.me/ntshch), [Толяновский](t.me/toliyansky), ' \
            '[Виктор](t.me/FrelVick), [Морго](t.me/margoiv_a), [Мишаня](t.me/Mich37), [Ксю](t.me/ksenia_boorda), [Ромолэ](t.me/Roman_Kazitskiy), [Эльтос](t.me/elvira_aes), ' \
            '[Аня](t.me/kebushka), [Таня](t.me/KostinaT), [Деннис](tg://user?id=503404575)'

# rapid
rapid = '/rapid'

# Барсук
suk = ['сук', 'cyk']
syuk = 'сюк'

# Для поздравления с юбилеем
happy_anniversary = '🥳 [{0}](tg://user?id={1}), с др!\nДобро пожаловать в клуб кому за {2} 😏'

# Для опроса
enter_question_new = '✅❌🤷 Введи тему опроса'
enter_question_gpt = 'Что хочешь узнать? 🧐'
poll_options = ['✅ Да', '❌ Нет', '🤷 Не знаю']
too_large_question = '🤷 Слишком длинная тема опроса, сократи до 291 символа'

# Для созвона
opros = 'Когда проведём шоблосозвон? Выбирайте день и ниже укажите время (относительно 🇷🇺: 🇫🇷-2, 🇷🇸-2, 🇧🇬-1, 🇬🇪+1, 🇰🇿+2). Опрос закроется через сутки'
meeting_options = ['Го в ЧТ', 'Го в ПТ', 'Го в СБ', 'Го в ВС', 'в 18:00 по МСК', 'в 19:00 по МСК', 'в 20:00 по МСК', 'в 21:00 по МСК']
meeting_link = '🎧[Дискорд](https://discord.gg/sDKJSg2d9q)\nИли Гугл Миит для запасного аэродрома\n'\
               'https://meet.google.com/tnj-dfkq-bpk (Админ Тарс) или https://meet.google.com/eky-ocyw-yhf (Админ Апол)'
meeting_pic = 'AgACAgIAAxkBAAJGiWP0of-RR4nekhlpNJdKUhywMV4NAALzyTEbiNKQS6LhqdN3LBprAQADAgADeAADLgQ'

# Для команды /usd
usd_pic = ['AgACAgIAAxkBAAJHhmTaCE6SoWoEh5banay5zgbROoO9AAIkyDEbrm3RSh-zi8Myj9vvAQADAgADeQADMAQ',
           'AgACAgIAAxkBAAJHbmTXm8165Ly6JWal4toSumUYtZgJAAIczDEb5I3ASo6qASduHbZkAQADAgADeAADMAQ',
           'AgACAgIAAxkBAAJHlmTaS9AZ49OJjA_5O-0AAcfw6i1Y1gACTMkxG65t0Uo5j_RIetD_YQEAAwIAA3gAAzAE',
           'AgACAgIAAxkBAAJHomTbnPNMcPKjuOLlrYL2dy4lx0gZAAJ-0jEbtWPZSoA36V56k08-AQADAgADeAADMAQ']
            
# Ошибки
errors = ['Ошибка команды /start',  # 0
          'Ошибка команды /help',  # 1
          'Ошибка при попытке обновления опроса /who',  # 2
          'Ошибка в обработчике Callback кнопок callback_buttons',  # 3
          'Ошибка команды /stat',  # 4
          'Ошибка в функции service_func.server_status',  # 5
          'Обращение из чужого чата',  # 6
          'Ошибка команды /who',  # 7
          'Ошибка команды /discount',  # 8
          'Ошибка в функции aaa (devka)',  # 9
          'ошибка в функции emotional daaamage',  # 10
          'Ошибка в функции russia',  # 11
          'Ошибка в функции vracha',  # 12
          'Ошибка в функции send_error',  # 13
          'Ошибка в функции team',  # 14
          'Ошибка в функции rapid',  # 15
          'Ошибка в функции barsuk',  # 16
          'Ошибка в функции barsyuk',  # 17
          'Ошибка при парсинге сайта ЦБР',  # 18
          'Ошибка при создании опроса',  # 19
          'Ошибка в обработчике текста send_text',  # 20
          'Ошибка в функции keyboards.button_func',  # 21
          'Ошибка при остановке опроса',  # 22
          'Ошибка при загрузке лога в функции share_log',  # 23
          'Ошибка в функции share_log',  # 24
          'Ошибка в педо-функции',  # 25
          'Ошибка при пине сообщения',  # 26
          'Ощибка в функции kirov',  # 27
          'Ошибка в функции meeting',  # 28
          'Ошибка в функции poll_results',  # 29
          'Ошибка в функции mammamia',  # 30
          'Ошибка в функции usd',  # 31
          'Ошибка команды /yapoznaumir',  # 32
          'Ошибка в функции send_media_id',  # 33
          'Ошибка в функции sdr',  # 34
          'Ошибка в функции отправки поздравления в Шоблу',  # 35
          'Ошибка при обновлении скидочных кнопок',  # 36
          'Ошибка в функции annet'  # 37
          ]

# ID участниеов Шобла - ReBorn в Telegram
shobla_member = {740100: {'name': 'Апол', 'dd_mm': '2.2', 'year': 1993},
                 155680674: {'name': 'Витя', 'dd_mm': '29.3', 'year': 1994},
                 873863: {'name': 'Кирюха', 'dd_mm': '7.4', 'year': 1993},
                 212589749: {'name': 'Максон', 'dd_mm': '13.2', 'year': 1993},
                 211717649: {'name': 'Ксю', 'dd_mm': '30.4', 'year': 1992},
                 165746780: {'name': 'Пауза', 'dd_mm': '28.3', 'year': 1993},
                 185997507: {'name': 'Мишаня', 'dd_mm': '1.9', 'year': 1993},
                 51994109: {'name': 'Лёха', 'dd_mm': '29.7', 'year': 1992},
                 228721090: {'name': 'Роман', 'dd_mm': '5.1', 'year': 1993},
                 154495805: {'name': 'Толян', 'dd_mm': '3.12', 'year': 1994},
                 2539125: {'name': 'Максончик', 'dd_mm': '28.3', 'year': 1992},
                 368345457: {'name': 'Аня Б.', 'dd_mm': '4.10', 'year': 1995},
                 113093545: {'name': 'Тарс', 'dd_mm': '2.11', 'year': 1989},
                 235208407: {'name': 'Канатик', 'dd_mm': '26.7', 'year': 1992},
                 385002370: {'name': 'Эля', 'dd_mm': '26.7', 'year': 1992},
                 213701955: {'name': 'Нтщ', 'dd_mm': '9.5', 'year': 1995},
                 434756061: {'name': 'Катя', 'dd_mm': '21.12', 'year': 1986},
                 358303246: {'name': 'Окс', 'dd_mm': '23.2', 'year': 1994},
                 135125333: {'name': 'Марго', 'dd_mm': '13.7', 'year': 1994},
                 428036107: {'name': 'Аня', 'dd_mm': '8.4', 'year': 1994},
                 503404575: {'name': 'Деннис', 'dd_mm': '24.5', 'year': 1993},
                 778173995: {'name': 'Таня', 'dd_mm': '2.9', 'year': 1997},
                 959656923: {'name': '🇲🇽 Seb', 'dd_mm': '25.7', 'year': 1995}
                 }
