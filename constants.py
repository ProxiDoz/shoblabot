#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
import telebot

# Тексты при командах /start и /help
help_text_light = '⛔ Вы не участник чата Шобла - ReBorn'
help_text = '🤖 *Shobla Bot* используется для:\n\n' \
            '1) ✅❌ создания опросов - /who\n' \
            '2) 🛍 вызова скидок - /discount\n' \
            '3) 💁‍♀️🚗 Встроенная девка за рулём\n' \
            '4) 👩🏻‍⚕️ Встроенный вызов врачаааа\n' \
            '5) 📌 Пин сообщения - просто ответь на необходимое сообщение ником бота @shoblabot\n' \
            '6) ✅ Сохранение гос.номера зеленого Rapida - /rapid\n\n' \
            '🌐 По кнопкам ниже доступны полезные ссылки'

# Полезные ссылки
cool_guys = telebot.types.InlineKeyboardButton(text='Полезные люди 🛠', url='https://docs.google.com/spreadsheets/d/1-0wBt89xTOXyCcmLLesnWnMxZPsL3j6gRMz9l60MKt4/edit')
signal_link = telebot.types.InlineKeyboardButton(text='Шобла в Signal 📟', url='https://signal.group/#CjQKIIGG0r5wKd81QpgnP-EpeYa2W7zHdbIxK80HwzQWmLFqEhCiyeF6zPiQ0n-2D__7vMaj')
film_photo = telebot.types.InlineKeyboardButton(text='Шобла в плёнке 📸', url='https://t.me/c/1126587083/247976')

# Клавиатура для команды /help
help_keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
help_keyboard.add(cool_guys, signal_link, film_photo)

# Данные для команды /discount
buttons = {}
buttons[0] = ['О\'КЕЙ 🛒',  # 0
	      'Лента 🛒',  # 1
	      'Перекресток 🛒',  # 2
	      'Карусель 🛒',  # 3
	      'Пятерочка 🛒',  # 4
	      'Магнит 🛒',  # 5
	      'Дикси 🛒',  # 6
	      'Prisma 🛒',  # 7
	      'Ашан 🛒',  # 8
              'Улыбка 🌈',  # 9
	      'Достаевский 🍕',  # 10
	      'Буше 🥐',  # 11
	      'Домовой 🛠',  # 12
	      'Подружка 💅',  # 13
	      'Л\'этуль 💛',  # 14
	      'Озерки 💊',  # 15
	      'Столички 💊']  # 16
# 'Икеа 🛋'
# 'Sephora 🖤'
# 'Лайм 🛒'

buttons[1] = ['disc_0', 'disc_1', 'disc_2', 'disc_3', 'disc_4', 'disc_5', 'disc_6', 'disc_7', 'disc_8', 'disc_9', 'disc_10', 'disc_11', 'disc_12',
	      'disc_13', 'disc_14', 'disc_15', 'disc_16']

buttons[2] = ['🛒 [О\'кей](https://i.imgur.com/TZV4nCd.jpg)',
              '🛒 [Лента](https://i.imgur.com/PE9txx0.jpg)',
              '🛒 [Перекресток](https://i.imgur.com/my5Q8RF.jpg)',
              '🛒 [Карусель](https://i.imgur.com/vwY6SB3.jpg)',
              '🛒 [Пятерочка](https://i.imgur.com/yTuhGWH.jpg)',
              '🛒 [Магнит](https://i.imgur.com/Nmn5pTt.png)',
              '🛒 [Дикси](https://i.imgur.com/FIQdWAh.png)',
              '🛒 [Prisma](https://i.imgur.com/tcFfgho.jpg)',
              '🛒 [Ашан](https://i.imgur.com/iGsQ2Ds.jpg)',
              '🌈 [Улыбка](https://i.imgur.com/bpcYZ2v.jpg)',
              '🍕 [Достаевский](https://i.imgur.com/LTx5ztX.jpg)\n*ТОЛЬКО ПРИ ЗАКАЗЕ ПО ТЕЛЕФОНУ*',
              '🥐 [Буше](https://i.imgur.com/H6ins0K.jpg)',
              '🛠 [Домовой](https://i.imgur.com/Tnn5WTG.jpg)',
              '💅 [Подружка](https://i.imgur.com/0NGsUpZ.jpg)',
              '💛 [Л\'этуль](https://i.imgur.com/CqWU2vj.jpg)',
              '💊 [Озерки](https://i.imgur.com/6bDnAK4.jpg)',
              '💊 [Столички](https://i.imgur.com/dhWmZdf.jpg)']
