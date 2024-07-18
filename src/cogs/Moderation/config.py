import discord
from discord.ext import commands
import os 

class config(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = "config", usage=f"{os.path.basename(__file__)[:-3]}", description = "Shows the Bot configuration for the server", aliases=["configuration","settings","setting"])
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def config(self, ctx:commands.Context):
        guild = self.client.db.guilds.find_one({"guild_id":ctx.guild.id})
        if guild and "prefix" in guild:
            prefix = guild['prefix']
        else:
            prefix = self.client.config['prefix']
        embed = discord.Embed(title="Server Configuration",color=self.client.config['color'])
        embed.add_field(name="Prefix:",value=f"`{prefix}`")
        embed.add_field(name="Disabled Commands:",value=f"`{'`,`'.join([cmd for cmd in guild['cmds']]) if guild and len(guild['cmds'])>0 else 'None'}`",inline=False)
        # enabled_command = ""
        # for folder in os.listdir('./cogs'):
        #     if(folder == "Developer"): continue
        #     enabled_command += f"`{'`, `'.join([filename[:-3] for filename in os.listdir(f'./cogs/{folder}') if filename.endswith('.py')])}`"
        # embed.add_field(name="Enabled Commands:",value=enabled_command)
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
        await ctx.reply(embed=embed)

async def setup(client):
    await client.add_cog(config(client))