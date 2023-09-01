import discord
from discord.ext import commands
import os

class enable(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(name = "enable",
                    usage=f"{os.path.basename(__file__)[:-3]} <command>",
                    description = "Enables The Mentioned Command",
                    aliases=["en"])
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def enable(self, ctx:commands.Context, cmnd: str):
        command = self.client.get_command(cmnd)
        if command is None: await ctx.reply(f"{self.client.emotes['failed']} | {cmnd} is not a Command!")
        guild_db = self.client.db.guilds.find_one({"guild_id":ctx.guild.id})
        if(not guild_db or 'cmds' not in guild_db):
            await ctx.reply(f"{self.client.emotes['failed']} | Command is already Enabled!")
            
        else:
            cmds = guild_db['cmds']
            if command.name in cmds:
                cmds.remove(command.name)
                self.client.db.guilds.update_one({"guild_id":ctx.guild.id},{"$set":{"cmds":cmds}})
                await ctx.reply(f"{self.client.emotes['success']} | Command Enabled!")
            else:
                await ctx.reply(f"{self.client.emotes['failed']} | Command is already Enabled!")
            
async def setup(client):
    await client.add_cog(enable(client))