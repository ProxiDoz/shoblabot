#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
import telebot

# Пути к файлам
log_file = '/root/log.txt'
activity_file = '/root/router/shoblabot/activity_count'
kirov_audio_path = '/root/router/shoblabot/audio/kirov.mp3'
mamma_audio_path = '/root/router/shoblabot/audio/mammamia.mp3'
sozvon_file = '/root/router/shoblabot/sozvon_poll'

# Тексты при командах /start и /help
help_text_light = '⛔ Вы не участник чата Шобла - ReBorn'
help_text = '🤖 *Shobla Bot* используется для:\n\n' \
            '1) ✅❌ Создания опросов - /who\n' \
            '2) 🎧 Формирование еженедельных шоблосозвонов\n' \
            '3) 🛍 Вызова скидок - /discount\n' \
            '4) 💁‍♀️🚗 Встроенная девка за рулём\n' \
            '5) 👩🏻‍⚕️ Встроенный вызов врачаааа\n' \
            '6) 📌 Пин сообщения - просто ответь на необходимое сообщение ником бота @shoblabot\n' \
            '7) ✅ Сохранение гос.номера зеленого Rapida - /rapid\n\n' \
            '⭐ Для пользователей с премиум подпиской доступны следующие команды:\n' \
            '/sozvon - вывод ссылок на шоблосозвон\n' \
            '/usd - вывод курса рубля\n' \
            '/log - вывод лога по состоянию бота\n' \
            '/stat - вывод статистики по командам и функциям бота\n\n' \
            '🌐 По кнопкам ниже доступны полезные ссылки'

# Полезные ссылки и клавиатуры к ним
cool_guys = telebot.types.InlineKeyboardButton(text='🛠Полезные люди', url='https://docs.google.com/spreadsheets/d/1-0wBt89xTOXyCcmLLesnWnMxZPsL3j6gRMz9l60MKt4/edit')
discord_link = telebot.types.InlineKeyboardButton(text='🎧Наш Discord', url='https://discord.gg/sDKJSg2d9q')
signal_link = telebot.types.InlineKeyboardButton(text='📟Наш Signal', url='https://signal.group/#CjQKIIGG0r5wKd81QpgnP-EpeYa2W7zHdbIxK80HwzQWmLFqEhCiyeF6zPiQ0n-2D__7vMaj')
film_photo = telebot.types.InlineKeyboardButton(text='📸Шобла в плёнке', url='https://t.me/c/1126587083/247976')
help_keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
help_keyboard.add(cool_guys, discord_link, signal_link, film_photo)

# Строка для месячной статистики
month_statistics = '🤖 *Статистика по боту за прошлый месяц:*\n\n' \
                   '✅❌ Создано опросов: *{0} шт*\n' \
                   '🛍  Запрошено скидок: *{1} раз*\n' \
                   '💁‍♀️🚗 Обнаружено девок за рулём: *{2} шт*\n' \
                   '👩🏻‍⚕️ Врача вызывали: *{3} раз*\n' \
                   '📌 Запинено сообщений: *{4} шт*\n' \
                   '✅️ Сохранено номеров Рапидов: *{5} шт*\n' \
                   '🦡 Отправлено барсуков: *{6} раз*\n' \
                   '💵 Рубль встал с колен: *{19} раз*\n' \
                   '🫡🇷🇺 Спето российских гимнов: *{7} раз*\n' \
                   '🌐 Заблокировано по маске /29: *{13} раз*\n' \
                   '🇬🇧 Переведено с транслитского: *{17} раз*\n' \
                   '🎤 Отрапортовано кировов: *{14} раз*\n' \
                   '🤌️️️️️️ Cпародировано итальянцев: *{18} раз*\n' \
                   '🥺 Получено эмоционального урона: *{15} раз*\n' \
                   '👥 Вызваны все участники Шоблы: *{8} раз*\n\n' \
                   'А так же отправлено следующих команд:\n\n' \
                   '/start: *{9} раз*\n' \
                   '/help: *{10} раз*\n' \
                   '/who: *{11} раз*\n' \
                   '/sozvon: *{16} раз*\n' \
                   '/rapid: *{12} раз*'

