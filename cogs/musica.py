import discord
import asyncio
from discord.ext import commands
import yt_dlp

class musica(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

        self.fila = {}
        self.looping = {}
        self.voice_clients = {}
        self.musica_atual = {}
        self.skip_ativo = {}

    async def conectar(self, ctx:commands.Context):
        if ctx.author.voice:
            guild_id = ctx.guild.id
            self.fila.setdefault(guild_id, [])
            self.looping.setdefault(guild_id, False)
            self.musica_atual.setdefault(guild_id, None)
            self.skip_ativo.setdefault(guild_id, False)
            channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                voice = await channel.connect()
                self.voice_clients[guild_id] = voice
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

    async def tocar_proxima(self, guild_id):
        fila = self.fila.get(guild_id, [])
        voice = self.voice_clients.get(guild_id)
        if not voice:
            return
        
        if self.skip_ativo.get(guild_id):
            self.skip_ativo[guild_id] = False
            self.musica_atual[guild_id] = None

        if self.looping.get(guild_id) and self.musica_atual.get(guild_id):
            musica = self.musica_atual[guild_id]
        else:
            if not fila:
                self.musica_atual[guild_id] = None
                return
            musica = fila.pop(0)
            self.musica_atual[guild_id] = musica
        
        source = discord.FFmpegPCMAudio(
            musica["url"],
            before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            options="-vn"
        )

        self.voice_clients[guild_id].play(
            source,
            after=lambda e: asyncio.run_coroutine_threadsafe(
                    self.tocar_proxima(guild_id),
                    self.bot.loop
            )
        )
        #talvez implemente titulo, não realmente necessário
        #await ctx.send(f"Tocando agora: **{musica['titulo']}**")

    @commands.command()
    async def vem(self, ctx:commands.Context):
        await self.conectar(ctx)

    @commands.command()
    async def vaza(self, ctx:commands.Context):
        await self.desconectar(ctx)

    @commands.command()
    async def tocar(self, ctx:commands.Context, *, url):
        guild_id = ctx.guild.id

        conectado = await self.conectar(ctx)
        if not conectado:
            return

        audio_url, titulo = await self.pegar_audio(url)      

        self.fila[guild_id].append({
            "url": audio_url,
            "titulo": titulo
        })

        if not ctx.voice_client.is_playing():
            await self.tocar_proxima(guild_id)

    @commands.command()
    async def loop(self, ctx:commands.Context):
        guild_id = ctx.guild.id

        self.looping.setdefault(guild_id, False)

        if self.looping[guild_id] == False:
            self.looping[guild_id] = True
            await ctx.send("Vamos repetir essa aí então!")

        elif self.looping[guild_id] == True:
            self.looping[guild_id] = False
            await ctx.send("Já deu de repeteco!")

    @commands.command()
    async def para(self, ctx:commands.Context):
        if not ctx.voice_client:
            await ctx.send("Nem to tocando, parça!")
            return

        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Parei! Parei!")

        elif ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("E vamo de novo!")

        else:
            await ctx.send("Nem to tocando, parça!")

    @commands.command()
    async def next(self, ctx:commands.Context):
        guild_id = ctx.guild.id
        if not ctx.voice_client:
            await ctx.send("Nem to tocando, parça!")
            return
        if ctx.voice_client.is_playing():
            self.skip_ativo[guild_id] = True
            ctx.voice_client.stop()
        else:
            await ctx.send("Nem to tocando, parça!")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot:
            return

        if before.channel is not None and after.channel is None:
            guild_id = member.guild.id

            self.fila.pop(guild_id, [])
            self.musica_atual.pop(guild_id, None)
            self.looping.pop(guild_id, False)
            self.voice_clients.pop(guild_id, None)
            self.skip_ativo.pop(guild_id, False)

async def setup(bot):
    await bot.add_cog(musica(bot))