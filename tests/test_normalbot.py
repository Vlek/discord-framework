import discord
from discord.ext import commands
import os

TOKEN = os.getenv("DISCORD_TOKEN") or ""

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)


@bot.command()
async def ping(ctx):
    await ctx.reply("pong")


bot.run(TOKEN)