# Данные для команды /discount
discounts = telebot.types.InlineKeyboardButton(text='💰 Все скидки', url='https://photos.app.goo.gl/Xu4UQWqhSTcBVwt27')
channel = telebot.types.InlineKeyboardButton(text='💳 Канал', url='https://t.me/joinchat/AAAAAEk6NVud6BKc7YzZ2g')
buttons = {}
buttons[0] = ['🆗 О\'кей',  # 0
              '🎗 Лента',  # 1
              '❎ Перекресток',  # 2
              '5️⃣ Пятерочка',  # 3
              '🧲 Магнит',  # 4
              '🛒 Дикси',  # 5
              '🛒 Ашан',  # 6
              '🛒 Верный',  # 7
              '🥐 Буше',  # 8
              '💊 Вита',  # 9
              '💊 Столички']  # 10
# 'Икеа 🛋'
# 'Лайм 🛒'
# 'Л\'этуль 💛'
# 'Sephora 🖤'
# 'Улыбка 🌈'    
# 'Prisma 🛒'
# 'Домовой 🛠'
# 'Подружка 💅
# 'Карусель 🛒'
# 'Достаевский 🍕'

buttons[1] = ['disc_0', 'disc_1', 'disc_2', 'disc_3', 'disc_4', 'disc_5', 'disc_6', 'disc_7', 'disc_8', 'disc_9', 'disc_10']

buttons[2] = ['🆗 [О\'кей](https://i.imgur.com/zhx9CkA.png)',
              '🎗 [Лента](https://i.imgur.com/SVq4ILS.png)',
              '❎ [Перекресток](https://i.imgur.com/5wra693.png)',
              '5️⃣ [Пятерочка](https://i.imgur.com/yTuhGWH.jpg)',
              '🧲 [Магнит](https://i.imgur.com/cbVdBnv.png)',
              '🛒 [Дикси](https://i.imgur.com/FIQdWAh.png)',
              '🛒 [Ашан](https://i.imgur.com/iGsQ2Ds.jpg)',
              '🛒 [Верный](https://i.imgur.com/Dxg7owo.png)',
              '🥐 [Буше](https://i.imgur.com/H6ins0K.jpg)',
              '💊 [Вита](https://i.imgur.com/37nibRA.png)',
              '💊 [Столички](https://i.imgur.com/vImCtCv.png)']

# '🛋 [Икеа](https://i.imgur.com/ThL03zt.jpg)'
# '🛒 [Лайм](https://i.imgur.com/hq39niT.jpg)'
# '💛 [Л\'этуль](https://i.imgur.com/CqWU2vj.jpg)'
# '🖤 [Sephora](https://i.imgur.com/qm2RlMr.jpg)'
# '🌈 [Улыбка](https://i.imgur.com/bpcYZ2v.jpg)'
# '🛒 [Prisma](https://i.imgur.com/tcFfgho.jpg)'
# '🛠 [Домовой](https://i.imgur.com/Tnn5WTG.jpg)'
# '💅 [Подружка](https://i.imgur.com/0NGsUpZ.jpg)'
# '🛒 [Карусель](https://i.imgur.com/vwY6SB3.jpg)'
# '🍕 [Достаевский](https://i.imgur.com/LTx5ztX.jpg)\n*ТОЛЬКО ПРИ ЗАКАЗЕ ПО ТЕЛЕФОНУ*'

# Девка
dvk = ['а', 'аа', 'a', 'aa']
devka = ['aaa', 'aaaa', 'aaaaa', 'aaaaaa', 'aaaaaaa', 'aaaaaaaa', 'aaaaaaaaa', 'aaaaaaaaaa', 'aaaaaaaaaaa', 'aaaaaaaaaaaa', 'aaaaaaaaaaaaa', 'aaaaaaaaaaaaaa', 'aaaaaaaaaaaaaaa',
         'ааа', 'аааа', 'ааааа', 'аааааа', 'ааааааа', 'аааааааа', 'ааааааааа', 'аааааааааа', 'ааааааааааа', 'аааааааааааа', 'ааааааааааааа', 'аааааааааааааа', 'ааааааааааааааа']

