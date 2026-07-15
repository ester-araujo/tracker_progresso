import sqlite3
from datetime import datetime

DB_NAME = "progresso.db"

def create_connection():
    """ Cria e retorna uma conexão com o banco de dados SQLite."""
    return sqlite3.connect(DB_NAME)

def create_table():
    """ Cria a tabela de progresso caso ela não exista."""
    conn = create_connection()
    cursor = conn.cursor()

    #Sql pra tabela de progresso
    cursor.execute ( """
        CREATE TABLE IF NOT EXISTS progress(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   titulo TEXT NOT NULL, 
                   categoria TEXT NOT NULL,
                   total_passos INTEGER NOT NULL, 
                   passo_atual INTEGER DEFAULT 0, 
                   ultima_anotacao TEXT,
                   data_atualizacao TEXT NOT NULL
                   ) """)
    
    conn.commit() #salva as alterações no banco de dados
    conn.close() #fecha a conexão com o banco de dados
    print("Tabela de progresso criada!")

def add_project(titulo, categoria, total_passos):
    """Insere um novo projeto na tabela """
    conn = create_connection()
    cursor = conn. cursor()

    #Coloca data e hora atual
    data_atual= datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

    # SQL para inserir dados 
    query = """
INSERT INTO progress (titulo, categoria, total_passos, passo_atual, data_atualizacao)
    VALUES (?, ?, ?, 0, ?)"""

    #executa a query passando os valores reais dentro da tupla
    cursor.execute(query, (titulo, categoria, total_passos, data_atual))
    conn.commit()
    conn.close()
    print(f"Projeto '{titulo}' adicionado com sucesso!") 


def get_all_projects():
    """Retorna todos os projetos da tabela"""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM progress")

    projects= cursor.fetchall()

    conn.close()
    return projects 

if __name__ == "__main__":
    create_table() 
    
    # Vamos listar os projetos salvos no banco:
    print("\n--- MEUS PROJETOS ---")
    lista = get_all_projects()
    for proj in lista:
        print(proj)




                   