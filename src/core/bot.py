import discord
from discord.ext import commands
import logging
import sys
import logging
from src.core.secrets import Env

intents = discord.Intents.all()
intents.presences = False
intents.voice_states = True

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

class Tether(Env):
    def __init__(self) -> None:
        super().__init__()
        self.client = commands.AutoShardedBot(command_prefix=";", intents=intents, help_command=None, case_insensitive=True)

    @commands.Cog.listener()
    async def on_ready(self):
        logs_channel = self.client.get_channel(tether.bot_logs)
        if logs_channel:
            await logs_channel.send(f'```✅ | Bot Started!```')
        print(f'✅ | {self.client.user.name} Is Ready!')

    async def run(self, token):
        async with self.client:
            await self.client.start(token)




# from datetime import datetime
# from src.core.validation import db_client
# import src.core.confirmation
# with open('config.json', 'r') as f:
#     config = json.load(f)
# with open('emoji.json', 'r') as f:
#     emotes = json.load(f)

    # def get_prefix(self, ctx):
    #     if ctx.content.startswith(self.client.user.mention + ' '): return f'{self.client.user.mention} '
    #     elif ctx.content.startswith(self.client.user.mention): return f'{self.client.user.mention}'
    #     guild_info = db_client.typhonbot.guilds.find_one({"guild_id":ctx.guild.id})
    #     if(guild_info and 'prefix' in guild_info):
    #         return guild_info['prefix']
    #     else:
    #         return config['prefix']
        
    # async def load(self,client):
    #     for folder in os.listdir("./src/cogs"):
    #         for filename in os.listdir(f'./src/cogs/{folder}'):
    #             if filename.endswith(".py"):
    #                 await client.load_extension(f"src.cogs.{folder}.{filename[:-3]}")
    #                 print(f"✅ | {filename[:-3]} Is Loaded!")

# client = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None, case_insensitive=True,)
# client.config = config
# client.emotes = emotes
# client.db = db_client.typhonbot

# @client.event
# async def on_ready():
#     logs_channel = client.get_channel(client.config["bot_logs"])
#     if logs_channel:
#         await logs_channel.send(f'```✅ | Bot Started!```')
#     print(f'✅ | {client.user.name} Is Ready!')

# @client.event
# async def on_command(ctx):
#     if not ctx.author.guild_permissions.administrator: return
#     guild_db = client.db.guilds.find_one({"guild_id":ctx.guild.id})

#     if not guild_db:
#         client.db.guilds.insert_one({"guild_id":ctx.guild.id, "updated":False})

#     if 'updated' not in guild_db:
#         guild_db["updated"] = False
        
#     if guild_db['updated'] == False:
#         client.db.guilds.update_one({"guild_id":ctx.guild.id},{"$set":{"updated":True}})
#         view = confirmation.Buttons(ctx)
#         msg = await ctx.send(f"{emotes['bot']} | A New Mail has arrived. Click To Read!",view=view,ephemeral=True)
#         await view.wait()
        
#         try:
#             if view.value == '1':
#                 if msg: await msg.delete()
#                 embed = discord.Embed.from_dict(client.db.updatelog.find_one({}))
#                 await ctx.send(embed=embed)
#                 target_channel = client.get_channel(config["update_channel"])
#                 if target_channel: await target_channel.send(f"```{ctx.author.name} - {ctx.author.id} in {ctx.guild.name} - {ctx.guild.id}```")
                
#             elif view.value == '2':
#                 if msg: await msg.delete()
#         except:
#             disable = confirmation.Disabled(ctx)
#             return await msg.edit(content=f"{emotes['bot']} | A New Mail has arrived. Run any command read the Mail!", view=disable)
                
# @client.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound): return
    
#     if not isinstance(error, commands.CommandOnCooldown):
#         ctx.command.reset_cooldown(ctx)

#     if isinstance(error,commands.CommandInvokeError):
#         if isinstance(error.original,asyncio.TimeoutError):
#             return await ctx.reply(f"{client.emotes['failed']} | Command Timed Out!")

