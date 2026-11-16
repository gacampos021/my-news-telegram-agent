# Agente de Notícias de Computação

Agente de LLM em Python, construído com o Google SDK, que busca notícias do mundo da computação, faz a triagem das mais relevantes e entrega um resumo diário no Telegram.

**Status:** versão 0.1 (primeira versão). Veja o Roadmap ao final para os próximos passos.

## Objetivo

Reduzir o ruído do noticiário de tecnologia. Em vez de acompanhar dezenas de fontes, você recebe todo dia útil, logo cedo, uma seleção curta com o que realmente importa.

## Como funciona

Todo dia útil às 7h da manhã, um cron aciona um script bash. Esse script executa o agente e, ao final, envia a mensagem gerada para o Telegram por meio de um bot.

O agente, por sua vez, segue três etapas:

1. **Busca:** coleta notícias recentes relacionadas ao mundo da computação.
2. **Triagem:** usa o LLM para avaliar o material coletado e escolher as notícias mais relevantes.
3. **Saída:** grava o resultado selecionado em um arquivo `.txt`, que é a base da mensagem enviada ao Telegram.

## Tecnologias

- Python
- Google SDK (modelos Gemini)
- Bot do Telegram
- Cron e Bash para agendamento e orquestração

## Pré-requisitos

- Python 3.10 ou superior
- Chave de API do Google AI
- Bot do Telegram criado pelo BotFather, com o token em mãos
- Identificador do chat do Telegram que receberá as mensagens
- Ambiente Linux ou macOS com cron disponível

## Configuração

As credenciais ficam em variáveis de ambiente, guardadas em um arquivo `.env` que não deve ser versionado:

- Chave de API do Google
- Token do bot do Telegram
- Identificador do chat do Telegram

Recomenda-se manter um arquivo `.env.example` no repositório, apenas com os nomes das variáveis, para facilitar a configuração em outras máquinas.

## Agendamento

O cron roda de segunda a sexta, às 7h. Alguns cuidados ao configurá-lo:

- Use caminhos absolutos, pois o cron executa com um ambiente mínimo.
- Confira o fuso horário do servidor, já que o horário do cron segue o dele.
- Redirecione a saída para um arquivo de log, para facilitar o diagnóstico de falhas.
- O cron não conhece feriados: ele dispara em todo dia útil de calendário.

## Saída

Cada execução gera um arquivo `.txt` com as notícias selecionadas, e esse conteúdo é enviado ao Telegram. O Telegram limita cada mensagem a 4096 caracteres, então saídas maiores precisam ser divididas em mais de uma mensagem.

## Roadmap

- Expandir as categorias de notícias (por exemplo: inteligência artificial, segurança, cloud, desenvolvimento, hardware e open source).
- Estruturar melhor o formato da mensagem do Telegram, com seções por categoria, títulos em destaque, resumos curtos e links clicáveis.
- Dividir automaticamente mensagens longas.
- Evitar notícias repetidas entre dias consecutivos.
- Avisar no próprio Telegram quando a execução falhar.
- Adicionar testes automatizados.

## Solução de problemas

- **O cron não executa:** verifique se o script tem permissão de execução e se o crontab usa caminhos absolutos.
- **A mensagem não chega:** confirme o identificador do chat e se você já iniciou uma conversa com o bot.
- **Erro de variável vazia:** o arquivo `.env` provavelmente não foi carregado pelo script.
- **Erro de autenticação no Google:** a chave de API pode estar inválida ou sem acesso ao modelo escolhido.

Em qualquer caso, o primeiro lugar para olhar é o arquivo de log da última execução.

## Licença

A definir.
