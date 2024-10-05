import logging
import os

import discord
import discord.ext

from discord_framework import DiscordBot


def test_discordbot():
    bot = DiscordBot()
    logger = logging.getLogger("discord")
    TOKEN = os.getenv("DISCORD_TOKEN") or ""

    @bot.command()
    async def ping(ctx: discord.abc.Messageable):
        logger.info("sending pong response to command")
        await ctx.send("pong")

    @bot.messageHandler
    async def logAllMessages(message: discord.Message):
        logger.info(f"{message.author.display_name}: {message.content}")
        await message.reply(message.content)

    bot.run(TOKEN)
