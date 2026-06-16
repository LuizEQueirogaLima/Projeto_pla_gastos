import pandas as pd
import os
import tratador_serv_local

def tratar_nubank(arquivo):
    # Tratamento e Limpeza do extrato Nubank
    nome = os.path.basename(arquivo)
    
    if nome.startswith('Nubank_'):
        # Tratamentos para extrato no geral
        df_bruto = pd.read_csv(arquivo, encoding='utf-8', sep=',', decimal=',')
        dados_tratados = df_bruto.copy()
        
        dados_tratados['feito_por'] = 'Luiz'
        dados_tratados['banco'] = 'Nubank'
        dados_tratados['modalidade'] = 'Crédito'
        
        dados_tratados['date'] = pd.to_datetime(dados_tratados['date'], format="%Y-%m-%d")
        dados_tratados['date'] = dados_tratados['date'].dt.strftime('%Y-%m-%d')
        dados_tratados['parcela'] = dados_tratados['title'].str.extract(r'(\d+/\d+)').fillna('-')
        dados_tratados['title'] = dados_tratados['title'].str.replace(r'\s*-\s*Parcela \d+/\d+', '', regex=True).str.strip() 
        
        dados_tratados = dados_tratados.rename(columns={'date': 'data','title': 'descricao', 'amount': 'valor'})
        return dados_tratados[['feito_por','data','descricao','valor','parcela','modalidade','banco']]
        
    elif nome.startswith('NU_'):
        # Tratamentos para dados de cartão de crédito
        df_bruto = pd.read_csv(arquivo, encoding='utf-8', sep=',', decimal=',')
        dados_tratados = df_bruto.copy()
        
        dados_tratados['feito_por'] = 'Luiz'
        dados_tratados['banco'] = 'Nubank'
        dados_tratados['modalidade'] = '-'
        dados_tratados['parcela'] = '-'
        
        dados_tratados['Data'] = pd.to_datetime(dados_tratados['Data'], format="%d/%m/%Y")
        dados_tratados['Data'] = dados_tratados['Data'].dt.strftime('%Y-%m-%d')
        
        # Identificando e tratando nomes especificos
        dados_tratados.loc[dados_tratados['Descrição'].str.contains('débito|debito', case=False, na=False), 'modalidade'] = 'Débito'
        dados_tratados.loc[dados_tratados['Descrição'].str.contains('transferência|ted|doc', case=False, na=False), 'modalidade'] = 'Transferência'
        dados_tratados.loc[dados_tratados['Descrição'].str.contains('pix', case=False, na=False), 'modalidade'] = 'PIX'
        dados_tratados.loc[dados_tratados['Descrição'].str.contains('Luiz', case=False, na=False), 'feito_por'] = 'Luiz'
        dados_tratados.loc[dados_tratados['Descrição'].str.contains('Stefanny', case=False, na=False), 'feito_por'] = 'Stéfanny'
        
        dados_tratados = dados_tratados.rename(columns={'Descrição':'descricao','Data': 'data','Valor': 'valor'})
        return dados_tratados[['feito_por','data','descricao','valor','parcela','modalidade','banco']]

def tratar_inter(arquivo):
    # Tratamento de dados do Banco Inter
    df_bruto = pd.read_csv(arquivo, sep=';', decimal=',', thousands='.', skiprows=5, encoding='utf-8')
    dados_tratados = df_bruto.copy()
    # Filtrando colunas para evitar quebra de dados no Pandas
    colu_data, colu_historico, colu_desc, colu_valor = dados_tratados.columns[0:4]
    
    dados_tratados[colu_data] = dados_tratados[colu_data].astype(str).str.strip()
    dados_tratados[colu_data] = pd.to_datetime(dados_tratados[colu_data], format="%d/%m/%Y")
    dados_tratados[colu_data] = dados_tratados[colu_data].dt.strftime('%Y-%m-%d')
    
    dados_tratados['feito_por'] = 'Luiz'
    dados_tratados['banco'] = 'Inter'
    dados_tratados['parcela'] = '-'
    dados_tratados['modalidade'] = '-'
    
    dados_tratados.loc[dados_tratados[colu_historico].str.contains('Pix', case=False, na=False), 'modalidade'] = 'PIX'
    dados_tratados.loc[dados_tratados[colu_historico].str.contains('débito|debito', case=False, na=False), 'modalidade'] = 'Débito'
    dados_tratados.loc[dados_tratados[colu_historico].str.contains('transferência', case=False, na=False), 'modalidade'] = 'Transferência'
    
    dados_tratados = dados_tratados.rename(columns={colu_data:'data', colu_desc:'descricao', colu_valor:'valor'})
    return dados_tratados[['feito_por','data','descricao','valor','parcela','modalidade','banco']]

