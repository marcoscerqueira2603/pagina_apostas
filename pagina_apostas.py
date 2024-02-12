#from turtle import width
from calendar import c
import streamlit as st
import pandas as pd
import os
from openpyxl import load_workbook
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
    
from scipy.stats import poisson

#import json

# Obtém a data atual
data_atual = date.today()

# Formata a data atual no formato "DD/MM/YYYY"
data_formatada = data_atual.strftime('%d/%m/%Y')

# Carrega os dados existentes do arquivo CSV ou cria um DataFrame vazio
st.set_page_config(
    page_title="Apostas",
    layout="wide"
)

st.title('Página de Análise')

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("chave_api.json", scope)
client = gspread.authorize(creds)



@st.cache_data(ttl=20)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

tendencias_2linhas = load_data(st.secrets["url_tendencias_2linhas"])

@st.cache_data(ttl=20)
def load_data2(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

tendencias_2gols = load_data2(st.secrets["url_tendencias_2gols"])

@st.cache_data(ttl=20)
def load_data3(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

entradas_2linhas = load_data3(st.secrets["url_entradas_2linhas"])

@st.cache_data(ttl=20)
def load_data4(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

entradas_2gols = load_data4(st.secrets["url_entradas_2gols"])

@st.cache_data(ttl=20)
def load_data5(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

entradas_anytimes = load_data5(st.secrets["url_entradas_anytime"])

@st.cache_data(ttl=20)
def load_data6(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

entradas_semmetodo = load_data6(st.secrets["url_entradas_semmetodo"])

@st.cache_data(ttl=20)
def load_data7(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

base_jogador = load_data7(st.secrets["url_jogador"])

@st.cache_data(ttl=20)
def load_data8(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

base_2gols_poisson = load_data8(st.secrets["url_2gols_poisson"])






# Interface para inserção de novos dados

tab1,tab2=  st.tabs(['Analise Jogo','Dash'])

#a
with tab1:

    ligas = ['chines','espanhol', 'frances','holandes','ingles','portugues','serie_a','serie_b','bundesliga', 'Mexico', 'italiano']
    liga = st.selectbox('Selecione a liga:', ligas, index=1, key ='lista_de_ligas')

    liga_string = liga
    liga = liga+'.xlsx'

    geral = pd.read_excel(liga, sheet_name='BD_Times')
    jogo = pd.read_excel(liga, sheet_name='BD_Jogo')
    nome_equipes = geral['Nome do Time'].unique()

    col1, col2= st.columns([1, 1,])
    with col1:
        casa = st.selectbox('Selecione o time da casa:', nome_equipes, index=1, key='time_casa')

    with col2:
        fora = st.selectbox('Selecione o time visitante:', nome_equipes, index=1, key='time_visitante')



    bd_casa_casa = jogo.loc[jogo['Casa'] == casa]
    bd_casa_fora = jogo.loc[jogo['Fora'] == casa]
    bd_fora_casa = jogo.loc[jogo['Casa'] == fora]
    bd_fora_fora = jogo.loc[jogo['Fora'] == fora]

    bd_u5casa = pd.concat([bd_casa_casa, bd_casa_fora]).sort_index()[-5:]
    bd_u5fora = pd.concat([bd_fora_casa, bd_fora_fora]).sort_index()[-5:]
    len(bd_u5fora.loc[bd_u5fora['Gols Marcados']>1])

    #Liga
    contagem_jogos_camp = len((jogo['Casa']))
    #Times
    bd_u5casac = bd_casa_casa[-5:]
    bd_u5foraf = bd_fora_fora[-5:]
    bd_u5casag = pd.concat([bd_casa_casa, bd_casa_fora]).sort_index()[-5:]
    bd_u5forag= pd.concat([bd_fora_casa, bd_fora_fora]).sort_index()[-5:]


    #Liga
    contagem_jogos_camp = len((jogo['Casa']))
    #Média
    ##Liga

    m_liga_gols = round(sum(jogo['Gols Marcados'])/contagem_jogos_camp,2)


    ##Time Casa

    m_u5casac_gols =  sum(bd_u5casac['Gols Marcados'])/5
    m_u5casag_gols = sum(bd_u5casag['Gols Marcados'])/5

    ##Time Fora

    m_u5foraf_gols =  sum(bd_u5foraf['Gols Marcados'])/5
    m_u5forag_gols = sum(bd_u5forag['Gols Marcados'])/5

    ##Time Fora

    ### 1.5Gols


    ##Liga


    o_liga_gols_1 = round(len(jogo.loc[jogo['Gols Marcados']>1])/contagem_jogos_camp,2)

    ##Time Casa

    o_u5casac_gols_1 = len(bd_u5casac.loc[bd_u5casac['Gols Marcados']>1])
    o_u5casag_gols_1 = len(bd_u5casag.loc[bd_u5casag['Gols Marcados']>1])

    ##Time Fora

    o_u5foraf_gols_1 =  len(bd_u5foraf.loc[bd_u5foraf['Gols Marcados']>1])
    o_u5forag_gols_1 = len(bd_u5forag.loc[bd_u5forag['Gols Marcados']>1])

    ###2.5 Gols

    ##Liga


    o_liga_gols_2 = round(len(jogo.loc[jogo['Gols Marcados']>2])/contagem_jogos_camp,2)

    ##Time Casa

    o_u5casac_gols_2 = len(bd_u5casac.loc[bd_u5casac['Gols Marcados']>2])
    o_u5casag_gols_2 = len(bd_u5casag.loc[bd_u5casag['Gols Marcados']>2])

    ##Time Fora

    o_u5foraf_gols_2 =  len(bd_u5foraf.loc[bd_u5foraf['Gols Marcados']>2])
    o_u5forag_gols_2 = len(bd_u5forag.loc[bd_u5forag['Gols Marcados']>2])


    ##Liga


    o_liga_ambos = round(len(jogo.loc[jogo['Ambos']==1])/contagem_jogos_camp,2)

    ##Time Casa

    o_u5casac_ambos = len(bd_u5casac.loc[bd_u5casac['Ambos'] == 1])
    o_u5casag_ambos = len(bd_u5casag.loc[bd_u5casag['Ambos']==1])

    ##Time Fora

    o_u5foraf_ambos =  len(bd_u5foraf.loc[bd_u5foraf['Ambos'] == 1])
    o_u5forag_ambos = len(bd_u5forag.loc[bd_u5forag['Ambos'] == 1])
    #Média
    ##Liga

    m_liga_cantos = round(sum(jogo['Cantos'])/contagem_jogos_camp,2)


    ##Time Casa

    m_u5casac_cantos =  sum(bd_u5casac['Cantos'])/5
    m_u5casag_cantos = sum(bd_u5casag['Cantos'])/5

    ##Time Fora

    m_u5foraf_cantos =  sum(bd_u5foraf['Cantos'])/5
    m_u5forag_cantos = sum(bd_u5forag['Cantos'])/5
    ### 6.5 Cantos


    ##Liga


    o_liga_cantos_6 = round(len(jogo.loc[jogo['Cantos']>6])/contagem_jogos_camp,2)

    ##Time Casa

    o_u5casac_cantos_6 = len(bd_u5casac.loc[bd_u5casac['Cantos']>6])
    o_u5casag_cantos_6 = len(bd_u5casag.loc[bd_u5casag['Cantos']>6])

    ##Time Fora

    o_u5foraf_cantos_6 =  len(bd_u5foraf.loc[bd_u5foraf['Cantos']>6])
    o_u5forag_cantos_6 = len(bd_u5forag.loc[bd_u5forag['Cantos']>6])

    ###7.5 cantos

    ##Liga


    o_liga_cantos_7 = round(len(jogo.loc[jogo['Cantos']>7])/contagem_jogos_camp,2)

    ##Time Casa

    o_u5casac_cantos_7 = len(bd_u5casac.loc[bd_u5casac['Cantos']>7])
    o_u5casag_cantos_7 = len(bd_u5casag.loc[bd_u5casag['Cantos']>7])

    ##Time Fora

    o_u5foraf_cantos_7 =  len(bd_u5foraf.loc[bd_u5foraf['Cantos']>7])
    o_u5forag_cantos_7 = len(bd_u5forag.loc[bd_u5forag['Cantos']>7])
    #Times
    bd_u5casact = geral.loc[(geral['Casa'] == 1)&(geral['Nome do Time'] == casa)][-5:]
    bd_u5casagt = geral.loc[geral['Nome do Time'] == casa] [-5:]
    bd_u5foraft = geral.loc[(geral['Casa'] == 0)&(geral['Nome do Time'] == fora)][-5:]
    bd_u5foragt = geral.loc[geral['Nome do Time'] == fora] [-5:]

    ###8.5 Gols

    ##Liga

    o_liga_cantos_8 = round(len(jogo.loc[jogo['Cantos']>8])/contagem_jogos_camp,2)

    ##Time Casa

    o_u5casac_cantos_8 = len(bd_u5casac.loc[bd_u5casac['Cantos']>8])
    o_u5casag_cantos_8 = len(bd_u5casag.loc[bd_u5casag['Cantos']>8])

    ##Time Fora

    o_u5foraf_cantos_8 =  len(bd_u5foraf.loc[bd_u5foraf['Cantos']>8])
    o_u5forag_cantos_8 = len(bd_u5forag.loc[bd_u5forag['Cantos']>8])

    #Times
    bd_u5casact = geral.loc[(geral['Casa'] == 1)&(geral['Nome do Time'] == casa)][-5:]
    bd_u5casagt = geral.loc[geral['Nome do Time'] == casa] [-5:]
    bd_u5foraft = geral.loc[(geral['Casa'] == 0)&(geral['Nome do Time'] == fora)][-5:]
    bd_u5foragt = geral.loc[geral['Nome do Time'] == fora] [-5:]

    #### Media

    ### Liga

    filtro_m_liga_gols_c = geral.loc[geral['Casa'] == 1]
    filtro_m_liga_gols_f = geral.loc[geral['Casa'] == 0]
    m_liga_golsc = round(sum(filtro_m_liga_gols_c['Gols Feitos'])/contagem_jogos_camp,2)
    m_liga_golsf = round(sum(filtro_m_liga_gols_f['Gols Feitos'])/contagem_jogos_camp,2)

    ###Time Casa Realizar Ação

    ##Casa
    m_u5casact_f_gols = sum(bd_u5casact['Gols Feitos'])/5
    m_u5foraft_r_gols = sum(bd_u5foraft['Gols sofridos'])/5

    ##Geral

    m_u5casagt_f_gols = sum(bd_u5casagt['Gols Feitos'])/5
    m_u5foragt_r_gols = sum(bd_u5foragt['Gols sofridos'])/5

    ###Time Fora Realizar Ação

    ##Fora
    m_u5foraft_f_gols = sum(bd_u5foraft['Gols Feitos'])/5
    m_u5casact_r_gols = sum(bd_u5casact['Gols sofridos'])/5

    ##Geral

    m_u5foragt_f_gols = sum(bd_u5foragt['Gols Feitos'])/5
    m_u5casagt_r_gols = sum(bd_u5casagt['Gols sofridos'])/5
    ### 0.5 Gols


    ##Liga


    o_ligac_gols_0 = round(len(filtro_m_liga_gols_c.loc[filtro_m_liga_gols_c['Gols Feitos']>0])/contagem_jogos_camp,2)
    o_ligaf_gols_0 = round(len(filtro_m_liga_gols_f.loc[filtro_m_liga_gols_f['Gols Feitos']>0])/contagem_jogos_camp,2)

    ##Time Casa Realizar ação

    #Jogos Casa
    o_u5casactf_gols_0 = len(bd_u5casact.loc[bd_u5casact['Gols Feitos']>0])
    o_u5foraftr_gols_0 = len(bd_u5foraft.loc[bd_u5foraft['Gols sofridos']>0])

    #Jogos Geral

    o_u5casagtf_gols_0 = len(bd_u5casagt.loc[bd_u5casagt['Gols Feitos']>0])
    o_u5foragtr_gols_0 = len(bd_u5foragt.loc[bd_u5foragt['Gols sofridos']>0])

    ##Time Fora Realizar a ação

    #Jogos Fora
    o_u5foraftf_gols_0 = len(bd_u5foraft.loc[bd_u5foraft['Gols Feitos']>0])
    o_u5casactr_gols_0 = len(bd_u5casact.loc[bd_u5casact['Gols sofridos']>0])

    #Jogos Geral

    o_u5foragtf_gols_0 = len(bd_u5foragt.loc[bd_u5foragt['Gols Feitos']>0])
    o_u5casagtr_gols_0 = len(bd_u5casagt.loc[bd_u5casagt['Gols sofridos']>0])
    #### Media

    ### Liga

    filtro_m_liga_cantos_c = geral.loc[geral['Casa'] == 1]
    filtro_m_liga_cantos_f = geral.loc[geral['Casa'] == 0]
    m_liga_cantosc = round(sum(filtro_m_liga_cantos_c['Cantos'])/contagem_jogos_camp,2)
    m_liga_cantosf = round(sum(filtro_m_liga_cantos_f['Cantos'])/contagem_jogos_camp,2)
    m_liga_cantos_times = round(sum(geral['Cantos'])/len(geral['Cantos']),2)

    ###Time Casa Realizar Ação

    ##Casa
    m_u5casact_f_cantos = sum(bd_u5casact['Cantos'])/5
    m_u5foraft_r_cantos = sum(bd_u5foraft['Cantos Forçados'])/5

    ##Geral

    m_u5casagt_f_cantos = sum(bd_u5casagt['Cantos'])/5
    m_u5foragt_r_cantos = sum(bd_u5foragt['Cantos Forçados'])/5

    ###Time Fora Realizar Ação

    ##Fora
    m_u5foraft_f_cantos = sum(bd_u5foraft['Cantos'])/5
    m_u5casact_r_cantos = sum(bd_u5casact['Cantos Forçados'])/5

    ##Geral

    m_u5foragt_f_cantos = sum(bd_u5foragt['Cantos'])/5
    m_u5casagt_r_cantos = sum(bd_u5casagt['Cantos Forçados'])/5
    ### 1.5 Cantos


    ##Liga


    o_ligac_cantos_1 = round(len(filtro_m_liga_cantos_c.loc[filtro_m_liga_cantos_c['Cantos']>1])/contagem_jogos_camp,2)
    o_ligaf_cantos_1 = round(len(filtro_m_liga_cantos_f.loc[filtro_m_liga_cantos_f['Cantos']>1])/contagem_jogos_camp,2)

    ##Time Casa Realizar ação

    #Jogos Casa
    o_u5casactf_cantos_1 = len(bd_u5casact.loc[bd_u5casact['Cantos']>1])
    o_u5foraftr_cantos_1 = len(bd_u5foraft.loc[bd_u5foraft['Cantos Forçados']>1])

    #Jogos Geral

    o_u5casagtf_cantos_1 = len(bd_u5casagt.loc[bd_u5casagt['Cantos']>1])
    o_u5foragtr_cantos_1 = len(bd_u5foragt.loc[bd_u5foragt['Cantos Forçados']>1])

    ##Time Fora Realizar a ação

    #Jogos Fora
    o_u5foraftf_cantos_1 = len(bd_u5foraft.loc[bd_u5foraft['Cantos']>1])
    o_u5casactr_cantos_1 = len(bd_u5casact.loc[bd_u5casact['Cantos Forçados']>1])

    #Jogos Geral

    o_u5foragtf_cantos_1 = len(bd_u5foragt.loc[bd_u5foragt['Cantos']>1])
    o_u5casagtr_cantos_1 = len(bd_u5casagt.loc[bd_u5casagt['Cantos Forçados']>1])


    ### 2.5 Cantos


    ##Liga


    o_ligac_cantos_2 = round(len(filtro_m_liga_cantos_c.loc[filtro_m_liga_cantos_c['Cantos']>2])/contagem_jogos_camp,2)
    o_ligaf_cantos_2 = round(len(filtro_m_liga_cantos_f.loc[filtro_m_liga_cantos_f['Cantos']>2])/contagem_jogos_camp,2)

    ##Time Casa Realizar ação

    #Jogos Casa
    o_u5casactf_cantos_2 = len(bd_u5casact.loc[bd_u5casact['Cantos']>2])
    o_u5foraftr_cantos_2 = len(bd_u5foraft.loc[bd_u5foraft['Cantos Forçados']>2])

    #Jogos Geral

    o_u5casagtf_cantos_2 = len(bd_u5casagt.loc[bd_u5casagt['Cantos']>2])
    o_u5foragtr_cantos_2 = len(bd_u5foragt.loc[bd_u5foragt['Cantos Forçados']>2])

    ##Time Fora Realizar a ação

    #Jogos Fora
    o_u5foraftf_cantos_2 = len(bd_u5foraft.loc[bd_u5foraft['Cantos']>2])
    o_u5casactr_cantos_2 = len(bd_u5casact.loc[bd_u5casact['Cantos Forçados']>2])

    #Jogos Geral

    o_u5foragtf_cantos_2 = len(bd_u5foragt.loc[bd_u5foragt['Cantos']>2])
    o_u5casagtr_cantos_2 = len(bd_u5casagt.loc[bd_u5casagt['Cantos Forçados']>2])

    ### 3.5 Cantos


    ##Liga


    o_ligac_cantos_3 = round(len(filtro_m_liga_cantos_c.loc[filtro_m_liga_cantos_c['Cantos']>3])/contagem_jogos_camp,2)
    o_ligaf_cantos_3 = round(len(filtro_m_liga_cantos_f.loc[filtro_m_liga_cantos_f['Cantos']>3])/contagem_jogos_camp,2)

    ##Time Casa Realizar ação

    #Jogos Casa
    o_u5casactf_cantos_3 = len(bd_u5casact.loc[bd_u5casact['Cantos']>3])
    o_u5foraftr_cantos_3 = len(bd_u5foraft.loc[bd_u5foraft['Cantos Forçados']>3])

    #Jogos Geral

    o_u5casagtf_cantos_3 = len(bd_u5casagt.loc[bd_u5casagt['Cantos']>3])
    o_u5foragtr_cantos_3 = len(bd_u5foragt.loc[bd_u5foragt['Cantos Forçados']>3])

    ##Time Fora Realizar a ação

    #Jogos Fora
    o_u5foraftf_cantos_3 = len(bd_u5foraft.loc[bd_u5foraft['Cantos']>3])
    o_u5casactr_cantos_3 = len(bd_u5casact.loc[bd_u5casact['Cantos Forçados']>3])

    #Jogos Geral

    o_u5foragtf_cantos_3 = len(bd_u5foragt.loc[bd_u5foragt['Cantos']>3])
    o_u5casagtr_cantos_3 = len(bd_u5casagt.loc[bd_u5casagt['Cantos Forçados']>3])


    ### 4.5 Cantos

    ##Liga


    o_ligac_cantos_4 = round(len(filtro_m_liga_cantos_c.loc[filtro_m_liga_cantos_c['Cantos']>4])/contagem_jogos_camp,2)
    o_ligaf_cantos_4 = round(len(filtro_m_liga_cantos_f.loc[filtro_m_liga_cantos_f['Cantos']>4])/contagem_jogos_camp,2)

    ##Time Casa Realizar ação

    #Jogos Casa
    o_u5casactf_cantos_4 = len(bd_u5casact.loc[bd_u5casact['Cantos']>4])
    o_u5foraftr_cantos_4 = len(bd_u5foraft.loc[bd_u5foraft['Cantos Forçados']>4])

    #Jogos Geral

    o_u5casagtf_cantos_4 = len(bd_u5casagt.loc[bd_u5casagt['Cantos']>4])
    o_u5foragtr_cantos_4 = len(bd_u5foragt.loc[bd_u5foragt['Cantos Forçados']>4])

    ##Time Fora Realizar a ação

    #Jogos Fora
    o_u5foraftf_cantos_4 = len(bd_u5foraft.loc[bd_u5foraft['Cantos']>4])
    o_u5casactr_cantos_4 = len(bd_u5casact.loc[bd_u5casact['Cantos Forçados']>4])

    #Jogos Geral

    o_u5foragtf_cantos_4 = len(bd_u5foragt.loc[bd_u5foragt['Cantos']>4])
    o_u5casagtr_cantos_4 = len(bd_u5casagt.loc[bd_u5casagt['Cantos Forçados']>4])


    ### 5.5 Cantos

    ##Liga


    o_ligac_cantos_5 = round(len(filtro_m_liga_cantos_c.loc[filtro_m_liga_cantos_c['Cantos']>5])/contagem_jogos_camp,2)
    o_ligaf_cantos_5 = round(len(filtro_m_liga_cantos_f.loc[filtro_m_liga_cantos_f['Cantos']>5])/contagem_jogos_camp,2)

    ##Time Casa Realizar ação

    #Jogos Casa
    o_u5casactf_cantos_5 = len(bd_u5casact.loc[bd_u5casact['Cantos']>5])
    o_u5foraftr_cantos_5 = len(bd_u5foraft.loc[bd_u5foraft['Cantos Forçados']>5])

    #Jogos Geral

    o_u5casagtf_cantos_5 = len(bd_u5casagt.loc[bd_u5casagt['Cantos']>5])
    o_u5foragtr_cantos_5 = len(bd_u5foragt.loc[bd_u5foragt['Cantos Forçados']>5])

    ##Time Fora Realizar a ação

    #Jogos Fora
    o_u5foraftf_cantos_5 = len(bd_u5foraft.loc[bd_u5foraft['Cantos']>5])
    o_u5casactr_cantos_5 = len(bd_u5casact.loc[bd_u5casact['Cantos Forçados']>5])

    #Jogos Geral

    o_u5foragtf_cantos_5 = len(bd_u5foragt.loc[bd_u5foragt['Cantos']>5])
    o_u5casagtr_cantos_5 = len(bd_u5casagt.loc[bd_u5casagt['Cantos Forçados']>5])

    analise_linha = [[casa, fora, '-', o_u5casac_gols_2, o_u5casag_gols_2, o_u5foraf_gols_2, o_u5forag_gols_2, m_u5casac_gols, m_u5casag_gols, m_u5foraf_gols, m_u5forag_gols, m_liga_gols, o_liga_gols_2, m_u5casact_f_cantos, m_u5casagt_f_cantos,   m_u5foraft_f_cantos,m_u5foragt_f_cantos, m_liga_cantosc, m_liga_cantosf,m_liga_cantos_times, liga_string]]
    analise_adicao = pd.DataFrame(analise_linha, columns= ['Casa', 'Fora','Bateu','Casa Fazer - M','Casa Fazer - G', 'Fora Fazer - M', 'Fora Fazer - G', 'Média Casa - M','Média Casa - G', 'Média Fora - M','Média Fora - G',  'Media Liga','Ocorrencia Liga', 'C - Média Casa - M','C - Média Casa - G', 'C - Média Fora - M', 'C- Média Fora - G',  'C - Media Liga - Casa', 'C - Media Liga - Fora','C - Média Times', 'Liga'])
    #analise_adicao = pd.concat([bd_analise, analise_linha])

    analise_adicao['Média Casa FM'] = np.where(analise_adicao['Média Casa - M'] > analise_adicao['Media Liga'], 1, 0)
    analise_adicao['Média Casa FG'] = np.where(analise_adicao['Média Casa - G'] > analise_adicao['Media Liga'], 1, 0)
    analise_adicao['Média Fora FM'] = np.where(analise_adicao['Média Fora - M'] > analise_adicao['Media Liga'], 1, 0)
    analise_adicao['Média Fora FG'] = np.where(analise_adicao['Média Fora - G'] > analise_adicao['Media Liga'], 1, 0)
    analise_adicao['Soma Média'] = analise_adicao['Média Casa FM'] + analise_adicao['Média Casa FG'] + analise_adicao['Média Fora FM'] + analise_adicao['Média Fora FG']
    analise_adicao['C - Média Casa FM'] = np.where(analise_adicao['C - Média Casa - M'] > analise_adicao['C - Media Liga - Casa'], 1, 0)
    analise_adicao['C - Média Casa FG'] = np.where(analise_adicao['C - Média Casa - G'] > analise_adicao['C - Média Times'], 1, 0)
    analise_adicao['C - Média Fora FM'] = np.where(analise_adicao['C - Média Fora - M'] > analise_adicao['C - Media Liga - Fora'], 1, 0)
    analise_adicao['C - Média Fora FG'] = np.where(analise_adicao['C- Média Fora - G'] > analise_adicao['C - Média Times'], 1, 0)
    analise_adicao['C - Soma Média'] = analise_adicao['C - Média Casa FM'] + analise_adicao['C - Média Casa FG'] + analise_adicao['C - Média Fora FM'] + analise_adicao['C - Média Fora FG']
    #parte do código que cria uma flag mostrando se tem linhas interessantes naquele jogo


    valores_1_5 = o_u5casac_gols_1 + o_u5casag_gols_1+  o_u5foraf_gols_1+  o_u5forag_gols_1
    valores_7_5 = o_u5casac_cantos_7+  o_u5casag_cantos_7+ o_u5foraf_cantos_7+ o_u5forag_cantos_7
    valores_8_5 = o_u5casac_cantos_8+ o_u5casag_cantos_8+ o_u5foraf_cantos_8+ o_u5forag_cantos_8
    # Primeira validação: "Interessante para gols"
    if valores_1_5 >=15:
        st.markdown('## **Interessante para Gols 1.5**')

    # Segunda validação: "Interessante para cantos"
    if valores_7_5 >=15:
        st.markdown('## **Interessante para Cantos 7.5**')
    if valores_8_5 >=15:
        st.markdown('## **Interessante para Cantos 8.5**')    


    #análise 2.5 poisson
    
    geral['Soma Gols'] = geral['Gols Feitos'] + geral['Gols sofridos']
    base_a = geral[geral['Nome do Time'] == casa]
    base_b = geral[geral['Nome do Time'] == fora]
    base_a = base_a.iloc[-10:]
    base_b= base_b.iloc[-10:]
    chance_time_a = poisson.pmf(0, base_a['Soma Gols'].mean()) + poisson.pmf(1, base_a['Soma Gols'].mean()) + poisson.pmf(2, base_a['Soma Gols'].mean())
    chance_time_b = poisson.pmf(0, base_b['Soma Gols'].mean()) + poisson.pmf(1, base_b['Soma Gols'].mean()) + poisson.pmf(2, base_b['Soma Gols'].mean())

    prob_a = round(1/(1- chance_time_a),2)
    prob_b = round(1/(1- chance_time_b),2)
    odd_bet_2gols = st.text_input('Odd Bet 2 gols')
    odd_bet_2gols = float(odd_bet_2gols)

    diferenca_a = odd_bet_2gols - prob_a
    diferenca_b = odd_bet_2gols - prob_b

    nova_linha_2gols_poisson = {"Time A": casa, "Time B": fora, "Odd_A": prob_a,  "Odd_B": prob_b, 
              "Odd Bet": odd_bet_2gols, 'Diferença_A': diferenca_a,  'Diferença_B': diferenca_b, 'Entrar': "-", 'Bateu': '-'}
    
    nova_linha_2gols_poisson = [casa, fora, prob_a, prob_b, odd_bet_2gols, diferenca_a, diferenca_b, "-", "-"]

    novas_linhas = []
    with st.form('form'):
        col1, col2, col3, col4 = st.columns([0.5, 0.5, 0.5, 0.5])

        with col1:
            if st.form_submit_button('Adicionar Linha 1.5'):
                nova_linha = [casa, fora, '-', '1.5', 'Gols', 'Jogo', o_u5casac_gols_1, o_u5casag_gols_1, o_u5foraf_gols_1, o_u5forag_gols_1, m_u5casac_gols, m_u5casag_gols, m_u5foraf_gols, m_u5forag_gols, m_liga_gols, m_liga_gols, o_liga_gols_1, o_liga_gols_1, liga_string, data_formatada]
                novas_linhas.append(nova_linha)
        
        with col2:
            if st.form_submit_button('Adicionar Linha 7.5'):
                nova_linha = [casa, fora, '-', '7.5', 'Cantos', 'Jogo', o_u5casac_cantos_7, o_u5casag_cantos_7, o_u5foraf_cantos_7, o_u5forag_cantos_7, m_u5casac_cantos, m_u5casag_cantos, m_u5foraf_cantos, m_u5forag_cantos, m_liga_cantos, m_liga_cantos, o_liga_cantos_7, o_liga_cantos_7, liga_string, data_formatada]
                novas_linhas.append(nova_linha)
        
        with col3:
            if st.form_submit_button('Adicionar Linha 8.5'):
                nova_linha = [casa, fora, '-', '8.5', 'Cantos', 'Jogo', o_u5casac_cantos_8, o_u5casag_cantos_8, o_u5foraf_cantos_8, o_u5forag_cantos_8, m_u5casac_cantos, m_u5casag_cantos, m_u5foraf_cantos, m_u5forag_cantos, m_liga_cantos, m_liga_cantos, o_liga_cantos_8, o_liga_cantos_8,liga_string, data_formatada]
                novas_linhas.append(nova_linha)
        with col4:
            if st.form_submit_button('Adicionar linha 2.5'):
                nova_linha_2gols_poisson  = [casa, fora, prob_a, prob_b, odd_bet_2gols, diferenca_a, diferenca_b, "-", "-"]
                nova_linha_2gols_poisson_df = pd.DataFrame(nova_linha_2gols_poisson, columns=base_2gols_poisson.columns)
                worksheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1t1FQveiownY0EsZeOLznEY5zT7I1jOzxy5Qst2vNR9g/edit#gid=0').get_worksheet(0)
        
        # Obter o número de linhas existentes na planilha
                num_rows = len(worksheet.get_all_values())
        
        # Inserir os dados nas linhas subsequentes
                values_to_insert = nova_linha_2gols_poisson_df.values.tolist()
                worksheet.insert_rows(values_to_insert, num_rows + 1) 

    # Adicionar as novas linhas ao DataFrame
            
    if novas_linhas:
        novas_linhas_df = pd.DataFrame(novas_linhas, columns=tendencias_2linhas.columns)
        #tendencias = pd.concat([tendencias, novas_linhas_df], ignore_index=True)

        # Atualizar a planilha com as novas linhas
        worksheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1t1FQveiownY0EsZeOLznEY5zT7I1jOzxy5Qst2vNR9g/edit?usp=sharing').get_worksheet(0)
        
        # Obter o número de linhas existentes na planilha
        num_rows = len(worksheet.get_all_values())
        
        # Inserir os dados nas linhas subsequentes
        values_to_insert = novas_linhas_df.values.tolist()
        worksheet.insert_rows(values_to_insert, num_rows + 1)  # Insere as linhas atualizadas a partir do final existente

        # Notificar o usuário sobre a atualização bem-sucedida
        st.success("Dados adicionados com sucesso à planilha!")


    st.title('Análise 1.5')
    col1, col2= st.columns([0.5, 0.5,])
    with col1:
        st.metric(label='Média de gols da Liga', value=m_liga_gols)

    with col2:
        st.metric(label='Ocorrência de jogos > 1 gols', value=o_liga_gols_1)

    col1, col2= st.columns([1, 1,])
    with col1:
        st.subheader(casa)

        st.markdown('**Últimos jogos em casa:** {}'.format(o_u5casac_gols_1))
        st.markdown('**Últimos jogos em geral:** {}'.format(o_u5casag_gols_1))
        st.markdown('**Média últimos 5 jogos em casa:** {}'.format(m_u5casac_gols))
        st.markdown('**Média últimos 5 jogos geral:** {}'.format(m_u5casag_gols))
        st.markdown('**Marcou nos últimos 5 em casa** {}'.format(o_u5casactf_gols_0))
        st.markdown('**Marcou nos últimos 5 em geral** {}'.format(o_u5casagtf_gols_0))
        st.markdown('**Média de marcados nos últimos 5 em casa** {}'.format(m_u5casact_f_gols))
        st.markdown('**Média de marcados nos últimos  5 em geral** {}'.format(m_u5casagt_f_gols))         

    with col2:
        st.subheader(fora)

        st.markdown('**Últimos jogos fora de casa:** {}'.format(o_u5foraf_gols_1))
        st.markdown('**Últimos jogos em geral:** {}'.format(o_u5forag_gols_1))
        st.markdown('**Média últimos 5 jogos forade casa:** {}'.format(m_u5foraf_gols))
        st.markdown('**Média últimos 5 jogos geral:** {}'.format(m_u5forag_gols))
        st.markdown('**Marcou nos últimos 5 em fora** {}'.format(o_u5foraftf_gols_0))
        st.markdown('**Marcou nos últimos 5 em geral** {}'.format(o_u5foragtf_gols_0))
        st.markdown('**Média de marcados nos últimos 5 fora de casa** {}'.format(m_u5foraft_f_gols))
        st.markdown('**Média de marcados nos últimos  5 em geral** {}'.format(m_u5foragt_f_gols))   

    st.title('Análise 2.5')

    col1, col2= st.columns([0.5, 0.5,])
    with col1:
        st.metric(label='Média de gols da Liga', value=m_liga_gols)

    with col2:
        st.metric(label='Ocorrência de jogos > 1 gols', value=o_liga_gols_2)


    col1, col2= st.columns([1, 1,])
    with col1:
        st.subheader(casa)

        st.markdown('**Últimos jogos em casa:** {}'.format(o_u5casac_gols_2))
        st.markdown('**Últimos jogos em geral:** {}'.format(o_u5casag_gols_2))
        st.markdown('**Média últimos 5 jogos em casa:** {}'.format(m_u5casac_gols))
        st.markdown('**Média últimos 5 jogos geral:** {}'.format(m_u5casag_gols))
          
       
    with col2:
        st.subheader(fora)

        st.markdown('**Últimos jogos fora de casa:** {}'.format(o_u5foraf_gols_2))
        st.markdown('**Últimos jogos em geral:** {}'.format(o_u5forag_gols_2))
        st.markdown('**Média últimos 5 jogos forade casa:** {}'.format(m_u5foraf_gols))
        st.markdown('**Média últimos 5 jogos geral:** {}'.format(m_u5forag_gols))
         

#a partir dce agora a parte dos escanteios

    st.title('Análise  Cantos 7.5')


    col1, col2, col3= st.columns([0.5, 0.5,0.5])
    with col1:
        st.metric(label='Média de cantos da Liga', value=m_liga_cantos)

    with col2:
        st.metric(label='Ocorrência de jogos > 7 Cantos', value=o_liga_cantos_7)
    with col3:
        st.metric(label='Ocorrência de jogos > 8 Cantos', value=o_liga_cantos_8)   

    col1, col2= st.columns([1, 1,])
    with col1:
        st.subheader(casa)

        st.markdown('**Últimos jogos em casa:** {}'.format(o_u5casac_cantos_7))
        st.markdown('**Últimos jogos em geral:** {}'.format(o_u5casag_cantos_7))
        st.markdown('**Média últimos 5 jogos em casa:** {}'.format(m_u5casac_cantos))
        st.markdown('**Média últimos 5 jogos geral:** {}'.format( m_u5casag_cantos))

    with col2:
        st.subheader(fora)

        st.markdown('**Últimos jogos fora de casa:** {}'.format(o_u5foraf_cantos_7))
        st.markdown('**Últimos jogos em geral:** {}'.format( o_u5forag_cantos_7))
        st.markdown('**Média últimos 5 jogos forade casa:** {}'.format(m_u5foraf_cantos))
        st.markdown('**Média últimos 5 jogos geral:** {}'.format(m_u5forag_cantos))

    st.title('Análise  Cantos 8.5')
    

    col1, col2= st.columns([1, 1,])
    with col1:
        st.subheader(casa)

        st.markdown('**Últimos jogos em casa:** {}'.format(o_u5casac_cantos_8))
        st.markdown('**Últimos jogos em geral:** {}'.format(o_u5casag_cantos_8))
        st.markdown('**Média últimos 5 jogos em casa:** {}'.format(m_u5casac_cantos))
        st.markdown('**Média últimos 5 jogos geral:** {}'.format( m_u5casag_cantos))

    with col2:
        st.subheader(fora)

        st.markdown('**Últimos jogos fora de casa:** {}'.format(o_u5foraf_cantos_8))
        st.markdown('**Últimos jogos em geral:** {}'.format(o_u5forag_cantos_8))
        st.markdown('**Média últimos 5 jogos forade casa:** {}'.format(m_u5foraf_cantos))
        st.markdown('**Média últimos 5 jogos geral:** {}'.format(m_u5forag_cantos))

    st.title('Linhas Extras - Cantos')

    col1, col2= st.columns([0.5, 0.5])
    with col1:
        st.metric(label='Média do mandante', value=m_liga_cantosc)

    with col2:
        st.metric(label='Média do visitante', value= m_liga_cantosf)
                      

    dados_cantos_extras = [[casa, fora,  '1.5', 'Casa', o_u5casactf_cantos_1, o_u5casagtf_cantos_1,  o_u5foraftr_cantos_1, o_u5foragtr_cantos_1, m_u5casact_f_cantos,m_u5casagt_f_cantos,  m_u5foraft_r_cantos, m_u5foragt_r_cantos,  o_ligac_cantos_1, o_ligaf_cantos_1],
                            [casa, fora, '1.5', 'Fora', o_u5foraftf_cantos_1, o_u5foragtf_cantos_1,  o_u5casactr_cantos_1, o_u5casagtr_cantos_1, m_u5foraft_f_cantos,m_u5foragt_f_cantos,  m_u5casact_r_cantos, m_u5casagt_r_cantos,   o_ligac_cantos_1, o_ligaf_cantos_1],
                            [casa, fora, '2.5', 'Casa', o_u5casactf_cantos_2, o_u5casagtf_cantos_2,  o_u5foraftr_cantos_2, o_u5foragtr_cantos_2, m_u5casact_f_cantos,m_u5casagt_f_cantos,  m_u5foraft_r_cantos, m_u5foragt_r_cantos,  o_ligac_cantos_2, o_ligaf_cantos_2],
                             [casa, fora, '2.5', 'Fora', o_u5foraftf_cantos_2, o_u5foragtf_cantos_2,  o_u5casactr_cantos_2, o_u5casagtr_cantos_2, m_u5foraft_f_cantos,m_u5foragt_f_cantos,  m_u5casact_r_cantos, m_u5casagt_r_cantos,  o_ligac_cantos_2, o_ligaf_cantos_2],
                            [casa, fora,  '3.5', 'Casa', o_u5casactf_cantos_3, o_u5casagtf_cantos_3,  o_u5foraftr_cantos_3, o_u5foragtr_cantos_3, m_u5casact_f_cantos,m_u5casagt_f_cantos,  m_u5foraft_r_cantos, m_u5foragt_r_cantos,  o_ligac_cantos_3, o_ligaf_cantos_3],
                             [casa, fora,  '3.5', 'Fora', o_u5foraftf_cantos_3, o_u5foragtf_cantos_3,  o_u5casactr_cantos_3, o_u5casagtr_cantos_3, m_u5foraft_f_cantos,m_u5foragt_f_cantos,  m_u5casact_r_cantos, m_u5casagt_r_cantos, o_ligac_cantos_3, o_ligaf_cantos_3]]    

    analise = pd.DataFrame(dados_cantos_extras, columns= ['Casa', 'Fora', 'Tipo de Linha','Bateu','Casa Fazer - M','Casa Fazer - G', 'Fora Fazer - M', 'Fora Fazer - G', 'Média Casa - M','Média Casa - G', 'Média Fora - M','Média Fora - G', 'Ocorrencia Liga Casa','Ocorrencia Liga Fora'])
    analise = analise.reset_index(drop=True)
    analise
    

with tab2:
    st.subheader("Entradas Gerais")

    entradas_2gols['Cluster'] = entradas_2gols['Cluster'] = '2gols'
    entradas_2linhas['Cluster'] = entradas_2linhas['Cluster'] = '2Linhas'
    entradas_anytimes['Cluster'] = entradas_anytimes['Cluster'] = 'Anytime'
    entradas_semmetodo['Cluster'] = entradas_semmetodo['Cluster'] = 'Sem Método'
    entradas = pd.concat([entradas_2gols, entradas_2linhas,entradas_anytimes, entradas_semmetodo])
    entradas =  entradas[entradas['Aposta Anulada?'] != "Sim"]
    selected_clusters = st.multiselect('Escolha os Clusters', entradas['Cluster'].unique(), default=entradas['Cluster'].unique())
    entradas = entradas[entradas['Cluster'].isin(selected_clusters)]
    entradas['Data'] = pd.to_datetime(entradas['Data'], errors='coerce')    
    entradas['Mês'] = entradas['Data'].dt.strftime('%b')
    entradas['Odd'] = entradas['Odd'].str.replace(',', '.').astype(float)
    entradas['Retorno - reduzido a odd'] = entradas.apply(lambda row: row['Odd'] if row['Resultado'] == 1 else 0, axis=1)
    entradas['Retorno - reduzido a odd'] = entradas['Retorno - reduzido a odd'].astype(float)

    entradas['Investimento'] = entradas['Investimento'].str.replace(',', '.').astype(float)
    entradas['Retorno'] = entradas['Retorno'].str.replace(',', '.').astype(float)
# Converter a coluna para float (ou int, dependendo do caso)
    entradas['Retorno - reduzido a odd'] = entradas['Retorno - reduzido a odd'].astype(float)
    entradas = entradas[entradas['Aposta Anulada?'] != "Sim"]
    investimento_total = round(entradas['Investimento'].sum(),2)
    retorno_total = round(entradas['Retorno'].sum(),2)
    qtd_apostas = len(entradas['Investimento'])
    #retorno_total_odd =  entradas['Odd'].sum()
    retorno_total_odd = round(entradas['Retorno - reduzido a odd'].sum(),2)

    
    retorno_total_percentual = round(((retorno_total/investimento_total)-1)*100,2)
    retorno_total_odd_percentual = round(((retorno_total_odd/qtd_apostas)-1)*100,2)

    delta_investimento = "Qtd Apostas: " + str(qtd_apostas)
    delta_retorno = 'Retorno reduzido a odd: ' + str(retorno_total_odd)
    delta_retorno_percentual = 'Retorno reduzido a odd percentual: ' + str(retorno_total_odd_percentual)
    entradas['Investimento - reduzido a odd'] = 1 
    col1, col2, col3= st.columns(3)

    with col1:
        st.metric('Investimento Total',investimento_total, delta= delta_investimento)

    with col2:
        st.metric('Retorno Total',retorno_total, delta = delta_retorno)
        
    with col3:
        st.metric('% retornado',retorno_total_percentual, delta = delta_retorno_percentual)

    col1, col2 = st.columns(2)

    order_months = ['Jan', 'Feb','Mar', 'Apr', 'May','Jul', 'Aug', 'Sep','Oct', 'Nov']
    entradas['Mês'] = pd.Categorical(entradas['Mês'], categories=order_months, ordered=True)

    opcao_radio = st.radio("Escolha a opção:", ['Normal', 'Odd'])

# Lógica para determinar colunas com base na opção selecionada
    if opcao_radio == 'Normal':
        col_investimento, col_retorno = 'Investimento', 'Retorno'
    elif opcao_radio == 'Odd':
        col_investimento, col_retorno = 'Investimento - reduzido a odd', 'Retorno - reduzido a odd'

    totais_por_mes = entradas.groupby('Mês').agg({col_investimento: 'sum', col_retorno: 'sum'}).reset_index()
    totais_por_mes['Lucro por mês'] = round(((totais_por_mes[col_retorno] / totais_por_mes[col_investimento]) - 1) * 100, 2)
    
    totais_por_mes.rename(columns={col_investimento: 'Investimento', col_retorno: 'Retorno'}, inplace=True)

    col1, col2 = st.columns(2)

# Gráfico 1: Barras de Investimento e Retorno por Mês
    fig1 = go.Figure()

    fig1.add_trace(
        go.Bar(
            x=totais_por_mes['Mês'],
            y=totais_por_mes['Investimento'],
            name='Investimento',
            marker=dict(color='blue'),
            text=round(totais_por_mes['Investimento'], 2),
        )
    )

    fig1.add_trace(
        go.Bar(
            x=totais_por_mes['Mês'],
            y=totais_por_mes['Retorno'],
            name='Retorno',
            marker=dict(color='orange'),
            text=round(totais_por_mes['Retorno'], 2),
        )
    )

    # Atualizar layout do gráfico 1
    fig1.update_xaxes(title_text='Mês', showgrid=False)
    fig1.update_yaxes(title_text='Valor', showgrid=False)
    fig1.update_layout(title_text='Investimento e Retorno por Mês')

    # Exibir o gráfico 1 na coluna 1
    col1.plotly_chart(fig1)

    # Gráfico 2: Linha de Lucro por Mês
    fig2 = go.Figure()

    fig2.add_trace(
        go.Scatter(
            x=totais_por_mes['Mês'],
            y=totais_por_mes['Lucro por mês'],
            mode='lines+markers+text',
            name='Lucro por Mês',
            text=round(totais_por_mes['Lucro por mês'], 2),
            textposition='top center',
            line=dict(
                width=3,
                color='green'
            )
        )
    )

    # Atualizar layout do gráfico 2
    fig2.update_xaxes(title_text='Mês', showgrid=False)
    fig2.update_yaxes(title_text='Lucro (%)', showgrid=False)
    fig2.update_layout(title_text='Lucro por Mês')

    # Exibir o gráfico 2 na coluna 2
    col2.plotly_chart(fig2)



    apostas_feitas = entradas.groupby('Mês').agg({'Investimento': 'count', 'Resultado': 'sum'}).reset_index()
    apostas_feitas['Resultado'] = pd.to_numeric(apostas_feitas['Resultado'], errors='coerce')
    apostas_feitas['Investimento'] = pd.to_numeric(apostas_feitas['Investimento'], errors='coerce')

    apostas_feitas['% de Aproveitamento'] = round(((apostas_feitas['Resultado'] /apostas_feitas['Investimento'])) * 100, 2)
    apostas_feitas.rename(columns={'Investimento': 'Qtd de Apostas', 'Resultado': 'Qtd de Acertos'}, inplace=True)

# Gráfico 1: Quantidade de aostas eitas
    fig1 = go.Figure()

    fig1.add_trace(
        go.Bar(
            x=apostas_feitas['Mês'],
            y=apostas_feitas['Qtd de Apostas'],
            name='Qtd de Apostas',
            marker=dict(color='green'),
            text=round(apostas_feitas['Qtd de Apostas'], 2),
        )
    )

    fig1.add_trace(
        go.Bar(
            x=apostas_feitas['Mês'],
            y=apostas_feitas['Qtd de Acertos'],
            name='Qtd de Acertos',
            marker=dict(color='red'),
            text=round(apostas_feitas['Qtd de Acertos'], 2),
        )
    )

    # Atualizar layout do gráfico 1
    fig1.update_xaxes(title_text='Mês', showgrid=False)
    fig1.update_yaxes(title_text='Qtd', showgrid=False)
    fig1.update_layout(title_text='Qtd de apostas e acertos por mês')

    # Exibir o gráfico 1 na coluna 1
    col1.plotly_chart(fig1)

    # Gráfico 2: % de aproveitamento
    fig2 = go.Figure()

    fig2.add_trace(
        go.Scatter(
            x=apostas_feitas['Mês'],
            y=apostas_feitas['% de Aproveitamento'],
            mode='lines+markers+text',
            name='% de Aproveitamento',
            text=round(apostas_feitas['% de Aproveitamento'], 2),
            textposition='top center',
            line=dict(
                width=3,
                color='blue'
            )
        )
    )

    # Atualizar layout do gráfico 2
    fig2.update_xaxes(title_text='Mês', showgrid=False)
    fig2.update_yaxes(title_text='% de acertos', showgrid=False)
    fig2.update_layout(title_text='Aproveitamento %')

    # Exibir o gráfico 2 na coluna 2
    col2.plotly_chart(fig2)

    st.subheader("Tendências")
    
    col1, col2= st.columns(2)

    tendencias_2linhas_filtrada =  tendencias_2linhas[tendencias_2linhas['Bateu'] != "-"]
    tendencias_2linhas_filtrada['Bateu'] = tendencias_2linhas_filtrada['Bateu'].astype(int)

    selected_clusters_tendencias = st.multiselect('Escolha o Tipo', tendencias_2linhas_filtrada['Tipo de Linha'].unique(), default=tendencias_2linhas_filtrada['Tipo de Linha'].unique())
    tendencias_2linhas_filtrada = tendencias_2linhas_filtrada[tendencias_2linhas_filtrada['Tipo de Linha'].isin(selected_clusters_tendencias)]    

    qtd_tendencias = len(tendencias_2linhas_filtrada['Bateu'])
    tendencias_2linhas_filtrada['Bateu'] = tendencias_2linhas_filtrada['Bateu'].astype(int)
    qtd_tendencias_aprov = round(tendencias_2linhas_filtrada['Bateu'].mean()*100,2)
    tendencias_2linhas_filtrada['Data'] = pd.to_datetime(tendencias_2linhas_filtrada['Data'], errors='coerce')    
    tendencias_2linhas_filtrada['Mês'] = tendencias_2linhas_filtrada['Data'].dt.strftime('%b')


    with col1:
       st.metric('Têndencias', qtd_tendencias)
    with col2:
        st.metric('Têndencias % aproveitamento', qtd_tendencias_aprov)

    fig_tendencias = go.Figure()
    cores_paises = ['#1f78b4', '#33a02c', '#e31a1c', '#ff7f00', '#6a3d9a', '#b15928', '#a6cee3', '#b2df8a', '#fb9a99', '#fdbf6f']
    pais_cor = dict(zip(tendencias_2linhas_filtrada['Pais'], cores_paises))
    lista_paises = tendencias_2linhas_filtrada['Pais'].unique()
    order_months_tendencias = ['Jan', 'Feb','Mar', 'Apr', 'May','Jul', 'Aug', 'Sep','Oct', 'Nov']

    tendencias_2linhas_filtrada_aprov = tendencias_2linhas_filtrada.pivot_table(index='Pais', columns='Tipo de Linha', values='Bateu', aggfunc='mean').reset_index()
    media_bateu_por_pais = tendencias_2linhas_filtrada.groupby('Pais')['Bateu'].mean().reset_index(name='Total')
    tendencias_2linhas_filtrada_aprov = pd.merge(tendencias_2linhas_filtrada_aprov, media_bateu_por_pais, how='left', on='Pais')   
    tendencias_2linhas_filtrada_aprov.iloc[:, 1:] *= 100
    tendencias_2linhas_filtrada_aprov = tendencias_2linhas_filtrada_aprov.round(0)

    for pais, cor in zip(tendencias_2linhas_filtrada_aprov['Pais'], cores_paises):
        fig_tendencias.add_trace(
            go.Bar(
                x=tendencias_2linhas_filtrada_aprov[tendencias_2linhas_filtrada_aprov['Pais'] == pais]['Pais'],
                y=tendencias_2linhas_filtrada_aprov[tendencias_2linhas_filtrada_aprov['Pais'] == pais]['Total'],
                name=pais,
                marker=dict(color=cor), 
                text=tendencias_2linhas_filtrada_aprov[tendencias_2linhas_filtrada_aprov['Pais'] == pais]['Total'],
            )
        )

    fig_tendencias.update_layout(barmode='stack', xaxis={'categoryorder':'array', 'categoryarray':order_months_tendencias})
    tendencias_2linhas_filtrada_count = tendencias_2linhas_filtrada.pivot_table(index='Pais', values='Bateu', aggfunc='count').reset_index()

    fig_tendencias.add_trace(
        go.Scatter(
            x=tendencias_2linhas_filtrada_count['Pais'],
            y=tendencias_2linhas_filtrada_count['Bateu'],
            mode='lines+markers',
            name='Contagem',
            line=dict(color='black', width=2),  # Cor e largura da linha
            text=tendencias_2linhas_filtrada_count['Bateu'],
            textposition='top center',
        )
    )
    st.plotly_chart(fig_tendencias)

    st.subheader("Análise Jogador")
    
    #apagar colunas existentes na tabela
    base_jogador = base_jogador.drop(['Distribuição', 'Desvio', 'Odd Justa', 'Apostar'], axis=1)
    base_jogador =  base_jogador[base_jogador['Começou?']  == 1]
    base_jogador['Odd Bet'] = base_jogador['Odd Bet'].str.replace(',', '.').astype(float)
    #separar tipos
    jogos_5 = [' [Jogo 11]', ' [Jogo 12]', ' [Jogo 13]', ' [Jogo 14]', ' [Jogo 15]']
    jogos_10 = [' [Jogo 6]', ' [Jogo 7]',  ' [Jogo 8]', ' [Jogo 9]', ' [Jogo 10]', ' [Jogo 11]', ' [Jogo 12]',  ' [Jogo 13]', ' [Jogo 14]', ' [Jogo 15]']
    jogos_15 = [' [Jogo 1]', ' [Jogo 2]', ' [Jogo 3]', ' [Jogo 4]', ' [Jogo 5]', ' [Jogo 6]', ' [Jogo 7]', ' [Jogo 8]', ' [Jogo 9]', ' [Jogo 10]', ' [Jogo 11]', ' [Jogo 12]', ' [Jogo 13]', ' [Jogo 14]', ' [Jogo 15]']


    tipos = {'jogos_5': jogos_5, 'jogos_10': jogos_10, 'jogos_15': jogos_15}
   
    
    for tipo, colunas in tipos.items():
        
        base_jogador['Odd_Justa - ' + tipo] = 1 / (1 - poisson.pmf(0, base_jogador[colunas].mean(axis=1))) + base_jogador[colunas].std(axis=1)
        base_jogador['Apostar? - ' + tipo] = base_jogador.apply(lambda row: 'Sim' if row['Odd Bet'] > row['Odd_Justa - ' + tipo] else 'Não', axis=1)

    tabela_sim_nao = pd.DataFrame()

    
    # Itera sobre as colunas 'Sim' + tipo
    for tipo in tipos.keys():
        # Agrupa os dados
        grupo = base_jogador.groupby('Apostar? - ' + tipo)
        
        # Calcula a soma da coluna 'Odd Bet' quando 'Bateu' é igual a 1
        soma_bateu = grupo.apply(lambda x: x[x['Bateu'] == 1]['Odd Bet'].sum())
        
        # Calcula a quantidade de valores em cada grupo
        quantidade = grupo.size()
        
        # Calcula o aproveitamento
        aproveitamento = soma_bateu / quantidade
        aproveitamento =round((aproveitamento-1)*100,2)
        
        # Cria um DataFrame com os resultados
        df_resultado = pd.DataFrame({'QTD': quantidade, 'Soma': soma_bateu, 'Aproveitamento': aproveitamento})
        df_resultado['Tipo'] = 'Sim - ' + tipo
        # Adiciona à tabela final
        tabela_sim_nao = pd.concat([tabela_sim_nao, df_resultado])
    tabela_sim_nao

   