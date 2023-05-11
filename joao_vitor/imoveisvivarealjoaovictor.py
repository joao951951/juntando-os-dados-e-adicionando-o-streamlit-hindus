import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

URL = "https://www.vivareal.com.br/aluguel/parana/londrina/"
page = requests.get(URL) 

soup = BeautifulSoup(page.content, 'html.parser')

informacoes = soup.find_all('div', class_='js-card-selector')

data = []
for article in informacoes:
  link = article.find("a")["href"]
  link = "https://www.vivareal.com.br"+link

  new_page = requests.get(link)
  soup_imovel = BeautifulSoup(new_page.content, "html.parser")
  description = soup_imovel.find('p', {'class': 'description__text'})
  description = description.text.strip()

  title = article.find('span', class_='property-card__title js-cardLink js-card-title').text.strip()

  details = article.find("ul", class_="property-card__details").text.strip()

  metros_quadrados = re.search(r'(\d+)\s+m²', details).group(1)
  metros_quadrados = int(metros_quadrados)

  quartos_match = re.search(r'(\d+)\s+Quartos', details)
  if quartos_match is not None:
      quartos = int(quartos_match.group(1))
  else:
      quartos = None

  banheiros_match = re.search(r'(\d+)\s+Banheiros', details)
  if banheiros_match is not None:
      banheiros = int(banheiros_match.group(1))
  else:
      banheiros = None

  localizacao = article.find('span', class_='property-card__address').text.strip()

  valor = article.find('div', class_='property-card__price js-property-card-prices js-property-card__price-small' ).text.strip()
  
  valor  = re.sub('[^0-9]', '', valor)
  valor = int(valor)

  data.append([title, metros_quadrados, quartos, banheiros, localizacao, valor, description])

df = pd.DataFrame(data, columns=['Título', 'Metros Quadrados', 'Quartos' , 'Banheiros' , 'Endereço', 'Valor', 'Descrição'])

df.to_csv('imoveisvivareal.csv', index=False)
