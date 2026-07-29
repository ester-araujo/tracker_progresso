import streamlit as st
import pandas as pd
import plotly.express as px
from database import(
     get_all_projects,
     create_table, 
     add_project,
     update_project, 
     delete_project
)

#Inicia o DB
create_table()

#Configura pagina
st.set_page_config(page_title="Tracker de Estudos", page_icon=":chart_with_upwards_trend:", layout="wide")

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
            font-size: 1.1rem !important; /* Tamanho do texto explicativo */
        }
        
        .stCaption {
            color: #A370F7 !important; /* Legendas em Electric Lilac */
            font-size: 2.2rem !important;
        }
            
            [data-testid="stMetricLabel"] p {
            color: #A3FFD6 !important; /* Mint Green para dar destaque */
            font-size: 1.1rem !important;
            font-weight: bold !important;
        }

        /* 6. Muda a cor do número  (Metric Value) */
        [data-testid="stMetricValue"] {
            color: #F4F1EA !important; /* Champanhe Claro*/
        }
            
        /* 7. Muda a cor de TODOS os rótulos de campos (Título do Projeto, Total de Módulos, etc.) */
        div[data-testid*="stWidgetLabel"] label, 
        label[data-testid="stWidgetLabel"] p {
            color: #F4F1EA !important; /* Champanhe Claro */
            font-size: 1.05rem !important;
            font-weight: 600 !important;
        }

        /* 8. muda os inputs e caixas de digitação */
        div[data-baseweb="input"] {
            background-color: #161224 !important; /* Fundo escuro para a caixinha de digitação */
            border-color: #A370F7 !important; /* Borda em Electric Lilac */
            color: #F4F1EA !important;
        }
        
        input[type="text"],
        input[type="number"], 
        div[data-baseweb="input"] input{
            color: #0d0b18 !important; 
            font-weight: 600 !important; 
        }
            
        button[aria-label="Decrease value"],
        button[aria-label="Increase value"] {
            color: #0d0b18 !important; 
         }

        /* 9. Cor do texto dentro do input */
        input {
            color:#0d0b18 !important; /* Champanhe Claro */
        }
    </style>
