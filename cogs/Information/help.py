import discord
from discord.ext import commands
import os 

class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.bot_has_permissions(embed_links=True)
    @commands.command(description='Returns Help Menu For The Bot Commands', usage=f"{os.path.basename(__file__)[:-3]} [command]")
    async def help(self,ctx,*arg):
        if(len(arg)):
            cmd = self.client.get_cog(arg[0].lower()).get_commands()
            menu = discord.Embed(title="Command Details",color=0xfb7c04, description=f"```- [] = Optional Arguments\n- <> = Required Arguments\n- Do Not Type These When Using Commands!```\n> {[c.description for c in cmd][0]}")
            if [c.aliases for c in cmd][0]:
                aliases = ['`, `'.join(c.aliases) for c in cmd][0]
            else:
                aliases = "None"
            menu.add_field(name="Aliases", value=f"`{aliases}`")
            menu.add_field(name="Usage", value=f"`{self.client.config['prefix']+[c.usage for c in cmd][0]}`")
            await ctx.reply(embed=menu)
        else:
            embed = discord.Embed(title="TYPHON BOT Commands",color=0xfb7c04)
            embed.add_field(name="",value=f"{self.client.emotes['success']} : Prefix For This Server : `{self.client.config['prefix']}`\n\
                            {self.client.emotes['success']} : Total Bot Commands : `{len(self.client.commands)}`\n\
                            {self.client.emotes['success']} : Type {self.client.config['prefix']}help <command> For More Info\n\
                            [Invite Typhon Bot](https://discord.com/api/oauth2/authorize?client_id=756052319417925633&permissions=2113268958&redirect_uri=https%3A%2F%2Fdiscord.com%2Finvite%2F5UqVvZj&response_type=code&scope=bot%20guilds.join%20applications.commands)\
                             | [Support Server](https://discord.com/invite/5UqVvZj)\
                             | [Vote For Typhon Bot](https://top.gg/bot/756052319417925633/vote)",inline=False)
            for folder in os.listdir('./cogs'):
                embed.add_field(name=f"{folder} Commands",value=f"`{'`, `'.join([filename[:-3] for filename in os.listdir(f'./cogs/{folder}') if filename.endswith('.py')])}`",inline=False)
            embed.set_thumbnail(url=self.client.user.display_avatar)
            embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
            await ctx.reply(embed=embed)

    @help.error
    async def missing_permissions(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            err = str(error).replace('Bot requires ','').replace(' permission(s) to run this command.', '')
            await ctx.reply(f"{self.client.emotes['failed']} | I Don't Have `{err}` Permission To Use This Command!")
        
async def setup(client):
    await client.add_cog(help(client))