
import plotly.express as px
import requests
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import streamlit.components.v1 as components
from PIL import Image
from functools import reduce
import io
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
from st_pages import Page, Section, add_page_title, show_pages
import re
from openpyxl import Workbook
import xlsxwriter
from openpyxl.utils.dataframe import dataframe_to_rows

st.set_page_config(page_title ="Análise aposta", layout="wide", initial_sidebar_state="collapsed")
st.title('Analisar Jogos')


#@st.experimental_memo.clear()
@st.cache_data

def importar_base(liga):
    if liga == "argentino":
        df = pd.read_excel("argentino.xlsx", sheet_name=['BD_Times', 'BD_Jogo'])
    elif liga == "serie_a":
        df = pd.read_excel("serie_a.xlsx", sheet_name=['BD_Times', 'BD_Jogo'])
    elif liga == "serie_b":
        df = pd.read_excel("serie_b.xlsx", sheet_name=['BD_Times', 'BD_Jogo'])
    elif liga == "Frânces":
        df = pd.read_excel("Frânces.xlsx", sheet_name=['BD_Times', 'BD_Jogo'])
    elif liga == "Bundesliga":
        df = pd.read_excel("Bundesliga.xlsx", sheet_name=['BD_Times', 'BD_Jogo'])
    elif liga == "Italiano":
        df = pd.read_excel("Italiano.xlsx", sheet_name=['BD_Times', 'BD_Jogo'])     
    elif liga == "LaLiga":
        df = pd.read_excel("LaLiga.xlsx", sheet_name=['BD_Times', 'BD_Jogo'])       
    elif liga == "Premier League":
        df = pd.read_excel("Premier League.xlsx", sheet_name=['BD_Times', 'BD_Jogo'])                   
    else:
        raise ValueError("Liga inválida: {}".format(liga))

    return df



