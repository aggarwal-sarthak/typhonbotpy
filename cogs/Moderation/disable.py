import os
from discord.ext import commands

class disable(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(usage=f"{os.path.basename(__file__)[:-3]} <command>", description = "Disables The Mentioned Command", aliases=["dis"])
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def disable(self, ctx:commands.Context, cmnd: str):
        command = self.client.get_command(cmnd)
        if(command.name=="disable" or "enable"):
            await ctx.reply(f"{self.client.emotes['failed']} | Cannot Disable `{command.name}`!")
            return
        if command is None: await ctx.reply(f"{self.client.emotes['failed']} | {cmnd} is not a Command!")
        guild_db = self.client.db.guilds.find_one({"guild_id":ctx.guild.id})
        if not guild_db:
            self.client.db.guilds.insert_one({
                "guild_id": ctx.guild.id,
                "cmds": [command.name]
            })
            await ctx.reply(f"{self.client.emotes['success']} | Command Disabled!")
        else:
            if('cmds' in guild_db):
                cmds = guild_db['cmds']
                if(command.name in cmds):
                    await ctx.reply(f"{self.client.emotes['failed']} | Command already Disabled!")
                    return
                cmds.append(command.name)
            else:
                cmds = [command.name]
            self.client.db.guilds.update_one({"guild_id":ctx.guild.id},{"$set":{"cmds":cmds}})
            await ctx.reply(f"{self.client.emotes['success']} | Command Disabled!")
                
            
async def setup(client):
    await client.add_cog(disable(client))