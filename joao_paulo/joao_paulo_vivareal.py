import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import streamlit as st

def scrappingJoao():
  url = "https://www.vivareal.com.br/aluguel/parana/londrina/"
  response = requests.get(url)
  soup = BeautifulSoup(response.content, "html.parser")
  page = soup.find_all("article", class_='property-card__container js-property-card')
  data_list = []
  progress_bar = st.progress(0)

  for i, data in enumerate(page):
    link = data.find("a")["href"]
    link = "https://www.vivareal.com.br"+link

    new_page = requests.get(link)
    soup_imovel = BeautifulSoup(new_page.content, "html.parser")
    description = soup_imovel.find('p', {'class': 'description__text'})

    if description is not None:
      description = description.text.strip()
    else:
      description = ""

    title = data.find("span", class_="property-card__title js-cardLink js-card-title").text.strip()
    details = data.find("ul", class_="property-card__details").text.strip()
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

    address = data.find("span", class_="property-card__address").text.strip()
    value = data.find("p").text.strip()
    value = re.sub(r'[^\d,]', '', value)
    value = float(value.replace(',', '.'))
    value = int(value)

    data_list.append([title, metros_quadrados, quartos, banheiros, address, value, description])
    if (i + 1) % (len(page) // 10) == 0:
      progress_bar.progress((i + 1) / len(page))

  df = pd.DataFrame(data_list, columns=['Título', 'Metros Quadrados', 'Quartos' , 'Banheiros' , 'Endereço', 'Valor', 'Descrição'])
  return df 