# ВРАЧА
vracha = ['врача', 'врачаа', 'врачааа', 'врачаааа', 'врачааааа', 'врачаааааа', 'врачааааааа', 'врачаааааааа',
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

kirov = ['киров', 'Киров', 'кирове', 'кировский', 'кировское', 'кировчане', 'кировчанское', 'кирова', 'кирову']

anthem = 'AwACAgIAAxkBAAJDIWLGyK15Ym3bMc0u5PU9YXtDDxHnAALtHAACbJI4SiCUtXmDfvoxKQQ'

mammamia = '🤌️️️️️️'
damage = '🥺'
emotional_daaamage = 'BAACAgIAAxkBAAJGdmPsjA5d_xkOhjrnmm6YYnkRPRx_AAJCJAAClVdoS2h9XwZuAAF-QS4E'

# team
team = '@team'
team_text = '⚠️ *Внимание, Шобла*\n\n' \
            '[Тарс](t.me/shackoor), ' \
            '[Апол](t.me/apoll), ' \
            '[Ивановский](t.me/ivanovmm), ' \
            '[Конатик](t.me/KanatoF), ' \
            '[Кир](t.me/zhuykovkb), ' \
            '[Катя](tg://user?id=434756061), ' \
            '[Максон](t.me/MrGogu), ' \
            '[Носик](tg://user?id=51994109), ' \
            '[Окз](t.me/oxy_genium), ' \
            '[Паузеньк](t.me/Pausenk), ' \
            '[НТЩ](t.me/ntshch), ' \
            '[Толяновский](t.me/toliyansky), ' \
            '[Виктор](t.me/FrelVick), ' \
            '[Морго](t.me/margoiv_a), ' \
            '[Мишаня](t.me/Mich37), ' \
            '[Ксю](t.me/ksenia_boorda), ' \
            '[Ромолэ](t.me/Roman_Kazitskiy), ' \
            '[Эльтос](t.me/elvira_aes), ' \
            '[Аня](t.me/kebushka), ' \
            '[Таня](t.me/KostinaT), ' \
            '[Деннис](tg://user?id=503404575)'

# rapid
rapid = '/rapid'

# Барсук
suk = ['сук', 'cyk']
syuk = 'сюк'

# IPv6
ip_block = '/29'

# Гит
git = 'гит'

# Для опроса
enter_question_new = '✅❌🤷 Введи тему опроса'
poll_options = ['✅ Да', '❌ Нет', '🤷 Не знаю']
too_large_question = '🤷 Слишком длинная тема опроса, сократи до 291 символа'
wrong_stop = 'Остановить опрос может только его создатель☝️(а не ты, пес)'

# Для созвона
opros = 'Когда проведём шоблосозвон? Выбирайте день и ниже укажите время (относительно 🇷🇺: 🇫🇷-1, 🇬🇪+1, 🇰🇿+3). Опрос закроется через сутки'
sozvon_options = ['Го в ЧТ', 'Го в ПТ', 'Го в СБ', 'Го в ВС', 'в 18:00 по МСК', 'в 19:00 по МСК', 'в 20:00 по МСК', 'в 21:00 по МСК']
sozvon_link = '🎧[Дискорд](https://discord.gg/sDKJSg2d9q)\nИли Гугл Миит для запасного аэродрома\nhttps://meet.google.com/tnj-dfkq-bpk (Админ Тарс) или https://meet.google.com/eky-ocyw-yhf (Админ Апол)'
sozvon_pic = 'AgACAgIAAxkBAAJGiWP0of-RR4nekhlpNJdKUhywMV4NAALzyTEbiNKQS6LhqdN3LBprAQADAgADeAADLgQ'

# Для команды /usd
usd_pic = ["AgACAgIAAxkBAAJHhmTaCE6SoWoEh5banay5zgbROoO9AAIkyDEbrm3RSh-zi8Myj9vvAQADAgADeQADMAQ",
           "AgACAgIAAxkBAAJHbmTXm8165Ly6JWal4toSumUYtZgJAAIczDEb5I3ASo6qASduHbZkAQADAgADeAADMAQ",
           "AgACAgIAAxkBAAJHlmTaS9AZ49OJjA_5O-0AAcfw6i1Y1gACTMkxG65t0Uo5j_RIetD_YQEAAwIAA3gAAzAE",
            "AgACAgIAAxkBAAJHomTbnPNMcPKjuOLlrYL2dy4lx0gZAAJ-0jEbtWPZSoA36V56k08-AQADAgADeAADMAQ"]
            
# Ошибки
errors = ['Ошибка команды /start',  # 0
          'Ошибка команды /help',  # 1
          'Ошибка при попытке обновления опроса /who',  # 2
          'Ошибка в обработчике Callback кнопок callback_buttons',  # 3
          'Ошибка команды /stat',  # 4
          'Ошибка в функции server_info',  # 5
          'Обращение из чужого чата',  # 6
          'Ошибка команды /who',  # 7
          'Ошибка команды /discount',  # 8
          'Ошибка в функции aaa (devka)',  # 9
          'ошибка в функции emotional daaamage',  # 10
          'Ошибка в функции russia',  # 11
          'Ошибка в функции vracha',  # 12
          '---',  # 13
          'Ошибка в функции team',  # 14
          'Ошибка в функции rapid',  # 15
          'Ошибка в функции barsuk',  # 16
          'Ошибка в функции barsyuk',  # 17
          'Ошибка в функции block',  # 18
          'Ошибка при создании опроса',  # 19
          'Ошибка в обработчике текста send_text',  # 20
          'Ошибка при получении статуса сервера',  # 21
          'Ошибка при остановке опроса',  # 22
          'Ошибка при загрузке лога',  # 23
          'Ошибка в функции share_log', # 24
          'Ошибка в педо-функции',  # 25
          'Ошибка при пине сообщения',  # 26
          'Ощибка в функции kirov',  # 27
          'Ошибка в функции sozvon',  # 28
          'Ошибка в функции poll_results',  # 29
          'Ошибка в функции mammamia',  # 30
          'Ошибка в функции usd'  # 31
          ]

# ID участниеов Шобла - ReBorn в Telegram
tg_ids = [740100,  # Я
          155680674,  # Виктор
          873863,  # Кирилл
          212589749,  # Макс Ефимов
          211717649,  # Ксю
          165746780,  # ||
          185997507,  # Мишаня
          51994109,  # Леха Носов
          228721090,  # Ромик
          154495805,  # ТоЛRн
          2539125,  # Макс Иванов
          368345457,  # Аня Стекольщикова/Балдина
          113093545,  # Тарас
          235208407,  # Игнатов
          385002370,  # Эля
          213701955,  # Нтщ
          434756061,  # Катя
          358303246,  # Окс
          135125333,  # Марго
          428036107,  # Аня
          503404575,  # Деннис
          778173995,  # Таня
          959656923]  # Seb

tg_names = ['Апол',
            'Витя',
            'Кирюха',
            'Максон',
            'Ксю',
            'Пауза',
            'Мишаня',
            'Лёха',
            'Роман',
            'Толян',
            'Максончик',
            'Аня Б.',
            'Тарс',
            'Канатик',
            'Эля',
            'Нтщ',
            'Катя',
            'Окс',
            'Марго',
            'Аня',
            'Деннис',
            'Таня',
            '🇲🇽 Seb']

tg_drs = ['2.2.1993',  # Я
          '29.3.1994',  # Виктор
          '7.4.1993',  # Кирилл
          '13.2.1993',  # Макс Ефимов
          '30.4.1992',  # Ксю
          '28.3.1993',  # ||
          '1.9.1993',  # Мишаня
          '29.7.1992',  # Леха Носов
          '5.1.1993',  # Ромик
          '3.12.1994',  # ТоЛRн
          '28.3.1992',  # Макс Иванов
          '4.10.1995',  # Аня Стекольщикова/Балдина
          '2.11.1989',  # Тарас
          '26.7.1992',  # Игнатов
          '26.7.1992',  # Эля
          '9.5.1995',  # Нтщ
          '21.12.1986',  # Катя
          '23.2.1994',  # Окс
          '13.7.1994',  # Марго
          '8.4.1994',  # Аня
          '24.5.1993',  # Деннис
          '2.9.1997',  # Таня
          '25.7.1995']  # Seb
