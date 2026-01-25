#!/usr/bin/python3.8.9
# -*- coding: utf-8 -*-
import telebot                      # Библиотека piTelegramBotAPI
import secret                       # Файл с токенами
from helpers import service_func    # Файл со служебными функциями

# Полезные ссылки и клавиатуры к ним
cool_guys = telebot.types.InlineKeyboardButton(text='🛠Полезные люди', url='https://docs.google.com/spreadsheets/d/1-0wBt89xTOXyCcmLLesnWnMxZPsL3j6gRMz9l60MKt4/edit')
signal_link = telebot.types.InlineKeyboardButton(text='📟Наш Signal', url='https://signal.group/#CjQKIIGG0r5wKd81QpgnP-EpeYa2W7zHdbIxK80HwzQWmLFqEhCiyeF6zPiQ0n-2D__7vMaj')
film_photo = telebot.types.InlineKeyboardButton(text='📸Шобла в плёнке', url='https://t.me/c/1126587083/247976')
help_keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
help_keyboard.add(cool_guys, signal_link, film_photo)

# Текст сообщения по inline-кнопке остановки опроса
wrong_stop = 'Остановить опрос может только его создатель☝️'

# Данные для клавиатуры в команде /discount
buttons = {0: ['🆗 Окей', '🎗 Лента', '❎ Перекресток', '5️⃣ Пятерка', '🧲 Магнит', '🛒 Дикси', '🛒 Ашан', '🛒 Верный', '🥐 Буше'],
           1: ['disc_0', 'disc_1', 'disc_2', 'disc_3', 'disc_4', 'disc_5', 'disc_6', 'disc_7', 'disc_8'],
           2: ['🆗 [Окей](https://i.imgur.com/zhx9CkA.png)',
               '🎗 [Лента](https://i.imgur.com/SVq4ILS.png)',
               '❎ [Перекресток](https://i.imgur.com/5wra693.png)',
               '5️⃣ [Пятерка](https://i.imgur.com/9sJyYcx.png)',
               '🧲 [Магнит](https://i.imgur.com/cbVdBnv.png)',
               '🛒 [Дикси](https://i.imgur.com/FIQdWAh.png)',
               '🛒 [Ашан](https://i.imgur.com/iGsQ2Ds.jpg)',
               '🛒 [Верный](https://i.imgur.com/Dxg7owo.png)',
               '🥐 [Буше](https://i.imgur.com/ZZUCgky.png)']}

# Начальная клавиатура со скидками
keyboard_start = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_start.add(telebot.types.InlineKeyboardButton(text='◀️ '+buttons[0][0], callback_data=buttons[1][0]),
                   telebot.types.InlineKeyboardButton(text='▶️ '+buttons[0][2], callback_data=buttons[1][2]))


# Определение функции по callback_data
def button_func(bot, call):
    try:
        stop_poll(bot, call) if call.data[0:4] == 'stop' else edit_discount(bot, call)  # Нажата кнопка остановки опроса или смены скидки
    except Exception as button_func_error:
        service_func.send_error(bot, call.message, 21, button_func_error)


# Функция по обновлению сообщения со скидками по кнопке
def edit_discount(bot, call):
    try:
        discount_id = int(call.data.split('_')[1])
        keyboard_update = telebot.types.InlineKeyboardMarkup(row_width=2)
        keyboard_update.add(telebot.types.InlineKeyboardButton(text='◀️ '+buttons[0][discount_id - 1], callback_data=buttons[1][discount_id - 1]),
                            telebot.types.InlineKeyboardButton(text='▶️ '+buttons[0][(discount_id + 1) % 9], callback_data=buttons[1][(discount_id + 1) % 9]))
        text = buttons[2][discount_id]
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode='Markdown', reply_markup=keyboard_update)
    except Exception as edit_discount_error:
        service_func.send_error(bot, call.message, 36, edit_discount_error)


# Функция остановки опроса
def stop_poll(bot, call):
    try:
        message_id, user_id = call.data[5:].split('_')
        bot.stop_poll(secret.shobla_id, int(message_id)) if call.from_user.id == int(user_id) else bot.answer_callback_query(call.id, wrong_stop, show_alert=True)
    except Exception as stop_poll_error:
        service_func.send_error(bot, call.message, 22, stop_poll_error)
