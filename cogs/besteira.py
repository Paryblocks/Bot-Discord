import discord
from discord.ext import commands

class besteira(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @commands.command()
    async def salve(self, ctx:commands.Context):
        nome = ctx.author.name
        apelido = ctx.author.display_name
        if nome == "paryblocks":
            await ctx.send(f"Ah sim.. Minha criadora, {apelido}! Quanto tempo até aquela sessão que eu vou ser o chefão?")
        elif nome == "wordy42":
            await ctx.send(f"{apelido}?!? Ouvi dizer que você é o monstro.. mas seria um monstro TENEBROSO?")
        elif nome == "raelvd":
            await ctx.send(f"O inimigo do normal e do senso comum, {apelido}! Pelo menos isso não te torna nem um pouco genérico.")
        elif nome == "_jacket_":
            await ctx.send(f"Como anda esse pescoço aí, {apelido}? Muita dor? Ou já se esqueceu?")
        elif nome == "eudu0111":
            await ctx.send(f"Nosso ETERNO especialista, {apelido}! Corremos risco do canto gutural subito hoje?")
        elif nome == "_sabbadini_":
            await ctx.send(f"Não, {apelido}, a ocupação da mãe deles não tem nada a ver com o que tá rolando na tua partida.")
        elif nome == "t_pitchas":
            await ctx.send(f"{apelido}.. Esse é o tal bom de Hotline Miami? Me pergunto se essa habilidade afeta outra coisa..")
        elif nome == "cronebr":
            await ctx.send(f"{apelido}! Esse cara sabe muito! Fundador do Bradesco.. Eu vou lá de vez em quando.. O mal também precisa de grana!")
        else:
            await ctx.send(f"Salve, {apelido}! Tudo sinistro?")

async def setup(bot):
    await bot.add_cog(besteira(bot))