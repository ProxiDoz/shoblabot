import requests
from xml.etree import ElementTree

cbr_url = 'https://www.cbr.ru/scripts/XML_daily.asp'


# Функция парсинга данных по курсу валют с сайти ЦБР с xml-содержимым
def get_exchange_rates():
    try:
        response = requests.get(cbr_url)  # Парсим страницу с xml содержимым
        tree = ElementTree.fromstring(response.content)  # Конвертируем из строки в дерево
        usd = '%.2f' % float(tree[16][5].text.replace(',', '.'))
        eur = '%.2f' % float(tree[17][5].text.replace(',', '.'))
        lar = '%.2f' % float(tree[13][5].text.replace(',', '.'))
        ten = '%.2f' % float(tree[21][4].text.replace(',', '.'))
        date = tree.attrib['Date']
        return usd, eur, lar, ten, date
    except Exception as get_exchange_rates_error:
        return get_exchange_rates_error
