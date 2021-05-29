 #!/usr/bin/python3.5
# -*- coding: utf-8 -*-
import vk  # Для использования VK API
import os  # Для проверки на существование файла
import json  # Представляет словарь в строку
import glob
import time  # Для представления времени в читаемом формате
import psutil
import random
import telebot
import cherrypy
import datetime
import constants
import secret
import threading
import bitly_api
import subprocess
from io import BytesIO  # Для отправки фотографий из Telegram в Шоблу
import tmdbsimple as tmdb
from datetime import timedelta
import urllib.request as urllib2  # Для отправки фотографий из Telegram в Шоблу
from urllib.parse import quote
import json
from telebot import apihelper

# https://t.me/socks?server=telegram.vpn99.net&port=55655
# https://t.me/socks?server=159.89.12.70&port=1080&user=telegram&pass=fuckrknfuck
# apihelper.proxy = {'https': 'socks5://swcbbabh:aYEbh6q5gQ@91.121.84.121:3306'}
# apihelper.proxy = {'https': 'socks5://Piterix:tgproxy@tgproxy.piter-ix.ru:6660'}
# apihelper.proxy = {'http': 'http://210b5a62-d786-469f-b97d-876cbdbbb54a.pub.cloud.scaleway.com:443'}
# apihelper.proxy = {'https': 'socks5://740100:7f0wrAke@185.211.245.136:1080'}
# tg://socks?server=tgproxy.piter-ix.ru&port=6660&user=Piterix&pass=tgproxy
# 91.121.84.121&port=3306&user=swcbbabh&pass=aYEbh6q5gQ',  # 33
# proxies = {
#     'http': 'socks5://740100:7f0wrAke@185.211.245.136:1080',
#     'https': 'socks5://740100:7f0wrAke@185.211.245.136:1080',
# }
# # # # # # # # # # # Инициализация # # # # # # # # # # #
# Переменные для ВК
session = vk.Session()
vk_api = vk.API(session)
photo_sizes = [75, 130, 604, 807, 1280, 2560]
video_sizes = [130, 320, 640, 800]

# Token бота
# pp = telegram.utils.request.Request(proxy_url='socks5://127.0.0.1:1080')
# bot = telegram.Bot(token=my_token, request=pp)
#
# updater = Updater(token='YOUR_TOKEN', request_kwargs={'proxy_url': 'socks5://127.0.0.1:1080/'})
#
# pp = apihelper.#(host='socks5://telegram.vpn99.net:55655')#127.0.0.1:1080')

bot = telebot.TeleBot(secret.tg_token)

# Инициализация переменных для Bitly
bitly_token = secret.bitly_token
bit = bitly_api.Connection(access_token=bitly_token)

# Служебные переменные
screen_id = None
reboot_or_not = {}

# Переменные для опроса
who_opros = {}
who_count = len(constants.who_will[0])
who_odd = who_count % 2

# Клавиатуры для скидок
keyboard_okey = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_bushe = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_dosta = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_pyatera = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_perik = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_lenta = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_domovoi = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_ikea = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_polushka = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_karusel = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_krasnoe = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_podr = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_sephora = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_prisma = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_lime = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_ulibka = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_letual = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_ozerki = telebot.types.InlineKeyboardMarkup(row_width=2)
keyboard_spar = telebot.types.InlineKeyboardMarkup(row_width=2)

okey = telebot.types.InlineKeyboardButton(text='О\'КЕЙ 🛒', callback_data='okey')
bushe = telebot.types.InlineKeyboardButton(text='Буше 🥐', callback_data='bushe')
dosta = telebot.types.InlineKeyboardButton(text='Достаевский 🍕', callback_data='dosta')
pyatera = telebot.types.InlineKeyboardButton(text='Пятерочка 🛒', callback_data='pyatera')
perik = telebot.types.InlineKeyboardButton(text='Перекресток 🛒', callback_data='perik')
lenta = telebot.types.InlineKeyboardButton(text='Лента 🛒', callback_data='lenta')
domovoi = telebot.types.InlineKeyboardButton(text='Домовой 🛠', callback_data='domovoi')
ikea = telebot.types.InlineKeyboardButton(text='Икеа 🛋', callback_data='ikea')
polushka = telebot.types.InlineKeyboardButton(text='Полушка 🛒', callback_data='polushka')
krasnoe = telebot.types.InlineKeyboardButton(text='К&Б 🍷', callback_data='krasnoe')
karusel = telebot.types.InlineKeyboardButton(text='Карусель 🛒', callback_data='karusel')
podr = telebot.types.InlineKeyboardButton(text='Подружка 💅', callback_data='podr')
sephora = telebot.types.InlineKeyboardButton(text='Sephora 🖤', callback_data='sephora')
prisma = telebot.types.InlineKeyboardButton(text='Prisma 🛒', callback_data='prisma')
lime = telebot.types.InlineKeyboardButton(text='Лайм 🛒', callback_data='lime')
ulibka = telebot.types.InlineKeyboardButton(text='Улыбка 🌈', callback_data='ulibka')
letual = telebot.types.InlineKeyboardButton(text='Л\'этуль 💛', callback_data='letual')
ozerki = telebot.types.InlineKeyboardButton(text='Озерки 💊', callback_data='ozerki')
spar = telebot.types.InlineKeyboardButton(text='SPAR 🛒', callback_data='spar')
discounts = telebot.types.InlineKeyboardButton(text='Все скидки 💰', url='https://photos.app.goo.gl/Xu4UQWqhSTcBVwt27')
channel = telebot.types.InlineKeyboardButton(text='Канал 💳', url='https://t.me/joinchat/AAAAAEk6NVud6BKc7YzZ2g')

# okey, lenta, perik, karusel, pyatera, polushka, prisma, lime, ulibka, krasnoe, dosta, bushe, domovoi, ikea, podr, letual, sephora, discounts
keyboard_okey.add(lenta, perik, karusel, pyatera, spar, polushka, prisma, lime, ulibka, krasnoe, dosta, bushe, domovoi, ikea, podr, letual, sephora, ozerki, discounts, channel)
keyboard_lenta.add(okey, perik, karusel, pyatera, spar, polushka, prisma, lime, ulibka, krasnoe, dosta, bushe, domovoi, ikea, podr, letual, sephora, ozerki, discounts, channel)
keyboard_perik.add(okey, lenta, karusel, pyatera, spar, polushka, prisma, lime, ulibka, krasnoe, dosta, bushe, domovoi, ikea, podr, letual, sephora, ozerki, discounts, channel)
keyboard_karusel.add(okey, lenta, perik, pyatera, spar, polushka, prisma, lime, ulibka, krasnoe, dosta, bushe, domovoi, ikea, podr, letual, sephora, ozerki, discounts, channel)
keyboard_pyatera.add(okey, lenta, perik, karusel, spar, polushka, prisma, lime, ulibka, krasnoe, dosta, bushe, domovoi, ikea, podr, letual, sephora, ozerki, discounts, channel)
keyboard_spar.add(okey, lenta, perik, karusel, pyatera, polushka, prisma, lime, ulibka, krasnoe, dosta, bushe, domovoi, ikea, podr, letual, sephora, ozerki, discounts, channel)
keyboard_polushka.add(okey, lenta, perik, karusel, pyatera, spar, prisma, lime, ulibka, krasnoe, dosta, bushe, domovoi, ikea, podr, letual, sephora, ozerki, discounts, channel)
keyboard_prisma.add(okey, lenta, perik, karusel, pyatera, spar, polushka, lime, ulibka, krasnoe, dosta, bushe, domovoi, ikea, podr, letual, sephora, ozerki, discounts, channel)
keyboard_lime.add(okey, lenta, perik, karusel, pyatera, spar, polushka, prisma, ulibka, krasnoe, dosta, bushe, domovoi, ikea, podr, letual, sephora, ozerki, discounts, channel)
keyboard_ulibka.add(okey, lenta, perik, karusel, pyatera, spar, polushka, prisma, lime, krasnoe, dosta, bushe, domovoi, ikea, podr, letual, sephora, ozerki, discounts, channel)
keyboard_krasnoe.add(okey, lenta, perik, karusel, pyatera, spar, polushka, prisma, lime, ulibka, dosta, bushe, domovoi, ikea, podr, letual, sephora, ozerki, discounts, channel)
keyboard_dosta.add(okey, lenta, perik, karusel, pyatera, spar, polushka, prisma, lime, ulibka, krasnoe, bushe, domovoi, ikea, podr, letual, sephora, ozerki, discounts, channel)
keyboard_bushe.add(okey, lenta, perik, karusel, pyatera, spar, polushka, prisma, lime, ulibka, krasnoe, dosta, domovoi, ikea, podr, letual, sephora, ozerki, discounts, channel)
keyboard_domovoi.add(okey, lenta, perik, karusel, pyatera, spar, polushka, prisma, lime, ulibka, krasnoe, dosta, bushe, ikea, podr, letual, sephora, ozerki, discounts, channel)
keyboard_ikea.add(okey, lenta, perik, karusel, pyatera, spar, polushka, prisma, lime, ulibka, krasnoe, dosta, bushe, domovoi, podr, letual, sephora, ozerki, discounts, channel)
keyboard_podr.add(okey, lenta, perik, karusel, pyatera, spar, polushka, prisma, lime, ulibka, krasnoe, dosta, bushe, domovoi, ikea, letual, sephora, ozerki, discounts, channel)
keyboard_letual.add(okey, lenta, perik, karusel, pyatera, spar, polushka, prisma, lime, ulibka, krasnoe, dosta, bushe, domovoi, ikea, podr, sephora, ozerki, discounts, channel)
keyboard_sephora.add(okey, lenta, perik, karusel, pyatera, spar, polushka, prisma, lime, ulibka, krasnoe, dosta, bushe, domovoi, ikea, podr, letual, ozerki, discounts, channel)
keyboard_ozerki.add(okey, lenta, perik, karusel, pyatera, spar, polushka, prisma, lime, ulibka, krasnoe, dosta, bushe, domovoi, ikea, podr, letual, sephora, discounts, channel)


