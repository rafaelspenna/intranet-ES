import streamlit as st
from funcs.retrieve_data_spreadsheet import load_data
from funcs.bussines_days_calc import calculate_business_days
import pandas as pd
from datetime import date

#Função que renderiza a página de visitas
def visitas():
    st.title("Visitas")
    
    #Definir vendedor
    vendedor = 'vendasremape@gmail.com'

    #Carregar dados da planilha para os DataFrames
    df_visitas = load_data("VISITAS", "%d/%m/%Y %H:%M:%S", "DATA")
    df_prospect = load_data("PROSPECÇÃO", "%d/%m/%Y %H:%M:%S", "DATA")
    df_aplicadores = load_data("QUESTIONÁRIO", "%d/%m/%Y %H:%M:%S", "DATA")

    #Definir colunas utilizadas em cada DataFrame
    visitas_coluns = ['DATA', 'CLIENTE', 'INDÚSTRIA', 'PERCEPÇÃO MERCADO', 'OBS']
    prospect_coluns = ['DATA', 'NOME DA EMPRESA', 'ENDEREÇO', 'RESPONSÁVEL', 'TELEFONE', 'E-MAIL', 'OBSERVAÇÕES']
    aplicadores_coluns = ['DATA', 'NOME', 'ENDEREÇO', 'TELEFONE', 'PRINCIPAIS DISTRIBUIDORES/LOJAS', 'PRINCIPAL DISTRIBUIDOR/LOJA']

    #Input de datas para filtrar as visitas
    initial_date = st.date_input("Data inicial", value=date.today())
    final_date = st.date_input("Data final", value=date.today())

    #Testa se as datas foram selecionadas corretamente
    if initial_date is not None and final_date is not None:
        initial_date = pd.to_datetime(initial_date).replace(hour=0, minute=0, second=0)
        final_date = pd.to_datetime(final_date).replace(hour=23, minute=59, second=59)
    else:
        st.warning("Por favor, selecione as datas inicial e final.")
    
    if initial_date > final_date:
        st.error("Data inicial deve ser anterior a data final.")
        return
    
    #Filtra os dados com base nos inputs de datas
    df_visitas_filtered = df_visitas.copy()
    df_visitas_filtered = df_visitas_filtered[(df_visitas_filtered['DATA'] >= initial_date) & (df_visitas_filtered['DATA'] <= final_date)]
    df_visitas_filtered = df_visitas_filtered[df_visitas_filtered['VENDEDOR'] == vendedor]

    df_prospect_filtered = df_prospect.copy()
    df_prospect_filtered = df_prospect_filtered[(df_prospect_filtered['DATA'] >= initial_date) & (df_prospect_filtered['DATA'] <= final_date)]
    df_prospect_filtered = df_prospect_filtered[df_prospect_filtered['VENDEDOR'] == vendedor]

    df_aplicadores_filtered = df_aplicadores.copy()
    df_aplicadores_filtered = df_aplicadores_filtered[(df_aplicadores_filtered['DATA'] >= initial_date) & (df_aplicadores_filtered['DATA'] <= final_date)]
    df_aplicadores_filtered = df_aplicadores_filtered[df_aplicadores_filtered['VENDEDOR'] == vendedor]

    #Tabela com quantidade de visitas, questionários e prospecções por dia útil
    bussiness_days = calculate_business_days(initial_date, final_date)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("Dias Úteis")
        st.metric(label="", value=bussiness_days)
    with col2:
        st.info("Quantidade de visitas")
        st.metric(label="", value=df_visitas_filtered.shape[0])
        st.info("Média diária de visitas")
        st.metric(label="", value=round(df_visitas_filtered.shape[0]/bussiness_days, 1))
    with col3:
        st.info("Quantidade de questionários")
        st.metric(label="", value=df_aplicadores_filtered.shape[0])
        st.info("Média diária de questionários")
        st.metric(label="", value=round(df_aplicadores_filtered.shape[0]/bussiness_days, 1))    
    with col4:
        st.info("Prospecções")
        st.metric(label="", value=df_prospect_filtered.shape[0])
        st.info("Média diária de prospecções")
        st.metric(label="", value=round(df_prospect_filtered.shape[0]/bussiness_days, 1))

    #Tabela com visitas
    st.subheader("Visitas")
    st.dataframe(df_visitas_filtered[visitas_coluns], hide_index=True)

    #Tabela com questionários
    st.subheader("Questionários")
    st.dataframe(df_aplicadores_filtered[aplicadores_coluns], hide_index=True)

    #Tabela com prospecções
    st.subheader("Prospecções")
    st.dataframe(df_prospect_filtered[prospect_coluns], hide_index=True)

