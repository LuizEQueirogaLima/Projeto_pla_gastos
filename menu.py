# Menu Principal
# Pandas para tratamento de dados
# Sqlite para criação do servidor local.
import tratador_info
import tratador_serv_local

def exibir_tela_principal():
    print("\n===================================")
    print("      SISTEMA DE GESTÃO FINANCEIRA   ")
    print("===================================")
    print("[1] Configurar Banco de Dados (1ª vez)")
    print("[2] Importar e Tratar Extrato Nubank")
    print("[0] Sair")
    print("===================================")

def iniciar_sistema():
    while True:
        exibir_tela_principal()
        escolha = input("Digite a opção desejada: ")

        if escolha == '1': # Puxando o arquivo que cria o arquivo .db
            print("Iniciando configuração...")
            tratador_serv_local.Criar_estutura_d_dados()
            
        elif escolha == '2':
            print("Processando extrato...")

            tratador_info.trat_movimentacoes_a()
            
        elif escolha == '0':
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    iniciar_sistema()