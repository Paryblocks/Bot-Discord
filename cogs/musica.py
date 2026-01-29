import discord
from discord.ext import commands

class musica(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @commands.command()
    async def vem(self, ctx:commands.Context):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await channel.connect()
            else: 
                await ctx.voice_client.move_to(channel)
        else:
            await ctx.send("Quer que eu toque sem estar na plateia? Não vai rolar.")

    @commands.command()
    async def vaza(self, ctx:commands.Context):
        if ctx.voice_client is None:
            await ctx.send("SAIR DA ONDE, MANÉ?!?")
        elif ctx.author.voice:
            if ctx.author.voice.channel == ctx.voice_client.channel:
                await ctx.voice_client.disconnect()
                await ctx.send("Valeu galera, fui!")
            else:
                await ctx.send("O show só acaba quando a plateia quiser, não vá estragar o show dos outros!")
        else:
            await ctx.send("O show só acaba quando a plateia quiser, não vá estragar o show dos outros!")

    @commands.command()
    async def tocar(self, ctx:commands.Context, musica):
        await ctx.send(musica)

async def setup(bot):
    await bot.add_cog(musica(bot))