#     if isinstance(error, commands.MissingRequiredArgument):
#         if ctx.command.parent is None:
#             return await ctx.invoke(client.get_command('help'), ctx.command.name)
#         else:
#             return await ctx.invoke(client.get_command('help'),ctx.command.parent.name, ctx.command.name)

#     if isinstance(error, commands.CommandOnCooldown):
#         now = datetime.now()
#         now = datetime.timestamp(now)
#         reply = await ctx.reply(f"{client.emotes['failed']} | Command On Cooldown! Try again <t:{int(now+error.retry_after)}:R> !")
#         await asyncio.sleep(error.retry_after)
#         if reply: return await reply.delete()

#     if isinstance(error, commands.MissingPermissions):
#         err = str(error).replace('You are missing ','').replace(' permission(s) to run this command.','')
#         return await ctx.reply(f"{client.emotes['failed']} | You Don't Have `{err}` Permission To Use This Command!")

#     if isinstance(error, commands.BotMissingPermissions):
#         err = str(error).replace('Bot requires ','').replace(' permission(s) to run this command.', '')
#         return await ctx.reply(f"{client.emotes['failed']} | I Don't Have `{err}` Permission To Use This Command!")
    
#     target_channel = client.get_channel(client.config["error_logs"])
#     if target_channel: await target_channel.send(f'```{ctx.command.name} : {error}```')

# @client.event
# async def on_guild_join(guild):
#     members_count = sum(1 for _ in guild.members)

#     invite_link = None
#     if guild.me.guild_permissions.create_instant_invite:
#         invite = await guild.text_channels[0].create_invite()
#         invite_link = invite.url

#     icon_url = guild.icon.replace(format="png") if guild.icon else None

#     embed = discord.Embed(title="JOINED A SERVER", color=0xfb7c04)
#     embed.add_field(name="SERVER NAME:", value=guild.name, inline=False)
#     embed.add_field(name="SERVER ID:", value=guild.id, inline=False)
#     embed.add_field(name="SERVER MEMBERS: ", value=members_count, inline=False)
#     if invite_link: embed.add_field(name="INVITE LINK:", value=invite_link, inline=False)
#     if icon_url: embed.set_thumbnail(url=icon_url)

#     client_total_servers = len(client.guilds)
#     client_total_members = sum(len(guild.members) for guild in client.guilds)
#     embed.set_footer(text=f"BOT SERVERS: {client_total_servers} | BOT MEMBERS: {client_total_members}")

#     target_channel = client.get_channel(client.config["join_logs"])
#     if target_channel: await target_channel.send(embed=embed)

# @client.event
# async def on_guild_remove(guild):
#     client.db.guilds.delete_one({"guild_id":guild.id})

#     members_count = sum(1 for _ in guild.members)
#     icon_url = guild.icon.replace(format="png") if guild.icon else None

#     embed = discord.Embed(title="LEFT A SERVER", color=0xfb7c04)
#     embed.add_field(name="SERVER NAME:", value=guild.name, inline=False)
#     embed.add_field(name="SERVER ID:", value=guild.id, inline=False)
#     embed.add_field(name="SERVER MEMBERS: ", value=members_count, inline=False)
#     if icon_url: embed.set_thumbnail(url=icon_url)

#     client_total_servers = len(client.guilds)
#     client_total_members = sum(len(guild.members) for guild in client.guilds)
#     embed.set_footer(text=f"BOT SERVERS: {client_total_servers} | BOT MEMBERS: {client_total_members}")

#     target_channel = client.get_channel(client.config["leave_logs"])
#     if target_channel: await target_channel.send(embed=embed)

# async def load():
#     for folder in os.listdir("./cogs"):
#         for filename in os.listdir(f'./cogs/{folder}'):
#             if filename.endswith(".py"):
#                 await client.load_extension(f"cogs.{folder}.{filename[:-3]}")
#                 print(f"✅ | {filename[:-3]} Is Loaded!")

# async def main():
#     async with client:
#         await load()
#         await client.start(config['token'])

# asyncio.run(main()) 

tether = Tether()