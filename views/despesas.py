import streamlit as st
import gspread
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.auth import default
import pandas as pd
from datetime import date
from funcs.retrieve_data_despesas import load_data_despesas

def despesas():
    st.title("💸 Despesas")
    st.write("Relatórios de despesas")
    
    vendedor = "vendasremape@gmail.com"
    
    # Carrega os dados usando a função cacheada
    df = load_data_despesas()

    # Filtro data inicial e final
    data_inicial = st.date_input("Data Inicial", value=date.today())
    data_final = st.date_input("Data Final", value=date.today())

    # Verifica se a data inicial é menor ou igual à data final
    if data_inicial > data_final:
        st.error("A Data Inicial não pode ser posterior à Data Final.")
        return

    # Filtra os dados com base nos filtros selecionados
    df_selected = df.copy()
    df_selected = df_selected[(df_selected['DATA'] >= data_inicial) & (df_selected['DATA'] <= data_final)]
    df_selected = df_selected[df_selected['VENDEDOR'] == vendedor]

    # Função para formatar o DataFrame
    def format_dataframe(df):
        df_formatted = df.copy()

        # Do not process financial columns; display them as they are
        df_formatted['OUTRAS DESPESAS'] = df_formatted['OUTRAS DESPESAS'].astype(str)

        # Format 'KM INICIAL' and 'KM FINAL' columns with '.' as thousands separator
        for col in ['KM INICIAL', 'KM FINAL']:
            df_formatted[col] = pd.to_numeric(df_formatted[col], errors='coerce')
            df_formatted[col] = df_formatted[col].apply(
                lambda x: f'{x:,.0f}'.replace(',', '.') if pd.notnull(x) else ''
            )

        # Format 'DATA' column to show only the date in 'DD/MM/YYYY' format
        df_formatted['DATA'] = df_formatted['DATA'].apply(
            lambda x: x.strftime('%d/%m/%Y') if pd.notnull(x) else ''
        )

        return df_formatted


    # Aplicar formatação ao DataFrame selecionado
    df_formatted = format_dataframe(df_selected)

    # Exibe a tabela de despesas com os dados filtrados e formatados
    exibir_colunas = ['DATA', 'KM INICIAL', 'KM FINAL', 'KM TOTAL' ,'ESTACIONAMENTO', 'PEDÁGIO', 'OUTRAS DESPESAS', 'DESCRIÇÃO DE OUTRAS DESPESAS']
    st.subheader("Tabela de Despesas")
    st.dataframe(df_formatted[exibir_colunas], hide_index=True)

    #Guarda o total de KM em uma variável
    df_formatted['KM TOTAL'] = pd.to_numeric(df_formatted['KM TOTAL'], errors='coerce')
    total_km = df_formatted['KM TOTAL'].sum()
    #Faz o somatório das despesas e guarda em uma variável
    df_formatted['ESTACIONAMENTO'] = df_formatted['ESTACIONAMENTO'].str.replace(',', '.')
    df_formatted['ESTACIONAMENTO'] = pd.to_numeric(df_formatted['ESTACIONAMENTO'], errors='coerce')
    total_estacionamento = df_formatted['ESTACIONAMENTO'].sum()
    df_formatted['PEDÁGIO'] = df_formatted['PEDÁGIO'].str.replace(',', '.')
    df_formatted['PEDÁGIO'] = pd.to_numeric(df_formatted['PEDÁGIO'], errors='coerce')
    total_pedagio = df_formatted['PEDÁGIO'].sum()
    df_formatted['OUTRAS DESPESAS'] = df_formatted['OUTRAS DESPESAS'].str.replace(',', '.')
    df_formatted['OUTRAS DESPESAS'] = pd.to_numeric(df_formatted['OUTRAS DESPESAS'], errors='coerce')
    total_outros = df_formatted['OUTRAS DESPESAS'].sum()
    
    #Organiza o resultado em cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("Total de KM")
        st.metric(label="", value=total_km)
    with col2:
        st.info("Total Estacionamento")
        st.metric(label="", value=format_currency(total_estacionamento))
    with col3:
        st.info("Total Pedágio")
        st.metric(label="", value=format_currency(total_pedagio))
    with col4:
        st.info("Total Outras Despesas")
        st.metric(label="", value=format_currency(total_outros))

#Função para formatar para R$
def format_currency(value):
    return f"R$ {value:,.2f}".replace('.', 'X').replace(',', '.').replace('X', ',')
