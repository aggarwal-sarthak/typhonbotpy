import discord
from discord.ext import commands
import os
import asyncio
import json
import logging
import sys

with open('config.json', 'r') as f:
    config = json.load(f)
with open('emoji.json', 'r') as f:
    emotes = json.load(f)

intents = discord.Intents.all()
intents.presences = False

client = commands.Bot(command_prefix=config['prefix'], intents=intents, help_command=None, case_insensitive=True,)
client.config = config
client.emotes = emotes

@client.command()
async def load(ctx,extension):
    await client.load_extension(f'cogs.{extension}')
    await ctx.reply(f"{client.emotes['success']} | Command {extension} Loaded Successfully!")

@client.command()
async def unload(ctx,extension):
    await client.unload_extension(f'cogs.{extension}')
    await ctx.reply(f"{client.emotes['success']} | Command {extension} Unloaded Successfully!")

@client.command()
async def reload(ctx,extension):
    await client.reload_extension(f'cogs.{extension}')
    await ctx.reply(f"{client.emotes['success']} | Command {extension} Reloaded Successfully!")

@client.event
async def on_ready():
    print(f'✅ | {client.user.name} Is Ready!')

async def load():
    for folder in os.listdir("./cogs"):
        for filename in os.listdir(f'./cogs/{folder}'):
            if filename.endswith(".py"):
                await client.load_extension(f"cogs.{folder}.{filename[:-3]}")

async def main():
    async with client:
        await load()
        await client.start(config['token'])

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.reply(f"{client.emotes['failed']} | Command On Cooldown `{error.retry_after:.2f}`s!")

    if isinstance(error, commands.MissingPermissions):
        err = str(error).replace('You are missing ','').replace(' permission(s) to run this command.','')
        await ctx.reply(f"{client.emotes['failed']} | You Don't Have `{err}` Permission To Use This Command!")

    if isinstance(error, commands.BotMissingPermissions):
        err = str(error).replace('Bot requires ','').replace(' permission(s) to run this command.', '')
        await ctx.reply(f"{client.emotes['failed']} | I Don't Have `{err}` Permission To Use This Command!")

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
asyncio.run(main())