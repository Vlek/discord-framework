import logging
from typing import Callable

import discord
from discord import Guild, Intents, Message, RawReactionActionEvent, Role
from discord.abc import GuildChannel
from discord.ext.commands import Bot


class DiscordBot(Bot):
    def __init__(self, intents=None, command_prefix="$") -> None:
        self.messageHandlers: list[Callable] = []
        self.messageDeletedHandlers: list[Callable] = []
        self.memberJoinHandlers: list[Callable] = []
        self.roleAddedHandlers: list[Callable] = []
        self.userBannedHandlers: list[Callable] = []
        self.emojiAddHandlers: list[Callable] = []
        self.emojiRemoveHandlers: list[Callable] = []
        self.onReadyHandlers: list[Callable] = []

        self.cooldowns: dict[str, int] = {}

        if not intents:
            intents = Intents.default()
            intents.message_content = True

        self.log = logging.getLogger("discord")

        super().__init__(command_prefix=command_prefix, intents=intents)

    def addOnReadyHandler(self, handler: Callable) -> bool:
        """Adds given on_ready handler to handlers."""
        added: bool = False

        if handler not in self.onReadyHandlers:
            self.onReadyHandlers.append(handler)
            added = True

        return added

    def onReadyHandler(self) -> Callable:
        def decorator(handler: Callable) -> None:
            self.addOnReadyHandler(handler)

        return decorator

    async def on_ready(self) -> None:
        """Handler broker for registered on_ready handlers."""
        for handler in self.onReadyHandlers:
            try:
                await handler()
            except Exception:
                logging.exception("")

    def addMessageHandler(self, handler: Callable) -> bool:
        """Adds given message handler to handlers."""
        added: bool = False

        if handler not in self.messageHandlers:
            self.messageHandlers.append(handler)
            added = True

        return added

    def messageHandler(self, cooldown: int = 0) -> Callable:
        def decorator(handler: Callable) -> None:
            self.addMessageHandler(handler)

            if cooldown:
                self.cooldowns[handler.__name__] = cooldown

        return decorator

    def removeMessageHandler(self, handler: Callable) -> bool:
        """Attempts to remove given handler from handlers."""
        removed: bool = False

        if handler in self.messageHandlers:
            self.messageHandlers.remove(handler)
            removed = True

        return removed

    async def on_message(self, message):
        """Handler broker for messages."""

        # Ignore messages coming from the bot itself
        if message.author == self.user:
            return

        for handler in self.messageHandlers:
            # We cannot be sure that the user's code will not have exceptions.
            # Need to log this information well so that it is easier to research
            # while also trying to make sure the Discord bot does not go down.
            try:
                await handler(message)
            except Exception:
                # This _should_ take care of logging the traceback correctly.
                logging.exception("")

        await self.process_commands(message)

    def addMemberJoinHandler(self, handler: Callable) -> bool:
        """Adds given member join handler to handlers."""
        added: bool = False

        if handler not in self.memberJoinHandlers:
            self.memberJoinHandlers.append(handler)
            added = True

        return added

    def removeMemberJoinHandler(self, handler: Callable) -> bool:
        """Removes given handler from member join handlers."""
        removed: bool = False

        if handler in self.memberJoinHandlers:
            self.memberJoinHandlers.remove(handler)
            removed = True

        return removed

    async def on_member_join(self, member) -> None:
        """Handler broker for member joins."""
        for handler in self.memberJoinHandlers:
            try:
                await handler(member)
            except Exception:
                logging.exception("")

    def memberJoinHandler(self) -> Callable:
        def decorator(handler: Callable) -> None:
            self.addMemberJoinHandler(handler)

        return decorator

    def addMemberBannedHandler(self, handler: Callable) -> bool:
        """Adds given member banned handler to handlers."""
        added: bool = False

        if handler not in self.userBannedHandlers:
            self.userBannedHandlers.append(handler)
            added = True

        return added

    def removeMemberBannedHandler(self, handler: Callable) -> bool:
        """Removed given member banned handler from handlers."""
        removed: bool = False

        if handler in self.userBannedHandlers:
            self.userBannedHandlers.remove(handler)
            removed = True

        return removed

    async def on_member_ban(self, member) -> None:
        """Handler broker for member banned."""
        for handler in self.userBannedHandlers:
            try:
                await handler(member)
            except Exception:
                logging.exception("")

    def memberBannedHandler(self) -> Callable:
        def decorator(handler: Callable) -> None:
            self.addMemberBannedHandler(handler)

        return decorator

    def addEmojiAddHandler(self, handler) -> bool:
        """Adds given emoji add handler to handlers."""
        added: bool = False

        if handler not in self.emojiAddHandlers:
            self.emojiAddHandlers.append(handler)
            added = True

        return added

    def removeEmojiAddHandler(self, handler) -> bool:
        """Removes given emoji add handler from handlers."""
        removed: bool = False

        if handler in self.emojiAddHandlers:
            self.emojiAddHandlers.remove(handler)
            removed = True

        return removed

    async def on_raw_reaction_add(self, payload: RawReactionActionEvent) -> None:
        for handler in self.emojiAddHandlers:
            try:
                await handler(payload)
            except Exception:
                logging.exception("")

    def emojiAddHandler(self) -> Callable:
        def decorator(handler: Callable) -> None:
            self.addEmojiAddHandler(handler)

        return decorator

    def addMessageDeletedHandler(self, handler) -> bool:
        """Adds a message delete handler to handlers."""
        added: bool = False

        if handler not in self.messageDeletedHandlers:
            self.messageDeletedHandlers.append(handler)
            added = True

        return added

    def removeMessageDeletedHandler(self, handler) -> bool:
        """Removes a message deleted handler from handlers."""
        removed: bool = False

        if handler in self.messageDeletedHandlers:
            self.messageDeletedHandlers.remove(handler)
            removed = True

        return removed

    async def on_message_delete(self, message: Message) -> None:
        """On message delete handler broker"""
        for handler in self.messageDeletedHandlers:
            try:
                await handler(message)
            except Exception:
                logging.exception("")

    def messageDeletedHandler(self) -> Callable:
        def decorator(handler: Callable) -> None:
            self.addMessageDeletedHandler(handler)

        return decorator

    def addEmojiRemoveHandler(self, handler) -> bool:
        """Adds an emoji remove handler to handlers."""
        added: bool = False

        if handler not in self.emojiRemoveHandlers:
            self.emojiRemoveHandlers.append(handler)

        return added

    def removeEmojiRemoveHandler(self, handler) -> bool:
        """Removes an emoji remove handler from handlers."""
        removed: bool = False

        if handler in self.emojiRemoveHandlers:
            self.emojiRemoveHandlers.remove(handler)
            removed = True

        return removed

    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent) -> None:
        for handler in self.emojiRemoveHandlers:
            try:
                await handler(payload)
            except Exception:
                logging.exception("")

    def emojiRemoveHandler(self) -> Callable:
        def decorator(handler: Callable) -> None:
            self.addEmojiRemoveHandler(handler)

        return decorator

    def getChannel(self, channelName: str) -> GuildChannel | None:
        channel: GuildChannel | None = discord.utils.get(
            self.get_all_channels(), name=channelName
        )

        return channel

    def getRole(self, guild: Guild, roleName: str) -> Role | None:
        role: Role | None = discord.utils.get(guild.roles, name=roleName)

        return role
