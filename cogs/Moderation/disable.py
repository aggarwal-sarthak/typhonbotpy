import discord
from discord.ext import commands


class disable(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(name = "disable",
                    usage=".disable <command>",
                    description = "Disables The Mentioned Command",
                    aliases=["dis"])
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def disable(self, ctx:commands.Context, command: str):
        guild_db = self.client.db.guilds.find_one({"guild_id":ctx.guild.id})
        if not guild_db:
            self.client.db.guilds.insert_one({
                "guild_id": ctx.guild.id,
                "cmds": [command]
            })
            await ctx.reply(f"{self.client.emotes['success']} | Command Disabled!")
        else:
            if('cmds' in guild_db):
                cmds = guild_db['cmds']
            else:
                cmds = [command]
            if(command not in cmds):
                cmds.append(command)
                self.client.db.guilds.update_one({"guild_id":ctx.guild.id},{"$set":{"cmds":cmds}})
                await ctx.reply(f"{self.client.emotes['success']} | Command Disabled!")
            else:
                await ctx.reply(f"{self.client.emotes['failed']} | Command already Disabled!")
            
            
async def setup(client):
    await client.add_cog(disable(client))