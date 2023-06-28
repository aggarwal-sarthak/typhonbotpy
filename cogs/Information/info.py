import discord
from discord.ext import commands
import os
import datetime

class info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")
        global start_time
        start_time = datetime.datetime.now()

    @commands.bot_has_permissions(embed_links=True)
    @commands.command(description='Returns The Information About Bot', aliases=['botinfo'], usage=f"{os.path.basename(__file__)[:-3]}")
    async def info(self, ctx):
        embedVar = discord.Embed(title="TYPHON BOT",color=0xfb7c04)
        embedVar.set_thumbnail(url=self.client.user.avatar)
        embedVar.add_field(name="Bot Version",value="BETA",inline=False)
        embedVar.add_field(name="Discord.py",value=discord.__version__,inline=False)
        embedVar.add_field(name="Owner",value=f"[{await self.client.fetch_user(self.client.config['owner'][0])}](https://discord.com/users/{self.client.config['owner'][0]})[<@!{self.client.config['owner'][0]}>]\n[{await self.client.fetch_user(self.client.config['owner'][1])}](https://discord.com/users/{self.client.config['owner'][1]})[<@!{self.client.config['owner'][1]}>]",inline=False)
        embedVar.add_field(name="Total Servers",value=len(self.client.guilds))
        # users = 0
        # for guild in self.client.guilds:
        #     users += guild.members
        # embedVar.add_field(name="Total Users",value=sum(guild.member_count for guild in self.client.guilds),inline=False)
        td = datetime.datetime.now() - start_time
        days = td.days
        hours, remainder = divmod(td.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime = f"{days}d {hours}hr {minutes}min {seconds}sec"
        embedVar.add_field(name="Uptime",value=str(uptime),inline=False)
        embedVar.add_field(name="Support Server",value="[Support Server](https://discord.gg/5UqVvZj)",inline=False)
        embedVar.add_field(name="Invite Bot",value="[Invite](https://discord.com/api/oauth2/authorize?client_id=756052319417925633&permissions=2113268958&redirect_uri=https%3A%2F%2Fdiscord.com%2Finvite%2F5UqVvZj&response_type=code&scope=bot%20guilds.join%20applications.commands)",inline=False)
        embedVar.add_field(name="Vote Us",value="[Vote](https://top.gg/bot/756052319417925633/vote)",inline=False)
        
        await ctx.reply(embed=embedVar)

    @info.error
    async def missing_permissions(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            err = str(error).replace('Bot requires ','').replace(' permission(s) to run this command.', '')
            await ctx.reply(f"{self.client.emotes['failed']} | I Don't Have `{err}` Permission To Use This Command!")

async def setup(client):
    await client.add_cog(info(client))