# # # # # # # # # # # Тело бота # # # # # # # # # # #
# Начальное сообщение
@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        try:
            tg_user_id = constants.tg_ids.index(message.chat.id)
        except:
            tg_user_id = 0
        if message.chat.id == secret.tg_chat_id or message.chat.id == constants.tg_ids[tg_user_id]:
            bot.send_message(secret.tg_requests_chat_id, '🕹 */start* от [{0}](tg://user?id={1})\n'
                                                            '*Чат:* {2}'.format(constants.tg_names[tg_user_id],
                                                                                str(message.from_user.id),
                                                                                str(message.chat.id)),
                             parse_mode='Markdown')
            bot.send_message(message.chat.id, constants.help_text, disable_web_page_preview=True, parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, constants.help_text_light, parse_mode='Markdown')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в команде /start:\n\n' + str(e))


# Вызов справки
@bot.message_handler(commands=['help'])
def handle_help(message):
    try:
        try:
            tg_user_id = constants.tg_ids.index(message.from_user.id)
        except:
            tg_user_id = 0
        if message.chat.id == secret.tg_chat_id or message.chat.id == constants.tg_ids[tg_user_id]:
            bot.send_message(secret.tg_requests_chat_id, '❓ */help* от [{0}](tg://user?id={1})\n'
                                                            '*Чат:* {2}'.format(constants.tg_names[tg_user_id],
                                                                                str(message.from_user.id),
                                                                                str(message.chat.id)),
                             parse_mode='Markdown')
            bot.send_message(message.chat.id, constants.help_text, disable_web_page_preview=True, parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, constants.help_text_light, parse_mode='Markdown')
        if message.chat.id == secret.apple_id:
            bot.send_message(secret.apple_id, constants.help_text_apple, disable_web_page_preview=True)
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в команде /help:\n\n' + str(e))


# # # # # # Служебные функции
# Функция отправки времени старта запуска бота
def send_start_time():
    try:
        date = time.time() + 10800
        bot.send_message(secret.apple_id,
                         '*Время запуска бота: *_{0}_'.format(time.strftime('%d.%m.%y %X', time.gmtime(date))),
                         parse_mode='Markdown')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции send_start_time:\n\n' + str(e))


# Функция отправки ошибки
def send_error(message, error_id):
    try:
        date = time.strftime('%d.%m.%y %X', time.gmtime(message.date + 10800))
        bot.send_message(secret.apple_id,
                         '*{0}\nОт:* {1} {2}\n*Username:* {3}\n*Чат:* {4} {5} {6} id: {7}\n*Сообщение:* {8}\n'
                         '*Время:* _{9}_'.format(constants.errors[error_id], str(message.from_user.first_name),
                                                 str(message.from_user.last_name), str(message.from_user.username),
                                                 str(message.chat.title), str(message.chat.first_name),
                                                 str(message.chat.last_name), str(message.chat.id), message.text, date),
                         parse_mode='Markdown')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции send_error:\n\n' + str(e))


# # # # # # Служебные команды
# Запрос информации о чате Telegram
@bot.message_handler(commands=['set'])
def set_chat_id(message):
    try:
        if message.from_user.id == secret.apple_id:
            bot.send_message(secret.apple_id, '*Информация о чате:*\nUsername: {0}\nType: {1}\nTitle: {2}\n'
                                                 'ID: {3}\nИмя: {4}\nФамилия: '
                                                 '{5}'.format(str(message.chat.username), str(message.chat.type),
                                                              str(message.chat.title), str(message.chat.id),
                                                              str(message.chat.first_name), str(message.chat.last_name)),
                             parse_mode='Markdown')
        else:
            send_error(message, 0)
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции set_chat_id:\n\n' + str(e))


# Отправка сообщения от лица бота
@bot.message_handler(commands=['send'])
def send_from_bot(message):
    try:
        if message.chat.id == secret.apple_id:
            try:
                text = message.text.split('&')
                bot.send_message(text[1], text[2])
            except:
                bot.send_message(secret.apple_id, '❌ Ошибка при отправке сообщения')
            else:
                send_error(message, 1)
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции send_from_bot:\n\n' + str(e))


# Срочное закрытие доступа к ВК
@bot.message_handler(commands=['close'])
def close_access(message):
    try:
        if message.chat.id == secret.apple_id:
            bot.send_message(message.chat.id, constants.close_access, parse_mode='Markdown')
        else:
            send_error(message, 2)
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции close_access:\n\n' + str(e))


# Вызов информации о сервере
@bot.message_handler(commands=['s'])
def server_info(message):
    try:
        if message.chat.id == secret.apple_id:
            try:
                keyboard = telebot.types.InlineKeyboardMarkup(row_width=3)
                restart_m = telebot.types.InlineKeyboardButton(text='🎬', callback_data='adm_rm')
                restart_f = telebot.types.InlineKeyboardButton(text='⛽', callback_data='adm_rf')
                restart_b = telebot.types.InlineKeyboardButton(text='📙', callback_data='adm_rb')
                server = telebot.types.InlineKeyboardButton(text='💾', callback_data='adm_si')
                screen = telebot.types.InlineKeyboardButton(text='📑', callback_data='adm_sc')
                text = telebot.types.InlineKeyboardButton(text='💬', callback_data='adm_sh')
                keyboard.add(restart_m, restart_f, restart_b)
                keyboard.add(text, screen, server)
                bot.send_message(message.chat.id, '👑 Admin panel', reply_markup=keyboard)
            except:
                send_error(message, 3)
        else:
            send_error(message, 2)
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции server_info:\n\n' + str(e))


# Функция бекапа всей базы по расписанию
def backup_base_by_time():
    try:
        threading.Timer(3600, backup_base_by_time).start()
        try:
            now_time = datetime.datetime.now()
            if now_time.weekday() is not 6 or (now_time.hour + 7) is not 22:
                return
            date = time.time() + 10800
            file_name = 'backup_{0}.tar'.format(time.strftime('%d_%m_%y-%H_%M_%S', time.gmtime(date)))
            subprocess.Popen(['tar', 'cf', file_name, '/root/router'])
            time.sleep(0.5)
            file = open('/root/router/' + file_name, 'rb')
            raw_bytes = BytesIO(file.read())
            raw_bytes.name = file_name
            bot.send_document(secret.apple_id, raw_bytes, caption='Файл бекапа за {0}\n'.format(
                time.strftime('%d.%m.%y %H:%M:%S', time.gmtime(date))))
            bashMove = "mv /root/router/{0} /root/backups".format(file_name)
            subprocess.Popen(bashMove.split(), stdout=subprocess.PIPE)
        except:
            bot.send_message(secret.apple_id, constants.errors[30])
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции backup_base_by_time:\n\n' + str(e))


# # # # # # Функции для работы с ВК
# Отправка геометки
def send_geo(message, item):
    try:
        coordinates = item['coordinates']
        latitude = coordinates.split(' ')[0]
        longitude = coordinates.split(' ')[1]
        bot.send_location(message.chat.id, latitude, longitude)
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции send_geo:\n\n' + str(e))


