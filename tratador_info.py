
import pandas as pd
import os
import tratador_serv_local


def trat_movimentacoes_a():

    extrato_de_entrada = 'Arquivo_teste.csv' 
    
    # Entrada Nubank
    if extrato_de_entrada.startswith(('Nubank', 'NU')):
        
        try:
                tratador_serv_local.Criar_estutura_d_dados() 

                if extrato_de_entrada.startswith('Nubank_'):
                    print("Arquivo configurado em crédito\n")
                    
                    dados_nao_tratados = pd.read_csv(extrato_de_entrada, encoding='utf-8', sep=',', decimal=',')
                    
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
                    
                    gerais_nao_tratados = pd.read_csv(extrato_de_entrada, encoding='utf-8', sep=',', decimal=',')
                    dados_tratados = gerais_nao_tratados
                    dados_tratados = gerais_nao_tratados.copy()
                    
                    # Inserindo colunas para a formatação correta da tabela
                    dados_tratados['feito_por'] = 'Não Informado'
                    dados_tratados['parcela'] = '-'
                    dados_tratados['modalidade'] = '-'
                    dados_tratados['banco'] = 'Nubank'

                    dados_tratados['Data'] = pd.to_datetime(dados_tratados['Data'], format="%d/%m/%Y")
                    dados_tratados['Data'] = dados_tratados['Data'].dt.strftime('%Y-%m-%d')
                    
                    # tratamento de dados para a coluna Modalidade
                    dados_tratados.loc[dados_tratados['Descrição'].str.contains('débito|debito', case=False, na=False), 'modalidade'] = 'Débito'
                    dados_tratados.loc[dados_tratados['Descrição'].str.contains('transferência|ted|doc', case=False, na=False), 'modalidade'] = 'Transferência'
                    dados_tratados.loc[dados_tratados['Descrição'].str.contains('pix', case=False, na=False), 'modalidade'] = 'PIX'
                    
                    # identificando nomes das pessoas dentro das transações financeiras s
                    dados_tratados.loc[dados_tratados['Descrição'].str.contains('pessoa 1 ', case=False, na=False), 'feito_por'] = 'pessoa 1'
                    dados_tratados.loc[dados_tratados['Descrição'].str.contains('pessoa 2', case=False, na=False), 'feito_por'] = 'pessoa 2'
                    
                    
                    dados_tratados = dados_tratados.rename(columns={'Descrição':'descricao','Data': 'data','Valor': 'valor'})
                    dados_tratados = dados_tratados[['feito_por','data','descricao','valor','parcela','modalidade','banco']]
                    
                    print(dados_tratados.info())

                    print(dados_tratados.head())
                    tratador_serv_local.Inserindo_em_arquivo(dados_tratados)
                    
    
                    
                    
        except FileNotFoundError:
            print(f"Arquivos em questão não foram encontrados dentro da pasta do projeto..")
            
    # Entrada Banco do Brasil
    if  extrato_de_entrada.startswith('Extrato'): 
        
        print("Tratando arquivo referente a sua Conta Corrente do Banco do Brasil...\n")
        
        df_bb_bruto = pd.read_csv(extrato_de_entrada, encoding='utf-8', sep=',', decimal=',')
        dados_tratados = df_bb_bruto.copy()
        
        dados_tratados.columns = dados_tratados.columns.str.strip()
        
        coluna_bugada = dados_tratados.columns[1] 
        dados_tratados = dados_tratados.rename(columns={coluna_bugada: 'Lançamento'}) 
        
        print("COLUNAS ENCONTRADAS!:", dados_tratados.columns.tolist())
        
        # Otimização de dados/ Encontrando especificidades em transações
        dados_tratados = dados_tratados[dados_tratados['Data'] != '00/00/0000']
        # ~ Invertendo lógica de verificação booleana para a entrada correta de informações.
        dados_tratados = dados_tratados[~dados_tratados['Lançamento'].str.contains('Saldo', case=False, na=False)]
        dados_tratados = dados_tratados[~dados_tratados['Lançamento'].str.contains('Estorno', case=False, na=False)]
        mask_recorrentes = dados_tratados['Lançamento'].str.contains('Tarifa', case=False, na=False)
        dados_tratados = dados_tratados[~((mask_recorrentes) & (dados_tratados.duplicated(subset=['Lançamento'])))]
        
        # Padronização do banco de dados SQlite
        dados_tratados['Data'] = pd.to_datetime(dados_tratados['Data'], format="%d/%m/%Y")
        dados_tratados['Data'] = dados_tratados['Data'].dt.strftime('%Y-%m-%d')
        
        dados_tratados['feito_por'] = 'Não definido' 
        dados_tratados['banco'] = 'Banco do Brasil'
        dados_tratados['parcela'] = '-'
        dados_tratados['modalidade'] = '-'
        
        # Descobrindo a modalidade
        dados_tratados.loc[dados_tratados['Lançamento'].str.contains('Pix', case=False, na=False), 'modalidade'] = 'PIX'
        dados_tratados.loc[dados_tratados['Lançamento'].str.contains('Tarifa|FIES', case=False, na=False), 'modalidade'] = 'Débito Automático'
        
        # dados_tratados = dados_tratados[~dados_tratados['Lançamento'].str.contains(r'S\s*A\s*L\s*D\s*O', case=False, na=False, regex=True)]
        dados_tratados = dados_tratados.rename(columns={
            'Data': 'data', 'Lançamento': 'descricao', 'Valor': 'valor'})
        
        dados_tratados = dados_tratados[['feito_por', 'data', 'descricao', 'valor', 'parcela', 'modalidade', 'banco']]

        print(dados_tratados.head(10))
        
        tratador_serv_local.Inserindo_em_arquivo(dados_tratados)
    # Entrada mercado Pago 
    if extrato_de_entrada.startswith('account_statement'):
        print(" Tratando arquivo de Conta do Mercado Pago...\n")

        # skiprows=3 ignora as primeiras linhas (o arquivo do mercado Pago gera um pré-relatório)
        df_mp_bruto = pd.read_csv(extrato_de_entrada, sep=';', decimal=',',thousands='.', skiprows=3, encoding='utf-8')
        dados_tratados = df_mp_bruto.copy()
        
        dados_tratados.columns = dados_tratados.columns.str.strip()
        
        # formatação de Data
        dados_tratados['RELEASE_DATE'] = pd.to_datetime(dados_tratados['RELEASE_DATE'], format="%d-%m-%Y")
        dados_tratados['RELEASE_DATE'] = dados_tratados['RELEASE_DATE'].dt.strftime('%Y-%m-%d')
        
        #Colunas obrigatórias
        dados_tratados['feito_por'] = 'Não definido'
        dados_tratados['banco'] = 'Mercado Pago'
        dados_tratados['parcela'] = '-'
        dados_tratados['modalidade'] = '-'
        
        # Renomeando colunas
        dados_tratados = dados_tratados.rename(columns={'RELEASE_DATE': 'data', 'TRANSACTION_TYPE': 'descricao','TRANSACTION_NET_AMOUNT': 'valor'})
        
        # Organizando categorias
        dados_tratados.loc[dados_tratados['descricao'].str.contains('Pix', case=False, na=False), 'modalidade'] = 'PIX'
        dados_tratados.loc[dados_tratados['descricao'].str.contains('Rendimentos', case=False, na=False), 'modalidade'] = 'Rendimento'
        
        # Reordenando colunas
        dados_tratados = dados_tratados[['feito_por', 'data', 'descricao', 'valor', 'parcela', 'modalidade', 'banco']]
        
        # Exibe no terminal para auditoria
        print("Tabela do Mercado Pago padronizada:")
        print(dados_tratados.head(15))                  
        tratador_serv_local.Inserindo_em_arquivo(dados_tratados)
        
if __name__ == "__main__":
    trat_movimentacoes_a()