def analise(casa,fora): 

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
  liga = [[casa, fora, '-', '1.5', 'Gols','Jogo', o_u5casac_gols_1, o_u5casag_gols_1, o_u5foraf_gols_1, o_u5forag_gols_1, m_u5casac_gols, m_u5casag_gols, m_u5foraf_gols, m_u5forag_gols, m_liga_gols, m_liga_gols, o_liga_gols_1, o_liga_gols_1],
      [casa, fora, '-', '2.5', 'Gols','Jogo', o_u5casac_gols_2, o_u5casag_gols_2, o_u5foraf_gols_2, o_u5forag_gols_2, m_u5casac_gols, m_u5casag_gols, m_u5foraf_gols, m_u5forag_gols, m_liga_gols, m_liga_gols, o_liga_gols_2, o_liga_gols_2],
      [casa, fora, '-', '0.5', 'Gols','Casa', o_u5casactf_gols_0, o_u5casagtf_gols_0,  o_u5foraftr_gols_0, o_u5foragtr_gols_0, m_u5casact_f_gols,m_u5casagt_f_gols,  m_u5foraft_r_gols, m_u5foragt_r_gols, m_liga_golsc, m_liga_golsf,  o_ligac_gols_0, o_ligaf_gols_0 ],
      [casa, fora, '-', '0.5', 'Gols','Fora', o_u5foraftf_gols_0, o_u5foragtf_gols_0,  o_u5casactr_gols_0, o_u5casagtr_gols_0, m_u5foraft_f_gols,m_u5foragt_f_gols,  m_u5casact_r_gols, m_u5casagt_r_gols, m_liga_golsc, m_liga_golsf,  o_ligac_gols_0, o_ligaf_gols_0 ],
      [casa, fora, '-', '6.5', 'Cantos','Jogo', o_u5casac_cantos_6, o_u5casag_cantos_6, o_u5foraf_cantos_6, o_u5forag_cantos_6, m_u5casac_cantos, m_u5casag_cantos, m_u5foraf_cantos, m_u5forag_cantos, m_liga_cantos, m_liga_cantos, o_liga_cantos_6, o_liga_cantos_6],
      [casa, fora, '-', '7.5', 'Cantos','Jogo', o_u5casac_cantos_7, o_u5casag_cantos_7, o_u5foraf_cantos_7, o_u5forag_cantos_7, m_u5casac_cantos, m_u5casag_cantos, m_u5foraf_cantos, m_u5forag_cantos, m_liga_cantos, m_liga_cantos, o_liga_cantos_7, o_liga_cantos_7],
      [casa, fora, '-', '1.5', 'Cantos','Casa', o_u5casactf_cantos_1, o_u5casagtf_cantos_1,  o_u5foraftr_cantos_1, o_u5foragtr_cantos_1, m_u5casact_f_cantos,m_u5casagt_f_cantos,  m_u5foraft_r_cantos, m_u5foragt_r_cantos, m_liga_cantosc, m_liga_cantosf,  o_ligac_cantos_1, o_ligaf_cantos_1],
      [casa, fora, '-', '1.5', 'Cantos','Fora', o_u5foraftf_cantos_1, o_u5foragtf_cantos_1,  o_u5casactr_cantos_1, o_u5casagtr_cantos_1, m_u5foraft_f_cantos,m_u5foragt_f_cantos,  m_u5casact_r_cantos, m_u5casagt_r_cantos, m_liga_cantosc, m_liga_cantosf,  o_ligac_cantos_1, o_ligaf_cantos_1],
      [casa, fora, '-', '2.5', 'Cantos','Casa', o_u5casactf_cantos_2, o_u5casagtf_cantos_2,  o_u5foraftr_cantos_2, o_u5foragtr_cantos_2, m_u5casact_f_cantos,m_u5casagt_f_cantos,  m_u5foraft_r_cantos, m_u5foragt_r_cantos, m_liga_cantosc, m_liga_cantosf,  o_ligac_cantos_2, o_ligaf_cantos_2],
      [casa, fora, '-', '2.5', 'Cantos','Fora', o_u5foraftf_cantos_2, o_u5foragtf_cantos_2,  o_u5casactr_cantos_2, o_u5casagtr_cantos_2, m_u5foraft_f_cantos,m_u5foragt_f_cantos,  m_u5casact_r_cantos, m_u5casagt_r_cantos, m_liga_cantosc, m_liga_cantosf,  o_ligac_cantos_2, o_ligaf_cantos_2],
      [casa, fora, '-', '3.5', 'Cantos','Casa', o_u5casactf_cantos_3, o_u5casagtf_cantos_3,  o_u5foraftr_cantos_3, o_u5foragtr_cantos_3, m_u5casact_f_cantos,m_u5casagt_f_cantos,  m_u5foraft_r_cantos, m_u5foragt_r_cantos, m_liga_cantosc, m_liga_cantosf,  o_ligac_cantos_3, o_ligaf_cantos_3],
      [casa, fora, '-', '3.5', 'Cantos','Fora', o_u5foraftf_cantos_3, o_u5foragtf_cantos_3,  o_u5casactr_cantos_3, o_u5casagtr_cantos_3, m_u5foraft_f_cantos,m_u5foragt_f_cantos,  m_u5casact_r_cantos, m_u5casagt_r_cantos, m_liga_cantosc, m_liga_cantosf,  o_ligac_cantos_3, o_ligaf_cantos_3],
      [casa, fora, '-', '4.5', 'Cantos','Casa', o_u5casactf_cantos_4, o_u5casagtf_cantos_4,  o_u5foraftr_cantos_4, o_u5foragtr_cantos_4, m_u5casact_f_cantos,m_u5casagt_f_cantos,  m_u5foraft_r_cantos, m_u5foragt_r_cantos, m_liga_cantosc, m_liga_cantosf,  o_ligac_cantos_4, o_ligaf_cantos_4],
      [casa, fora, '-', '4.5', 'Cantos','Fora', o_u5foraftf_cantos_4, o_u5foragtf_cantos_4,  o_u5casactr_cantos_4, o_u5casagtr_cantos_4, m_u5foraft_f_cantos,m_u5foragt_f_cantos,  m_u5casact_r_cantos, m_u5casagt_r_cantos, m_liga_cantosc, m_liga_cantosf,  o_ligac_cantos_4, o_ligaf_cantos_4],
      [casa, fora, '-', '5.5', 'Cantos','Casa', o_u5casactf_cantos_5, o_u5casagtf_cantos_5,  o_u5foraftr_cantos_5, o_u5foragtr_cantos_5, m_u5casact_f_cantos,m_u5casagt_f_cantos,  m_u5foraft_r_cantos, m_u5foragt_r_cantos, m_liga_cantosc, m_liga_cantosf,  o_ligac_cantos_5, o_ligaf_cantos_5],
      [casa, fora, '-', '5.5', 'Cantos','Fora', o_u5foraftf_cantos_5, o_u5foragtf_cantos_5,  o_u5casactr_cantos_5, o_u5casagtr_cantos_5, m_u5foraft_f_cantos,m_u5foragt_f_cantos,  m_u5casact_r_cantos, m_u5casagt_r_cantos, m_liga_cantosc, m_liga_cantosf,  o_ligac_cantos_5, o_ligaf_cantos_5]]
      
    
  analise = pd.DataFrame(liga, columns= ['Casa', 'Fora','Bateu','Linha', 'Tipo de Linha', 'Quem Faz','Casa Fazer - M','Casa Fazer - G', 'Fora Fazer - M', 'Fora Fazer - G', 'Média Casa - M','Média Casa - G', 'Média Fora - M','Média Fora - G',  'Media Liga Casa','Media Liga Fora','Ocorrencia Liga Casa','Ocorrencia Liga Fora'])

  return analise

dados_filtrados = None
    
tab1, tab2,tab3,tab4,tab5 = st.tabs(['Inserir Partidas','Analisar Jogos','Linhas Extras','Linhas Selecionadas','Analise 2.5'])

