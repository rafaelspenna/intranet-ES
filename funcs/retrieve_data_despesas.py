import gspread
import pandas as pd
from google.auth import default

def load_data_despesas():
    # Obter as credenciais padrão do ambiente (IAM do Cloud Run)
    creds, _ = default(scopes=[
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly",
    ])
    
    # Autenticar com o gspread
    client = gspread.authorize(creds)

    # Acessar a planilha pelo ID
    sheet = client.open_by_key("1u1do3URWqU6_E9DAKenpm9F7BfKGw7sBNrtp0yxSwzk")
    worksheet = sheet.worksheet("DESPESAS")

    # Obter todos os dados e converter para um DataFrame
    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])  # Ignorar cabeçalho
    df = df.dropna(how="all")  # Remover linhas vazias

    # Converter a coluna "DATA" para o formato datetime
    df['DATA'] = pd.to_datetime(df['DATA'], format="%d/%m/%Y", errors='coerce').dt.date

    return df

