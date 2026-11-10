# Agente IA para Trello com Google ADK

Um agente conversacional desenvolvido em Python utilizando o Agent Development Kit (ADK) do Google e o modelo Gemini. Este assistente pessoal atua diretamente na gestão de produtividade, organizando, listando e modificando tarefas de um quadro do Trello a partir de comandos em linguagem natural.

## 🛠️ Ferramentas do Agente

O agente foi configurado com quatro ferramentas principais (tools) que interagem com a API do Trello:

* **`listar_tarefas`**: Lê o quadro "DIO" e retorna todas as tarefas ou filtra por listas específicas (ex: "A fazer", "Concluído").
* **`criar_tarefa`**: Adiciona novos cards à lista "A fazer", formatando automaticamente a data de entrega.
* **`mover_tarefa`**: Altera o status de um card existente, movendo-o entre as listas de forma autônoma.
* **`remover_tarefa`**: Exclui um card permanentemente quando solicitado.

## 🚀 Melhorias Implementadas

Além dos requisitos base do projeto, desenvolvi as seguintes otimizações com foco em resiliência e usabilidade:

1. **Correção do Fuso Horário (Timezone):** Ajuste na injeção da data (`due_date`) com fixação ao meio-dia em UTC (`T12:00:00.000Z`), corrigindo o bug onde as datas chegavam ao Trello com um dia de atraso.
2. **Filtro de Acentos e Padronização:** Criação da função `remover_acentos` utilizando a biblioteca `unicodedata`. O agente agora reconhece comandos com ou sem acentuação e diferenças de maiúsculas/minúsculas (ex: "concluido" = "Concluído").
3. **Gestão de Exceções Generalizada:** Implementação de blocos `try/except` em todas as ferramentas de rede, garantindo que o agente retorne mensagens de erro claras na interface em caso de falha de conexão, sem derrubar o servidor.
4. **Ferramenta de Remoção:** Adição da função `remover_tarefa` com iteração por todas as listas do quadro para localizar e excluir cards de forma precisa.

## ⚙️ Como Configurar e Rodar

### Pré-requisitos
* Python 3.10 ou superior
* Chave de API do Google AI Studio (Gemini)
* Credenciais do Trello (API Key e Token)

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/SEU_USUARIO/agente-trello-gemini.git](https://github.com/SEU_USUARIO/agente-trello-gemini.git)
   cd agente-trello-gemini
