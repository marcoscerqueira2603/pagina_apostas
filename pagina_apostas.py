import streamlit as st
import pandas as pd

# Função para armazenar e recuperar dados usando cache
@st.cache(allow_output_mutation=True)
def load_data():
    try:
        df = pd.read_csv('data.csv')
    except FileNotFoundError:
        df = pd.DataFrame({'Nome': [], 'Idade': []})
    return df

# Página principal
st.title('Página de Informações')

# Carregar dados usando a função de cache
df = load_data()

# Aba para inserir informações
with st.sidebar:
    st.header('Inserir Informações')
    nome = st.text_input('Nome:')
    idade = st.number_input('Idade:', min_value=0)

    if st.button('Salvar'):
        df = df.append({'Nome': nome, 'Idade': idade}, ignore_index=True)
        df.to_csv('data.csv', index=False)
        st.success('Informações salvas com sucesso!')

# Mostrar DataFrame atualizado
st.write('Informações Atuais:')
st.write(df)
