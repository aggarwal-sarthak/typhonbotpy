from discord.ext import commands
import os
from core.check import is_command_enabled

class setprefix(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client

    @commands.command(description= "Sets The Mentioned Symbol As Server Prefix", aliases=['set','sp','setpre','prefix'], usage=f"{os.path.basename(__file__)[:-3]} <Symbol>" )
    @commands.check(is_command_enabled)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def setprefix(self, ctx, symbol:str):
        guild_db = self.client.db.guilds.find_one({"guild_id":ctx.guild.id})
        
        if(len(symbol)>4):
            return await ctx.reply(f"{self.client.emotes['failed']} | Prefix Cannot Be Longer Than 4 Characters!")
        
        if not guild_db and symbol != self.client.config["prefix"]:
            self.client.db.guilds.insert_one({
                "guild_id": ctx.guild.id,
                "prefix": symbol
            })
        elif symbol != self.client.config["prefix"]:
            self.client.db.guilds.update_one({"guild_id":ctx.guild.id},{"$set":{"prefix":symbol}})
        else:
            self.client.db.guilds.update_one({"guild_id":ctx.guild.id},{"$unset":{"prefix":""}})
        await ctx.reply(f"{self.client.emotes['success']} | Prefix Updated To: `{symbol}`")

async def setup(client):
    await client.add_cog(setprefix(client))