# '🛋 [Икеа](https://i.imgur.com/ThL03zt.jpg)'
# '🖤 [Sephora](https://i.imgur.com/qm2RlMr.jpg)'
# '🛒 [Лайм](https://i.imgur.com/hq39niT.jpg)'

# Девка
dvk = ['а', 'аа', 'a', 'aa']
devka = ['aaa', 'aaaa', 'aaaaa', 'aaaaaa', 'aaaaaaa', 'aaaaaaaa', 'aaaaaaaaa', 'aaaaaaaaaa', 'aaaaaaaaaaa', 'aaaaaaaaaaaa',
         'ааа', 'аааа', 'ааааа', 'аааааа', 'ааааааа', 'аааааааа', 'ааааааааа', 'аааааааааа', 'ааааааааааа', 'аааааааааааа']

# ВРАЧА
vracha = ['врача', 'врачаа', 'врачааа', 'врачаааа', 'врачааааа', 'врачаааааа', 'врачааааааа', 'врачаааааааа',
          'враача', 'враачаа', 'враачааа', 'враачаааа', 'враачааааа', 'враачаааааа', 'враачааааааа', 'враачаааааааа',
          'врааача', 'врааачаа', 'врааачааа', 'врааачаааа', 'врааачааааа', 'врааачаааааа', 'врааачааааааа', 'врааачаааааааа',
          'враааача', 'враааачаа', 'враааачааа', 'враааачаааа', 'враааачааааа', 'враааачаааааа', 'враааачааааааа', 'враааачаааааааа',
          'врааааача', 'врааааачаа', 'врааааачааа', 'врааааачаааа', 'врааааачааааа', 'врааааачаааааа', 'врааааачааааааа', 'врааааачаааааааа',
          'враааааача', 'враааааачаа', 'враааааачааа', 'врааааачаааа', 'враааааачааааа', 'враааааачаааааа', 'враааааачааааааа', 'враааааачаааааааа']

# РАСИЯ
russia = ['ра\nси\nя', 'ра си я', 'расия',
          'ро\nси\nя', 'ро си я', 'росия',
          'ра\nсс\nея', 'ра сс ея', 'рассея',
          'ро\nис\nся', 'ро ис ся', 'роисся']

# team
team = '@team'

# rapid
rapid = '/rapid'

# Барсук
suk = ['сук', 'cyk']
syuk = ['сюк']

# IPv6
ip_block = ['/29']

# Гит
git1 = ' гит'
git2 = 'гит'

# Для опроса
enter_question_new = '✅❌🤷 Введи тему опроса'
poll_options = ['✅ Да', '❌ Нет', '🤷 Не знаю']
too_large_question = '🤷 Слишком длинная тема опроса, сократи до 293 символов'
wrong_stop = 'Остановить опрос может только его создатель☝️(а не ты, пес)'

enter_question = '✅❌ Введи тему опроса'
who_will = {}
who_will[0] = ['Апол',  # 0
               'Канат',  # 1
               'Лёха',  # 2
               'Нтщ',  # 3
               'Толян',  # 4
               'Виктор',  # 5
               'Кирилл',  # 6
               'Эля',  # 7
               'Тарс',  # 8
               'Пауза',  # 9
               'Макс Е.',  # 10
               'Макс И.',  # 11
               'Катя',  # 12
               'Окс',  # 13
               'Ксю',  # 14
               'Роман',  # 15
               'Марго',  # 16
               'Мишаня',  #17
			   'Аня',  #18
			   'Деннис']  # 19

who_will[1] = ['❌ Апол',  # 0
               '❌ Канат',  # 1
               '❌ Лёха',  # 2
               '❌ Нтщ',  # 3
               '❌ Толян',  # 4
               '❌ Виктор',  # 5
               '❌ Кирилл',  # 6
               '❌ Эля',  # 7
               '❌ Тарс',  # 8
               '❌ Пауза',  # 9
               '❌ Макс Е.',  # 10
               '❌ Макс И.',  # 11
               '❌ Катя',  # 12
               '❌ Окс',  # 13
               '❌ Ксю',  # 14
               '❌ Роман',  # 15
               '❌ Марго',  # 16
               '❌ Мишаня',  #17
			   '❌ Аня',  #18
			   '❌ Деннис']  # 19

