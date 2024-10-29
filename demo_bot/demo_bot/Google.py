import os
import random
import logging
import discord
import google.generativeai as genai
from discord.ext import commands
from dotenv import load_dotenv
from bot.client import TheBot
from bot.client import prefix_finder
from bot.commands import MainCog

# Carrega as variáveis de ambiente
load_dotenv()

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração do Google Gemini
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Configurar o bot do Discord
intents = discord.Intents.default()
intents.message_content = True

# Criar uma instância do bot com o prefix_finder
bot = TheBot(command_prefix=prefix_finder, intents=intents)

# Contexto do chat para manter a personalidade do bot
SYSTEM_PROMPT = """Você é o assistente virtual do projeto de extensão da USP chamado CorvusIA, 
criado em 2024. Seu foco é auxiliar os membros do servidor com informações sobre inteligência 
artificial e projetos na USP São Carlos. Suas respostas devem ser informativas e engraçadas, mas
sempre curtas. Use emojis relacionados a corvos (como 🐦, 🦅, ou qualquer outro que represente 
corvos de forma criativa) para tornar as interações mais divertidas e envolventes. Lembre-se de manter
um tom amigável e acolhedor, refletindo o espírito colaborativo do projeto.


O algoritmo de votação do bot funciona assim:

Comando de Votação (!cmd *dia da semana*):

Quando o usuário digita !cmd segunda, !cmd terça, etc., o bot cria uma seleção de horários (das 9h às 22h) para o dia escolhido.
O usuário seleciona um horário, e o bot registra o voto associando o ID do usuário, dia da semana e horário em um dicionário de votos.
Registro de Votos:

Cada voto é armazenado no dicionário, com a estrutura user_id: dia_da_semana: horário, permitindo múltiplos votos por usuário e dias diferentes.
Comando para Exibir Votos (!cmd votos):

Quando !cmd votos é digitado, o bot lista todos os votos registrados para cada usuário e dia, mostrando o resumo dos horários escolhidos.
Esse fluxo permite que o bot registre e exiba votos de vários usuários, mantendo os dados de forma organizada!






"""

@bot.event
async def on_ready():
    logger.info(f'{bot.user} está online e pronto!')
    await bot.add_cog(MainCog(bot))  # Adiciona o cog com await
    await bot.tree.sync()  # Sincroniza os comandos do aplicativo

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    if bot.user.mentioned_in(message):
        await handle_mention(message)
    elif random.random() < 0.1: 
        await respond_to_message(message)

async def handle_mention(message):
    logger.info("Bot mencionado!")
    content = message.content.replace(f'<@{bot.user.id}>', '').strip()
    
    if content:
        logger.info(f"Conteúdo da mensagem: {content}")
        try:
            prompt = f"{SYSTEM_PROMPT}\n\nMensagem do usuário: {content}"
            response = model.generate_content(prompt)
            await message.channel.send(response.text)
            logger.info(f"Resposta gerada: {response.text}")
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {e}")
            await message.channel.send("Desculpe, tive um problema ao processar sua mensagem. ")

async def respond_to_message(message):
    try:
        prompt = f"{SYSTEM_PROMPT}\n\nResponda a esta mensagem de forma natural: {message.content}"
        response = model.generate_content(prompt)
        await message.channel.send(response.text)
    except Exception as e:
        logger.error(f"Erro ao gerar resposta: {e}")
        
def run_bot(disc_token):
    bot.run(disc_token)