# Загрузка вложений в сообщении
def get_attachment(message, attachment):
    try:
        if attachment:
            if attachment['type'] == 'photo':
                photo_link = 'photo_2560'
                for size in photo_sizes:
                    if attachment['photo']['width'] <= size:
                        photo_link = 'photo_' + str(size)
                        break
                bot.send_chat_action(message.chat.id, 'upload_photo')
                file = urllib2.urlopen(attachment['photo'][photo_link])
                raw_bytes = BytesIO(file.read())  # Байты картинки
                raw_bytes.name = 'photo.jpg'
                try:
                    bot.send_photo(message.chat.id, raw_bytes)  # Отправляем фото
                except:
                    send_error(message, 4)
                    bot.send_message(message.chat.id,
                                     'Ошибка при загрузке фото.\nСсылка: {0}'.format(attachment['photo'][photo_link]))
                file.close()  # Закрываем соединение
                raw_bytes.close()
            elif attachment['type'] == 'audio':
                bot.send_message(message.chat.id, '<b>Аудио:</b> <a href="{2}">{0} - {1}</a>'.format(
                    attachment['audio']['artist'],
                    attachment['audio']['title'], attachment['audio']['url']), parse_mode='HTML')
            elif attachment['type'] == 'gift':
                bot.send_chat_action(message.chat.id, 'upload_photo')
                file = urllib2.urlopen(attachment['gift']['thumb_256'])
                raw_bytes = BytesIO(file.read())  # Байты картинки
                raw_bytes.name = 'photo.jpg'
                try:
                    bot.send_photo(message.chat.id, raw_bytes, caption='Подарок')  # Отправляем фото
                except:
                    bot.send_message(message.chat.id,
                                     'Ошибка при загрузке подарка.\nСсылка: {0}'.format(attachment['gift']['thumb_256']))
                    send_error(message, 5)
                file.close()  # Закрываем соединение
                raw_bytes.close()
            elif attachment['type'] == 'link':
                link = bit.shorten(attachment['link']['url'])
                bot.send_message(message.chat.id, '<b>Прикрепленная ссылка</b>: ' + link['url'],
                                 parse_mode='HTML')
            elif attachment['type'] == 'doc':
                link = bit.shorten(attachment['doc']['url'])
                bot.send_message(message.chat.id,
                                 '<b>Документ:</b> {0}\n{1}'.format(attachment['doc']['title'], link['url']),
                                 parse_mode='HTML')
            elif attachment['type'] == 'video':
                video_link = 'https://vk.com/video{0}_{1}'.format(attachment['video']['owner_id'],
                                                                  attachment['video']['id'], parse_mode='HTML')
                link = bit.shorten(video_link)
                bot.send_message(message.chat.id,
                                 '<b>Видео:</b> {0}\n<b>Ссылка:</b> {1}'.format(
                                     attachment['video']['title'], link['url']), parse_mode='HTML')
            elif attachment['type'] == 'sticker':
                bot.send_chat_action(message.chat.id, 'upload_photo')
                file = urllib2.urlopen(attachment['sticker']['photo_256'])
                raw_bytes = BytesIO(file.read())  # Байты картинки
                raw_bytes.name = 'photo.png'
                try:
                    bot.send_photo(message.chat.id, raw_bytes, caption='Стикер')  # Отправляем фото
                except:
                    bot.send_message(message.chat.id,
                                     'Ошибка при загрузке стикера.\nСсылка: {0}'.format(attachment['sticker']['photo_256']))
                    send_error(message, 6)
                file.close()  # Закрываем соединение
                raw_bytes.close()
            elif attachment['type'] == 'wall':
                if attachment['wall']['from_id'] != attachment['wall']['id'] != 0:
                    link = 'https://vk.com/wall{0}_{1}'.format(attachment['wall']['from_id'], attachment['wall']['id'])
                    bot.send_message(message.chat.id, '<b>Пост: </b>' + link, parse_mode='HTML')
                    attachments = attachment['wall'].get('attachments')  # Вложения
                    if attachments:
                        for items in attachments:
                            if items['type'] == 'link':
                                get_attachment(message, attachment=items)
                else:
                    bot.send_message(message.chat.id, '<b>Пост: Запись не найдена</b>', parse_mode='HTML')
            elif attachment['type'] == 'wall_reply':
                link = 'https://vk.com/wall{0}_{1}'.format(attachment['wall_reply']['owner_id'],
                                                           attachment['wall_reply']['post_id'])
                text = '<b>Комментарий к записи на стене:</b>\n{0}\n{1}'.format(attachment['wall_reply']['text'], link)
                bot.send_message(message.chat.id, text, parse_mode='HTML')
            elif attachment['type'] == 'market':
                text = '<b>Товар:</b> {0}\n<b>Цена:</b> {1} {2}\n<b>Описание:</b> ' \
                       '{3}'.format(attachment['market']['title'], int(attachment['market']['price']['amount']) / 100,
                                    attachment['market']['price']['currency']['name'], attachment['market']['description'])
                bot.send_chat_action(message.chat.id, 'upload_photo')
                file = urllib2.urlopen(attachment['market']['thumb_photo'])
                raw_bytes = BytesIO(file.read())  # Байты картинки
                raw_bytes.name = 'photo.jpg'
                try:
                    bot.send_photo(message.chat.id, raw_bytes)  # Отправляем фото товара
                    bot.send_message(message.chat.id, text, parse_mode='HTML')
                except:
                    bot.send_message(message.chat.id,
                                     'Ошибка при загрузке товара.\n{0}\nСсылка: {1}'.format(text, attachment['market'][
                                         'thumb_photo']), parse_mode='HTML')
                    send_error(message, 7)
                file.close()  # Закрываем соединение
                raw_bytes.close()
            elif attachment['type'] == 'market_album':
                bot.send_message(message.chat.id, '*Подборка товаров*', parse_mode='Markdown')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции get_attachment:\n\n' + str(e))


# Получение ссыли вложения из пересланного сообщения
def get_attachment_link(attachments):
    try:
        attachment = attachments[0]
        if attachment:
            if attachment['type'] == 'photo':
                link = 'photo_2560'
                for size in photo_sizes:
                    if attachment['photo']['width'] <= size:
                        link = 'photo_' + str(size)
                        break
                link = attachment['photo'][link]
            # Не работает с новым Audio API (https://vk.com/dev/audio_api)
            elif attachment['type'] == 'audio':
                link = attachment['audio']['url']
            elif attachment['type'] == 'gift':
                link = attachment['gift']['thumb_256']
            elif attachment['type'] == 'link':
                link = attachment['link']['url']
            elif attachment['type'] == 'doc':
                link = attachment['doc']['url']
            elif attachment['type'] == 'video':
                link = 'https://vk.com/video{0}_{1}'.format(attachment['video']['owner_id'], attachment['video']['id'])
            elif attachment['type'] == 'sticker':
                link = attachment['sticker']['photo_256']
            elif attachment['type'] == 'wall':
                link = 'https://vk.com/wall{0}_{1}'.format(attachment['wall']['from_id'], attachment['wall']['id'])
            elif attachment['type'] == 'wall_reply':
                link = 'https://vk.com/wall{0}_{1}'.format(attachment['wall_reply']['owner_id'],
                                                           attachment['wall_reply']['post_id'])
            return link
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции get_attachment_link:\n\n' + str(e))


# Запрос имени собеседника
def get_name(message, user_id):
    try:
        try:
            if user_id > 0:  # Если сообщение от пользователя
                name_response = vk_api.users.get(user_ids=user_id, access_token=secret.vk_token, v=5.52)
                return name_response[0]['first_name'] + ' ' + name_response[0]['last_name']
            else:  # Если сообщение от группы
                name_response = vk_api.groups.getById(group_id=str(user_id * (-1)), access_token=secret.vk_token, v=5.85)
                return name_response[0]['name'] + ' (группа)'
        except:  # Иначе выдать ошибку при получении имени собечедника
            bot.send_message(message.chat.id, constants.errors[6], reply_to_message_id=message.message_id)
            send_error(message, 8)
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции get_name:\n\n' + str(e))


# Отправка пересланных сообщений
def send_fwd_messages(message, fwd_messages):
    try:
        text_to_send = '\n<b>Пересланные собщения:</b>'
        fwd_id = 1
        for item in fwd_messages:
            date = time.strftime('%X %d.%m', time.gmtime(item['date'] + 10800))
            name = get_name(message, item['user_id'])  # Запрос на получение имени
            if item['body'] is not '':
                text_to_send += '\n\t\t\t\t<b>{0}) {1}</b>\n\t\t\t\t<i>{2}</i>\n\t\t\t\t{3}'.format(fwd_id, name, date,
                                                                                                    item['body'])
            else:
                text_to_send += '\n\t\t\t\t<b>{0}) {1}</b>\n\t\t\t\t<i>{2}</i>'.format(fwd_id, name, date)
            if 'attachments' in item:
                link = get_attachment_link(item['attachments'])
                text_to_send += '\n\t\t\t\t<a href="{0}">Вложение</a>'.format(link)
            elif 'geo' in item:
                text_to_send += '\n\t\t\t\t<b>Карта</b>'
            elif 'fwd_messages' in item:
                text_to_send += '\n\t\t\t\t<b>Пересланные собщения</b>'
            fwd_id += 1
        return text_to_send
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции send_fwd_messages:\n\n' + str(e))