who_will[2] = ['✅ Апол',  # 0 \u2705
               '✅ Канат',  # 1
               '✅ Лёха',  # 2
               '✅ Нтщ',  # 3
               '✅ Толян',  # 4
               '✅ Виктор',  # 5
               '✅ Кирилл',  # 6
               '✅ Эля',  # 7
               '✅ Тарс',  # 8
               '✅ Пауза',  # 9
               '✅ Макс Е.',  # 10
               '✅ Макс И.',  # 11
               '✅ Катя',  # 12
               '✅ Окс',  # 13
               '✅ Ксю',  # 14
               '✅ Роман',  # 15
               '✅ Марго',  # 16
			   '✅ Мишаня',  #17
			   '✅ Аня',  #18
			   '✅ Деннис']  # 19

who_will[3] = ['🤷🏼‍♂️ Апол',  # 0
               '🤷🏻‍♂️ Канат',  # 1
               '🤷🏻‍♂️ Лёха',  # 2
               '🤷🏼‍♀️ Нтщ',  # 3
               '🤷🏻‍♂️ Толян',  # 4
               '🤷🏼‍♂️ Виктор',  # 5
               '🤷🏻‍♂️ Кирилл',  # 6
               '🤷🏼‍♀️ Эля',  # 7
               '🤷🏼‍♂️ Тарс',  # 8
               '🤷🏻‍♀️ Пауза',  # 9
               '🤷🏻‍♂️ Макс Е.',  # 10
               '🤷🏻‍♂️ Макс И.',  # 11
               '🤷🏼‍♀️ Катя',  # 12
               '🤷🏻‍♀️ Окс',  # 13
               '🤷🏻‍♀️ Ксю',  # 14
               '🤷🏼‍♂️ Роман',  # 15
               '🤷🏻‍♀️ Марго',  # 16
			   '🤷🏻‍♂️ Мишаня',  #17
			   '🤷🏻‍♀️ Аня',  #18
			   '🤷🏻‍♂️ Деннис']  # 19

who_will_ids = [740100,  # 0
                235208407,  # 1
                51994109,  # 2
                213701955,  # 3
                154495805,  # 4
                155680674,  # 5
                873863,  # 6
                385002370,  # 7
                113093545,  # 8
                165746780,  # 9
                212589749,  # 10
                2539125,  # 11
                434756061,  # 12
                358303246,  # 13
                211717649,  # 14
                228721090,  # 15
                135125333,  # 16
                185997507,  # 17
				428036107,  # 18
				503404575]  # 19

# Ошибки
errors = ['Ошибка команды /start',  # 0
	  'Ошибка команды /help', # 1
	  ' ',  # 2
	  ' ',  # 3
	  'Ошибка команды /stat',  # 4
	  'Ошибка в функции server_info',  # 5
          'Обращение из чужого чата',  # 6
	  'Ошибка команды /who',  # 7
	  'Ошибка команды /discount',  # 8
	  'Ошибка в функции aaa',  # 9
	  'Ошибка в функции aaaa',  # 10
	  'Ошибка в функции russia',  # 11
	  'Ошибка в функции vracha',  # 12
	  'Ошибка в функции git',  # 13
	  'Ошибка в функции team',  # 14
	  'Ошибка в функции rapid',  # 15
	  'Ошибка в функции barsuk',  # 16
	  'Ошибка в функции barsyuk',  # 17
	  'Ошибка в функции block',  # 18
	  'Ошибка при создании опроса',  # 19
	  'Ошибка в обработчике текста send_text',  # 20
	  'Ошибка при получении статуса сервера',  # 21
	  'Ошибка при остановке опроса',  # 22
	  'Ошибка при попытке обновления опроса /who',  # 23
	  'Ошибка в обработчике Callback кнопок callback_buttons',  # 24
	  'Ошибка в функции отправки поздравления в Шоблу sdr()']  # 25

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
	  428036107,  #Аня
	  503404575]  #Деннис  

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
	    'Деннис']

tg_drs = ['2.2',  # Я
          '29.3',  # Виктор
          '7.4',  # Кирилл
          '13.2',  # Макс Ефимов
          '30.4',  # Ксю
          '28.3',  # ||
          '1.9',  # Мишаня
          '29.7',  # Леха Носов
          '5.1',  # Ромик
          '3.12',  # ТоЛRн
          '28.3',  # Макс Иванов
          '4.10',  # Аня Стекольщикова/Балдина
          '2.11',  # Тарас
          '26.7',  # Игнатов
          '26.7',  # Эля
          '9.5',  # Нтщ
          '21.12',  # Катя
          '23.2',  # Окс
          '13.7',  # Марго
	  '8.4',  # Аня
	  '24.5']  # Деннис