def tratar_bb(arquivo):
    # Tratamento de dados do banco do Brasil
    
    df_bruto = pd.read_csv(arquivo, encoding='utf-8', sep=',', decimal=',')
    dados_tratados = df_bruto.copy()
    
    dados_tratados.columns = dados_tratados.columns.str.strip()
    # Atribuindo a variável a info de uma coluna com nome quebrado
    coluna_bugada = dados_tratados.columns[1] 
    dados_tratados = dados_tratados.rename(columns={coluna_bugada: 'Lançamento'})
    
    dados_tratados = dados_tratados[dados_tratados['Data'] != '00/00/0000']
    dados_tratados = dados_tratados[~dados_tratados['Lançamento'].str.contains('Saldo|Estorno', case=False, na=False, regex=True)]
    
    dado_repetido = dados_tratados['Lançamento'].str.contains('FIES|Tarifa', case=False, na=False)
    dados_tratados = dados_tratados[~((dado_repetido) & (dados_tratados.duplicated(subset=['Lançamento'])))]
    
    dados_tratados['Data'] = pd.to_datetime(dados_tratados['Data'], format="%d/%m/%Y")
    dados_tratados['Data'] = dados_tratados['Data'].dt.strftime('%Y-%m-%d')
    
    dados_tratados['feito_por'] = 'Luiz'
    dados_tratados['banco'] = 'Banco do Brasil'
    dados_tratados['parcela'] = '-'
    dados_tratados['modalidade'] = '-'
    
    dados_tratados.loc[dados_tratados['Lançamento'].str.contains('Pix', case=False, na=False), 'modalidade'] = 'PIX'
    dados_tratados.loc[dados_tratados['Lançamento'].str.contains('Tarifa|FIES', case=False, na=False), 'modalidade'] = 'Débito Automático'
    
    dados_tratados = dados_tratados[~dados_tratados['Lançamento'].str.contains(r'S\s*A\s*L\s*D\s*O', case=False, na=False, regex=True)]
    dados_tratados = dados_tratados.rename(columns={'Data': 'data', 'Lançamento': 'descricao', 'Valor': 'valor'})
    
    return dados_tratados[['feito_por', 'data', 'descricao', 'valor', 'parcela', 'modalidade', 'banco']]

def tratar_mercado_pago(arquivo):
    # Tratamento de dados Mercado Pago
    print("Tratando arquivo de Conta do Mercado Pago...\n")
    df_bruto = pd.read_csv(arquivo, sep=';', decimal=',', thousands='.', skiprows=3, encoding='utf-8')
    dados_tratados = df_bruto.copy()
    
    dados_tratados.columns = dados_tratados.columns.str.strip()
    dados_tratados['RELEASE_DATE'] = pd.to_datetime(dados_tratados['RELEASE_DATE'], format="%d-%m-%Y")
    dados_tratados['RELEASE_DATE'] = dados_tratados['RELEASE_DATE'].dt.strftime('%Y-%m-%d')
    
    dados_tratados['feito_por'] = 'Luiz'
    dados_tratados['banco'] = 'Mercado Pago'
    dados_tratados['parcela'] = '-'
    dados_tratados['modalidade'] = '-'
    
    dados_tratados = dados_tratados.rename(columns={'RELEASE_DATE': 'data', 'TRANSACTION_TYPE': 'descricao','TRANSACTION_NET_AMOUNT': 'valor'})
    
    dados_tratados.loc[dados_tratados['descricao'].str.contains('Pix', case=False, na=False), 'modalidade'] = 'PIX'
    dados_tratados.loc[dados_tratados['descricao'].str.contains('Rendimentos', case=False, na=False), 'modalidade'] = 'Rendimento'
    
    return dados_tratados[['feito_por', 'data', 'descricao', 'valor', 'parcela', 'modalidade', 'banco']]

def processar_extrato(caminho_arquivo):
    # Identifica caso o arquivo não exista na página
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: O arquivo  não foi encontrado.")
        return False

    # Garante a redundância do programa, criando o arquivo .db caso ele não exista
    tratador_serv_local.Criar_estutura_d_dados()
    
    # A variável matriz_limpa vai capturar o 'return' de quem processar o arquivo
    matriz_limpa = None

    nome_arquivo = os.path.basename(caminho_arquivo)
    # Cascata programada de acordo com os tipos de extratos encontrados em cada banco
    
    # Nubank
    if nome_arquivo.startswith(('Nubank', 'NU')): 
        matriz_limpa = tratar_nubank(caminho_arquivo)
    # Inter    
    elif nome_arquivo.endswith('-CSV.csv') or '-CSV' in caminho_arquivo:
        matriz_limpa = tratar_inter(caminho_arquivo)
    # Banco do Brasil
    elif nome_arquivo.startswith('Extrato'):
        matriz_limpa = tratar_bb(caminho_arquivo)
    # Mercado Pago    
    elif nome_arquivo.startswith('account_statement'):
        matriz_limpa = tratar_mercado_pago(caminho_arquivo)
    else:
        print("Formato de arquivo não reconhecido pelo sistema.")
        return False
    # Ponto de saída 
    if matriz_limpa is not None and not matriz_limpa.empty:
            tratador_serv_local.Inserindo_em_arquivo(matriz_limpa)
            return True 
        
    return False

if __name__ == "__main__":
    processar_extrato()

