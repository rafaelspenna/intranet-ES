import pandas as pd
from funcs.retrieve_data_spreadsheet import load_data

def calculate_business_days(start_date, end_date, holidays=None):
    # Garantir que as datas estão no formato datetime
    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date, format="%Y-%m-%d %H:%M:%S", errors='coerce')
    if isinstance(end_date, str):
        end_date = pd.to_datetime(end_date, format="%Y-%m-%d %H:%M:%S", errors='coerce')
    
    # Verificar se a conversão foi bem-sucedida
    if pd.isnull(start_date) or pd.isnull(end_date):
        raise ValueError("Uma ou ambas as datas não puderam ser convertidas para datetime.")
    
    # Criar intervalo de datas com pandas
    all_dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Filtrar apenas os dias úteis (segunda a sexta-feira)
    business_days = all_dates[all_dates.weekday < 5]  # 0 a 4 correspondem a segunda a sexta-feira
    
    # Carregar os feriados, se não forem fornecidos
    if holidays is None:
        holidays_data = load_data("DADOS", "%d/%m/%Y", "FERIADOS")
        holidays = holidays_data["FERIADOS"].dropna()
    
    # Converter feriados para datetime, garantindo o formato correto
    holidays = pd.to_datetime(holidays, format="%d/%m/%Y", errors='coerce').dropna()
    
    # Remover feriados dos dias úteis
    business_days = business_days[~business_days.isin(holidays)]
    
    # Retornar o número de dias úteis
    return len(business_days)
