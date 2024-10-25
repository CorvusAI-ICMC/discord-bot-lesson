import logging
import discord
from discord import app_commands
from discord.ext import commands

logger = logging.getLogger(__name__)

class DiaSemanaSelect(discord.ui.Select):
    def __init__(self, dia_semana):
        opcoes = [f"{i}:00" for i in range(9, 23)]
        super().__init__(
            placeholder="Selecione um horário",
            options=[discord.SelectOption(label=opcao) for opcao in opcoes],
            custom_id=dia_semana
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Voto registrado para {self.custom_id} às {interaction.data.values[0]}", ephemeral=True)


class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="chat")
    async def chat(self, ctx: commands.Context):
        await ctx.send("Not in the mood right now")

    @commands.command(name="subtract")
    async def subtract(self, ctx: commands.Context, num1: int, num2: int):
        await ctx.send(f"A diferença é {num1 - num2}!")

    @app_commands.command(name="slash")
    async def slash(self, interaction: discord.Interaction):
        await interaction.response.send_message("Slash command!")

    @commands.command(name="segunda")
    async def segunda(self, ctx: commands.Context):
        logger.info("Comando segunda chamado")
        
        view = discord.ui.View()
        view.add_item(DiaSemanaSelect("segunda"))
        
        mensagem = "Escolha o melhor horário para segunda-feira:"
        await ctx.send(content=mensagem, view=view)

    @commands.command(name="terca")
    async def terca(self, ctx: commands.Context):
        logger.info("Comando terça chamado")
        
        view = discord.ui.View()
        view.add_item(DiaSemanaSelect("terca"))
        
        mensagem = "Escolha o melhor horário para terça-feira:"
        await ctx.send(content=mensagem, view=view)

    @commands.command(name="quarta")
    async def quarta(self, ctx: commands.Context):
        logger.info("Comando quarta chamado")
        
        view = discord.ui.View()
        view.add_item(DiaSemanaSelect("quarta"))
        
        mensagem = "Escolha o melhor horário para quarta-feira:"
        await ctx.send(content=mensagem, view=view)

    @commands.command(name="quinta")
    async def quinta(self, ctx: commands.Context):
        logger.info("Comando quinta chamado")
        
        view = discord.ui.View()
        view.add_item(DiaSemanaSelect("quinta"))
        
        mensagem = "Escolha o melhor horário para quinta-feira:"
        await ctx.send(content=mensagem, view=view)

    @commands.command(name="sexta")
    async def sexta(self, ctx: commands.Context):
        logger.info("Comando sexta chamado")
        
        view = discord.ui.View()
        view.add_item(DiaSemanaSelect("sexta"))
        
        mensagem = "Escolha o melhor horário para sexta-feira:"
        await ctx.send(content=mensagem, view=view)

    @commands.command(name="sabado")
    async def sabado(self, ctx: commands.Context):
        logger.info("Comando sábado chamado")
        
        view = discord.ui.View()
        view.add_item(DiaSemanaSelect("sabado"))
        
        mensagem = "Escolha o melhor horário para sábado:"
        await ctx.send(content=mensagem, view=view)


def setup(bot):
    bot.add_cog(MainCog(bot))