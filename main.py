import discord
from discord.ext import commands
import os

intents = discord.Intents.all()
bot = commands.Bot("$", intents=intents)

async def carregar_cogs():
    for arquivo in os.listdir('cogs'):
        if arquivo.endswith('.py'):
            await bot.load_extension(f"cogs.{arquivo[:-3]}")

@bot.event
async def on_ready():
    await carregar_cogs()
    print("O pai tá ON!")


with open('token.txt', 'r') as file:
    token = file.readlines()[0]
bot.run(token)
