import requests
from bs4 import BeautifulSoup
import csv
import re

def categorize_items(item_list):
    categories = {
        'Dormitórios': 0,
        'Suítes': 0,
        'Vagas': 0,
        'Banheiros': 0,
        'Metros Quadrados': 0 
    }

    for item in item_list:
        if 'Dormitório' in item:
            categories['Dormitórios'] = int(item.split()[0])
        elif 'Suíte' in item:
            categories['Suítes'] = int(item.split()[0])
        elif 'Vaga' in item:
            categories['Vagas'] = int(item.split()[0])
        elif 'Banheiro' in item:
            categories['Banheiros'] = int(item.split()[0])
        elif 'm²' in item:
            categories['Metros Quadrados'] = int(re.sub('[^0-9]', '', item))

    return categories


url = "https://www.imobiliariaperez.com.br/alugar?preco_minimo=1.800&preco_maximo=2.500&page=1"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

imoveis = soup.find_all("section", class_="elementor-section elementor-inner-section elementor-element elementor-element-36b9f9be list-property-section elementor-section-boxed elementor-section-height-default elementor-section-height-default")

listLink = []

with open('imoveis.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Titulo', 'Metros Quadrados','Quartos', 'Banheiros', 'Endereço', 'Valor', 'Descrição'])

    for section in imoveis:

        titulo = section.find("div", class_="list-title").text.strip()
        link = section.find("a")["href"]
        valor = section.find("div", class_="col-md-12 col-sm-12 list-price").text.strip()

        listLink.append(link)

        # Faz uma nova requisição HTTP GET para obter o conteúdo HTML da página do imóvel
        response_imovel = requests.get(link)
        soup_imovel = BeautifulSoup(response_imovel.content, "html.parser")

        # Encontre a div com a classe
        property_icons_div = soup_imovel.find('div', {'class': 'elementor-element elementor-element-3cc2379d property-icons-div elementor-widget elementor-widget-text-editor'})

        # Encontre todas as divs com a classe 
        col_6_divs = property_icons_div.find_all('div', {'class': 'col-6 col-md-2'})

        item_list = []

        # Adiciona o título, link e os valores dos itens em uma lista
        for col_6_div in col_6_divs:
            item_list.append(col_6_div.text.strip())

        # Categoriza os itens e adiciona as quantidades no arquivo CSV
        categories = categorize_items(item_list)
        writer.writerow([titulo, categories['Metros Quadrados'], categories['Dormitórios'], categories['Banheiros'], 'endereco', valor, 'descricao'])
