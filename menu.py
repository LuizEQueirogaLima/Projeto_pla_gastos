# Informações de Interface
# Bibliotecas que devem ser importadas: Pandas, customtkinter, matplotlib
import customtkinter as ctk 
from tkinter import filedialog
import pandas as pd
import sqlite3
import os 
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from matplotlib.ticker import MultipleLocator 
import tratador_info

# Configuração global de aparência da interface
ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("green") 

# Converte o valor em float para  o valor em reais.
def formatar_moeda_br(valor):
    texto = f"R$ {valor:,.2f}"
    texto = texto.replace(",", "X").replace("." , ",").replace("X", ".")
    return texto

# Conecta ao arquivo .db e extrai as informações
def carregar_dados_do_sqlite():
    
    nome_banco = 'banco_gastos.db'
    
    if not os.path.exists(nome_banco):
        print("Aviso: O arquivo banco_gastos.db não foi encontrado na pasta atual.")
        return pd.DataFrame()

    try:
        # Seleciona a tabela pelo nome dado a ela dentro do aquivo .db
        with sqlite3.connect(nome_banco) as conexao:
            df = pd.read_sql_query("SELECT * FROM tabela_gastos", conexao)

            if not df.empty:
                df['data'] = pd.to_datetime(df['data'])
            return df
            
    except Exception as e:
        print(f"Erro crítico ao ler o banco de dados: {e}")
        return pd.DataFrame()

