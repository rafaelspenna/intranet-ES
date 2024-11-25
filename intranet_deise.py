import streamlit as st
from views.visitas import visitas
from views.despesas import despesas

# Configuração da página
st.set_page_config(page_title="Remape ES", page_icon=":computer:", layout="wide")

#CSS para centralizar o texto dos componentes st.metric
st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("Promotor Remape ES")

    #Dicionário que mapeia as páginas
    PAGES = {
        "Despesas e KM": despesas,
        "Visitas": visitas
    }

    #Seleção da página
    st.sidebar.title("Menu")
    selection = st.sidebar.radio("Navegação", list(PAGES.keys()))

    #Renderização da página
    PAGES[selection]()

if __name__ == "__main__":
    main()

    