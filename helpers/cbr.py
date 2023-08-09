import requests
from bs4 import BeautifulSoup

url = 'https://www.cbr.ru/currency_base/daily/'

def wordInMessage():
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  
  table = soup.find('table', {'class': 'data'})
  
  for row in table.find_all('tr'):
      tds = row.find_all('td')
      
      if len(tds) == 5 and tds[1].text.strip() == "USD":
          return tds[-1].text

  return "Жеппа твоя доллар"
