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
                    banco TEXT NOT NULL,
                    UNIQUE (data, descricao, valor, banco)
                )
            ''')
        print(" Tabela base criada e conexão fechada com sucesso!")
        
    except sqlite3.Error as erro:
        print(f" Ocorreu um erro ao configurar o banco de dados: {erro}") 
 

def Inserindo_em_arquivo(dados_tratados):
    nome_banco = 'banco_gastos.db'
    try:
        dados_tratados = dados_tratados.drop_duplicates()
        
        with sqlite3.connect(nome_banco) as conexao:
            cursor = conexao.cursor()
            dados_tratados.to_sql('tabela_temporaria', conexao, if_exists='replace', index=False)
            
            cursor.execute('''
                INSERT OR IGNORE INTO tabela_gastos (
                    feito_por, data, descricao, valor, parcela, modalidade, banco)
                SELECT feito_por, data, descricao, valor, parcela, modalidade, banco 
                FROM tabela_temporaria
            ''')
            
            linhas_inseridas = cursor.rowcount
            
            cursor.execute('DROP TABLE tabela_temporaria')
            
            print(f" Inserção Inteligente: {linhas_inseridas} transações inéditas salvas no banco. (Duplicatas ignoradas).")
            
    except Exception as e:
        print(f" Erro ao realizar a transação no banco de dados: {e}")    

# Isso permite testar o arquivo sozinho, se precisar
#if __name__ == "__main__":
#    Criar_estutura_d_dados()
    

        
   
