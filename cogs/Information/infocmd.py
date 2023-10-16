import discord
from discord.ext import commands
import os 
from validation import is_command_enabled
import datetime 

class infocmd(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description='Returns Help Menu For The Bot Commands', usage=f"{os.path.basename(__file__)[:-3]} [command]")
    @commands.check(is_command_enabled)
    @commands.bot_has_permissions(embed_links=True)
    async def help(self,ctx,*arg):
        res = self.client.db.guilds.find_one({"guild_id": ctx.guild.id})
        if res and "prefix" in res:
            prefix = res['prefix']
        else:
            prefix = self.client.config['prefix']

        if not arg:
            embed = discord.Embed(color=self.client.config['color'])
            embed.add_field(name="",value=f"[Invite Me](https://discord.com/api/oauth2/authorize?client_id=756052319417925633&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.com%2Finvite%2F5UqVvZj&response_type=code&scope=bot%20guilds.join%20applications.commands) **|** [Support Server](https://discord.com/invite/5UqVvZj) **|** [Vote Me](https://top.gg/bot/756052319417925633/vote)",inline=False)
            for folder in os.listdir('./cogs'):
                if(ctx.author.id not in self.client.config['owner'] and folder == "Developer"): continue
                embed.add_field(name=f"{folder}",value=f"`{'`, `'.join([filename[:-3] for filename in os.listdir(f'./cogs/{folder}') if filename.endswith('.py')])}`",inline=False)
            embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
            return await ctx.reply(embed=embed)
            
        if(len(arg)>0):
            cmd = self.client.get_command(arg[0].lower())
            if cmd is None:
                return await ctx.reply(f"{self.client.emotes['failed']} | Command not Found!")
        if(len(arg)>1 and isinstance(cmd,commands.Group)):
            subcmd = cmd.get_command(arg[1].lower())
            if(subcmd is not None):
                cmd = subcmd
        if(len(arg)>2 and isinstance(cmd,commands.Group)):
            subcmd = cmd.get_command(arg[2].lower())
            if(subcmd is not None):
                cmd = subcmd

        desc = f'**Description:** `{cmd.description if cmd.description else "None"}`\n**Usage:** `{cmd.usage if cmd.usage else "None"}`\n**Aliases:** `{"`, `".join([c for c in cmd.aliases]) if cmd.aliases else "None"}`\n**Cooldown:** `{str(int(cmd.cooldown.per))+"s" if cmd.cooldown is not None else "None"}`'
        if isinstance(cmd, commands.Group):
            subs= ''
            for name in cmd.commands:
                subs += f'`{prefix}{name}`\n'
            desc += f'\n\n**Subcommands:**\n{subs}'
        embed = discord.Embed(title=f"Command: {cmd.name}",color=self.client.config['color'], description=desc)
        await ctx.reply(embed=embed)

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

    @commands.command(description='Returns Bot Ping', usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.check(is_command_enabled)
    async def ping(self, ctx):
        latency = self.client.latency
        await ctx.reply(f'{self.client.emotes["success"]} | {round(latency * 1000)}ms!')   

async def setup(client):
    await client.add_cog(infocmd(client))