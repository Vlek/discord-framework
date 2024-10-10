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

    @bot.messageHandler(cooldown=5)
    async def logAllMessages(message: discord.Message):
        logger.info(f"{message.author.display_name}: {message.content}")
        await message.reply(message.content)

    @bot.memberJoinHandler()
    async def welcomeNewMember(mbr: discord.Member) -> None:
        logger.info(f"New member joined! {mbr.nick}")
        channel: discord.Channel = bot.get_channel(1291233677547933801)
        await channel.send(f"Welcome, {mbr.nick}!")

    bot.run(TOKEN)


if __name__ == "__main__":
    test_discordbot()