with tab1:
    liga = st.selectbox("Escolha a liga:", ("argentino", "serie_a", "serie_b", "Frânces", "Bundesliga", "Italiano","LaLiga", "Premier League"))
    dfs = importar_base(liga)
    geral = dfs['BD_Times']
    jogo = dfs['BD_Jogo']

    jogos = st.number_input("Quantidade de jogos", min_value=1, max_value=10, value=1)

    if jogos == 1:
        col1, col2 = st.columns(2)
        with col1:
            casa1 = st.text_input("Time Casa 1:", key="casa1")
        with col2:
            fora1 = st.text_input("Time Fora 1:", key="fora1")        

    elif jogos == 2:
        col1, col2 = st.columns(2)    
        with col1:
            casa1 = st.text_input("Time Casa 1:", key="casa1")
            casa2 = st.text_input("Time Casa 2:", key="casa2")
        with col2:
            fora1 = st.text_input("Time Fora 1:", key="fora1")  
            fora2 = st.text_input("Time Fora 2:", key="fora2")          
    elif jogos == 3:
        col1, col2 = st.columns(2)    
        with col1:
            casa1 = st.text_input("Time Casa 1:", key="casa1")
            casa2 = st.text_input("Time Casa 2:", key="casa2")
            casa3 = st.text_input("Time Casa 3:", key="casa3")            
        with col2:
            fora1 = st.text_input("Time Fora 1:", key="fora1")  
            fora2 = st.text_input("Time Fora 2:", key="fora2")      
            fora3 = st.text_input("Time Fora 3:", key="fora3")       
    elif jogos == 4:
        col1, col2 = st.columns(2)    
        with col1:
            casa1 = st.text_input("Time Casa 1:", key="casa1")
            casa2 = st.text_input("Time Casa 2:", key="casa2")
            casa3 = st.text_input("Time Casa 3:", key="casa3")        
            casa4 = st.text_input("Time Casa 4:", key="casa4")            
        with col2:
            fora1 = st.text_input("Time Fora 1:", key="fora1")  
            fora2 = st.text_input("Time Fora 2:", key="fora2")      
            fora3 = st.text_input("Time Fora 3:", key="fora3")  
            fora4 = st.text_input("Time Fora 4:", key="fora4")  
    elif jogos == 5:
        col1, col2 = st.columns(2)    
        with col1:
            casa1 = st.text_input("Time Casa 1:", key="casa1")
            casa2 = st.text_input("Time Casa 2:", key="casa2")
            casa3 = st.text_input("Time Casa 3:", key="casa3")        
            casa4 = st.text_input("Time Casa 4:", key="casa4")  
            casa5 = st.text_input("Time Casa 5:", key="casa5")              
        with col2:
            fora1 = st.text_input("Time Fora 1:", key="fora1")  
            fora2 = st.text_input("Time Fora 2:", key="fora2")      
            fora3 = st.text_input("Time Fora 3:", key="fora3")  
            fora4 = st.text_input("Time Fora 4:", key="fora4")   
            fora5 = st.text_input("Time Fora 5:", key="fora5")            
    else: 
        print('erro')
        

    #button_clicked = st.button("Analisar Jogos")

    global planilhas
    global planilhas1
    global planilhas2
    global planilhas3
    global planilhas4
    global planilhas5
    global planilhas6
    global planilhas7
    global planilhas8
    global planilhas9
    global planilhas10
    global filtro_gols
    global filtro_gols1
    global filtro_gols2
    global filtro_gols3
    global filtro_gols4
    global filtro_gols5
    global filtro_gols6
    global filtro_gols7
    global filtro_gols8
    global filtro_gols9
    global filtro_gols10
    global filtro_cantos
    global filtro_cantos1
    global filtro_cantos2
    global filtro_cantos3
    global filtro_cantos4
    global filtro_cantos5
    global filtro_cantos6
    global filtro_cantos7
    global filtro_cantos8
    global filtro_cantos9
    global filtro_cantos10
    
    


    if jogos == 1:
        planilhas = analise(casa1, fora1)
        dados_filtrados = planilhas.iloc[planilhas.loc[planilhas['Quem Faz'] == 'Jogo'].index]
        dados_filtrados = dados_filtrados.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]
        filtro_gols = planilhas.loc[(planilhas['Quem Faz'] == 'Jogo') & (planilhas['Tipo de Linha'] == 'Gols') & (planilhas['Linha'] == '1.5')]   
        filtro_cantos = planilhas.loc[(planilhas['Quem Faz'] == 'Jogo') & (planilhas['Tipo de Linha'] == 'Cantos') & (planilhas['Linha'] == '7.5')]  
        dados_filtrados_ex = planilhas.iloc[planilhas.loc[planilhas['Quem Faz'] != 'Jogo'].index]
        dados_filtrados_ex = dados_filtrados_ex.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]        
        dados_filtrados_25 = planilhas.loc[(planilhas['Quem Faz'] == 'Jogo') & (planilhas['Tipo de Linha'] == 'Gols') & (planilhas['Linha'] == '2.5')]        
    elif jogos == 2:
        planilhas1 =  analise(casa1, fora1)
        planilhas2 =  analise(casa2, fora2)   
        dados_filtrados1 = planilhas1.iloc[planilhas1.loc[planilhas1['Quem Faz'] == 'Jogo'].index]
        dados_filtrados1 = dados_filtrados1.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]
        dados_filtrados2 = planilhas2.iloc[planilhas2.loc[planilhas2['Quem Faz'] == 'Jogo'].index]
        dados_filtrados2 = dados_filtrados2.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]
        filtro_gols1 =  planilhas1.loc[(planilhas1['Quem Faz'] == 'Jogo') & (planilhas1['Tipo de Linha'] == 'Gols') & (planilhas1['Linha'] == '1.5')]
        filtro_cantos1 = planilhas1.loc[(planilhas1['Quem Faz'] == 'Jogo') & (planilhas1['Tipo de Linha'] == 'Cantos') & (planilhas1['Linha'] == '7.5')]
        filtro_gols2 =  planilhas2.loc[(planilhas2['Quem Faz'] == 'Jogo') & (planilhas2['Tipo de Linha'] == 'Gols') & (planilhas2['Linha'] == '1.5')]
        filtro_cantos2 = planilhas2.loc[(planilhas2['Quem Faz'] == 'Jogo') & (planilhas2['Tipo de Linha'] == 'Cantos') & (planilhas2['Linha'] == '7.5')]
        dados_filtrados1_ex = planilhas1.iloc[planilhas1.loc[planilhas1['Quem Faz'] != 'Jogo'].index]
        dados_filtrados1_ex = dados_filtrados1_ex.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]
        dados_filtrados2_ex = planilhas2.iloc[planilhas2.loc[planilhas2['Quem Faz'] != 'Jogo'].index]
        dados_filtrados2_ex = dados_filtrados2_ex.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]
        dados_filtrados_25_1 =  planilhas1.loc[(planilhas1['Quem Faz'] == 'Jogo') & (planilhas1['Tipo de Linha'] == 'Gols') & (planilhas1['Linha'] == '2.5')]   
        dados_filtrados_25_2 =  planilhas2.loc[(planilhas2['Quem Faz'] == 'Jogo') & (planilhas2['Tipo de Linha'] == 'Gols') & (planilhas2['Linha'] == '2.5')]  
        dados_filtrados_25 = pd.concat(dados_filtrados_25_1, dados_filtrados_25_2, ignore_index=True)     
                                                                                                                         
                                                                                                                         
    elif jogos == 3:
        planilhas1 =  analise(casa1, fora1)
        planilhas2 =  analise(casa2, fora2) 
        planilhas3 =  analise(casa2, fora2)  
        dados_filtrados1 = planilhas1.iloc[planilhas1.loc[planilhas1['Quem Faz'] == 'Jogo'].index]
        dados_filtrados1 = dados_filtrados1.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]
        dados_filtrados2 = planilhas2.iloc[planilhas2.loc[planilhas2['Quem Faz'] == 'Jogo'].index]
        dados_filtrados2 = dados_filtrados2.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]
        dados_filtrados3 = planilhas3.iloc[planilhas3.loc[planilhas3['Quem Faz'] == 'Jogo'].index]
        dados_filtrados3 = dados_filtrados3.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]        
        filtro_gols1 =  planilhas1.loc[(planilhas1['Quem Faz'] == 'Jogo') & (planilhas1['Tipo de Linha'] == 'Gols') & (planilhas1['Linha'] == '1.5')]
        filtro_cantos1 = planilhas1.loc[(planilhas1['Quem Faz'] == 'Jogo') & (planilhas1['Tipo de Linha'] == 'Cantos') & (planilhas1['Linha'] == '7.5')]
        filtro_gols2 =  planilhas2.loc[(planilhas2['Quem Faz'] == 'Jogo') & (planilhas2['Tipo de Linha'] == 'Gols') & (planilhas2['Linha'] == '1.5')]
        filtro_cantos2 = planilhas2.loc[(planilhas2['Quem Faz'] == 'Jogo') & (planilhas2['Tipo de Linha'] == 'Cantos') & (planilhas2['Linha'] == '7.5')]     
        filtro_gols3 =  planilhas3.loc[(planilhas3['Quem Faz'] == 'Jogo') & (planilhas3['Tipo de Linha'] == 'Gols') & (planilhas3['Linha'] == '1.5')]
        filtro_cantos3 = planilhas3.loc[(planilhas3['Quem Faz'] == 'Jogo') & (planilhas3['Tipo de Linha'] == 'Cantos') & (planilhas3['Linha'] == '7.5')] 
        dados_filtrados1_ex = planilhas1.iloc[planilhas1.loc[planilhas1['Quem Faz'] != 'Jogo'].index]
        dados_filtrados1_ex = dados_filtrados1_ex.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]
        dados_filtrados2_ex = planilhas2.iloc[planilhas2.loc[planilhas2['Quem Faz'] != 'Jogo'].index]
        dados_filtrados2_ex = dados_filtrados2_ex.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]
        dados_filtrados3_ex = planilhas3.iloc[planilhas3.loc[planilhas3['Quem Faz'] != 'Jogo'].index]
        dados_filtrados3_ex = dados_filtrados3_ex.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]         
        dados_filtrados_25_1 =  planilhas1.loc[(planilhas1['Quem Faz'] == 'Jogo') & (planilhas1['Tipo de Linha'] == 'Gols') & (planilhas1['Linha'] == '2.5')]   
        dados_filtrados_25_2 =  planilhas2.loc[(planilhas2['Quem Faz'] == 'Jogo') & (planilhas2['Tipo de Linha'] == 'Gols') & (planilhas2['Linha'] == '2.5')] 
        
        dados_filtrados_25_3 =  planilhas3.loc[(planilhas2['Quem Faz'] == 'Jogo') & (planilhas3['Tipo de Linha'] == 'Gols') & (planilhas3['Linha'] == '2.5')] 
        
        
        dados_filtrados_25 = pd.concat(dados_filtrados_25_1, dados_filtrados_25_2,dados_filtrados_25_3, ignore_index=True)                                                                                                                            
    elif jogos == 4:
        planilhas1 =  analise(casa1, fora1)
        planilhas2 =  analise(casa2, fora2) 
        planilhas3 =  analise(casa2, fora2)
        planilhas4 =  analise(casa2, fora2)  
        dados_filtrados1 = planilhas1.iloc[planilhas1.loc[planilhas1['Quem Faz'] == 'Jogo'].index]
        dados_filtrados1 = dados_filtrados1.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]
        dados_filtrados2 = planilhas2.iloc[planilhas2.loc[planilhas2['Quem Faz'] == 'Jogo'].index]
        dados_filtrados2 = dados_filtrados2.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]
        dados_filtrados3 = planilhas3.iloc[planilhas3.loc[planilhas4['Quem Faz'] == 'Jogo'].index]
        dados_filtrados3 = dados_filtrados3.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]          
        dados_filtrados4 = planilhas4.iloc[planilhas4.loc[planilhas4['Quem Faz'] == 'Jogo'].index]
        dados_filtrados4 = dados_filtrados4.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]        
        filtro_gols1 =  planilhas1.loc[(planilhas1['Quem Faz'] == 'Jogo') & (planilhas1['Tipo de Linha'] == 'Gols') & (planilhas1['Linha'] == '1.5')]
        filtro_cantos1 = planilhas1.loc[(planilhas1['Quem Faz'] == 'Jogo') & (planilhas1['Tipo de Linha'] == 'Cantos') & (planilhas1['Linha'] == '7.5')]
        filtro_gols2 =  planilhas2.loc[(planilhas2['Quem Faz'] == 'Jogo') & (planilhas2['Tipo de Linha'] == 'Gols') & (planilhas2['Linha'] == '1.5')]
        filtro_cantos2 = planilhas2.loc[(planilhas2['Quem Faz'] == 'Jogo') & (planilhas2['Tipo de Linha'] == 'Cantos') & (planilhas2['Linha'] == '7.5')]     
        filtro_gols3 =  planilhas3.loc[(planilhas3['Quem Faz'] == 'Jogo') & (planilhas3['Tipo de Linha'] == 'Gols') & (planilhas3['Linha'] == '1.5')]
        filtro_cantos3 = planilhas3.loc[(planilhas3['Quem Faz'] == 'Jogo') & (planilhas3['Tipo de Linha'] == 'Cantos') & (planilhas3['Linha'] == '7.5')]  
        filtro_gols4 =  planilhas4.loc[(planilhas4['Quem Faz'] == 'Jogo') & (planilhas4['Tipo de Linha'] == 'Gols') & (planilhas4['Linha'] == '1.5')]
        filtro_cantos4 = planilhas4.loc[(planilhas4['Quem Faz'] == 'Jogo') & (planilhas4['Tipo de Linha'] == 'Cantos') & (planilhas4['Linha'] == '7.5')] 
        dados_filtrados1 = planilhas1.iloc[planilhas1.loc[planilhas1['Quem Faz'] != 'Jogo'].index]
        dados_filtrados1_ex = dados_filtrados1_ex.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]
        dados_filtrados2_ex = planilhas2.iloc[planilhas2.loc[planilhas2['Quem Faz'] != 'Jogo'].index]
        dados_filtrados2_ex = dados_filtrados2_ex.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]
        dados_filtrados3_ex = planilhas3.iloc[planilhas3.loc[planilhas4['Quem Faz'] != 'Jogo'].index]
        dados_filtrados3_ex = dados_filtrados3_ex.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]          
        dados_filtrados4_ex = planilhas4.iloc[planilhas4.loc[planilhas4['Quem Faz'] != 'Jogo'].index]
        dados_filtrados4_ex = dados_filtrados4_ex.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]     
        dados_filtrados_25_1 =  planilhas1.loc[(planilhas1['Quem Faz'] == 'Jogo') & (planilhas1['Tipo de Linha'] == 'Gols') & (planilhas1['Linha'] == '2.5')] 
        dados_filtrados_25_2 =  planilhas2.loc[(planilhas2['Quem Faz'] == 'Jogo') & (planilhas2['Tipo de Linha'] == 'Gols') & (planilhas2['Linha'] == '2.5')] 
        dados_filtrados_25_3 =  planilhas3.loc[(planilhas2['Quem Faz'] == 'Jogo') & (planilhas3['Tipo de Linha'] == 'Gols') & (planilhas3['Linha'] == '2.5')]  
        dados_filtrados_25_4 =  planilhas4.loc[(planilhas4['Quem Faz'] == 'Jogo') & (planilhas4['Tipo de Linha'] == 'Gols') & (planilhas4['Linha'] == '2.5')]      
        dados_filtrados_25 = pd.concat(dados_filtrados_25_1, dados_filtrados_25_2,dados_filtrados_25_3,dados_filtrados_25_4, ignore_index=True)                                                                                                                                                                            
    elif jogos == 5:
        planilhas1 =  analise(casa1, fora1)
        planilhas2 =  analise(casa2, fora2) 
        planilhas3 =  analise(casa2, fora2)
        planilhas4 =  analise(casa2, fora2)  
        planilhas5 =  analise(casa2, fora2)         
        dados_filtrados1 = planilhas1.iloc[planilhas1.loc[planilhas1['Quem Faz'] == 'Jogo'].index]
        dados_filtrados1 = dados_filtrados1.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]
        dados_filtrados2 = planilhas2.iloc[planilhas2.loc[planilhas2['Quem Faz'] == 'Jogo'].index]
        dados_filtrados2 = dados_filtrados2.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]
        dados_filtrados3 = planilhas3.iloc[planilhas3.loc[planilhas4['Quem Faz'] == 'Jogo'].index]
        dados_filtrados3=  dados_filtrados3.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]          
        dados_filtrados4 = planilhas4.iloc[planilhas4.loc[planilhas4['Quem Faz'] == 'Jogo'].index]
        dados_filtrados4 = dados_filtrados4.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]      
        dados_filtrados5 = planilhas5.iloc[planilhas5.loc[planilhas5['Quem Faz'] == 'Jogo'].index]
        dados_filtrados5 = dados_filtrados5.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]           
        filtro_gols1 =  planilhas1.loc[(planilhas1['Quem Faz'] == 'Jogo') & (planilhas1['Tipo de Linha'] == 'Gols') & (planilhas1['Linha'] == '1.5')]
        filtro_cantos1 = planilhas1.loc[(planilhas1['Quem Faz'] == 'Jogo') & (planilhas1['Tipo de Linha'] == 'Cantos') & (planilhas1['Linha'] == '7.5')]
        filtro_gols2 =  planilhas2.loc[(planilhas2['Quem Faz'] == 'Jogo') & (planilhas2['Tipo de Linha'] == 'Gols') & (planilhas2['Linha'] == '1.5')]
        filtro_cantos2 = planilhas2.loc[(planilhas2['Quem Faz'] == 'Jogo') & (planilhas2['Tipo de Linha'] == 'Cantos') & (planilhas2['Linha'] == '7.5')]     
        filtro_gols3 =  planilhas3.loc[(planilhas3['Quem Faz'] == 'Jogo') & (planilhas3['Tipo de Linha'] == 'Gols') & (planilhas3['Linha'] == '1.5')]
        filtro_cantos3 = planilhas3.loc[(planilhas3['Quem Faz'] == 'Jogo') & (planilhas3['Tipo de Linha'] == 'Cantos') & (planilhas3['Linha'] == '7.5')]  
        filtro_gols4 =  planilhas4.loc[(planilhas4['Quem Faz'] == 'Jogo') & (planilhas4['Tipo de Linha'] == 'Gols') & (planilhas4['Linha'] == '1.5')]
        filtro_cantos4 = planilhas4.loc[(planilhas4['Quem Faz'] == 'Jogo') & (planilhas4['Tipo de Linha'] == 'Cantos') & (planilhas4['Linha'] == '7.5')]  
        filtro_gols5 =  planilhas5.loc[(planilhas5['Quem Faz'] == 'Jogo') & (planilhas5['Tipo de Linha'] == 'Gols') & (planilhas5['Linha'] == '1.5')]
        filtro_cantos5 = planilhas5.loc[(planilhas5['Quem Faz'] == 'Jogo') & (planilhas5['Tipo de Linha'] == 'Cantos') & (planilhas5['Linha'] == '7.5')]    
        dados_filtrados1_ex = planilhas1.iloc[planilhas1.loc[planilhas1['Quem Faz'] != 'Jogo'].index]
        dados_filtrados1_ex = dados_filtrados1_ex.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]
        dados_filtrados2_ex = planilhas2.iloc[planilhas2.loc[planilhas2['Quem Faz'] != 'Jogo'].index]
        dados_filtrados2_ex = dados_filtrados2_ex.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]
        dados_filtrados3_ex = planilhas3.iloc[planilhas3.loc[planilhas4['Quem Faz'] != 'Jogo'].index]
        dados_filtrados3_ex =  dados_filtrados3_ex.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]          
        dados_filtrados4_ex = planilhas4.iloc[planilhas4.loc[planilhas4['Quem Faz'] != 'Jogo'].index]
        dados_filtrados4_ex = dados_filtrados4_ex.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]      
        dados_filtrados5_ex = planilhas5.iloc[planilhas5.loc[planilhas5['Quem Faz'] != 'Jogo'].index]
        dados_filtrados5_ex = dados_filtrados5_ex.iloc[:, [3,4,6,7,8,9,10,11,12,13,14,15,16]]
        dados_filtrados_25_1 =  planilhas1.loc[(planilhas1['Quem Faz'] == 'Jogo') & (planilhas1['Tipo de Linha'] == 'Gols') & (planilhas1['Linha'] == '2.5')]           
        dados_filtrados_25_2 =  planilhas2.loc[(planilhas2['Quem Faz'] == 'Jogo') & (planilhas2['Tipo de Linha'] == 'Gols') & (planilhas2['Linha'] == '2.5')] 
        dados_filtrados_25_3 =  planilhas3.loc[(planilhas2['Quem Faz'] == 'Jogo') & (planilhas3['Tipo de Linha'] == 'Gols') & (planilhas3['Linha'] == '2.5')]  
        dados_filtrados_25_4 =  planilhas4.loc[(planilhas4['Quem Faz'] == 'Jogo') & (planilhas4['Tipo de Linha'] == 'Gols') & (planilhas4['Linha'] == '2.5')]  
        
        dados_filtrados_25_5 =  planilhas5.loc[(planilhas5['Quem Faz'] == 'Jogo') & (planilhas5['Tipo de Linha'] == 'Gols') & (planilhas5['Linha'] == '2.5')]           
        dados_filtrados_25 = pd.concat(dados_filtrados_25_1, dados_filtrados_25_2,dados_filtrados_25_3,dados_filtrados_25_4,dados_filtrados_25_5, axis=0)                                                                                                                              
    else:
        print('Erro')    
