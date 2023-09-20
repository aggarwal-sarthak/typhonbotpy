import discord
from discord.ext import commands
import os 

class settings(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(name = "settings",
                    usage=f"{os.path.basename(__file__)[:-3]}",
                    description = "Shows the Bot configuration for the server",
                    aliases=["configuration","config","setting"])
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def settings(self, ctx:commands.Context):
        guild = self.client.db.guilds.find_one({"guild_id":ctx.guild.id})
        if guild and "prefix" in guild:
            prefix = guild['prefix']
        else:
            prefix = self.client.config['prefix']
        embed = discord.Embed(title="Server Configuration",color=0xfb7c04)
        embed.add_field(name="Prefix:",value=f"`{prefix}`")
        
        embed.add_field(name="Disabled Commands:",value=f"`{'`,`'.join([cmd for cmd in guild['cmds']]) if guild and len(guild['cmds'])>0 else 'None'}`",inline=False)
        enabled_command = ""
        for folder in os.listdir('./cogs'):
            if(folder == "Developer"): continue
            enabled_command += f"`{'`, `'.join([filename[:-3] for filename in os.listdir(f'./cogs/{folder}') if filename.endswith('.py')])}`"
        embed.add_field(name="Enabled Commands:",value=enabled_command)
        await ctx.send(embed=embed)



async def setup(client):
    await client.add_cog(settings(client))