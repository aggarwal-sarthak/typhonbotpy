import discord
from discord.ext import commands
import os 
from validation import is_command_enabled

class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.command(description='Returns Help Menu For The Bot Commands', usage=f"{os.path.basename(__file__)[:-3]} [command]")
    @commands.check(is_command_enabled)
    @commands.bot_has_permissions(embed_links=True)
    async def help(self,ctx,*arg):
        res = self.client.db.guilds.find_one({"guild_id": ctx.guild.id})
        if res and "prefix" in res:
            prefix = res['prefix']
        else:
            prefix = self.client.config['prefix']
        if(len(arg)):
            cmd = self.client.get_command(arg[0].lower())
            if cmd is None: return
            if(len(arg)>1):
                subcmd = cmd.get_command(arg[1].lower())
                if(subcmd is not None):
                    cmd = subcmd
            menu = discord.Embed(title="Command Details",color=0xfb7c04, description=f"```- [] = Optional Arguments\n- <> = Required Arguments\n- Do Not Type These When Using Commands!```\n> {cmd.description}")
            if (cmd.aliases):
                aliases = '`, `'.join([c for c in cmd.aliases])
            else:
                aliases = "None"
            menu.add_field(name="Aliases", value=f"`{aliases}`")
            if(cmd.usage):
                usage = (prefix+cmd.usage).replace('\n',f'\n{prefix}')
                menu.add_field(name="Usage", value=f'`{usage}`',inline=False)
            if isinstance(cmd,commands.Group):
                menu.add_field(name="Subcommands", value=f'`{", ".join([c.name for c in cmd.commands])}`',inline=False)
            menu.add_field(name="Cooldown", value=f'`{str(int(cmd.cooldown.per))+"s" if cmd.cooldown is not None else "No Cooldown!"}`',inline=False)
            await ctx.reply(embed=menu)
        else:
            embed = discord.Embed(title="TYPHON BOT Commands",color=0xfb7c04)
            embed.add_field(name="",value=f"{self.client.emotes['success']} : Prefix For This Server : `{prefix}`\n\
                            {self.client.emotes['success']} : Total Bot Commands : `{len(self.client.commands)}`\n\
                            {self.client.emotes['success']} : Type {prefix}help <command> For More Info\n\
                            [Invite Typhon Bot](https://discord.com/api/oauth2/authorize?client_id=756052319417925633&permissions=2113268958&redirect_uri=https%3A%2F%2Fdiscord.com%2Finvite%2F5UqVvZj&response_type=code&scope=bot%20guilds.join%20applications.commands)\
                             | [Support Server](https://discord.com/invite/5UqVvZj)\
                             | [Vote For Typhon Bot](https://top.gg/bot/756052319417925633/vote)",inline=False)
            for folder in os.listdir('./cogs'):
                if(folder=="Developer"): continue
                embed.add_field(name=f"{folder} Commands",value=f"`{'`, `'.join([filename[:-3] for filename in os.listdir(f'./cogs/{folder}') if filename.endswith('.py')])}`",inline=False)
            embed.set_thumbnail(url=self.client.user.display_avatar)
            embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
            await ctx.reply(embed=embed)

async def setup(client):
    await client.add_cog(help(client))