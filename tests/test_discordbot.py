import logging
import os

import discord
import discord.ext
from discord import Member, Message, Role, TextChannel
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

    @bot.command()
    async def buddy(ctx, mbr: Member) -> None:
        buddyRole: Role = bot.getRole(ctx, "Buddies")
        generalChannel: TextChannel = bot.getChannel("general")

        await mbr.add_roles(buddyRole)
        await generalChannel.send(f"Welcome, {mbr.name}!")

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