# Отправка сообщений из ВКонтакте из диалогов
def send_vk_dialogs_messages():
    try:
        threading.Timer(11, send_vk_dialogs_messages).start()
        if secret.vk_token:  # Если token установлен
            chat = telebot.types.Chat(secret.apple_id, 'private')
            chat_2 = telebot.types.Chat(secret.tg_chat_id, 'group')
            message_fwd = telebot.types.Message(11218, secret.apple_id, 1476657939, chat, None, {'audio': None})
            message_geo_att = telebot.types.Message(10000, secret.apple_id, 1476657939, chat_2, None, {'audio': None})
            try:
                response = vk_api.messages.getDialogs(unread=1, access_token=secret.vk_token, v=5.64)
                if response:  # Если есть непрочитанные сообщения
                    for items in response['items']:
                        if items['message'].get('chat_id') is None:  # Если это диалог, а не чат
                            vk_user_id = constants.ids.index(items['message']['user_id'])
                            if items['message']['read_state'] == 0 and vk_user_id >= 0:  # Если есть непрочитанные сообщения
                                try:
                                    hist_response = vk_api.messages.getHistory(count=5, user_id=constants.ids[vk_user_id],
                                                                               access_token=secret.vk_token,
                                                                               v=5.64)  # Запрос истории переписки
                                    vk_api.messages.markAsRead(peer_id=constants.ids[vk_user_id],
                                                               access_token=secret.vk_token, v=5.73)
                                    name = constants.vk_names[vk_user_id]
                                    bot.send_chat_action(secret.tg_chat_id, 'typing')
                                    bot.send_message(secret.tg_chat_id,
                                                     'Пишет *' + name + ':*', parse_mode='Markdown')
                                    for item in hist_response['items'][::-1]:
                                        if item['out'] == 0 and item['read_state'] == 0:
                                            attachments = item.get('attachments')  # Вложения
                                            geo = item.get('geo')  # Если прикреплена геометка
                                            fwd_messages = item.get('fwd_messages')  # Если пересланы сообщения
                                            text_to_send = item['body']
                                            if fwd_messages:
                                                text_to_send += send_fwd_messages(message_fwd, fwd_messages)
                                            try:
                                                for text_parts in telebot.util.split_string(
                                                        text_to_send.replace('<br>', '\n'), 3000):
                                                    bot.send_message(secret.tg_chat_id, text_parts, parse_mode='HTML',
                                                                     disable_web_page_preview=True)
                                                if geo:
                                                    send_geo(message_geo_att, geo)
                                                if attachments:
                                                    for att_items in attachments:
                                                        get_attachment(message_geo_att, attachment=att_items)
                                                vk_api.messages.markAsRead(peer_id=constants.ids[vk_user_id],
                                                                           access_token=secret.vk_token, v=5.73)
                                                bot.send_message(secret.tg_requests_chat_id, '📨 от *{0}*'.format(name),
                                                                 parse_mode='Markdown')
                                            except:
                                                vk_api.messages.markAsRead(peer_id=constants.ids[vk_user_id],
                                                                           access_token=secret.vk_token, v=5.73)
                                                vk_api.messages.send(user_id=constants.ids[vk_user_id],
                                                                     message=constants.errors[9],
                                                                     access_token=secret.vk_token,
                                                                     v=5.52)
                                                message_error = telebot.types.Message(11218, secret.apple_id,
                                                                                      item.get('date'), chat, None,
                                                                                      {'text': text_to_send,
                                                                                       'from_user': constants.vk_names[
                                                                                           vk_user_id]})
                                                send_error(message_error, 9)
                                except:  # Иначе выдать ошибку загрузки истории
                                    bot.send_message(secret.apple_id, 'Error while getting dialog history\n' +
                                                     constants.errors[10] + '\nСообщение от ' + constants.vk_names[
                                                         vk_user_id])
            except:  # Иначе выдать ошибку при загрузке списка диалогов
                tg = 0
                # bot.send_message(secret.apple_id, 'Error while getting dialog list\n' + constants.errors[11])
        else:
            bot.send_message(secret.apple_id, '<b>' + constants.errors[12] + '</b> в send_vk_dialogs_messages()',
                             parse_mode='HTML')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции отправки сообщений из ВК send_vk_dialogs_messages:\n\n' + str(e))


# Проверка новых заявок в друзья
def new_friends():
    try:
        threading.Timer(60, new_friends).start()  # Каждые полчаса - 1800, каждые 10 мин - 600
        chat = telebot.types.Chat(secret.apple_id, 'private')
        message = telebot.types.Message(11218, secret.apple_id, 1476657939, chat, None, {'audio': None})
        try:
            movies = glob.glob('/var/run/screen/S-root/*.movies')
            books = glob.glob('/var/run/screen/S-root/*.books')
            fuel = glob.glob('/var/run/screen/S-root/*.fuel')
            global screen_id
            if movies == []:
                bot.send_message(secret.apple_id, '🎬 Movies Bot упал.\n/restart_m')
                # if books == []:
                #     bot.send_message(secret.apple_id, '📙 Books Bot упал.\n/restart_b')
                # if fuel == []:
                #     bot.send_message(secret.apple_id, '⛽️ Fuel Bot упал.\n/restart_f')
        except:
            bot.send_message(secret.apple_id, 'Ошибка при поиске скринов')
        if secret.vk_token:  # Если token установлен
            get_response = vk_api.friends.getRequests(out=0, access_token=secret.vk_token,
                                                      v=5.62)  # Запрос истории переписки
            if get_response['count'] > 0:  # Если в ответе есть новые заявки
                for item in get_response['items']:
                    name = get_name(message, item)
                    keyboard = telebot.types.InlineKeyboardMarkup()
                    add = telebot.types.InlineKeyboardButton(text='Добавить', callback_data='add_' + str(item))
                    keyboard.add(add)
                    bot.send_message(secret.apple_id, '*{0}* хочет добавиться в друзья\nvk.com/id{1}'.format(name, item),
                                     reply_markup=keyboard, parse_mode='Markdown')
                    vk_api.friends.delete(user_id=item, access_token=secret.vk_token, v=5.62)
        else:
            send_error(message, 12)
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции new_frinds:\n\n' + str(e))


# # # # # # Общие команды
# Функция вызова подключения прокси
@bot.message_handler(commands=['fuckrkn'])
def fuckrkn(message):
    try:
        try:
            user_id = constants.tg_ids.index(message.from_user.id)
            if user_id is not None:
                keyboard = telebot.types.InlineKeyboardMarkup()
                n_proxy = 46  # random.randint(0, len(constants.proxy) - 1)
                proxy = telebot.types.InlineKeyboardButton(text='Подключить прокси 🚀', url=constants.proxy[n_proxy])
                keyboard.add(proxy)
                bot.send_message(message.chat.id, constants.fuckrkn, parse_mode='Markdown', reply_markup=keyboard)
                bot.send_message(secret.tg_requests_chat_id, '🚀 */fuckrkn* от [{0}](tg://user?id={1})'
                                                                '\n*Чат:* {2}\n*Прокси №{3}:* '
                                                                '\n{4}'.format(constants.tg_names[user_id],
                                                                               str(message.from_user.id),
                                                                               str(message.chat.id), str(n_proxy),
                                                                               constants.proxy[n_proxy].replace('_',
                                                                                                                '\\_')),
                                 parse_mode='Markdown', disable_web_page_preview=True)
        except:
            send_error(message, 29)
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции fuckrkn:\n\n' + str(e))


# Функция отправки опроса в чат
@bot.message_handler(commands=['who'])
def who_will(message):
    try:
        try:
            user_id = constants.tg_ids.index(message.from_user.id)
            if user_id is not None:
                bot.send_message(secret.tg_requests_chat_id, '✅ */who* от [{0}](tg://user?id={1})\n'
                                                                '*Чат:* {2}'.format(constants.tg_names[user_id],
                                                                                    str(message.from_user.id),
                                                                                    str(message.chat.id)),
                                 parse_mode='Markdown')
                force_reply = telebot.types.ForceReply(True)
                bot.send_message(message.chat.id, constants.enter_question, reply_to_message_id=message.message_id,
                                 reply_markup=force_reply)
        except:
            send_error(message, 2)
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции who_will:\n\n' + str(e))


# Отправка скидок
@bot.message_handler(commands=['discount'])
def send_discount(message):
    try:
        user_id = constants.tg_ids.index(message.from_user.id)
        if user_id is not None:
            if user_id is 16:
                bot.send_message(message.chat.id, '🛒 [Перекресток](https://i.imgur.com/my5Q8RF.jpg)',
                                 reply_markup=keyboard_perik,
                                 parse_mode='Markdown')
            elif user_id is 18:
                bot.send_message(message.chat.id, '🛒 [Перекресток](https://i.imgur.com/my5Q8RF.jpg)',
                                 reply_markup=keyboard_perik,
                                 parse_mode='Markdown')
            else:
                bot.send_message(message.chat.id, '🛒 [О\'КЕЙ](https://i.imgur.com/TZV4nCd.jpg)', reply_markup=keyboard_okey,
                                 parse_mode='Markdown')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции send_discount:\n\n' + str(e))


# Отправка ссылки на канал Shobla Music
@bot.message_handler(commands=['music'])
def send_invite_link(message):
    try:
        user_id = constants.tg_ids.index(message.from_user.id)
        if user_id is not None:
            keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
            channel = telebot.types.InlineKeyboardButton(text='Осн. канал 🎵', url='https://t.me/shoblamisuc')
            youtube = telebot.types.InlineKeyboardButton(text='YouTube 🔊',
                                                         url='https://www.youtube.com/playlist?list=PLMFYsuwPgRL3YH-tNyB5dh3VhBF40m9XG')
            kach = telebot.types.InlineKeyboardButton(text='Чтобы качало 😎', url='https://t.me/shoblakach')
            dance = telebot.types.InlineKeyboardButton(text='Потанцевать 💃', url='https://t.me/shobladance')
            keyboard.add(channel, youtube)
            keyboard.add(kach, dance)
            bot.send_message(message.chat.id, '🎧 Добро пожаловать в общий плейлист *Shobla Music*!', parse_mode='Markdown',
                             reply_markup=keyboard)
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции send_invite_link:\n\n' + str(e))


