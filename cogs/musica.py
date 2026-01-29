import discord
import asyncio
from discord.ext import commands
import yt_dlp

class musica(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    async def conectar(self, ctx:commands.Context):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await channel.connect()
                return True
            else: 
                await ctx.voice_client.move_to(channel)
                return True
        else:
            await ctx.send("Quer que eu toque sem estar na plateia? Não vai rolar.")
            return False

    async def desconectar(self, ctx:commands.Context):
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

    def extrair_audio(self, url):
        #Fazendo o cliente ser android pra não forçar a execução de JS
        YTDLP_OPTS = {
            "format": "bestaudio[ext=m4a]/bestaudio/best",
            "quiet": True,
            "noplaylist": True,
            "extractor_args": {
                "youtube": {
                    "player_client": ["android"]
                }
            }
        }

        with yt_dlp.YoutubeDL(YTDLP_OPTS) as ydl:
            info = ydl.extract_info(url, download=False)
            return info["url"], info.get("title", "Titulo Desconhecido")

    async def pegar_audio(self, url):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.extrair_audio, url)

    @commands.command()
    async def vem(self, ctx:commands.Context):
        await self.conectar(ctx)

    @commands.command()
    async def vaza(self, ctx:commands.Context):
        await self.desconectar(ctx)

    @commands.command()
    async def tocar(self, ctx:commands.Context, *, url):
        conectado = await self.conectar(ctx)
        if not conectado:
            return
        
        audio_url, titulo = await self.pegar_audio(url)
        
        #Temporario enquanto não implemento fila
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        source = discord.FFmpegPCMAudio(
            audio_url,
            before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            options="-vn"
        )

        ctx.voice_client.play(source)

        await ctx.send(f"Tocando agora: **{titulo}**")

async def setup(bot):
    await bot.add_cog(musica(bot))