import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# --- 0. CARREGAR ENV ---
load_dotenv()

# --- 1. CONFIGURAÇÕES ---
API_KEY = os.getenv("GEMINI_API_KEY")
WORKSPACE = os.path.abspath("C:\\Users\\icaro\\projects\\WorkspaceAI")

# Cria a pasta de trabalho se ela não existir
if not os.path.exists(WORKSPACE):
    os.makedirs(WORKSPACE)

# --- 2. FERRAMENTAS (O QUE O AGENTE PODE FAZER) ---
def salvar_codigo(nome_arquivo: str, conteudo: str) -> str:
    """Cria ou edita um arquivo de código na pasta workspace."""
    caminho_completo = os.path.join(WORKSPACE, nome_arquivo)
    os.makedirs(os.path.dirname(caminho_completo), exist_ok=True)
    with open(caminho_completo, "w", encoding="utf-8") as f:
        f.write(conteudo)
    return f"Arquivo '{nome_arquivo}' salvo com sucesso no workspace."

def ler_codigo(nome_arquivo: str) -> str:
    """Lê o conteúdo de um arquivo para análise."""
    caminho_completo = os.path.join(WORKSPACE, nome_arquivo)
    if os.path.exists(caminho_completo):
        with open(caminho_completo, "r", encoding="utf-8") as f:
            return f.read()
    return f"Erro: O arquivo '{nome_arquivo}' não foi encontrado."

def pegar_entrada_multilinha():
    print("\n👨‍💻 Você (digite 'ENVIAR' em uma linha nova para processar ou 'sair' para encerrar):")
    linhas = []
    while True:
        linha = input()
        if linha.upper() == "ENVIAR":
            break
        if linha.lower() in ["sair", "exit"]:
            return "sair"
        linhas.append(linha)
    return "\n".join(linhas)

# --- 3. INICIALIZAÇÃO DO AGENTE ---
client = genai.Client(api_key=API_KEY)

# Configura o "Cérebro" e as Ferramentas
config = types.GenerateContentConfig(
    system_instruction="""Você é um Agente Programador Sênior. 
    Sempre use a função 'salvar_codigo' para entregar códigos prontos.
    Se o usuário pedir para revisar um código, use 'ler_codigo' primeiro.
    Seja conciso e técnico.""",
    tools=[salvar_codigo, ler_codigo],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False)
)

def rodar_agente():
    chat = client.chats.create(model="gemini-2.5-flash", config=config)
    print("🤖 Agente Unificado Pronto! (Digite 'sair' para parar)")
    
    while True:
        comando = pegar_entrada_multilinha()
        if comando.lower() in ["sair", "exit", "quit"]:
            print("👋Até logo")
            break
            
        print("⏳ Agente pensando e agindo...")
        try:
            resposta = chat.send_message(comando)
            print(f"\n🤖 Agente: {resposta.text}")
        except Exception as e:
            print(f"❌ Ocorreu um erro: {e}")

if __name__ == "__main__":
    rodar_agente()