# Функция опроса про фильм
@bot.message_handler(commands=['kinch'])
def who_will_kinch(message):
    try:
        user_id = constants.tg_ids.index(message.from_user.id)
        if user_id is not None:
            bot.send_message(secret.tg_requests_chat_id, '🎬 */kinch* от [{0}](tg://user?id={1})\n'
                                                            '*Чат:* {2}'.format(constants.tg_names[user_id],
                                                                                str(message.from_user.id),
                                                                                str(message.chat.id)),
                             parse_mode='Markdown')
            force_reply = telebot.types.ForceReply(True)
            bot.send_message(message.chat.id, constants.send_movie, reply_to_message_id=message.message_id,
                             reply_markup=force_reply)
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции who_will_kinch:\n\n' + str(e))

# Отправка стикера со статистикой про Коронавирус в шоблу
# @bot.message_handler(commands=['corona'])
# def corona(message):
#     try:
#         bot.send_sticker(secret.tg_chat_id, 'CAACAgIAAxkBAAJ7k16EtnmSM4Wzy5BjSryqZymDondiAAK3oAIAAZJlSgvdtGD02Ww35xgE')  # Мир
#         bot.send_sticker(secret.tg_chat_id, 'CAACAgIAAxkBAAJ7jV6EthT3WNF6k-BA1cyMC4A395VyAAK4oAIAAZJlSgtYkgABa0Y4cncYBA')  # Россия
#     except Exception as e:
#         bot.send_message(secret.apple_id, 'Ошибка в функции corona:\n\n' + str(e))

# # # # # # Обработка данных
# Обработка девки за рулем
# TODO: deprecated. Need delete if function below will be approved
@bot.message_handler(func=lambda
        message: message.text and message.text.lower() in constants.dvk and message.chat.id == secret.tg_chat_id)
def aaa(message):
    try:
        bot.send_message(secret.tg_chat_id, 'Двк з рлм')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции aaa:\n\n' + str(e))


@bot.message_handler(func=lambda
        message: message.text and message.text.lower() in constants.devka and message.chat.id == secret.tg_chat_id)
# TODO: message: message.text and is_message_has_only_a_char(message.text) and message.chat.id == secret.tg_chat_id)
def aaaa(message):
    try:
        #if (len(message.text) <= 3):
        #    bot.send_message(secret.tg_chat_id, 'Двк з рлм')
        #else:
        #    bot.send_message(secret.tg_chat_id, 'Девка за рулём')

        bot.send_message(secret.tg_chat_id, 'Девка за рулём')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции aaaa:\n\n' + str(e))


# Обработка врача
@bot.message_handler(func=lambda
        message: message.text and message.text.lower() in constants.vracha and message.chat.id == secret.tg_chat_id)
def vracha(message):
    try:
        bot.send_document(secret.tg_chat_id, 'CgADAgADRgIAAkbDcEn-Ox-uqrgsHgI', caption='@oxy_genium')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции vracha:\n\n' + str(e))


# Обработка гита
# @bot.message_handler(func=lambda
#         message: constants.git1 in message.text.lower() and message.chat.id == secret.tg_chat_id)
# def git1(message):
#     try:
#         bot.send_message(secret.tg_chat_id, 'Хуит')
#     except Exception as e:
#         bot.send_message(secret.apple_id, 'Ошибка в функции git1:\n\n' + str(e))


@bot.message_handler(func=lambda
        message: message.text and message.text.lower() in constants.git2 and message.chat.id == secret.tg_chat_id)
def git2(message):
    try:
        bot.send_message(secret.tg_chat_id, 'Хуит')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции git2:\n\n' + str(e))

# Обработка @team
@bot.message_handler(func=lambda
        message: message.text and constants.team in message.text.lower() and message.chat.id == secret.tg_chat_id)
def team(message):
    try:
        bot.send_message(chat_id=secret.tg_chat_id, disable_notification=False, reply_to_message_id=message.message_id , text='⚠️ *Внимание, Шобла*\n\n[Тарс](t.me/shackoor), [Апол](t.me/apoll), [Ивановский](t.me/ivanovmm), [Конатик](t.me/KanatoF), [Кир](t.me/zhuykovkb), [Катя](tg://user?id=434756061), [Максон](t.me/MrGogu), [Носик](tg://user?id=51994109), [Окз](t.me/oxy_genium), [Паузеньк](t.me/Pausenk), [НТЩ](t.me/ntshch), [Толяновский](t.me/toliyansky), [Виктор](t.me/FrelVick), [Морго](t.me/margoiv_a), [Мишаня](t.me/Mich37), [Ксю](t.me/ksenia_boorda), [Ромолэ](t.me/Roman_Kazitskiy), [Эльтос](t.me/elvira_aes), [Аня](t.me/kebushka), [Деннис](tg://user?id=503404575)', disable_web_page_preview=True, parse_mode="MarkdownV2")
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции team:\n\n' + str(e))

# Обработка @rapid
@bot.message_handler(func=lambda
        message: message.text and message.text.lower().startswith(constants.rapid) and message.chat.id == secret.tg_chat_id)
def rapid(message):
    try:
        # Сплитуем строку выпилив предварительно ненужные пробелы по бокам
        data = message.text.lower().strip().split(" ")
    
        # Получаем количество элементов сплитованой строки
        # и если тока 1 элемент то значит аргумент не передали
        # следовательно help по дефолту
        size = len(data)
        value = 'help' if size == 1 else data[1]
        
        # Ну тут почти без изменений, тока data[1] became value
        response = urllib2.urlopen('https://https.tyamsha.keenetic.name/rapid?data=' + quote(value) + '&memberid=' + str(message.from_user.id))
        answer = json.loads(str(response.read(), 'utf-8'))
        bot.send_message(secret.tg_chat_id, answer['message'], parse_mode='Markdown')
    except Exception as e:
        bot.send_message(secret.zhuykovkb_apple_id, 'Ошибка в функции rapid:\n\nДанные ' + quote(value) + '\n\nТекст ошибки ' + str(e))

# Обработка барсука
@bot.message_handler(func=lambda
        message: message.text and message.text.lower() in constants.suk and message.chat.id == secret.tg_chat_id)
def barsuk(message):
    try:
        bot.send_message(secret.tg_chat_id, 'Барсук')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции barsuk:\n\n' + str(e))
        

# Обработка барсюка
@bot.message_handler(func=lambda
        message: message.text and message.text.lower() in constants.syuk and message.chat.id == secret.tg_chat_id)
def barsyuk(message):
    try:
        bot.send_message(secret.tg_chat_id, 'Барсюк')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции barsyuk:\n\n' + str(e))
        

# Обработка IPv6
@bot.message_handler(func=lambda
        message: message.text and message.text.lower() in constants.ip_block and message.chat.id == secret.tg_chat_id)
def block(message):
    try:
        bot.send_message(secret.tg_chat_id, 'Значит так, - сразу нахуй!')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в функции block:\n\n' + str(e))
        

