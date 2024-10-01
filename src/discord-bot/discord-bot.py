import discord
from typing import Callable, Self
import logging


class DiscordBot(discord.Client):
    def __init__(self) -> Self:
        self.messageHandlers: list[Callable] = []

    def addMessageHandler(self, handler: Callable) -> bool:
        """Adds given message handler to handlers."""
        added: bool = False

        if handler not in self.messageHandlers:
            self.messageHandlers.append(handler)
            added = True

        return added

    def removeMessageHandler(self, handler: Callable) -> bool:
        """Attempts to remove given handler from handlers."""
        removed: bool = False

        if handler in self.messageHandlers:
            self.messageHandlers.remove(handler)
            removed = True

        return removed

    def on_message(self, message):
        """Handler broker for messages."""

        for handler in self.messageHandlers:
            # We cannot be sure that the user's code will not have exceptions.
            # Need to log this information well so that it is easier to research
            # while also trying to make sure the Discord bot does not go down.
            try:
                handler(message)
            except Exception as ex:
                logging.error("An error occurred while running given handler: " + ex)
