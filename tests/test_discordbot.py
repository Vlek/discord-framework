import logging
import os

import discord
import discord.ext
from discord import Message, TextChannel
from discord.ext import commands

from discord_framework import DiscordBot


def test_discordbot():
    bot = DiscordBot()
    logger = logging.getLogger("discord")
    TOKEN = os.getenv("DISCORD_TOKEN") or ""

    @bot.command()
    async def ping(ctx: discord.abc.Messageable):
        logger.info("sending pong response to command")
        await ctx.send("pong")

    @bot.command()
    @commands.has_role("mod")
    async def poop(ctx):
        logger.info("mod only command called")
        await ctx.send("💩")

    @bot.messageHandler(cooldown=5)
    async def logAllMessages(message: discord.Message):
        logger.info(f"{message.author.display_name}: {message.content}")
        await message.reply(message.content)

    @bot.memberJoinHandler()
    async def welcomeNewMember(mbr: discord.Member) -> None:
        logger.info(f"New member joined! {mbr.nick}")
        channel: discord.Channel = bot.get_channel(1291233677547933801)
        await channel.send(f"Welcome, {mbr.nick}!")

    @bot.messageDeletedHandler()
    async def logDeletedMessage(msg: Message) -> None:
        logger.info("User attempted to delete a message!")
        await msg.channel.send(f"{msg.author.nick} tried to do a dirty delete!")

        deleteChannel: TextChannel = bot.getChannel("deleted-shit")

        await deleteChannel.send(f"{msg.author.name}: {msg.content}")

    bot.run(TOKEN)


if __name__ == "__main__":
    test_discordbot()
