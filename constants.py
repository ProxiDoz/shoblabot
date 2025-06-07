#!/usr/bin/python3.8.9
# -*- coding: utf-8 -*-

# Тексты при командах /start и /help
help_text = '🤖 *Shobla Bo* может многое:\n\n' \
            '1) ✅❌ Создание опросов - /who\n' \
            '2) 🎧 Ссылка на шоблодискорд - /meeting\n' \
            '3) 🛍 Вывод скидок - /discount\n' \
            '4) 💁‍♀️🚗 Встроенная девка за рулём\n' \
            '5) 👩🏻‍⚕️ Встроенный вызов врача\n' \
            '6) 📌 Пин сообщения - просто ответь на необходимое сообщение ником бота @shoblabot\n' \
            '7) ✅ Сохранение гос.номера зеленого Rapida - /rapid\n' \
            '8) 💵 Вывод курса рубля - /usd\n' \
            '9) 🤖📋 Вывод лога по состоянию бота - /log\n' \
            '10) 🌐 По кнопкам ниже доступны полезные ссылки'

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

# Барсук
suk = ['сук', 'cyk', 'сюк']

# Для поздравления с юбилеем
happy_anniversary = '🥳 [{0}](tg://user?id={1}), с др!\nДобро пожаловать в клуб кому за {2} 😏'

# Для опроса
enter_question_new = '✅❌🤷 Введи тему опроса'
poll_options = ['✅ Да', '❌ Нет', '🤷 Не знаю']
too_large_question = '🤷 Слишком длинная тема опроса, сократи до 291 символа'

# Для созвона
meeting_link = '🎧[Дискорд](https://discord.gg/sDKJSg2d9q)'
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
          'Ошибка команды /s',  # 4
          'Ошибка в функции service_func.server_status',  # 5
          '---',  # 6
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
          '---',  # 17
          '---',  # 18
          'Ошибка при создании опроса',  # 19
          'Ошибка в обработчике текста send_text',  # 20
          'Ошибка в функции keyboards.button_func',  # 21
          'Ошибка при остановке опроса',  # 22
          '---',  # 23
          'Ошибка в функции share_log',  # 24
          'Ошибка в педо-функции',  # 25
          'Ошибка при пине сообщения',  # 26
          'Ощибка в функции kirov',  # 27
          'Ошибка в функции meeting',  # 28
          '---',  # 29
          'Ошибка в функции mammamia',  # 30
          'Ошибка в функции usd',  # 31
          'Ошибка в функции unpin',  # 32
          'Ошибка в функции send_media_id',  # 33
          'Ошибка в функции scheduled_messages',  # 34
          'Ошибка в функции отправки поздравления в Шоблу',  # 35
          'Ошибка при обновлении скидочных кнопок',  # 36
          'Ошибка в функции annet'  # 37
          ]
