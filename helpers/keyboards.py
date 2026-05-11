#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import telebot                      # Библиотека piTelegramBotAPI
import secret                       # Файл с токенами
from helpers.service_func import handler_error  # Импорт декоратора ошибок

# Полезные ссылки и клавиатуры к ним
cool_guys = telebot.types.InlineKeyboardButton(text='🛠Полезные люди', url='https://docs.google.com/spreadsheets/d/1-0wBt89xTOXyCcmLLesnWnMxZPsL3j6gRMz9l60MKt4/edit')
signal_link = telebot.types.InlineKeyboardButton(text='📟Наш Signal', url='https://signal.group/#CjQKIIGG0r5wKd81QpgnP-EpeYa2W7zHdbIxK80HwzQWmLFqEhCiyeF6zPiQ0n-2D__7vMaj')
film_photo = telebot.types.InlineKeyboardButton(text='📸Шобла в плёнке', url='https://t.me/c/1126587083/247976')
help_keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
help_keyboard.add(cool_guys, signal_link, film_photo)

# Текст сообщения по inline-кнопке остановки опроса
wrong_stop = 'Остановить опрос может только его создатель☝️'

# Данные для клавиатуры в команде /discount
buttons = {0: ['🆗 Окей', '🎗 Лента', '❎+5️⃣ Перик+5ка', '🧲 Магнит', '🛒 Дикси', '🛒 Ашан', '🛒 Верный'],
           1: ['disc_0', 'disc_1', 'disc_2', 'disc_3', 'disc_4', 'disc_5', 'disc_6'],
           2: ['🆗 [Окей](https://i.imgur.com/zhx9CkA.png) (1/7)',
               '🎗 [Лента](https://i.imgur.com/SVq4ILS.png) (2/7)',
               '❎+5️⃣ [Перик+5ка](https://i.imgur.com/5wra693.png) (3/7)\nКарта для обоих магазинов',
               '🧲 [Магнит](https://i.imgur.com/cbVdBnv.png) (4/7)',
               '🛒 [Дикси](https://i.imgur.com/FIQdWAh.png) (5/7)',
               '🛒 [Ашан](https://i.imgur.com/iGsQ2Ds.jpg) (6/7)',
               '🛒 [Верный](https://i.imgur.com/Dxg7owo.png) (7/7)']}

# Начальная клавиатура со скидками
keyboard_start = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_start.add(telebot.types.InlineKeyboardButton(text='◀️ '+buttons[0][1], callback_data=buttons[1][1]),
                   telebot.types.InlineKeyboardButton(text='▶️ '+buttons[0][3], callback_data=buttons[1][3]))


# Определение функции по callback_data
@handler_error(24)
def button_func(bot, call):
    stop_poll(bot, call) if call.data[0:4] == 'stop' else edit_discount(bot, call)  # Нажата кнопка остановки опроса или смены скидки


# Функция по обновлению сообщения со скидками по кнопке
@handler_error(25)
def edit_discount(bot, call):
    discount_id = int(call.data.split('_')[1])
    keyboard_update = telebot.types.InlineKeyboardMarkup(row_width=2)
    keyboard_update.add(telebot.types.InlineKeyboardButton(text='◀️ '+buttons[0][discount_id - 1], callback_data=buttons[1][discount_id - 1]),
                        telebot.types.InlineKeyboardButton(text='▶️ '+buttons[0][(discount_id + 1) % 7], callback_data=buttons[1][(discount_id + 1) % 7]))
    text = buttons[2][discount_id]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode='Markdown', reply_markup=keyboard_update)


# Функция остановки опроса
@handler_error(26)
def stop_poll(bot, call):
    message_id, user_id = call.data[5:].split('_')
    bot.stop_poll(secret.shobla_id, int(message_id)) if call.from_user.id == int(user_id) else bot.answer_callback_query(call.id, wrong_stop, show_alert=True)
