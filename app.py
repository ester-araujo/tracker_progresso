import streamlit as st
from database import get_all_projects, create_table

#Inicia o DB
create_table()

#Configura pagina
st.set_page_config(page_title="Tracker de Estudos", page_icon=":stars", layout="wide")

# Injetando CSS 
st.markdown("""
    <style>
        /* 1. Mudando o fundo do app e da barra lateral */
        .stApp {
            background-color: #0d0b72; /* Um roxo/preto bem escuro para o fundo geral */
        }
        
        [data-testid="stSidebar"] {
            background-color: #F4F1EA; /* O seu Dark Purple na barra lateral */
        }

        /* 2. Controlando o tamanho e a cor dos Títulos (H1) */
        h1 {
            color: #FF4191!important; /* Neon Pink */
            font-size: 2.8rem !important; /* Aumenta ou diminui o tamanho aqui */
            font-weight: 800 !important;
        }

        /* 3. Controlando o tamanho e a cor dos Subtítulos (H3) */
        h3 {
            color: #A3FFD6 !important; /* Mint Green */
            font-size: 1.8rem !important; /* Tamanho dos títulos dos projetos */
        }

        /* 4. Customizando os nossos containers de projetos */
        div[data-testid="stBlock"] {
            border-color: #F4F1EA !important; /* Borda em Electric Lilac */
            background-color: #F4F1EA!important; /* Fundo do card um pouco mais claro que o geral */
        }
        
        /* 5. Mudando a cor dos textos gerais e captions */
        .stMarkdown p {
            color: #ffffff !important;
            font-size: 1.1rem !important; /* Ajusta o tamanho do texto explicativo */
        }
        
        .stCaption {
            color: #A370F7 !important; /* Legendas em Electric Lilac */
            font-size: 2.2rem !important;
        }
    </style>
""", unsafe_allow_html=True)

#Barra lateral de navegação
st.sidebar.title("Navegação")
st.sidebar.markdown("---")

#Menu de Seleção 
menu = st.sidebar.radio(
    "Menu de Navegação:",
    ["Ver Projetos", "Adicionar Projeto", "Estatisticas"]
)


#Titulo Principal 

if menu == "Ver Projetos": 
    st.title("Meu Tracker de Estudos")
    st.subheader("Acompanhe seu progresso de estudos, cursos e certificações")

    st.write("Este é um aplicativo simples para acompanhar projetos pessoais.")

    #Buscando a lista de projetos no db
    projetos = get_all_projects()

    if not projetos:
        st.info("Nenhum projeto encontrado. Adicione um novo projeto!")
    else: 
        st.markdown("### Projetos Existentes")
    
        #Exibindo os projetos em uma tabela
        for projeto in projetos:
            id_proj, titulo, categoria, total_passos, passo_atual, ultima_anotacao, data_ = projeto
            porcentagem = (passo_atual / total_passos)  if total_passos > 0 else 0.0

            #Cria um container pra cada projeto 
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"### **{titulo}**")
                    st.caption(f"Categoria:{categoria} | Atualizado em: {data_}")
                    if ultima_anotacao:
                        st.markdown(f"*Última anotação: {ultima_anotacao}*")

                with col2:
                    st.metric(label="Progresso", value=f"{passo_atual}/{total_passos}")
                    st.progress(porcentagem)

elif menu == "Adicionar Projetos":
    st.title("Adicionar Novo Projeto")
    st.write("Aqui vai ter um formulario de cadastro do projeto")

elif menu == "Estatísticas":
    st.title("Visão Geral")
    st.write("Aqui vai ter graficos de estatiticas") 
