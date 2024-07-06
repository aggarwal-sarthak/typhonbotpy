import discord
from discord.ext import commands
import os
import datetime
from src.core.validation import is_command_enabled

class info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        global start_time
        start_time = datetime.datetime.now()

    @commands.command(description='Returns Information About Bot', aliases=['botinfo'], usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.bot_has_permissions(embed_links=True)
    @commands.check(is_command_enabled)
    async def info(self, ctx):
        embed = discord.Embed(title=f'{self.client.user.name}',color=self.client.config['color'])
        embed.add_field(name="Discord.py",value=discord.__version__,inline=False)
        embed.add_field(name="Owner",value=f"[{await self.client.fetch_user(self.client.config['owner'][0])}](https://discord.com/users/{self.client.config['owner'][0]}) [<@!{self.client.config['owner'][0]}>]\n[{await self.client.fetch_user(self.client.config['owner'][1])}](https://discord.com/users/{self.client.config['owner'][1]}) [<@!{self.client.config['owner'][1]}>]",inline=False)
        embed.add_field(name="Total Servers",value=len(self.client.guilds),inline=False)
        embed.add_field(name="Total Users",value=sum(len(guild.members) for guild in self.client.guilds),inline=False)
        td = datetime.datetime.now() - start_time
        days = td.days
        hours, remainder = divmod(td.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime = f"{days}d {hours}hr {minutes}min {seconds}sec"
        embed.add_field(name="Uptime",value=str(uptime),inline=False)
        embed.add_field(name="",value=f"[Invite Me](https://discord.com/api/oauth2/authorize?client_id=756052319417925633&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.com%2Finvite%2F5UqVvZj&response_type=code&scope=bot%20guilds.join%20applications.commands) **|** [Support Server](https://discord.com/invite/5UqVvZj) **|** [Vote Me](https://top.gg/bot/756052319417925633/vote)",inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
        await ctx.reply(embed=embed)

async def setup(client):
    await client.add_cog(info(client))