""", unsafe_allow_html=True)

#Barra lateral de navegação
st.sidebar.title("Menu de Navegação")
st.sidebar.markdown("---")

#Menu de Seleção 
menu = st.sidebar.radio(
    "Selecione uma opção:",
    ["Ver Projetos", "Adicionar Novo Projeto", "Estatísticas"]
)


# ------ABA:Ver Projetos -------

if menu == "Ver Projetos": 
    st.title("Meu Tracker de Estudos")
    st.subheader("Acompanhe seu progresso de estudos, cursos e certificações!")

    st.write("*Este é um aplicativo simples para acompanhar projetos pessoais.")

    #Recupera a lista de projetos no db
    projetos = get_all_projects()

    if not projetos:
        st.info("Nenhum projeto encontrado. Adicione um novo projeto!")
    else: 
        st.markdown("### Projetos Existentes:")
    
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
    
# Área de edição e exclusão de projetos
                with st.expander("Gerenciar Projetos"):
                    col_input, col_note = st.columns([1,2])

                    with col_input:
                        novo_passo = st.number_input(
                            "Passo Atual", 
                            min_value=0,
                            max_value=total_passos,
                            value=passo_atual, 
                            key=f"passo_{id_proj}" 
                        )
                    
                    with col_note:
                        nova_anotacao = st.text_input(
                            "Nova Anotação", 
                            value=ultima_anotacao if ultima_anotacao else "", 
                            key=f"note_{id_proj}"
                        )
                    
                    bnt_salvar, bnt_excluir = st.columns([1,1])

                    with bnt_salvar:
                        if st.button("Salvar Projeto", key=f"bnt_save_{id_proj}"):
                            update_project(id_proj, passo_atual, ultima_anotacao)
                            st.success("Progresso atualizado com sucesso!")
                            st.rerun()

                    with bnt_excluir:
                        if st.button("Excluir Projeto", key=f"bnt_del_{id_proj}"):
                            delete_project(id_proj)
                            st.warning("Projeto Excluído")
                            st.rerun()

                        
# ------ABA:Adicionar Novo Projeto -------
elif menu == "Adicionar Novo Projeto":
    st.title("Adicionar Novo Projeto")
    st.write("Preencha os campos abaixo pra adicionar um novo projeto")


    with st.form(key="form_add_project", clear_on_submit=True):
        col_titulo, col_categoria = st.columns([2, 1])

        with col_titulo:
            titulo =  st.text_input("Titulo do Projeto", placeholder="Ex: Curso de Python")

        with col_categoria: 
          categoria = st.selectbox(
            "Categoria ", 
            ["Curso", "Certificação", "Estudo Pessoal", "Outros"]
            )

        col_passos, col__anotacao = st.columns([1, 2])

        with col_passos:
             total_passos = st.number_input("Total de Modulos/Aulas", min_value=1, value=10, step=1)
        

        #Botão de envio do formulario
        submit_button = st.form_submit_button("Adicionar Projeto")

    #Validação e Envio para o db
    if submit_button: 
        if not titulo.strip():
            st.error("O Título do projeto é obrigatório!")
        else:
            #Função para adicionar o projeto no banco de dados
            try: 
                st.success(f"Projeto '{titulo}' adicionado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao adicionar projeto: {e}")

# ------ABA:Estatísticas -------
elif menu == "Estatísticas":
    st.title("Painel de Desempenho")
    st.write("Análise em tempo real seu progresso.")

    projetos = get_all_projects()

    if not projetos:
        st.info("Nenhum dado disponível. Adicione porjetos para começar a visualizar suas estastísticas!")
    else:
        #Transforma os dados em um DataFrame Pandas
        df = pd.DataFrame(
            projetos,
            columns=["id","titulo","categoria","total_passos", "passo_atual", "ultima_anotacao", "data_atualizacao"]
        )

        #Calcula a porcentagem de progesso de cada projeto 
        df["progresso_pct"] = (df["passo_atual"]/ df["total_passos"])*100

        #Metricas de Topo(KPIs)
        total_projetos = len(df)
        concluidos = len(df[df["passo_atual"]==df["total_passos"]])
        total_modulos = df["total_passos"].sum()
        modulos_completos = df["passo_atual"].sum()

        col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
        col_kpi1.metric("Total de Projetos", total_projetos)
        col_kpi2.metric("Projetos Concluídos", concluidos)
        col_kpi3.metric("Total de Módulos", total_modulos)
        col_kpi4.metric("Módulos Concluídos", modulos_completos)

        st.markdown("---")

        #---GRAFICOS INTERATIVOS COM PLOTLY---
        col_graf1, col_graf2 = st.columns(2)

        with col_graf1:
            #Grafico de barras
            fig_barras = px.bar(
                df,
                x="progresso_pct",
                y="titulo",
                orientation="h",
                title="Progresso por Projeto (%)",
                labels={"progresso_pct": "PRogresso (%)","titulo":"Projeto"},
                color_discrete_sequence=["#FF4191"]
            )

            fig_barras.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0)",
                font_color="#F4F1EA",
                xaxis=dict(range=[0, 100], gridcolor="#161224")
            )

            st.plotly_chart(fig_barras, use_container_width=True)

            with col_graf2:
                #Grafico de Rosca
                fig_rosca =px.pie(
                    df, 
                    names="categoria",
                    title="Distribuição por Categoria",
                    hole=0.5,
                    color_discrete_sequence=["#A3FFD6", "#A370F7", "#FF4191", "#F4F1EA"]
                )

                fig_rosca.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)", 
                    font_color="#F4F1EA"
                )

                st.plotly_chart(fig_rosca, use_container_width=True)