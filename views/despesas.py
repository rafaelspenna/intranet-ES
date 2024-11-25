import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import date

def despesas():
    st.title("💸 Despesas")
    st.write("Relatórios de despesas")
    
    vendedor = "vendasremape@gmail.com"

    @st.cache_data(ttl=600)  # Cache os dados por 10 minutos
    def load_data():
        # Configure a conexão com o Google Sheets usando gspread e google-auth
        scope = ["https://www.googleapis.com/auth/spreadsheets.readonly", 
                "https://www.googleapis.com/auth/drive.readonly"]
        creds = Credentials.from_service_account_info(
            {
            "type": "service_account",
            "project_id": "pedidos-414920",
            "private_key_id": "38d5984fac1beb4d948108ae2af8c34c9c1b5785",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCGBqOLhUW8tg5J\ne/ELq5vRY+/Xf9+Ztkax3Jrjln9ENF8jse7anq1p4NraB8Z+Ci68oIJlL96vKky+\nrz0cjYi7Wh51UqrAwi+fB/0bXGilcP6cECuzYJcMmvqs698TZR0QDQNL/fl9UUK2\nO3bXZZIuCt2CTW/euL7ernO1pKE7Se8PV0eZ/go5QJoqrSpTNM+8xp1pKIlGfcTn\nTTRhgaZdhTIUACOc6H7eHWxpbEHwgvuqdf1fKf8TNe7Oz2AgcW/6xIgmNLRifqku\n0mnDwFGf2+LsxVTnro9Ep/KIYvaQQagl6Bof7SxkXJRJQkrG7QP9fh1+oz5No4pV\nQCxiGHKLAgMBAAECggEAITvmNAOhLlFKq6gjNoygP8TzRVG9JYWQdCxK8CJyfnwq\nF1TY8LcmMzoBqs0AyGJIApgenW7IXlEz5JjZo4npHOQU52zPUKsWWe4GMlGw1U12\npUZRP9K0wfhwLo7yqwGIumEvrxlUU2HiFAQczP6vx+ED2nrPQcA3/EnwAVvIa0Xn\nNNznuGA/0b+YFA/rawM1feZ/R+G/1BHszXKf45x032aSBMx7T64P+7VbIM3bIl9I\nYqvKZoAd5ZgUsSgpa/qEFxGD2766+G/O6mChZQz0hL9XDL+KpRSWhI4mulZLQ9ff\nVwnXpbsYLNQ9cX0yFSxPyiqBSVMtwr29WTmeSulJ8QKBgQC8EybhRJmEJ1rYuN1V\nVoB9SUIMNBI3R4+p75M6GQaBnNNQ3aPXO18nhuuBctBZ9bkaNsLcUV8V42sfBfFZ\nV4R5QZDfXdY4HLIig/CpbrpgzkZWiGojbpY9lrCJRiLjVfI8ecgr3R0+1VAe+aI+\nAek+NYui1MpCBQPQErmTl96CKQKBgQC2bkkPP0q3qPYH9bn5pSfgkmzXLPlW7ee2\nMM7kZg86jpP1Wr3mxbwSHD4M1FjEtJJK5wYVJ+caLsTGF8aXxapwM0794CmTdVAm\nyuYaSTwK+SBJhQi8i53g1uXLhH2kxDVw83NtB/aqb93/rD32pZDXFf9/6W9EPnyp\nBtq5jC6tkwKBgBHpuRBHml+N6AcwRFR2crJ8IcBLzVhahoJnARzNeWMq7q2LDqnX\nS87V+ORRbSrETqcChDi7v1S0XmWMCVq7DTEHX6cGpvqdMRI8gtWAaFwECYsAXyuU\nwtaG3bWVaolAjFvaNYiH/NsZMhJhMGS7hd2Y9/3ASqtTEvPkdKxsEJNRAoGAKOFh\n4dbPCYUFTRdVi4nk+8AUP8vGPCKnz/3z/t6X/wlAQrUI5RPeZziI9xsGoV3Ngpdu\nl4MPmKBuW+2sBQq4fNgilWWMK40YXvkMw0sx90uIXrE/GfE3edDuQcL43NlTGHKV\npRMpxVu4JbkVUZYcdPZrAODwnBxclwwAK6AsPZ0CgYBwYxxHNXYmoRq3DhE0ZBUY\nI5nhDjZb6Jed3MNeavRYxsqbSc9tZPT8IHiAoiHtr6kVefMq4aWhm8YsVweWkq4Y\nG3lnfNV7C5xqvYq5bdVeURxdNt3WeQiqVIv4hJoPOfzza4GB5dMKmEOVdE999FCe\n/Wv4PW0kjQxigpjF2qAq9A==\n-----END PRIVATE KEY-----\n",
            "client_email": "pedidos-remape@pedidos-414920.iam.gserviceaccount.com",
            "client_id": "102502740439687819075",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/pedidos-remape%40pedidos-414920.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
            } 
                ,scopes=scope)
        client = gspread.authorize(creds)

        # Acessa a planilha e a aba desejada
        sheet = client.open_by_key("1u1do3URWqU6_E9DAKenpm9F7BfKGw7sBNrtp0yxSwzk")
        worksheet = sheet.worksheet("DESPESAS")
        
        # Obtém os dados e converte para DataFrame
        data = worksheet.get_all_values()
        df = pd.DataFrame(data, columns=data[0])
        df = df.dropna(how="all")  # Remove linhas completamente vazias
        # Conversão da coluna "DATA" para datetime e extrai somente a data
        df['DATA'] = pd.to_datetime(df['DATA'], format="%d/%m/%Y", errors='coerce').dt.date

        return df

    # Carrega os dados usando a função cacheada
    df = load_data()

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
