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
            usage = (self.client.config["prefix"]+[c.usage for c in cmd][0]).replace('\n',f'\n{self.client.config["prefix"]}')
            menu.add_field(name="Usage", value=f'`{usage}`')
            await ctx.reply(embed=menu)
        else:
            res = self.client.db.guilds.find_one({"guild_id": ctx.guild.id})
            print(res)
            if res and "prefix" in res:
                prefix = res['prefix']
            else:
                prefix = self.client.config['prefix']
            embed = discord.Embed(title="TYPHON BOT Commands",color=0xfb7c04)
            embed.add_field(name="",value=f"{self.client.emotes['success']} : Prefix For This Server : `{prefix}`\n\
                            {self.client.emotes['success']} : Total Bot Commands : `{len(self.client.commands)}`\n\
                            {self.client.emotes['success']} : Type {prefix}help <command> For More Info\n\
                            [Invite Typhon Bot](https://discord.com/api/oauth2/authorize?client_id=756052319417925633&permissions=2113268958&redirect_uri=https%3A%2F%2Fdiscord.com%2Finvite%2F5UqVvZj&response_type=code&scope=bot%20guilds.join%20applications.commands)\
                             | [Support Server](https://discord.com/invite/5UqVvZj)\
                             | [Vote For Typhon Bot](https://top.gg/bot/756052319417925633/vote)",inline=False)
            for folder in os.listdir('./cogs'):
                embed.add_field(name=f"{folder} Commands",value=f"`{'`, `'.join([filename[:-3] for filename in os.listdir(f'./cogs/{folder}') if filename.endswith('.py')])}`",inline=False)
            embed.set_thumbnail(url=self.client.user.display_avatar)
            embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
            await ctx.reply(embed=embed)

async def setup(client):
    await client.add_cog(help(client))