with tab2:  
    
    def adicionar_linha(linha, filtro):
        if 'linhas_analisadas' not in st.session_state:
            st.session_state['linhas_analisadas'] = pd.DataFrame(columns=['Casa', 'Fora', 'Bateu', 'Linha', 'Tipo de Linha', 'Quem Faz', 'Casa Fazer - M', 'Casa Fazer - G', 'Fora Fazer - M', 'Fora Fazer - G', 'Média Casa - M', 'Média Casa - G', 'Média Fora - M', 'Média Fora - G','Media Liga Casa', 'Media Liga Fora', 'Ocorrencia Liga Casa', 'Ocorrencia Liga Fora'])
        if linha == 'Gols':

            st.session_state['linhas_analisadas'] = pd.concat([st.session_state['linhas_analisadas'], filtro], ignore_index=True)
        elif linha == 'Cantos':
            st.session_state['linhas_analisadas'] = pd.concat([st.session_state['linhas_analisadas'], filtro], ignore_index=True)        
        else:
            raise ValueError("Linha inválida. Escolha 'Gols' ou 'Cantos'.")

        return st.session_state['linhas_analisadas']
            
    if jogos == 1:
        st.write("{} x {}".format(casa1, fora1))
        st.dataframe(dados_filtrados)
        if st.button('Adicionar Gols'):
            adicionar_linha('Gols', filtro_gols)
        if st.button('Adicionar Cantos'):
            adicionar_linha('Cantos',filtro_cantos)

    elif jogos == 2:
        st.write("{} x {}".format(casa1, fora1))
        st.dataframe(dados_filtrados1)
        if st.button('Adicionar Gols1'):
            adicionar_linha('Gols', filtro_gols1)
        if st.button('Adicionar Cantos1'):
            adicionar_linha('Cantos', filtro_cantos1)
            
        st.write("{} x {}".format(casa2, fora2))
        st.dataframe(dados_filtrados2)     
        if st.button('Adicionar Gols2'):
            adicionar_linha('Gols', filtro_gols2)
        if st.button('Adicionar Cantos2'):
            adicionar_linha('Cantos', filtro_cantos2)
    elif jogos == 3:
        st.write("{} x {}".format(casa1, fora1))
        st.dataframe(dados_filtrados1)
        if st.button('Adicionar Gols1'):
            adicionar_linha('Gols', filtro_gols1)
        if st.button('Adicionar Cantos1'):
            adicionar_linha('Cantos', filtro_cantos1)
            
        st.write("{} x {}".format(casa2, fora2))
        st.dataframe(dados_filtrados2)     
        if st.button('Adicionar Gols2'):
            adicionar_linha('Gols', filtro_gols2)
        if st.button('Adicionar Cantos2'):
            adicionar_linha('Cantos', filtro_cantos2)    
            
        st.write("{} x {}".format(casa3, fora3))
        st.dataframe(dados_filtrados3)     
        if st.button('Adicionar Gols3'):
            adicionar_linha('Gols', filtro_gols3)
        if st.button('Adicionar Cantos3'):
            adicionar_linha('Cantos', filtro_cantos3)  
    elif jogos == 4:
        st.write("{} x {}".format(casa1, fora1))
        st.dataframe(dados_filtrados1)
        if st.button('Adicionar Gols1'):
            adicionar_linha('Gols', filtro_gols1)
        if st.button('Adicionar Cantos1'):
            adicionar_linha('Cantos', filtro_cantos1)
            
        st.write("{} x {}".format(casa2, fora2))
        st.dataframe(dados_filtrados2)     
        if st.button('Adicionar Gols2'):
            adicionar_linha('Gols', filtro_gols2)
        if st.button('Adicionar Cantos2'):
            adicionar_linha('Cantos', filtro_cantos2)    
            
        st.write("{} x {}".format(casa3, fora3))
        st.dataframe(dados_filtrados3)     
        if st.button('Adicionar Gols3'):
            adicionar_linha('Gols', filtro_gols3)
        if st.button('Adicionar Cantos3'):
            adicionar_linha('Cantos', filtro_cantos3)     
            
        st.write("{} x {}".format(casa4, fora4))
        st.dataframe(dados_filtrados4)     
        if st.button('Adicionar Gols4'):
            adicionar_linha('Gols', filtro_gols4)
        if st.button('Adicionar Cantos4'):
            adicionar_linha('Cantos', filtro_cantos4)  
            
    elif jogos == 5:
        st.write("{} x {}".format(casa1, fora1))
        st.dataframe(dados_filtrados1)
        if st.button('Adicionar Gols1'):
            adicionar_linha('Gols', filtro_gols1)
        if st.button('Adicionar Cantos1'):
            adicionar_linha('Cantos', filtro_cantos1)
            
        st.write("{} x {}".format(casa2, fora2))
        st.dataframe(dados_filtrados2)     
        if st.button('Adicionar Gols2'):
            adicionar_linha('Gols', filtro_gols2)
        if st.button('Adicionar Cantos2'):
            adicionar_linha('Cantos', filtro_cantos2)    
            
        st.write("{} x {}".format(casa3, fora3))
        st.dataframe(dados_filtrados3)     
        if st.button('Adicionar Gols3'):
            adicionar_linha('Gols', filtro_gols3)
        if st.button('Adicionar Cantos3'):
            adicionar_linha('Cantos', filtro_cantos3)     
            
        st.write("{} x {}".format(casa4, fora4))
        st.dataframe(dados_filtrados4)     
        if st.button('Adicionar Gols4'):
            adicionar_linha('Gols', filtro_gols4)
        if st.button('Adicionar Cantos4'):
            adicionar_linha('Cantos', filtro_cantos4)     
            
            
        st.write("{} x {}".format(casa5, fora5))
        st.dataframe(dados_filtrados5)     
        if st.button('Adicionar Gols5'):
            adicionar_linha('Gols', filtro_gols5)
        if st.button('Adicionar Cantos5'):
            adicionar_linha('Cantos', filtro_cantos5)               
                        
            
    else:
        print('Erro')
