# SQLite Viewer 
# Pandas para tratamento de dados
# Sqlite para criação do servidor local.


# Arquivo 1

import sqlite3
import os

def Criar_estutura_d_dados():
    """
    Cria o arquivo do banco de dados e a tabela principal com 
    a estrutura rigorosa de colunas solicitada.
    """
    nome_banco = 'banco_gastos.db'
    print(f" Iniciando a configuração do banco: {nome_banco}")
    
    try:
        with sqlite3.connect(nome_banco) as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tabela_gastos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    feito_por TEXT NOT NULL,
                    data TEXT NOT NULL,
                    descricao TEXT NOT NULL,
                    valor REAL NOT NULL,
                    parcela TEXT DEFAULT '-',
                    modalidade TEXT NOT NULL,
                    banco TEXT NOT NULL
                )
            ''')
        print(" Tabela base criada e conexão fechada com sucesso!")
        
    except sqlite3.Error as erro:
        print(f" Ocorreu um erro ao configurar o banco de dados: {erro}") 
 

def Inserindo_em_arquivo(dados_tratados):
    nome_banco = 'banco_gastos.db'
    try:
        with sqlite3.connect(nome_banco) as conexao:
            dados_tratados.to_sql('tabela_gastos', conexao, if_exists='append', index=False)
            print(f"Sucesso! {len(dados_tratados)} linhas foram tratadas e enviadas ao banco de dados.")
    except Exception as e:
        print(f"Erro ao inserir dados {e}")       

# Isso permite testar o arquivo sozinho, se precisar
#if __name__ == "__main__":
#    Criar_estutura_d_dados()
    

        
   
