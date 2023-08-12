import streamlit as st
import pandas as pd
import os

# Carrega os dados existentes do arquivo CSV ou cria um DataFrame vazio
data_file = 'data.csv'
if os.path.exists(data_file):
    df = pd.read_csv(data_file)
else:
    df = pd.DataFrame(columns=['Time A', 'Placar A', 'Time B', 'Placar B'])

# Interface para inserção de novos dados
st.title('Inserir Dados de Jogos de Futebol')
time_a = st.text_input('Time A')
placar_a = st.number_input('Placar A', min_value=0)
time_b = st.text_input('Time B')
placar_b = st.number_input('Placar B', min_value=0)

if st.button('Inserir'):
    new_row = {'Time A': time_a, 'Placar A': placar_a, 'Time B': time_b, 'Placar B': placar_b}
    df = df.append(new_row, ignore_index=True)
    df.to_csv(data_file, index=False)
    st.success('Dados inseridos com sucesso!')

# Mostra os dados inseridos
st.title('Dados de Jogos de Futebol')
st.dataframe(df)


