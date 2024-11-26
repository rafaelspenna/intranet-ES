# Use a imagem oficial lightweight do Python
FROM python:3.11.4-slim

# Setar o diretório de trabalho
WORKDIR /app

# Copie o arquivo de requirements para dentro do container
COPY requirements.txt requirements.txt

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação para dentro do container
COPY . /app

# Expor a porta que o Streamlit vai rodar
EXPOSE 8080

# Rodar o app streamlit
CMD ["streamlit", "run", "intranet_deise.py", "--server.port=8080", "--server.address=0.0.0.0"]