with tab3:
    
    if jogos == 1:
        st.write("{} x {}".format(casa1, fora1))
        st.dataframe(dados_filtrados_ex)
    elif jogos == 2:
        st.write("{} x {}".format(casa1, fora1))
        st.dataframe(dados_filtrados1_ex)
            
        st.write("{} x {}".format(casa2, fora2))
        st.dataframe(dados_filtrados2_ex)     

    elif jogos == 3:
        st.write("{} x {}".format(casa1, fora1))
        st.dataframe(dados_filtrados1_ex)

            
        st.write("{} x {}".format(casa2, fora2))
        st.dataframe(dados_filtrados2_ex)     

            
        st.write("{} x {}".format(casa3, fora3))
        st.dataframe(dados_filtrados_ex)     

    elif jogos == 4:
        st.write("{} x {}".format(casa1, fora1))
        st.dataframe(dados_filtrados1_ex)

            
        st.write("{} x {}".format(casa2, fora2))
        st.dataframe(dados_filtrados2_ex)     

            
        st.write("{} x {}".format(casa3, fora3))
        st.dataframe(dados_filtrados3_ex)     

            
        st.write("{} x {}".format(casa4, fora4))
        st.dataframe(dados_filtrados4_ex)     

            
    elif jogos == 5:
        st.write("{} x {}".format(casa1, fora1))
        st.dataframe(dados_filtrados1_ex)

            
        st.write("{} x {}".format(casa2, fora2))
        st.dataframe(dados_filtrados2_ex)     
   
            
        st.write("{} x {}".format(casa3, fora3))
        st.dataframe(dados_filtrados3_ex)     

            
        st.write("{} x {}".format(casa4, fora4))
        st.dataframe(dados_filtrados4_ex)     
            
        st.write("{} x {}".format(casa5, fora5))
        st.dataframe(dados_filtrados5_ex)                  
                        
            
    else:
        print('Erro')
    
    
