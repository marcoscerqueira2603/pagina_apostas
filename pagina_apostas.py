import streamlit as st
import pandas as pd
import os
from openpyxl import load_workbook
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date
import numpy as np
import plotly.express as px
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



@st.cache_data()
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

tendencias = load_data(st.secrets["public_gsheets_url"])

@st.cache_data()
def load_data2(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

analise_2_5 = load_data2(st.secrets["public_gsheets_url2"])



# Interface para inserção de novos dados

tab1,tab2=  st.tabs(['Analise Jogo','Dash'])


with tab1:

    ligas = ['chines','espanhol', 'frances','holandes','ingles','portugues','serie_a','serie_b']
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

    ###7.5 Gols

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
                worksheet = client.open_by_url('https://docs.google.com/spreadsheets/d/17YiO2vWLU2iM8DHG7bFWI8VjKcx_aOqeww6bjvJOMRs/edit#gid=1561702516').get_worksheet(0)
        
        # Obter o número de linhas existentes na planilha
                num_rows = len(worksheet.get_all_values())
        
        # Inserir os dados nas linhas subsequentes
                values_to_insert = analise_adicao.values.tolist()
                worksheet.insert_rows(values_to_insert, num_rows + 1) 


    # Adicionar as novas linhas ao DataFrame
            
    if novas_linhas:
        novas_linhas_df = pd.DataFrame(novas_linhas, columns=tendencias.columns)
        #tendencias = pd.concat([tendencias, novas_linhas_df], ignore_index=True)

        # Atualizar a planilha com as novas linhas
        worksheet = client.open_by_url('https://docs.google.com/spreadsheets/d/11pW8bTEOeKUXOb7kd53_MJwGUHG19fLWTfHvpIYVUIY/edit#gid=0').get_worksheet(0)
        
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
        st.markdown('**Média últimos 5 jogos forade casa:** {}'.format(m_u5casac_cantos))
        st.markdown('**Média últimos 5 jogos geral:** {}'.format(m_u5casag_cantos))

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
        st.markdown('**Média últimos 5 jogos forade casa:** {}'.format(m_u5casac_cantos))
        st.markdown('**Média últimos 5 jogos geral:** {}'.format(m_u5casag_cantos))

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

    df_tendencias = tendencias 

    df_tendencias['Data'] = pd.to_datetime(df_tendencias['Data'], format='mixed', dayfirst=True)
    df_tendencias['mês'] = df_tendencias['Data'].dt.strftime('%b')
    
    df_tendencias = df_tendencias[df_tendencias['Bateu'] != "-"]
    df_tendencias['Bateu'] = df_tendencias['Bateu'].astype(int)  # Convertendo 'bateu' para int
    df_grouped = df_tendencias.groupby(['mês', 'Tipo de Linha'])['Bateu'].mean().reset_index()

    # Criando o gráfico usando Plotly Express
    fig_tendencias = px.bar(df_grouped, x='mês', y='Bateu', color='Tipo de Linha',
                         title='Aproveitamento por Mês - Cantos vs. Gols',
                         labels={'Bateu': 'Aproveitamento (%)'},
                         barmode='group')
    
    fig_tendencias.update_layout(xaxis_title='Mês', yaxis_title='Aproveitamento (%)')
    # Exibindo o gráfico
    st.plotly_chart(fig_tendencias)