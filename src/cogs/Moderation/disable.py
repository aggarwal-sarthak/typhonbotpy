import os
from discord.ext import commands
from src.core.validation import is_command_enabled

class disable(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(usage=f"{os.path.basename(__file__)[:-3]} <command>", description = "Disables The Mentioned Command", aliases=["dis"])
    @commands.check(is_command_enabled)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def disable(self, ctx:commands.Context, cmnd: str):
        command = self.client.get_command(cmnd)
        if(command.name=="disable" or command.name=="enable"):
            return await ctx.reply(f"{self.client.emotes['failed']} | Cannot Disable `{command.name}`!")
            
        if command is None: await ctx.reply(f"{self.client.emotes['failed']} | {cmnd} Is Not A Command!")
        guild_db = self.client.db.guilds.find_one({"guild_id":ctx.guild.id})

        if not guild_db:
            self.client.db.guilds.insert_one({
                "guild_id": ctx.guild.id,
                "cmds": [command.name]
            })
            return await ctx.reply(f"{self.client.emotes['success']} | Command `{command.name}` Disabled For This Server!")
        
        if('cmds' in guild_db):
            cmds = guild_db['cmds']
            if(command.name in cmds):
                return await ctx.reply(f"{self.client.emotes['failed']} | Command `{command.name}` Is Already Disabled!")
                
            cmds.append(command.name)
        else:
            cmds = [command.name]

        self.client.db.guilds.update_one({"guild_id":ctx.guild.id},{"$set":{"cmds":cmds}})
        await ctx.reply(f"{self.client.emotes['success']} | Command `{command.name}` Disabled For This Server!")
                
async def setup(client):
    await client.add_cog(disable(client))