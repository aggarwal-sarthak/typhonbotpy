from discord.ext import commands
import os
from validation import is_command_enabled

class enable(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(usage=f"{os.path.basename(__file__)[:-3]} <command>", description = "Enables The Mentioned Command", aliases=["en"])
    @commands.check(is_command_enabled)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def enable(self, ctx:commands.Context, cmnd: str):
        command = self.client.get_command(cmnd)
        if command is None: await ctx.reply(f"{self.client.emotes['failed']} | {cmnd} Is Not A Command!")
        guild_db = self.client.db.guilds.find_one({"guild_id":ctx.guild.id})
        if(not guild_db or 'cmds' not in guild_db):
            await ctx.reply(f"{self.client.emotes['failed']} | Command `{command.name}` Is Already Enabled!")
            
        else:
            cmds = guild_db['cmds']
            if command.name in cmds:
                cmds.remove(command.name)
                self.client.db.guilds.update_one({"guild_id":ctx.guild.id},{"$set":{"cmds":cmds}})
                await ctx.reply(f"{self.client.emotes['success']} | Command `{command.name}` Enabled For This Server!")
            else:
                await ctx.reply(f"{self.client.emotes['failed']} | Command `{command.name}` Is Already Enabled!")
            
async def setup(client):
    await client.add_cog(enable(client))