# Обработчик текста
@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        # Если это реплай
        if message.reply_to_message is not None and message.reply_to_message.from_user.id == secret.bot_id:
            if message.reply_to_message.text[0:23] == '💬 Что написать в Шоблу?':
                try:
                    bot.send_message(secret.tg_chat_id, message.text)
                    bot.send_message(secret.apple_id, '✅ Сообщение отправлено')
                except:
                    send_error(message, 13)
            # Запрос внесения опроса
            elif message.reply_to_message.text == constants.enter_question:
                try:
                    date = str(time.time() + 10800)
                    date = date.split('.')[0]
                    # Копирование пустого опроса в who
                    bashCopy = "cp /root/router/shoblabot/opros /root/router/shoblabot/who"
                    processC = subprocess.Popen(bashCopy.split(), stdout=subprocess.PIPE)
                    time.sleep(1)
                    # Переименование опроса в date
                    bashRename = 'mv /root/router/shoblabot/who/opros /root/router/shoblabot/who/{0}'.format(date)
                    processR = subprocess.Popen(bashRename.split(), stdout=subprocess.PIPE)
                    opros = '*Опрос:* ' + message.text
                    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
                    # button = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
                    button = [None] * who_count
                    i = 0
                    while i < who_count - 1:
                        button[i] = telebot.types.InlineKeyboardButton(text=constants.who_will[0][i],
                                                                       callback_data='opr_' + str(i) + '_' + date)
                        button[i + 1] = telebot.types.InlineKeyboardButton(text=constants.who_will[0][i + 1],
                                                                           callback_data='opr_' + str(i + 1) + '_' + date)
                        keyboard.add(button[i], button[i + 1])
                        i += 2
                    if 1 == who_count % 2:
                        button[i] = telebot.types.InlineKeyboardButton(text=constants.who_will[0][i],
                                                                       callback_data='opr_' + str(i) + '_' + date)
                        keyboard.add(button[i])
                    bot.send_message(secret.tg_chat_id, opros, reply_markup=keyboard, parse_mode='Markdown')
                    bot.send_message(secret.tg_requests_chat_id, date, parse_mode='Markdown')
                except:
                    bot.send_message(message.chat.id, constants.errors[14])
                    send_error(message, 14)
            elif message.reply_to_message.text == constants.send_movie:
                try:
                    moviename = message.text
                    moviename = moviename.replace('"', '')
                    moviename = moviename.replace('\'', '')
                    # date = message.date + 10800
                    if moviename is '':  # Введено некорректное название фильма
                        send_error(message, 15)
                        force_reply = telebot.types.ForceReply(True)
                        bot.send_message(message.chat.id, constants.send_movie,
                                         reply_to_message_id=message.message_id, reply_markup=force_reply)
                    else:  # Все введено корректно
                        ######################
                        try:
                            bot.send_message(message.chat.id, constants.tmdb_search, parse_mode='Markdown')
                            tmdb.API_KEY = secret.tmdb_token
                            search = tmdb.Search()
                            keyboard = telebot.types.InlineKeyboardMarkup()
                            movies = search.movie(query=moviename, language='ru')
                            if movies['total_results'] != 0:
                                sorted_movies = sorted(movies['results'], key=lambda k: k['popularity'], reverse=True)
                                for movie in sorted_movies:
                                    if movie['release_date'] is not '':
                                        name = movie['title'] + ' (' + movie['release_date'].split('-')[0] + ')'
                                    else:
                                        name = movie['title']
                                    button = telebot.types.InlineKeyboardButton(text=name,
                                                                                callback_data='tmdb_' + str(movie['id']))
                                    keyboard.add(button)
                                no_film = telebot.types.InlineKeyboardButton(text=constants.no_film,
                                                                             callback_data='no_tmdb')
                                keyboard.add(no_film)
                                text = '{0}*"{1}"*.'.format(constants.tmdb_choose, moviename)
                                bot.send_message(secret.tg_chat_id, text, reply_markup=keyboard, parse_mode='Markdown')
                            else:
                                text = '{0}*"{1}"*?'.format(constants.no_tmdb, moviename)
                                button_yes = telebot.types.InlineKeyboardButton(text=constants.da_net[0],
                                                                                callback_data='save_my_movie')
                                button_no = telebot.types.InlineKeyboardButton(text=constants.da_net[1],
                                                                               callback_data='dont_save')
                                keyboard.add(button_yes, button_no)
                                if message.chat.id != secret.tg_chat_id:
                                    bot.send_message(message.chat.id,
                                                     'Перейди в [Шоблу](https://t.me/joinchat/AAtLBEMmWssNkWB1BBQX9g) для выбора фильма 🎬',
                                                     parse_mode='Markdown', disable_web_page_preview=True)
                                bot.send_message(secret.tg_chat_id, text, reply_markup=keyboard, parse_mode='Markdown')
                        except:
                            bot.send_message(message.chat.id, constants.errors[9])
                            send_error(message, 16)
                except:
                    bot.send_message(message.chat.id, constants.errors[10])
                    send_error(message, 17)
            elif message.text == '@shoblabot':
                bot.pin_chat_message(chat_id=secret.tg_chat_id, message_id=message.reply_to_message.message_id,
                                     disable_notification=False)
        elif message.reply_to_message is not None and message.text == '@shoblabot':
            bot.pin_chat_message(chat_id=secret.tg_chat_id, message_id=message.reply_to_message.message_id,
                                 disable_notification=False)
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в обработчике текста send_text:\n\n' + str(e))

