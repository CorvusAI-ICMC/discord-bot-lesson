import logging
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

class DiaSemanaSelect(discord.ui.Select):
    def __init__(self, cog, dia_semana):
        self.cog = cog  # Referência ao cog principal para armazenar o voto
        self.dia_semana = dia_semana
        
        opcoes = [f"{i}:00" for i in range(9, 23)]
        super().__init__(
            placeholder="Selecione um horário",
            options=[discord.SelectOption(label=opcao) for opcao in opcoes],
            custom_id=dia_semana
        )

    async def callback(self, interaction: discord.Interaction):
        # Obtém o valor selecionado pelo usuário
        horario_selecionado = self.values[0]
        
        # Registra o voto do usuário no cog
        self.cog.registrar_voto(interaction.user.id, self.dia_semana, horario_selecionado)
        
        # Confirmação de voto para o usuário
        await interaction.response.send_message(
            f"Voto registrado para {self.dia_semana} às {horario_selecionado}", 
            ephemeral=True
        )


class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.votos = {}  # Dicionário para armazenar votos de usuários

    def registrar_voto(self, user_id, dia_semana, horario):
        # Armazena o voto do usuário para o dia e horário escolhidos
        if user_id not in self.votos:
            self.votos[user_id] = {}
        self.votos[user_id][dia_semana] = horario
        
        logger.info(f"Voto registrado: Usuário {user_id} escolheu {horario} em {dia_semana}")

    async def exibir_votos(self, ctx):
        # Exibe todos os votos registrados
        mensagem = "Votos registrados:\n"
        for user_id, dias in self.votos.items():
            mensagem += f"\nUsuário {user_id}:\n"
            for dia, horario in dias.items():
                mensagem += f"  {dia}: {horario}\n"
        await ctx.send(mensagem or "Nenhum voto registrado.")

    @commands.command(name="segunda")
    async def segunda(self, ctx: commands.Context):
        logger.info("Comando segunda chamado")
        
        view = discord.ui.View(timeout=86.400)
        view.add_item(DiaSemanaSelect(self, "segunda"))
        
        mensagem = "Escolha o melhor horário para segunda-feira:"
        await ctx.send(content=mensagem, view=view)

    # Comandos para outros dias da semana, seguindo o mesmo padrão
    @commands.command(name="terca")
    async def terca(self, ctx: commands.Context):
        logger.info("Comando terça chamado")
        view = discord.ui.View(timeout=86.400)
        view.add_item(DiaSemanaSelect(self, "terca"))
        await ctx.send("Escolha o melhor horário para terça-feira:", view=view)

    @commands.command(name="quarta")
    async def quarta(self, ctx: commands.Context):
        logger.info("Comando quarta chamado")
        view = discord.ui.View(timeout=86.400)
        view.add_item(DiaSemanaSelect(self, "quarta"))
        await ctx.send("Escolha o melhor horário para quarta-feira:", view=view)

    @commands.command(name="quinta")
    async def quinta(self, ctx: commands.Context):
        logger.info("Comando quinta chamado")
        view = discord.ui.View(timeout=86.400)
        view.add_item(DiaSemanaSelect(self, "quinta"))
        await ctx.send("Escolha o melhor horário para quinta-feira:", view=view)

    @commands.command(name="sexta")
    async def sexta(self, ctx: commands.Context):
        logger.info("Comando sexta chamado")
        view = discord.ui.View(timeout=86.400)
        view.add_item(DiaSemanaSelect(self, "sexta"))
        await ctx.send("Escolha o melhor horário para sexta-feira:", view=view)

    @commands.command(name="sabado")
    async def sabado(self, ctx: commands.Context):
        logger.info("Comando sábado chamado")
        view = discord.ui.View(timeout=86.400)
        view.add_item(DiaSemanaSelect(self, "sabado"))
        await ctx.send("Escolha o melhor horário para sábado:", view=view)

    @commands.command(name="votos")
    async def votos(self, ctx: commands.Context):
        # Exibe todos os votos registrados quando o comando "!votos" é chamado
        await self.exibir_votos(ctx)


def setup(bot):
    bot.add_cog(MainCog(bot))