with tab4:
    if 'linhas_analisadas' in st.session_state:
        st.write("Planilhas:")
        st.dataframe(st.session_state['linhas_analisadas'])

    df_tendencias = pd.read_excel("tendencias.xlsx")
    df_concatenado = pd.concat([df_tendencias, st.session_state['linhas_analisadas']], axis=0)

    temp_excel_file = "temp_excel_file.xlsx"
    df_concatenado.to_excel(temp_excel_file, index=False)

    st.download_button("Baixar arquivo Excel", data=open(temp_excel_file, 'rb'), file_name='tendencias.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    
def adicionar_linha_2(dados_filtrados_25):
    if 'Linhas_2.5' not in st.session_state:
        st.session_state['Linhas_2.5'] = pd.DataFrame(columns=['Casa', 'Fora', 'Bateu', 'Linha', 'Tipo de Linha', 'Quem Faz', 'Casa Fazer - M', 'Casa Fazer - G', 'Fora Fazer - M', 'Fora Fazer - G', 'Média Casa - M', 'Média Casa - G', 'Média Fora - M', 'Média Fora - G','Media Liga Casa', 'Media Liga Fora', 'Ocorrencia Liga Casa', 'Ocorrencia Liga Fora'])

    st.session_state['Linhas_2.5'] = pd.concat([st.session_state.get('Linhas_2.5', pd.DataFrame()), dados_filtrados_25], ignore_index=True)

    return st.session_state['Linhas_2.5']

with tab5:
    if st.button("Clique aqui"):
        adicionar_linha_2(dados_filtrados_25)
    
    st.dataframe(st.session_state.get('Linhas_2.5', pd.DataFrame()))