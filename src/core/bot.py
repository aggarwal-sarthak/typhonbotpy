import os
import logging
import sys
import discord
from discord.ext import commands
from pymongo import MongoClient
from src.core.constants import Constants
from src.core.secrets import Env
from src.core.events import EventHandler

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class Tether(Env):
    def __init__(self):
        super().__init__()
        intents = discord.Intents.default()
        intents.guilds = True
        intents.messages = True
        intents.message_content = True
        intents.members = True
        self.client = commands.AutoShardedBot(
            command_prefix=self.get_prefix,
            intents=intents,
            help_command=None,
            case_insensitive=True,
        )
        self.constants = Constants()
        self.db = MongoClient(self.mongo_uri).typhonbot

        self.event_handler = EventHandler(self)

    def get_prefix(self, bot, message):
        if message.content.startswith(self.client.user.mention + " "):
            return [f"{self.client.user.mention} "]
        elif message.content.startswith(self.client.user.mention):
            return [f"{self.client.user.mention}"]

        guild_info = self.db.guilds.find_one({"guild_id": message.guild.id})
        return (
            guild_info["prefix"]
            if guild_info and "prefix" in guild_info
            else self.prefix
        )

    async def load_cogs(self):
        for folder in os.listdir("./src/cogs"):
            for filename in os.listdir(f"./src/cogs/{folder}"):
                if filename.endswith(".py"):
                    cog_name = f"src.cogs.{folder}.{filename[:-3]}"
                    try:
                        await self.client.load_extension(cog_name)
                        logging.info(
                            f"{self.constants.success_emoji} {filename[:-3]} Is Loaded!"
                        )
                    except Exception as e:
                        logging.error(
                            f"{self.constants.error_emoji} Failed To Load {cog_name}: {e}"
                        )

    async def run(self, token):
        await self.load_cogs()
        await self.client.start(token)


tether = Tether()
