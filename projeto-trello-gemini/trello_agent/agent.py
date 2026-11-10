import os
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from trello import TrelloClient
from google.adk.agents import Agent

# Carrega o .env que está na pasta raiz (projeto-trello-gemini/.env)
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


def remover_acentos(texto: str) -> str:
    """Remove acentos de uma string e padroniza em minúsculas para comparações."""
    if not texto:
        return ""
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    ).lower().strip()


def conectar_trello() -> Optional[TrelloClient]:
    """Estabelece a ligação com a API do Trello usando as credenciais do .env."""
    api_key = os.getenv('TRELLO_API_KEY')
    token = os.getenv('TRELLO_TOKEN')
    if not api_key or not token:
        return None
    try:
        return TrelloClient(api_key=api_key, token=token)
    except Exception as e:
        print(f"Erro ao conectar ao Trello: {e}")
        return None


def obter_quadro(cliente: TrelloClient, nome_quadro: str = 'DIO'):
    """Busca o quadro alvo no Trello ignorando diferenças de maiúsculas/minúsculas."""
    quadros = cliente.list_boards()
    return next((b for b in quadros if b.name.lower() == nome_quadro.lower()), None)


def listar_tarefas(status: str = "") -> str:
    """
    Lista as tarefas do quadro DIO.
    Pode listar todas (se status for vazio) ou filtrar por um status específico
    (ex: 'A fazer', 'Em andamento', 'Concluído').
    """
    try:
        cliente = conectar_trello()
        if not cliente:
            return "Erro: Não foi possível conectar ao Trello. Verifique o arquivo .env."

        quadro_alvo = obter_quadro(cliente)
        if not quadro_alvo:
            return "Erro: Quadro 'DIO' não encontrado."

        status_filtro = remover_acentos(status)
        resposta = []

        for lista in quadro_alvo.list_lists():
            if status_filtro and status_filtro not in remover_acentos(lista.name):
                continue

            resposta.append(f"\n📋 Status: {lista.name}")
            cartoes = lista.list_cards()

            if not cartoes:
                resposta.append("   (Sem tarefas)")
            else:
                for cartao in cartoes:
                    resposta.append(f"   - {cartao.name}")

        if not resposta:
            return f"Nenhuma lista encontrada para o status '{status}'."

        return "\n".join(resposta)
    except Exception as e:
        return f"Erro ao listar tarefas: {e}"


def criar_tarefa(nome: str, descricao: str = "", data: str = "") -> str:
    """
    Cria uma nova tarefa (card) na lista 'A fazer' do quadro DIO.
    Aceita nome da tarefa, descrição opcional e data no formato YYYY-MM-DD ou DD/MM/YYYY.
    """
    try:
        cliente = conectar_trello()
        if not cliente:
            return "Erro: Não foi possível conectar ao Trello. Verifique o arquivo .env."

        quadro_alvo = obter_quadro(cliente)
        if not quadro_alvo:
            return "Erro: Quadro 'DIO' não encontrado."

        lista_a_fazer = next(
            (lista for lista in quadro_alvo.list_lists() if 'a fazer' in remover_acentos(lista.name)),
            None
        )
        if not lista_a_fazer:
            return "Erro: Lista 'A fazer' não encontrada no quadro."

        descricao_completa = descricao
        if data:
            descricao_completa = f"{descricao}\nData alvo: {data}".strip()

        lista_a_fazer.add_card(name=nome, desc=descricao_completa)
        return f"Sucesso! Tarefa '{nome}' criada na lista 'A fazer'."
    except Exception as e:
        return f"Erro ao criar a tarefa: {e}"


def mover_tarefa(nome_tarefa: str, status_destino: str) -> str:
    """
    Move uma tarefa (card) existente para uma nova lista de status
    ('A fazer', 'Em andamento' ou 'Concluído').
    """
    try:
        cliente = conectar_trello()
        if not cliente:
            return "Erro: Não foi possível conectar ao Trello. Verifique o arquivo .env."

        quadro_alvo = obter_quadro(cliente)
        if not quadro_alvo:
            return "Erro: Quadro 'DIO' não encontrado."

        status_normalizado = remover_acentos(status_destino)
        listas_do_quadro = quadro_alvo.list_lists()

        # 1. Encontrar a lista de destino (aceita com ou sem acento)
        lista_destino = next(
            (lista for lista in listas_do_quadro if remover_acentos(lista.name) == status_normalizado),
            None
        )
        if not lista_destino:
            return f"Erro: Lista de destino '{status_destino}' não encontrada."

        # 2. Procurar o card em todas as listas
        cartao_encontrado = None
        for lista in listas_do_quadro:
            for cartao in lista.list_cards():
                if remover_acentos(cartao.name) == remover_acentos(nome_tarefa):
                    cartao_encontrado = cartao
                    break
            if cartao_encontrado:
                break

        if not cartao_encontrado:
            return f"Erro: Tarefa '{nome_tarefa}' não encontrada."

        # 3. Mover o card
        cartao_encontrado.change_list(lista_destino.id)
        return f"Sucesso! Tarefa '{nome_tarefa}' movida para '{lista_destino.name}'."
    except Exception as e:
        return f"Erro ao mover a tarefa: {e}"


# Injeta a data atual automaticamente na instrução
data_hoje = datetime.now().strftime("%d/%m/%Y")

instrucoes = f"""
Você é um assistente pessoal focado em produtividade que organiza as minhas tarefas no Trello.
A data de hoje é {data_hoje}.

Siga sempre este fluxo:
1. Comece a conversa perguntando quais são as minhas tarefas de hoje, já informando a data atual ({data_hoje}).
2. Use a ferramenta 'criar_tarefa' para cada nova tarefa que eu mencionar.
3. Se eu pedir para ver o que tenho para fazer, use 'listar_tarefas'.
4. Quando eu disser que terminei algo ou que comecei, use 'mover_tarefa' para atualizar o status (ex: mover para 'Concluído' ou 'Em andamento').
Seja breve e direto nas respostas.
"""

root_agent = Agent(
    name="trello_agent",
    model="gemini-3.8-flash",
    instruction=instrucoes,
    tools=[listar_tarefas, criar_tarefa, mover_tarefa]
)