class AppGestaoFinanceira(ctk.CTk):
    def __init__(self):
        # Importando da classe original
        super().__init__()

        self.title("Sistema de Gestão Financeira")
        self.geometry("1200x750")
        
        # Carregando banco de dados
        self.df_gastos = carregar_dados_do_sqlite()
        
        # Tela de menu principal
        self.abrir_menu_principal()

    # Destroi todos os elementos em tela.
    def limpar_tela_atual(self):
        for componente in self.winfo_children():
            componente.destroy()


    def abrir_menu_principal(self):
        self.limpar_tela_atual()
        # Configura a malha para centralizar o conteúdo do menu.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Configuração base para todos os elementos em tela.
        frame_menu = ctk.CTkFrame(self, fg_color="transparent")
        frame_menu.grid(row=0, column=0)
        
        titulo = ctk.CTkLabel(frame_menu, text="Menu Principal", font=("Times New Roman", 32, "bold")) 
        titulo.pack(pady=(0, 40)) 
        
        # Botão de importação de arquivos .CSV
        btn_import = ctk.CTkButton(frame_menu, text="Importar Extratos", width=250, height=50, 
                                        font=("Times New Roman", 16, "bold"), fg_color="#1e293b", 
                                        hover_color="#334155",command=self.abrir_importacao)
        btn_import.pack(pady=10)
        
        btn_dashboard = ctk.CTkButton(
            frame_menu, text="Dashboard", font=("Times New Roman", 16,"bold"), 
            width=250, height=50, fg_color="#1e293b",
            hover_color="#334155", command=self.abrir_dashboard
        )

        btn_dashboard.pack(pady=10)
        
        btn_transacoes = ctk.CTkButton(
            frame_menu, text="Edição Detalhada", font=("Times New Roman", 16), 
            width=250, height=50, fg_color="#444444", hover_color="#555555"
        )
        btn_transacoes.pack(pady=10)

    def abrir_dashboard(self):
        self.limpar_tela_atual()
        
        # O Dashboard ocupa a tela inteira
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # A linha 1 (onde fica o gráfico/tabela) expande
        
        #Cabeçalho do DashBoard
        frame_topo = ctk.CTkFrame(self, fg_color="transparent")
        frame_topo.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0)) # sticky funciona de uma forma de fixar todo o espaço 

        bt_voltar = ctk.CTkButton(
            frame_topo, text="← Voltar ao Menu", font=("AriTimes New Romanal", 14), 
            width=150, fg_color="#c0392b", hover_color="#e74c3c", command=self.abrir_menu_principal
        )

        bt_voltar.pack(side="left")
        
        lbl_titulo_dash = ctk.CTkLabel(frame_topo, text="Dashboard Financeiro", font=("Times New Roman", 20, "bold"))
        lbl_titulo_dash.pack(side="right")

        #Área do Dashboard
        frame_corpo = ctk.CTkFrame(self, fg_color="transparent")
        frame_corpo.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        frame_corpo.grid_columnconfigure(0, weight=1)
        frame_corpo.grid_rowconfigure(0, weight=1) # Espaço do gráfico
        frame_corpo.grid_rowconfigure(1, weight=1) # Espaço da tabela
        
        # 1. Desenho do Gráfico de Torre
        frame_grafico = ctk.CTkFrame(frame_corpo)
        frame_grafico.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        if not self.df_gastos.empty:
            self.desenhar_grafico_torre(frame_grafico)
        else:
            vazio_lbl = ctk.CTkLabel(frame_grafico, text="Nenhum dado encontrado no banco banco_gastos.db", font=("ArTimes New Romanial", 16))
            vazio_lbl.pack(expand=True)

        # 2. Histórico de Movimentações com Barra de Rolagem
        frame_tabela = ctk.CTkFrame(frame_corpo)
        frame_tabela.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        
        titulo_tabela = ctk.CTkLabel(frame_tabela, text="Histórico de Movimentações", font=("Times New Roman", 16, "bold"))
        titulo_tabela.pack(pady=(10, 5), padx=10, anchor="w")
        
        scroll_tabela = ctk.CTkScrollableFrame(frame_tabela, fg_color="#2b2b2b")
        scroll_tabela.pack(fill="both", expand=True, padx=10, pady=10)
        
        if not self.df_gastos.empty:
            self.preencher_lista_historico(scroll_tabela)
            
    def abrir_importacao(self):
        self.limpar_tela_atual()
        
        # Variável interna para segurar o caminho do arquivo na memória
        self.arquivo_para_processar = None 

        cabecalho = ctk.CTkFrame(self, height=50, fg_color="#202936")
        cabecalho.pack(fill="x", side="top")
        
        # Retorna ao menu
        bt_voltar = ctk.CTkButton(cabecalho, text="← VOLTAR", width=100, command=self.abrir_menu_principal)
        bt_voltar.pack(side="left", padx=20, pady=10)

        import_frame = ctk.CTkFrame(self, corner_radius=30)
        import_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.6)
        
        lbl_instrucao = ctk.CTkLabel(import_frame, text="Importação de Extratos", font=("Times New Roman", 20, "bold"))
        lbl_instrucao.pack(pady=30)
        
        self.path_label = ctk.CTkLabel(import_frame, text="Nenhum arquivo selecionado...", text_color="gray", font=("Times New Roman", 14))
        self.path_label.pack(pady=10)
        
        # Botão para importar arquivos
        btn_browse = ctk.CTkButton(import_frame, text="1. PROCURAR ARQUIVO CSV", font=("Times New Roman", 14, "bold"), command=self.selecionar_arquivo)
        btn_browse.pack(pady=10)
        
        # Botão para processar dados no arquivo .db
        self.btn_salvar_bd = ctk.CTkButton(import_frame, text="2. PROCESSAR E SALVAR", fg_color="#27ae60", hover_color="#2ecc71",
                                           font=("Times New Roman", 14, "bold"), state="disabled", command=self.executar_salvamento)
        self.btn_salvar_bd.pack(pady=20)

        self.lbl_aviso = ctk.CTkLabel(import_frame, text="", font=("Times New Roman", 16, "bold"))
        self.lbl_aviso.pack(pady=10)
    
    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")]) 
        if caminho:
            self.arquivo_para_processar = caminho 
            
            self.path_label.configure(text=f"Arquivo selecionado: {caminho.split('/')[-1]}", text_color="#f1c40f")
            self.lbl_aviso.configure(text="Pronto para processar.", text_color="white")
            self.btn_salvar_bd.configure(state="normal")
            
    def executar_salvamento(self):
        if self.arquivo_para_processar:
            self.lbl_aviso.configure(text="Analisando e salvando... Aguarde.", text_color="yellow")
            self.update() # Força o CustomTkinter a atualizar a tela imediatamente
            
            # Chama o Pandas em outro arquivo.
            sucesso = Tratador_info.processar_extrato(self.arquivo_para_processar)
            
            if sucesso:
                self.lbl_aviso.configure(text="Sucesso! Dados salvos no banco SQLite.", text_color="#2ecc71")
                # Desativa o botão para evitar que o usuário clique duas vezes e mande duplicado
                self.btn_salvar_bd.configure(state="disabled") 
                
                # Recarrega os dados do banco para a memória, 
                self.df_gastos = carregar_dados_do_sqlite() 
            else:
                self.lbl_aviso.configure(text="Erro: Formato de banco não reconhecido ou arquivo inválido.", text_color="#e74c3c")
        
    # Construção de Componentes visuais
    def desenhar_grafico_torre(self, parent):
        #Constrói o gráfico de barras
        df_plot = self.df_gastos.copy()
        
        meses_pt = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun', 
                    7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}
        
        df_plot['Mes_Nome'] = df_plot['data'].dt.month.map(meses_pt)
        df_plot['Mes_Num'] = df_plot['data'].dt.month
        df_plot['Volume_Absoluto'] = df_plot['valor'].abs()
        
        pivot = df_plot.pivot_table(index='Mes_Nome', columns='modalidade', values='Volume_Absoluto', aggfunc='sum', fill_value=0)
        pivot = pivot.loc[df_plot.sort_values('Mes_Num')['Mes_Nome'].unique()]

        plt.style.use('dark_background') 
        fig, ax = plt.subplots(figsize=(8, 3.5), facecolor='#2b2b2b')
        ax.set_facecolor('#2b2b2b')
        
        pivot.plot(kind='bar', stacked=True, ax=ax, colormap='Set2')
        
        # Trava as linhas de grade de 500 em 500
        ax.yaxis.set_major_locator(MultipleLocator(500))
        plt.xticks(rotation=0)
        ax.set_xlabel("")
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def preencher_lista_historico(self, parent):
        parent.grid_columnconfigure((0,1,2,3,4,5), weight=1)
        
        cabecalhos = ["Data", "Responsável", "Descrição", "Modalidade", "Banco", "Valor"]
        for col_idx, texto in enumerate(cabecalhos):
            lbl_cabecalho = ctk.CTkLabel(parent, text=texto, font=("Times New Roman", 14, "bold"), text_color="gray")
            lbl_cabecalho.grid(row=0, column=col_idx, sticky="w", padx=5, pady=(0, 10))
        
        df_historico = self.df_gastos.sort_values(by='data', ascending=False)
        
        linha_atual = 1
        for _, linha in df_historico.iterrows():
            data_br = linha['data'].strftime('%d/%m/%Y')
            valor_br = formatar_moeda_br(linha['valor'])
            cor_valor = "#2ecc71" if linha['valor'] > 0 else "#e74c3c"
            
            ctk.CTkLabel(parent, text=data_br, font=("Times New Roman", 12)).grid(row=linha_atual, column=0, sticky="w", padx=5, pady=2)
            ctk.CTkLabel(parent, text=str(linha['feito_por']), font=("Times New Roman", 12)).grid(row=linha_atual, column=1, sticky="w", padx=5, pady=2)
            
            desc_curta = str(linha['descricao'])[:30] + ("..." if len(str(linha['descricao'])) > 30 else "")
            ctk.CTkLabel(parent, text=desc_curta, font=("Times New Roman", 12)).grid(row=linha_atual, column=2, sticky="w", padx=5, pady=2)
            
            ctk.CTkLabel(parent, text=str(linha['modalidade']), font=("Times New Roman", 12)).grid(row=linha_atual, column=3, sticky="w", padx=5, pady=2)
            ctk.CTkLabel(parent, text=str(linha['banco']), font=("Times New Roman", 12)).grid(row=linha_atual, column=4, sticky="w", padx=5, pady=2)
            ctk.CTkLabel(parent, text=valor_br, font=("Times New Roman", 13, "bold"), text_color=cor_valor).grid(row=linha_atual, column=5, sticky="w", padx=5, pady=2)
            
            linha_atual += 1

if __name__ == "__main__":
    app = AppGestaoFinanceira()
    app.mainloop() # O main loop garante que o código rode infinitamente até que o usuário feche a tela