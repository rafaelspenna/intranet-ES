"""
    Função para carregar dados de uma planilha do Google Sheets.
    worksheet_name: str - Nome da aba da planilha a ser carregada.
    date_format: str - Formato da data na planilha. -> "%d/%m/%Y" ou "%d/%m/%Y %H:%M:%S"
    data_col: str - Nome da coluna que contém a data.
"""

import gspread
import pandas as pd
from google.auth import default
import streamlit as st

@st.cache_data(ttl=600)  # Cache os dados por 10 minutos
def load_data(worksheet_name, date_format, data_col):
    # Obter as credenciais padrão do ambiente (IAM no Cloud Run ou local com GOOGLE_APPLICATION_CREDENTIALS)
    creds, _ = default(scopes=[
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly",
    ])
    
    # Autenticar com gspread
    client = gspread.authorize(creds)

    # Acessa a planilha pelo ID
    sheet = client.open_by_key("1u1do3URWqU6_E9DAKenpm9F7BfKGw7sBNrtp0yxSwzk")
    worksheet = sheet.worksheet(worksheet_name)

    # Obtém os dados e converte para DataFrame
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    df = df.dropna(how="all")  # Remove linhas completamente vazias

    # Conversão da coluna "DATA" para datetime usando o formato especificado
    df[data_col] = pd.to_datetime(df[data_col], format=date_format, errors='coerce')

    return df