# Обработчик Call Back Data
@bot.callback_query_handler(func=lambda call: True)
def callback_buttons(call):
    try:
        # Вызов панели администратора
        if call.data[0:4] == 'adm_':
            command = call.data.split('_')[1]
            if command == 'rm':
                try:
                    subprocess.Popen(["bash", "/root/router/start3"])
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                              text='🎬 Movies Bot запущен')
                except:
                    send_error(call.message, 18)
            elif command == 'rf':
                try:
                    subprocess.Popen(["bash", "/root/router/startfuel"])
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                              text='⛽️ Fuel Bot запущен')
                except:
                    send_error(call.message, 19)
            elif command == 'rb':
                try:
                    subprocess.Popen(["bash", "/root/router/startbooks"])
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                              text='📙 Books Bot запущен')
                except:
                    send_error(call.message, 20)
            elif command == 'si':
                try:
                    ram = psutil.virtual_memory()
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                              text='💽 RAM: {0}%'.format(ram[2]))
                except:
                    send_error(call.message, 21)
            elif command == 'sc':
                try:
                    global screen_id
                    # movies = glob.glob('/var/run/screen/S-root/*.movies')
                    # books = glob.glob('/var/run/screen/S-root/*.books')
                    # fuel = glob.glob('/var/run/screen/S-root/*.fuel')
                    # router = glob.glob('/var/run/screen/S-root/*.router')
                    shoblabot = glob.glob('/var/run/screen/S-root/*.shobla')
                    # screen_id = movies[0].split('t/')[1] + ' ' + books[0].split('t/')[1] + ' ' + fuel[0].split('t/')[
                    #     1] + ' ' + router[0].split('t/')[1] + ' ' + shoblabot[0].split('t/')[1]
                    # screen_id = movies[0].split('t/')[1] + ' ' + shoblabot[0].split('t/')[1]
                    screen_id = shoblabot[0].split('t/')[1]
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text='📑 ' + screen_id)
                except:
                    send_error(call.message, 22)
            elif command == 'sh':
                try:
                    force_reply = telebot.types.ForceReply(True)
                    bot.send_message(secret.apple_id, '💬 Что написать в Шоблу?', reply_markup=force_reply)
                except:
                    send_error(call.message, 23)
        elif call.data[0:2] == 'op':
            user_id = int(call.data.split('_')[1])
            try:
                date = call.data.split('_')[2]
                if call.from_user.id == constants.who_will_ids[user_id]:
                    # Загружаем данные из файла date
                    if os.path.isfile('/root/router/shoblabot/who/{0}'.format(date)):
                        with open('/root/router/shoblabot/who/{0}'.format(date), 'r') as lang:
                            who_opros = json.loads(lang.read())
                    who_opros[str(call.from_user.id)] = (who_opros[str(call.from_user.id)] + 1) % 3 + 1
                    # button = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
                    button = [None] * who_count
                    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
                    i = 0
                    while i < who_count - 1:
                        button[i] = telebot.types.InlineKeyboardButton(text=constants.who_will[who_opros[str(constants.who_will_ids[i])]][i],callback_data='opr_' + str(i) + '_' + date)
                        button[i + 1] = telebot.types.InlineKeyboardButton(text=constants.who_will[who_opros[str(constants.who_will_ids[i + 1])]][i + 1],callback_data='opr_' + str(i + 1) + '_' + date)
                        keyboard.add(button[i], button[i + 1])
                        i += 2
                    if 1 == who_count % 2:
                        button[i] = telebot.types.InlineKeyboardButton(
                            text=constants.who_will[who_opros[str(constants.who_will_ids[i])]][i],
                            callback_data='opr_' + str(i) + '_' + date)
                        keyboard.add(button[i])
                    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                  reply_markup=keyboard)
                    if who_opros[str(1)] == 0:
                        who_opros[str(1)] = 1
                        bot.pin_chat_message(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                             disable_notification=False)
                    # Записываем данные в файл
                    with open('/root/router/shoblabot/who/{0}'.format(date), 'w') as lang:
                        lang.write(json.dumps(who_opros))
            except:
                send_error(call.message, 24)
                bot.send_message(secret.apple_id, '*Ошибка от:* {0}'.format(constants.who_will[0][user_id]),
                                 parse_mode='Markdown')
        elif call.data[0:2] == 'kp':
            user_id = int(call.data.split('_')[1])
            try:
                date = call.data.split('_')[2]
                if call.from_user.id == constants.who_will_ids[user_id]:
                    # Загружаем данные из файла date
                    if os.path.isfile('/root/router/shoblabot/kinch/{0}'.format(date)):
                        with open('/root/router/shoblabot/kinch/{0}'.format(date), 'r') as lang:
                            who_opros = json.loads(lang.read())
                    who_opros[str(call.from_user.id)] = (who_opros[str(call.from_user.id)] + 1) % 3 + 1
                    # button = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
                    button = [None] * who_count
                    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
                    i = 0
                    while i < who_count - 1:
                        button[i] = telebot.types.InlineKeyboardButton(
                            text=constants.who_will[who_opros[str(constants.who_will_ids[i])]][i],
                            callback_data='kpr_' + str(i) + '_' + date)
                        button[i + 1] = telebot.types.InlineKeyboardButton(
                            text=constants.who_will[who_opros[str(constants.who_will_ids[i + 1])]][i + 1],
                            callback_data='kpr_' + str(i + 1) + '_' + date)
                        keyboard.add(button[i], button[i + 1])
                        i += 2
                    if 1 == who_count % 2:
                        button[i] = telebot.types.InlineKeyboardButton(
                            text=constants.who_will[who_opros[str(constants.who_will_ids[i])]][i],
                            callback_data='kpr_' + str(i) + '_' + date)
                        keyboard.add(button[i])
                    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                  reply_markup=keyboard)
                    if who_opros[str(1)] == 0:
                        who_opros[str(1)] = 1
                        bot.pin_chat_message(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                             disable_notification=True)
                    # Записываем данные в файл
                    with open('/root/router/shoblabot/kinch/{0}'.format(date), 'w') as lang:
                        lang.write(json.dumps(who_opros))
            except:
                send_error(call.message, 25)
                bot.send_message(secret.apple_id, '*Ошибка от:* {0}'.format(constants.who_will[0][user_id]),
                                 parse_mode='Markdown')
        elif call.data[0:5] == 'tmdb_':
            m_id = call.data.split('_')[1]
            try:
                tmdb.API_KEY = secret.tmdb_token
                moviename = tmdb.Movies(int(m_id)).info(language='ru')['title']
                moviename = moviename.replace('"', '')
                moviename = moviename.replace('\'', '')
                link = 'https://www.themoviedb.org/movie/' + m_id
                info = tmdb.Movies(int(m_id)).info(language='ru')
                moviename = info['title']
                original_title = info['original_title']
                if info['release_date'] is not '':
                    year = info['release_date'].split('-')[0]
                    premier = info['release_date'][8:10] + ' '
                    premier += constants.info_month[int(info['release_date'][5:7])] + ' ' + year
                else:
                    year = 'N/A'
                    premier = 'N/A'
                genre = info['genres']
                genres = ''
                for item in genre:
                    genres += item['name'] + ', '
                imdb_link = 'http://www.imdb.com/title/' + info['imdb_id']
                rating = info['vote_average']
                description = info['overview']
                if description is not None:
                    description = description.replace('<br>', '\n')
                    description = description.replace('<br/>', '\n')
                    description = description.replace('<br />', '\n')
                runtime = info['runtime']
                try:
                    runtime = str(runtime) + ' мин / ' + str(timedelta(minutes=int(runtime)))[:-3]
                except:
                    runtime = '-'
                text = '*{0}* _({1})_\n🇬🇧 *Eng:* {2}\n🎭 *{3}:* {4}\n⭐️ *{5}:* ' \
                       '{6}\n📅 *{7}:* {8}\n⏰ *{9}*: {10}\nℹ️ *{11}*: {12}'.format(moviename, year, original_title,
                                                                                   constants.info_fields[0], genres[0:-2],
                                                                                   constants.info_fields[8], rating,
                                                                                   constants.info_fields[3], premier,
                                                                                   constants.info_fields[9], runtime,
                                                                                   constants.info_fields[6], description)
                date = str(time.time() + 10800)
                date = date.split('.')[0]
                # Копирование пустого опроса в who
                bashCopy = "cp /root/router/shoblabot/opros /root/router/shoblabot/kinch"
                processC = subprocess.Popen(bashCopy.split(), stdout=subprocess.PIPE)
                time.sleep(1)
                # Переименование опроса в date
                bashRename = 'mv /root/router/shoblabot/kinch/opros /root/router/shoblabot/kinch/{0}'.format(date)
                processR = subprocess.Popen(bashRename.split(), stdout=subprocess.PIPE)
                opros = '*Опрос*: кто пойдет на фильм?\n{0}\n' \
                        '[{1}]({2})\n[{3}]({4})'.format(text, constants.info_link[0], link,
                                                        constants.info_link[1], imdb_link)
                keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
                # button = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
                button = [None] * who_count
                i = 0
                while i < who_count - 1:
                    button[i] = telebot.types.InlineKeyboardButton(text=constants.who_will[0][i],
                                                                   callback_data='kpr_' + str(i) + '_' + date)
                    button[i + 1] = telebot.types.InlineKeyboardButton(text=constants.who_will[0][i + 1],
                                                                       callback_data='kpr_' + str(i + 1) + '_' + date)
                    keyboard.add(button[i], button[i + 1])
                    i += 2
                if 1 == who_count % 2:
                    button[i] = telebot.types.InlineKeyboardButton(text=constants.who_will[0][i],
                                                                   callback_data='kpr_' + str(i) + '_' + date)
                    keyboard.add(button[i])
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=opros, reply_markup=keyboard, parse_mode='Markdown',
                                      disable_web_page_preview=True)
            except:
                send_error(call.message, 26)
                bot.send_message(secret.apple_id, '*Ошибка от:* {0}'.format(
                    constants.who_will[0][constants.who_will_ids.index(call.from_user.id)]), parse_mode='Markdown')
                try:
                    link = 'https://www.themoviedb.org/movie/' + m_id
                    date = str(time.time() + 10800)
                    date = date.split('.')[0]
                    # Копирование пустого опроса в who
                    bashCopy = "cp /root/router/shoblabot/opros /root/router/shoblabot/kinch"
                    processC = subprocess.Popen(bashCopy.split(), stdout=subprocess.PIPE)
                    time.sleep(1)
                    # Переименование опроса в date
                    bashRename = 'mv /root/router/shoblabot/kinch/opros /root/router/shoblabot/kinch/{0}'.format(date)
                    processR = subprocess.Popen(bashRename.split(), stdout=subprocess.PIPE)
                    opros = '*Опрос:* кто пойдет на фильм:\n{0}'.format(link)
                    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
                    # button = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
                    button = [None] * who_count
                    i = 0
                    while i < who_count - 1:
                        button[i] = telebot.types.InlineKeyboardButton(text=constants.who_will[0][i],
                                                                       callback_data='kpr_' + str(i) + '_' + date)
                        button[i + 1] = telebot.types.InlineKeyboardButton(text=constants.who_will[0][i + 1],
                                                                           callback_data='kpr_' + str(i + 1) + '_' + date)
                        keyboard.add(button[i], button[i + 1])
                        i += 2
                    if 1 == who_count % 2:
                        button[i] = telebot.types.InlineKeyboardButton(text=constants.who_will[0][i],
                                                                       callback_data='kpr_' + str(i) + '_' + date)
                        keyboard.add(button[i])
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text=opros, reply_markup=keyboard, parse_mode='Markdown',
                                          disable_web_page_preview=True)
                except:
                    bot.send_message(call.message.chat.id, constants.errors[27])
                    send_error(call.message, 27)
                    bot.send_message(secret.apple_id, '*Ошибка от:* {0}'.format(
                        constants.who_will[0][constants.who_will_ids.index(call.from_user.id)]), parse_mode='Markdown')
        elif call.data == 'no_tmdb':
            try:
                moviename = str(call.message.text.split('"')[1])
                text = '{0}*"{1}"*?'.format(constants.no_tmdb_yes_no, moviename)
                keyboard = telebot.types.InlineKeyboardMarkup()
                button_yes = telebot.types.InlineKeyboardButton(text=constants.da_net[0],
                                                                callback_data='save_my_movie')
                button_no = telebot.types.InlineKeyboardButton(text=constants.da_net[1],
                                                               callback_data='dont_save')
                keyboard.add(button_yes, button_no)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text,
                                      reply_markup=keyboard, parse_mode='Markdown', disable_web_page_preview=True)
            except:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=constants.tmdb_errors[1], parse_mode='Markdown',
                                      disable_web_page_preview=True)
                bot.send_message(secret.apple_id,
                                 'Боту пишет ОШИБКА id: ' + str(call.from_user.id) + '\n' + constants.tmdb_errors[1])
        elif call.data == 'save_my_movie':
            try:
                moviename = str(call.message.text.split('"')[1])
                moviename = moviename.replace('"', '')
                moviename = moviename.replace('\'', '')
                date = str(time.time() + 10800)
                date = date.split('.')[0]
                # Копирование пустого опроса в who
                bashCopy = "cp /root/router/shoblabot/opros /root/router/shoblabot/kinch"
                processC = subprocess.Popen(bashCopy.split(), stdout=subprocess.PIPE)
                time.sleep(1)
                # Переименование опроса в date
                bashRename = 'mv /root/router/shoblabot/kinch/opros /root/router/shoblabot/kinch/{0}'.format(date)
                processR = subprocess.Popen(bashRename.split(), stdout=subprocess.PIPE)
                link = 'https://www.google.ru/search?q={0}'.format(moviename.replace(' ', '+'))
                opros = '*Опрос*: кто пойдет на фильм {0}?\n[Найти в Google]({1})'.format(moviename, link)
                keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
                # button = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
                button = [None] * who_count
                i = 0
                while i < who_count - 1:
                    button[i] = telebot.types.InlineKeyboardButton(text=constants.who_will[0][i],
                                                                   callback_data='kpr_' + str(i) + '_' + date)
                    button[i + 1] = telebot.types.InlineKeyboardButton(text=constants.who_will[0][i + 1],
                                                                       callback_data='kpr_' + str(i + 1) + '_' + date)
                    keyboard.add(button[i], button[i + 1])
                    i += 2
                if 1 == who_count % 2:
                    button[i] = telebot.types.InlineKeyboardButton(text=constants.who_will[0][i],
                                                                   callback_data='kpr_' + str(i) + '_' + date)
                    keyboard.add(button[i])
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=opros, parse_mode='Markdown', reply_markup=keyboard,
                                      disable_web_page_preview=True)
            except:
                bot.send_message(call.message.chat.id, constants.errors[28])
                send_error(call.message, 28)
                bot.send_message(secret.apple_id, '*Ошибка от:* {0}'.format(
                    constants.who_will[0][constants.who_will_ids.index(call.from_user.id)]), parse_mode='Markdown')
        elif call.data == 'dont_save':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=constants.canceled, parse_mode='Markdown')
        elif call.data == 'okey':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🛒 [О\'кей](https://i.imgur.com/TZV4nCd.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_okey)
        elif call.data == 'bushe':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🥐 [Буше](https://i.imgur.com/H6ins0K.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_bushe)
        elif call.data == 'dosta':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🍕 [Достаевский](https://i.imgur.com/LTx5ztX.jpg)\n*ТОЛЬКО ПРИ ЗАКАЗЕ ПО ТЕЛЕФОНУ*',
                                  parse_mode='Markdown', reply_markup=keyboard_dosta)
        elif call.data == 'pyatera':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🛒 [Пятерочка](https://i.imgur.com/yTuhGWH.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_pyatera)
        elif call.data == 'perik':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🛒 [Перекресток](https://i.imgur.com/my5Q8RF.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_perik)
        elif call.data == 'lenta':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🛒 [Лента](https://i.imgur.com/Cf4GkXUh.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_lenta)
        elif call.data == 'domovoi':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🛠 [Домовой](https://i.imgur.com/Tnn5WTG.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_domovoi)
        elif call.data == 'ikea':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🛋 [Икеа](https://i.imgur.com/ThL03zt.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_ikea)
        elif call.data == 'polushka':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🛒 [Полушка](https://i.imgur.com/3SvY9T7.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_polushka)
        elif call.data == 'karusel':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🛒 [Карусель](https://i.imgur.com/vwY6SB3.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_karusel)
        elif call.data == 'krasnoe':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🍷 [К&Б](https://i.imgur.com/l9g2rO3.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_krasnoe)
        elif call.data == 'podr':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='💅 [Подружка](https://i.imgur.com/0NGsUpZ.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_podr)
        elif call.data == 'sephora':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🖤 [Sephora](https://i.imgur.com/qm2RlMr.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_sephora)
        elif call.data == 'prisma':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🛒 [Prisma](https://i.imgur.com/tcFfgho.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_prisma)
        elif call.data == 'lime':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🛒 [Лайм](https://i.imgur.com/hq39niT.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_lime)
        elif call.data == 'ulibka':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='[Улыбка](https://i.imgur.com/bpcYZ2v.jpg) 🌈', parse_mode='Markdown',
                                  reply_markup=keyboard_ulibka)
        elif call.data == 'letual':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='💛 [Л\'этуль](https://i.imgur.com/CqWU2vj.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_letual)
        elif call.data == 'ozerki':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='💊 [Озерки](https://i.imgur.com/6bDnAK4.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_ozerki)
        elif call.data == 'spar':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='🛒 [SPAR](https://i.imgur.com/pi3xSt3.jpg)', parse_mode='Markdown',
                                  reply_markup=keyboard_spar)
        ########################
        elif call.data[0:4] == 'add_':
            user_id = int(call.data.split('_')[1])
            vk_api.friends.add(user_id=user_id, access_token=secret.vk_token, v=5.62)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Заявка принята')
    except Exception as e:
        bot.send_message(secret.apple_id, 'Ошибка в обработчике Callback кнопок callback_buttons:\n\n' + str(e))


# Отправка сообщения по перезагрузке бота
def reboot_me():
    try:
        threading.Timer(3600, reboot_me).start()  # Каждые полчаса - 1800, каждые 10 мин - 600, каждый день - 86400
        now_time = datetime.datetime.now()
        bot.send_message(secret.apple_id, str(now_time.hour + 8))
        if (now_time.hour + 8) is not 23:
            return
        if os.path.isfile('/root/router/shoblabot/reboot_or_not'):
            with open('/root/router/shoblabot/reboot_or_not', 'r') as lang:
                reboot_or_not = json.loads(lang.read())
        bot.send_message(secret.apple_id, str(reboot_or_not['1']))
        if reboot_or_not['1'] == 1:
            # Перезагрузка бота
            reboot_or_not['1'] = 0
            with open('/root/router/shoblabot/reboot_or_not', 'w') as lang:
                lang.write(json.dumps(reboot_or_not))
            bot.send_message(secret.apple_id, "go to reboot")
            # subprocess.Popen(["bash", "/root/router/start3"])
            bot.send_message(secret.apple_id, "reboot is done")
        elif reboot_or_not['1'] == 0:
            reboot_or_not['1'] = 1
            with open('/root/router/shoblabot/reboot_or_not', 'w') as lang:
                lang.write(json.dumps(reboot_or_not))
            bot.send_message(secret.apple_id, "reboot is not ready")
    except Exception as e:
        bot.send_message(secret.apple_id,
                         'Ошибка в функции отправки сообщения по перезагрузке бота reboot_me():\n\n' + str(e))


# Отправка поздравления с др в Шоблу
def sdr():
    try:
        threading.Timer(3600, sdr).start()  # Каждые полчаса - 1800, каждые 10 мин - 600
        now_time = datetime.datetime.now()
        dr = str(now_time.day) + '.' + str(now_time.month)
        i = 0
        if (now_time.hour + 8) is not 10:
            return
        if dr == str(28.5):  # День Баяна в Шобле отмечается 28 мая
                bot.send_message(secret.tg_chat_id, 'Шобла, поздравляю с Днём Баяна🪗!🕺💃🥳', parse_mode='Markdown')
        for item in constants.tg_drs:
            if item == dr:
                bot.send_message(secret.tg_chat_id,
                                 '[{0}](tg://user?id={1}), с др!'.format(constants.tg_names[i], constants.tg_ids[i]),
                                 parse_mode='Markdown')
            i += 1
    except Exception as e:
        bot.send_message(secret.apple_id,
                         'Ошибка в функции отправки поздравления в Шоблу sdr():\n\n' + str(e))


# Запуск функций
# try:
# eclair()
# except Exception as e:
# bot.send_message(secret.apple_id, 'Ошибка в запуске встроенный функций:\neclair()\n' + str(e))


try:
    bot.remove_webhook()
except Exception as e:
    bot.send_message(secret.apple_id, 'Ошибка в запуске встроенный функций:\nremove_webjook()\n\n' + str(e))

try:
    send_start_time()
except Exception as e:
    bot.send_message(secret.apple_id, 'Ошибка в запуске встроенный функций:\n\send_start_time()\n\n' + str(e))

try:
    sdr()
except Exception as e:
    bot.send_message(secret.apple_id, 'Ошибка в запуске встроенный функций:\n\sdr()\n\n' + str(e))

# try:
#     backup_base_by_time()
# except Exception as e:
#     bot.send_message(secret.apple_id, 'Ошибка в запуске встроенный функций:\n\backup_base_by_time()\n\n' + str(e))
# try:
#     reboot_me()
# except Exception as e:
#     bot.send_message(secret.apple_id, 'Ошибка в запуске встроенный функций:\nreboot_me()\n\n' + str(e))

# try:
#     # send_vk_dialogs_messages()  # Включаем функцию для получения сообщений из ВКонтакте
#     new_friends()
# except Exception as e:
#     bot.send_message(secret.apple_id,
#                      'Ошибка в запуске встроенный функций:\n# send_vk_dialog_messages\n\new_friends()\n\n' + str(e))

# Отправка стикера о Коронавирусе в Шоблу
# def coronasticker():
#     try:
#         threading.Timer(3600, sdr).start()  # Каждые полчаса - 1800, каждые 10 мин - 600
#         now_time = datetime.datetime.now()
#         if (now_time.hour + 8) is not 10:
#             return
#         bot.send_sticker(secret.tg_chat_id, 'CAACAgIAAxkBAAJ7k16EtnmSM4Wzy5BjSryqZymDondiAAK3oAIAAZJlSgvdtGD02Ww35xgE')  # Мир
#         bot.send_sticker(secret.tg_chat_id, 'CAACAgIAAxkBAAJ7jV6EthT3WNF6k-BA1cyMC4A395VyAAK4oAIAAZJlSgtYkgABa0Y4cncYBA')  # Россия
#     except Exception as e:
#         bot.send_message(secret.apple_id, 'Ошибка в функции отправки поздравления в Шоблу coronasticker():\n\n' + str(e))

# try:
#     coronasticker()
# except Exception as e:
#     bot.send_message(secret.apple_id, 'Ошибка в запуске встроенный функций:\n\coronasticker()\n\n' + str(e))

try:
    bot.polling()
except Exception as e:
    bot.send_message(secret.apple_id, 'Ошибка при запуске bot.polling():\n\n' + str(e))

# class WebhookServer(object):
# index равнозначно /, т.к. отсутствию части после ip-адреса (грубо говоря)
#    @cherrypy.expose
#    def index(self):
#        length = int(cherrypy.request.headers['content-length'])
#        json_string = cherrypy.request.body.read(length).decode("utf-8")
#        update = telebot.types.Update.de_json(json_string)
#        bot.process_new_updates([update])
#        return ''

# if __name__ == '__main__':
#    cherrypy.config.update({
#        'server.socket_host': '127.0.0.1',
#        'server.socket_port': 7771,
#        'engine.autoreload.on': False
#    })
#    cherrypy.quickstart(WebhookServer(), '/', {'/': {}})
