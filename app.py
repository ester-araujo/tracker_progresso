import streamlit as st
from database import get_all_projects, create_table

create_table()

st.set_page_config(page_title="Tracker de Estudos", page_icon=":stars", layout="centered")


#Titulo Principal 
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
