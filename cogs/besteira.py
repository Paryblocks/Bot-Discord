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
            await ctx.send(f"{apelido}?!? Ouvi dizer que você é o monstro.. mas você não é um monstro TENEBROSO!")
        #elif nome == "raelvd":
            #await ctx.send(f"Opa, {apelido}! WIP")
        #elif nome == "_jacket_":
            #await ctx.send(f"WIP, {apelido}!")
        #elif nome == "eudu0111":
            #await ctx.send(f"WIP, {apelido}!")
        #elif nome == "_sabbadini_":
            #await ctx.send(f"WIP, {apelido}!")
        #elif nome == "t_pitchas":
            #await ctx.send(f"WIP, {apelido}!")
        elif nome == "cronebr":
            await ctx.send(f"{apelido}! Esse cara sabe muito! Fundador do Bradesco.. Eu vou lá de vez em quando.. O mal também precisa de grana!")
        else:
            await ctx.send(f"Salve, {apelido}! Tudo sinistro?")

async def setup(bot):
    await bot.add_cog(besteira(bot))