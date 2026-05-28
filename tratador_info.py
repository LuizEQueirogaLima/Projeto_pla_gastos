
import pandas as pd
import os
import tratador_serv_local


def trat_movimentacoes_a():

    extrato_de_entrada = 'Arquivo teste.csv' 
    
    if extrato_de_entrada.startswith(('Nubank', 'NU')):
        
        try:
                tratador_serv_local.Criar_estutura_d_dados() 

                if extrato_de_entrada.startswith('Nubank_'):
                    print("Arquivo configurado em crédito\n")
                    
                    dados_nao_tratados = pd.read_csv(extrato_de_entrada)
                    
                    dados_tratados = dados_nao_tratados
                    dados_tratados = dados_nao_tratados.copy()
                    
                    dados_tratados['feito_por'] = 'Não Informado'
                    dados_tratados['banco'] = 'Nubank' 
                    dados_tratados['modalidade'] = 'Crédito'
                    
                    dados_tratados['date'] = pd.to_datetime(dados_tratados['date'], format="%Y-%m-%d")
                    dados_tratados['date'] = dados_tratados['date'].dt.strftime('%Y-%m-%d')
                    
                    dados_tratados['parcela'] = dados_tratados['title'].str.extract(r'(\d+/\d+)')
                    dados_tratados['parcela'] = dados_tratados['parcela'].fillna('-')
                    

                    dados_tratados['title'] = dados_tratados['title'].str.replace(r'\s*-\s*Parcela \d+/\d+', '', regex=True).str.strip() 

                    dados_tratados = dados_tratados.rename(columns={'date': 'data','title': 'descricao', 'amount': 'valor'})
                    
                    dados_tratados = dados_tratados[['feito_por','data','descricao','valor','parcela','modalidade','banco']]

                    print(dados_tratados.info())

                    print(dados_tratados.head())
                    tratador_serv_local.Inserindo_em_arquivo(dados_tratados)
                elif extrato_de_entrada.startswith('NU_'):
                    print("Arquivo configurado transações de pix e débito\n")
                    
                    gerais_nao_tratados = pd.read_csv(extrato_de_entrada)
                    dados_tratados = gerais_nao_tratados
                    dados_tratados = gerais_nao_tratados.copy()
                    
                    
                    dados_tratados['feito_por'] = 'Não Informado'
                    dados_tratados['banco'] = 'Nubank'
                    dados_tratados['parcela'] = '-'
                    dados_tratados['modalidade'] = '-'
                    
                    dados_tratados['Data'] = pd.to_datetime(dados_tratados['Data'], format="%d/%m/%Y")
                    dados_tratados['Data'] = dados_tratados['Data'].dt.strftime('%Y-%m-%d') 
                    
                    dados_tratados.loc[dados_tratados['Descrição'].str.contains('pix', case=False, na=False), 'modalidade'] = 'PIX'
                    
                    dados_tratados.loc[dados_tratados['Descrição'].str.contains('débito|debito', case=False, na=False), 'modalidade'] = 'Débito'
                    
                    dados_tratados.loc[dados_tratados['Descrição'].str.contains('transferência|ted|doc', case=False, na=False), 'modalidade'] = 'Transferência'
                    
                    
                    dados_tratados = dados_tratados.rename(columns={'Descrição':'descricao','Data': 'data','Valor': 'valor'})
                    dados_tratados = dados_tratados[['feito_por','data','descricao','valor','parcela','modalidade','banco']]
                    
                    print(dados_tratados.info())

                    print(dados_tratados.head())
                    tratador_serv_local.Inserindo_em_arquivo(dados_tratados)
                    
                    
                    
                    
        except FileNotFoundError:
            print(f"Arquivos em questão não foram encontrados dentro da pasta do projeto..")
            
    
        
if __name__ == "__main__":
    trat_movimentacoes_a()
