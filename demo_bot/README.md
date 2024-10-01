# Discord Bot Lesson - Demo

## Criando o ambiente

### Instalando os componentes individualmente

```bash
# Cria um novo ambiente virtual
micromamba create -n discord-bot-lesson -c conda-forge python=3.12
# Ativa o ambiente na sessão atual
micromamba activate discord-bot-lesson
# Instalação das dependências iniciais
micromamba install -c conda-forge python-dotenv discord.py
```

### Instalando os componentes com o `env.lock`

```bash
micromamba env create -n discord-bot-lesson -f env.yml
```

### Gerando o lockfile

```bash
micromamba env export -n discord-bot-lesson --no-build > env.yml
```

## Executando o bot

**Importante**: O bot precisa de um token de acesso para o Discord, que pode ser obtido [aqui](https://discord.com/developers/applications).
**Importante**: O token deve estar em uma variável de ambiente chamada `DISCORD_TOKEN` no arquivo `.env`.

### Local

```bash
# Ativatar o ambiente
micromamba activate discord-bot-lesson

# Executar o bot
python ./demo_bot
```

### Docker Compose

```bash
# Iniciando o ambiente
docker compose up -d --build

# Parar o ambiente
docker compose down

# Logs
docker compose logs -f

