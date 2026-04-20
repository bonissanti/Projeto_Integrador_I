# Projeto Integrador I

Sistema web para agendamento e gerenciamento de usuários, desenvolvido em Django como parte do Projeto Integrador I da Univesp.

Os clientes fazem agendamentos via **bot do WhatsApp**; ao confirmar, o agendamento é persistido no banco e um evento é criado automaticamente no **Google Calendar** da profissional. A gestão de clientes, serviços e agendamentos é feita pelo **Django Admin** customizado.

---

## 🛠️ Stack

- **Python 3.10+** — linguagem (compatível com Django 6)
- **Django 6.0** — framework web
- **SQLite** — banco de dados (desenvolvimento)
- **Google Calendar API** — integração de eventos
- **WhatsApp Cloud API** — webhook do bot
- **uv** — gerenciador de pacotes
- **Make** — automação de tarefas

---

## 📋 Pré-requisitos

- **Python 3.10+** (o Makefile detecta `python3` automaticamente)
- **Make**
- Opcional para integrações:
  - Arquivo `calendar_credentials.json` na pasta `Backend/proj_integrador/` (service account do Google)
  - Token e webhook do WhatsApp Cloud API

---

## 🚀 Instalação e Configuração

### 1. Clone e prepare o ambiente

```bash
git clone <url-do-repo>
cd Projeto_Integrador_I
make setup            # Cria .venv, instala uv e dependências
```

### 2. Configure o `.env`

Crie um arquivo `.env` na raiz do projeto com:

```dotenv
SECRET_KEY=gere-uma-chave-longa-e-aleatoria
VERIFY_TOKEN=seu-token-do-whatsapp-webhook
```

> **Dica**: para gerar uma `SECRET_KEY` forte, rode:
> `python3 -c "import secrets; print(secrets.token_urlsafe(64))"`

### 3. Ative o ambiente e prepare o banco

```bash
make activate         # Abre um shell com o venv ativado
make migrate          # Aplica as migrações
make createsuperuser  # Cria o usuário administrador do painel
```

### 4. Rode o servidor

```bash
make runserver        # http://localhost:8000
```

Acesse o painel em **http://localhost:8000/admin**.

---

## 🧑‍💼 Painel Administrativo

O Django Admin foi customizado para a gestão diária dos agendamentos:

- **Agendamentos**: lista com badge de status colorido, indicador de sincronização com Google Calendar, `date_hierarchy` por data, busca por nome/telefone do cliente, filtros por status e data, e **ações em lote** para *cancelar* ou *marcar como concluídos* vários agendamentos de uma vez.
- **Clientes**: busca por nome, telefone ou email; filtro de clientes deletados.
- **Serviços**: gestão de tipos de trança, preço (em BRL) e duração.
- **Formulário de agendamento**: valida que a data escolhida não esteja no passado (na criação) e usa picker `datetime-local`.

---

## 🤖 Bot do WhatsApp

O fluxo do bot é uma máquina de estados implementada em `WhatsAppBot/engine.py`. Estados cobrem: boas-vindas, cadastro, escolha de data, local de atendimento, confirmação, cancelamento e consulta de agendamentos.

**Webhook**: exposto em `WhatsAppBot/urls.py`. Para desenvolvimento local, use `ngrok` (há um `ngrok.yml` de exemplo) e registre a URL pública no painel do WhatsApp Cloud API.

> ⚠️ **Nota**: o estado das conversas hoje é mantido em memória (`conversations` dict). Reiniciar o servidor descarta as sessões ativas. Persistência em banco está no `PLANO_DE_ACAO.md`.

---

## 🗓️ Integração com Google Calendar

Ao salvar um `Appointment` com `status='scheduled'`, o método `save()` chama `Agendamento.calendar_utils.criar_evento_google_calendar`, que:

1. Usa uma *service account* do Google (arquivo `calendar_credentials.json`).
2. Cria um evento de 2 horas no calendário configurado (`CALENDAR_ID`).
3. Persiste o `google_event_id` no `Appointment`.

Se o arquivo de credenciais estiver ausente, a integração é **pulada com um warning** (o agendamento é gravado no banco normalmente).

---

## 🧪 Testes

```bash
make test             # Roda a suite completa (19 testes)
make check            # Verifica a configuração do Django
```

---

## 📁 Estrutura

```
Projeto_Integrador_I/
├── Backend/
│   └── proj_integrador/
│       ├── Agendamento/           # models, admin, calendar_utils, managers
│       │   ├── migrations/
│       │   └── tests/
│       ├── Usuario/               # API REST de CRUD de clientes
│       ├── WhatsAppBot/           # engine (state machine), webhook, helper
│       │   └── bot/
│       ├── config/                # settings.py, urls.py
│       └── manage.py
├── Makefile                       # Automação dos comandos do projeto
├── Taskfile.yml                   # Alternativa ao Make (Task runner)
├── docker-compose.yml             # Execução em container
├── requirements.txt               # Dependências Python
├── PLANO_DE_ACAO.md               # Roadmap de melhorias e dívidas técnicas
└── ngrok.yml                      # Config de túnel para dev do webhook
```

---

## 📋 Comandos principais

| Comando | Descrição |
|---|---|
| `make setup` | Cria `.venv` e instala tudo |
| `make activate` | Abre um shell com o venv ativado |
| `make migrate` | Aplica migrações no banco |
| `make makemigrations` | Gera novas migrações a partir das mudanças nos models |
| `make runserver` | Sobe o servidor em `http://localhost:8000` |
| `make createsuperuser` | Cria conta de admin |
| `make test` | Roda os testes |
| `make check` | Verifica a configuração do Django |
| `make update-requirements` | Atualiza `requirements.txt` |
| `make clean` | Remove o `.venv` e caches |
| `make help` | Lista todos os comandos |

---

## 💡 Dicas

- **Erro "SECRET_KEY must not be empty"**: crie o `.env` na raiz do projeto (passo 2).
- **Integração Google falhando**: verifique se `calendar_credentials.json` está em `Backend/proj_integrador/` e se o email do calendário em `calendar_utils.py` (`CALENDAR_ID`) tem a service account compartilhada.
- **Testes não encontram nada**: rode via `make test` (ele entra no diretório correto); rodar `python manage.py test` manualmente exige estar dentro de `Backend/proj_integrador/`.
- **Para limpar tudo e recomeçar**: `make clean && make setup`.

---

## 🗺️ Próximos passos

Veja o [PLANO_DE_ACAO.md](./PLANO_DE_ACAO.md) para a lista priorizada de melhorias — incluindo persistência de estado do bot, validação HMAC do webhook, settings por ambiente e exclusão de evento no Google quando agendamento é cancelado.
