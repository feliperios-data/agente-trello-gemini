# Agente IA para Trello com Google ADK

Projeto desenvolvido como entrega prática do desafio da trilha **DXC - IA do Zero ao Primeiro Agente**, promovida pela [Digital Innovation One (DIO)](https://www.dio.me/) em parceria com a **DXC Technology**.

Trata-se de um agente conversacional em Python construído com o Agent Development Kit (ADK) do Google e o modelo Gemini. O assistente atua na gestão de produtividade, criando, listando, movendo e excluindo tarefas de um quadro do Trello a partir de comandos em linguagem natural.

## 🛠️ Ferramentas do Agente

O agente foi configurado com quatro ferramentas principais (`tools`) que interagem com a API do Trello via `py-trello`:

* **`listar_tarefas`**: Lê o quadro "DIO" e retorna todas as tarefas ou filtra por listas específicas (ex: "A fazer", "Em andamento", "Concluído").
* **`criar_tarefa`**: Adiciona novos cards à lista "A fazer", incluindo descrição e prazo formatado.
* **`mover_tarefa`**: Altera o status de um card existente, movendo-o entre as listas conforme o andamento informado na conversa.
* **`remover_tarefa`**: Localiza e exclui um card permanentemente quando solicitado.

## 🚀 Melhorias Implementadas

Além dos requisitos base do desafio, foram implementadas as seguintes melhorias técnicas:

1. **Correção do Fuso Horário (Timezone):** Ajuste no envio do parâmetro `due` fixando o horário ao meio-dia em UTC (`T12:00:00.000Z`), corrigindo o comportamento em que as datas chegavam ao Trello com um dia a menos no fuso horário do Brasil (UTC-3).
2. **Normalização de Strings e Filtro de Acentos:** Criação da função `remover_acentos` com a biblioteca nativa `unicodedata`. O agente aceita variações com ou sem acento e diferentes capitalizações (ex: `"concluido"` ou `"Concluído"`).
3. **Centralização da Conexão e Busca do Quadro:** Funções auxiliares `conectar_trello` e `obter_quadro` para evitar repetição de código entre as ferramentas.
4. **Tratamento de Exceções Generalizado:** Uso de blocos `try/except` em todas as ferramentas para capturar falhas de rede ou de API sem interromper a execução do agente.
5. **Ferramenta de Exclusão de Cards:** Implementação da função `remover_tarefa` para completar o ciclo CRUD de tarefas no quadro.

## ⚙️ Como Configurar e Rodar

### Pré-requisitos
* Python 3.10 ou superior
* Chave de API do Google AI Studio (`GOOGLE_API_KEY`)
* Credenciais de desenvolvedor do Trello (`TRELLO_API_KEY` e `TRELLO_TOKEN`)
* Um quadro no Trello chamado **DIO** contendo as listas: `A fazer`, `Em andamento` e `Concluído`

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/SEU_USUARIO/agente-trello-gemini.git](https://github.com/SEU_USUARIO/agente-trello-gemini.git)
   cd agente-trello-gemini
