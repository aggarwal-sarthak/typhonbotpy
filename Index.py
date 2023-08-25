import discord
from discord.ext import commands
import os
import asyncio
import json
import logging
import sys
from datetime import datetime
from pymongo import MongoClient
import time 
with open('config.json', 'r') as f:
    config = json.load(f)
with open('emoji.json', 'r') as f:
    emotes = json.load(f)

try:
    uri = "mongodb+srv://TyphonBotDB:sarthak13@typhonbotcluster.dxwct.mongodb.net/?retryWrites=true&w=majority"
    db_client = MongoClient(uri)

    db_client.admin.command('ping')
    print("✅ | Successfully Connected to MongoDB!")
except Exception as e:
    print(e)

intents = discord.Intents.all()
intents.presences = False
intents.voice_states = True

def get_prefix(client, ctx):
    guild_info = db_client.typhonbot.guilds.find_one({"guild_id":ctx.guild.id})
    # print("\n\n\n\n", guild_info['guild_id'])
    if(guild_info and 'prefix' in guild_info):
        return guild_info['prefix']
    else:
        return config['prefix']

client = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None, case_insensitive=True,)
client.config = config
client.emotes = emotes
client.db = db_client.typhonbot

@client.event
async def on_ready():
    print(f'✅ | {client.user.name} Is Ready!')

@client.event
async def on_command_error(ctx, error):
    print("\n\n\n\n\n\n",vars(error))
    if isinstance(error,commands.CommandInvokeError):
        if isinstance(error.original,asyncio.TimeoutError):
            await ctx.reply(f"{client.emotes['failed']} | Command Timed Out!")
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.invoke(client.get_command('help'), ctx.command.name)
    if isinstance(error, commands.CommandOnCooldown):
        now = datetime.now()
        now = datetime.timestamp(now)
        reply = await ctx.reply(f"{client.emotes['failed']} | Command On Cooldown! Try again <t:{int(now+error.retry_after)}:R> !")
        await asyncio.sleep(error.retry_after)
        await reply.delete()
    if isinstance(error, commands.MissingPermissions):
        err = str(error).replace('You are missing ','').replace(' permission(s) to run this command.','')
        await ctx.reply(f"{client.emotes['failed']} | You Don't Have `{err}` Permission To Use This Command!")

    if isinstance(error, commands.BotMissingPermissions):
        err = str(error).replace('Bot requires ','').replace(' permission(s) to run this command.', '')
        await ctx.reply(f"{client.emotes['failed']} | I Don't Have `{err}` Permission To Use This Command!")

@client.event
async def on_guild_join(guild):
    # client.db.guilds.insert_one({
    #     "guild_id":guild.id,
    #     "prefix":"",
    #     "cmds":[],
    # })

    members_count = sum(1 for _ in guild.members)

    invite_link = None
    if guild.me.guild_permissions.create_instant_invite:
        invite = await guild.text_channels[0].create_invite()
        invite_link = invite.url

    icon_url = guild.icon.replace(format="png") if guild.icon else None

    embed = discord.Embed(title="JOINED A SERVER", color=0xfb7c04)
    embed.add_field(name="SERVER NAME:", value=guild.name, inline=False)
    embed.add_field(name="SERVER ID:", value=guild.id, inline=False)
    embed.add_field(name="SERVER MEMBERS: ", value=members_count, inline=False)
    if invite_link: embed.add_field(name="INVITE LINK:", value=invite_link, inline=False)
    if icon_url: embed.set_thumbnail(url=icon_url)

    client_total_servers = len(client.guilds)
    client_total_members = sum(len(guild.members) for guild in client.guilds)
    embed.set_footer(text=f"BOT SERVERS: {client_total_servers} | BOT MEMBERS: {client_total_members}")

    target_channel = client.get_channel(client.config["join_logs"])
    if target_channel: await target_channel.send(embed=embed)

@client.event
async def on_guild_remove(guild):
    client.db.guilds.delete_one({"guild_id":guild.id})

    members_count = sum(1 for _ in guild.members)
    icon_url = guild.icon.replace(format="png") if guild.icon else None

    embed = discord.Embed(title="LEFT A SERVER", color=0xfb7c04)
    embed.add_field(name="SERVER NAME:", value=guild.name, inline=False)
    embed.add_field(name="SERVER ID:", value=guild.id, inline=False)
    embed.add_field(name="SERVER MEMBERS: ", value=members_count, inline=False)
    if icon_url: embed.set_thumbnail(url=icon_url)

    client_total_servers = len(client.guilds)
    client_total_members = sum(len(guild.members) for guild in client.guilds)
    embed.set_footer(text=f"BOT SERVERS: {client_total_servers} | BOT MEMBERS: {client_total_members}")

    target_channel = client.get_channel(client.config["leave_logs"])
    if target_channel: await target_channel.send(embed=embed)

async def load():
    for folder in os.listdir("./cogs"):
        for filename in os.listdir(f'./cogs/{folder}'):
            if filename.endswith(".py"):
                await client.load_extension(f"cogs.{folder}.{filename[:-3]}")

async def main():
    async with client:
        await load()
        await client.start(config['token'])

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
asyncio.run(main()) 