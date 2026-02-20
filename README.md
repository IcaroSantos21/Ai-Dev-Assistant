# 🚀 ai_dev_assistant: Seu Engenheiro de Software Sênior Pessoal com IA

## Visão Geral

O `ai_dev_assistant` é um agente de inteligência artificial projetado para atuar como um engenheiro de software sênior, especializado em depuração e refatoração de código. Ele interage de forma conversacional, utilizando as capacidades do modelo Gemini do Google e um conjunto de ferramentas personalizadas para ler, analisar e modificar arquivos em um workspace definido.

## Arquitetura

A arquitetura do `ai_dev_assistant` é modular e segue o padrão de um **Agente de IA Habilitado por Ferramentas (Tool-Augmented AI Agent)**, dividido em componentes chave que orquestram a interação do usuário com o LLM e as operações no sistema de arquivos.

![Diagrama de Arquitetura Simplificado](https://www.plantuml.com/plantuml/svg/TO_D2eCn34Nx-op5qCqY2y-gQ0S00o3e-d91n093G0K3M0J2N32S015L0K-fMvCg2t5-rMvG954R0O7g6S21-x7N8Ff1j9S8Q5T0_bI0K73-s5s6B8D6N7A-a9k-e2l8Q4Q0e0W0E0Q7O5j6C4Q1U7R1W8o1w6S5R0i2l0j3Y0D4O30-p4U0V8J448O4T2S0D1V0S8Q4C5S8V2m8_jY0m0Y4w0e5X8o8c5B7w4-sQ02L8u8g7h0H0u0Q712h7S4W4E4v62g6g2H7T2K8v1i7K3E4r8X1H6Q610S8S6Z00)

### Componentes Principais:

1.  **Configuração do Ambiente (`.env` & `os`):**
    *   **Carregamento de Variáveis de Ambiente:** Utiliza `python-dotenv` para carregar chaves de API e outras configurações sensíveis do arquivo `.env`, garantindo que credenciais não sejam expostas diretamente no código.
    *   **Gestão de Workspace:** Define um diretório de trabalho (`WORKSPACE`) onde todas as operações de arquivo serão executadas. Se o diretório não existir, ele é criado automaticamente. Isso isola o agente em seu próprio ambiente de projeto.

2.  **Conjunto de Ferramentas (Tooling):**
    *   Este é o coração da capacidade de interação do agente com o ambiente. Funções Python são definidas e registradas como "ferramentas" que o LLM pode chamar.
    *   `salvar_codigo(nome_arquivo: str, conteudo: str) -> str`: Permite ao agente criar ou modificar arquivos dentro do `WORKSPACE`. Essencial para aplicar refatorações ou correções.
    *   `ler_codigo(nome_arquivo: str) -> str`: Habilita o agente a ler o conteúdo de qualquer arquivo no `WORKSPACE`, fundamental para entender o contexto do código e depurar.
    *   `listar_arquivos() -> str`: Fornece ao agente a capacidade de listar os arquivos e pastas no `WORKSPACE`, ajudando na navegação e compreensão da estrutura do projeto.
    *   `pegar_entrada_multilinha()`: Uma utilidade para capturar entradas complexas do usuário, permitindo que o usuário digite várias linhas de instruções ou código antes de enviar.

3.  **Inicialização e Configuração do Agente (Google Gemini API):**
    *   **Cliente Gemini:** O `genai.Client` é inicializado com a `API_KEY`, estabelecendo a conexão com os serviços do Google Gemini.
    *   **Instrução do Sistema (`system_instruction`):** Uma `system_instruction` detalhada é fornecida ao modelo, definindo o "persona" do agente (Engenheiro de Software Sênior, Debugger, Refactorer) e suas diretrizes operacionais (identificar gargalos, sugerir melhorias Clean Code/SOLID, usar `ler_codigo` para erros, explicar o PORQUÊ das mudanças). Isso molda o comportamento e as prioridades do agente.
    *   **Registro de Ferramentas:** As funções `salvar_codigo` e `ler_codigo` (e implicitamente outras que podem ser adicionadas) são passadas para a configuração do modelo (`tools=[salvar_codigo, ler_codigo]`).
    *   **Chamada de Função Automática (`automatic_function_calling`):** Habilitada para permitir que o modelo decida de forma autônoma qual ferramenta usar e quando, com base na conversa e na `system_instruction`.

4.  **Loop de Execução do Agente (`rodar_agente`):**
    *   **Criação de Chat:** Um novo chat é iniciado com o modelo Gemini (`client.chats.create(model="gemini-2.5-flash", config=config)`).
    *   **Interação Contínua:** Um loop `while True` mantém o agente ativo, esperando a entrada do usuário.
    *   **Processamento da Entrada:** A entrada do usuário é capturada via `pegar_entrada_multilinha()`.
    *   **Envio para o LLM:** A mensagem do usuário é enviada para o modelo Gemini (`chat.send_message(comando)`). O modelo então processa a entrada, decide se deve usar uma ferramenta e gera uma resposta textual.
    *   **Exibição da Resposta:** A resposta do agente (incluindo resultados de chamadas de ferramentas) é impressa para o usuário.
    *   **Tratamento de Erros:** Um bloco `try-except` básico lida com exceções durante a interação com o modelo.

## Como Funciona

1.  O usuário inicia o agente.
2.  O agente espera a entrada do usuário.
3.  Quando o usuário envia uma solicitação (ex: "Refatore o arquivo `meu_modulo.py` para seguir os princípios SOLID"), o agente:
    *   Analisa a solicitação com seu "cérebro" (modelo Gemini).
    *   Baseado na `system_instruction` e nas ferramentas disponíveis, ele pode decidir chamar `ler_codigo('meu_modulo.py')` para entender o contexto.
    *   Após analisar o código, ele gera uma refatoração e pode chamar `salvar_codigo('meu_modulo.py', 'novo_conteudo_refatorado')` para aplicar as mudanças.
    *   Finalmente, ele responde ao usuário com o resultado de suas ações ou um pedido de mais informações.

## Vantagens da Arquitetura

*   **Extensibilidade:** Novas ferramentas podem ser facilmente adicionadas para expandir as capacidades do agente (ex: ferramentas para executar testes, analisar dependências, etc.).
*   **Controle e Contexto:** A `system_instruction` oferece um controle granular sobre o comportamento do agente, garantindo que ele opere dentro das diretrizes desejadas (Clean Code, SOLID, etc.).
*   **Interatividade:** A interface conversacional torna a interação intuitiva para o usuário.
*   **Isolamento:** O conceito de `WORKSPACE` garante que as operações do agente sejam contidas e não afetem arquivos fora do projeto.

## Configuração

1.  **Variáveis de Ambiente:** Crie um arquivo `.env` na raiz do projeto com sua chave de API do Gemini:
    ```
    GEMINI_API_KEY=SUA_CHAVE_AQUI
    ```
2.  **Instalação de Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

## Como Rodar

```bash
python main.py
```

Após iniciar, o agente estará pronto para receber seus comandos. Digite `ENVIAR` em uma nova linha para processar sua entrada ou `sair` para encerrar.