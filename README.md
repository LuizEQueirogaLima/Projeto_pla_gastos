# Sistema de Gestão Financeira.

Este projeto consiste em uma aplicação de automação e controle financeiro pessoal executada localmente. O objetivo principal é eliminar o trabalho manual que ocorre com frequência na atualização de planilhas de controle de gastos. Para isso, foi construído um pipeline de dados capaz de receber faturas e extratos bancários brutos, tratar as informações e retornar o histórico de despesas de forma estruturada, padronizada e detalhada.

A ideia central é que o usuário apenas forneça os arquivos exportados pelo banco, deixando para o sistema todo o trabalho pesado de higienização de textos, identificação de parcelas e classificação das modalidades de pagamento.

## Estado Atual do Projeto

O sistema evoluiu de um simples script de terminal para uma aplicação Desktop completa e robusta. O pipeline de dados, que antes operava de forma manual e engessada, agora conta com uma Interface Gráfica de Usuário (GUI) interativa e moderna construída com CustomTkinter.

A inserção do nome do arquivo não é mais feita diretamente no código, o sistema possui um explorador nativo que permite a seleção dinâmica dos extratos. Além disso, o motor de leitura foi expandido, através do uso avançado de Expressões Regulares (Regex), a aplicação já é capaz de realizar a triagem automática e o tratamento de extratos de múltiplas instituições, incluindo Nubank, Banco Inter, Banco do Brasil e Mercado Pago, diferenciando perfeitamente faturas de cartão de crédito de movimentações em conta geral (PIX, débito, transferências).


## Tecnologias e Ferramentas Utilizadas
A arquitetura foi pensada de forma simplificada, utilizei as seguintes tecnologias e bibliotecas:

* Interface Gráfica

  * CustomTkinter com Tkinter: Utilizados em conjunto para estruturar toda a parte visual do aplicativo. Essa combinação garantiu a construção de um design limpo, moderno e direto ao ponto, proporcionando uma experiência de usuário focada na usabilidade sem a necessidade de frameworks complexos.

* Tratamento e Padronização de Dados

  * Pandas: Atua como a ferramenta principal para o processamento das informações. O sistema coleta dados brutos de extratos bancários em formato .csv e utiliza o Pandas para limpar e padronizar as tabelas. Para isso, foram aplicados recursos avançados como Expressões Regulares (Regex), conversão temporal com pd.to_datetime e isolamento de variáveis complexas (como parcelas) através do método str.extract.

* Armazenamento Local

    * SQLite: O armazenamento dos dados financeiros é feito de forma segura e leve através deste banco de dados Serverless (sem servidor). O Python possui integração nativa com o SQLite, o que permitiu a criação de um banco de dados estritamente local (salvo em um arquivo .db), dispensando instalações de servidores SQL na máquina do usuário.

* Renderização de Gráficos

  * Matplotlib (pyplot e MultipleLocator): Estas são as bibliotecas responsáveis pelo motor de renderização matemática do dashboard. Elas processam os dados financeiros e calculam com precisão as posições de acordo com os eixos X e Y, gerando visualizações gráficas de evolução patrimonial com marcadores ajustados para facilitar a leitura.

* Integração com o Sistema Operacional

  * Módulo OS (Operating System): Uma biblioteca nativa do Python responsável por fazer a ponte de comunicação e busca de diretórios diretamente com o sistema operacional. Um exemplo prático da sua aplicação no projeto é o uso do comando os.path.exists, que atua como um sistema de segurança verificando se o arquivo do banco de dados já foi criado no hardware local antes de executar qualquer inserção.


## Próximos Passos

* Com a base lógica e visual já fixadas, as próximas implementações tem a intenção de aumentar a inteligência analítica do sistema:

  - Dashboard Interativo Completo: Aprofundar o uso do Matplotlib para gerar gráficos de composição sazonal, distribuição por bancos e resumos de gastos mensais na tela principal.

  - Categorização Inteligente: Mapear e classificar automaticamente o setor de compras (Alimentação, Transporte, Saúde, Lazer) através da análise de palavras-chave presentes nas descrições das faturas.

  - Módulo de Exportação: Adicionar a capacidade de gerar relatórios consolidados em formato PDF diretamente pela interface.
