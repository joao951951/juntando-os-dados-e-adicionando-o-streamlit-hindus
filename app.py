import streamlit as st
import pandas as pd
from joao_paulo.joao_paulo_vivareal import scrappingJoao

st.title("Web Scraper de Imóveis")

# Cria um botão para executar a função scrape
if st.button("Executar Web Scraper Joao Paulo"):
    df = scrappingJoao()  # Chama a função scrape() do arquivo joao_paulo.py
    st.dataframe(df)  # Exibe o DataFrame resultante na interface do Streamlit
    st.download_button("Download CSV", data=df.to_csv().encode('utf-8'), file_name='imoveis.csv', mime='text/csv')