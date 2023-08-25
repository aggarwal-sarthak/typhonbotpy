from discord.ext import commands
import os

class setprefix(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client

    @commands.has_permissions(administrator=True)
    @commands.command(description= "Sets The Mentioned Symbol As Server Prefix", aliases=['set','sp','setpre'], usage=f"{os.path.basename(__file__)[:-3]} <Symbol>" )
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def setprefix(self, ctx, symbol:str):
        guild_db = self.client.db.guilds.find_one({"guild_id":ctx.guild.id})
        
        if(len(symbol)>4):
            await ctx.reply(f"{self.client.emotes['failed']} | Prefix Cannot be longer than 4 Characters!")
            return
        
        if not guild_db:
            self.client.db.guilds.insert_one({
                "guild_id": ctx.guild.id,
                "prefix": symbol
            })
        else:
            self.client.db.guilds.update_one({"guild_id":ctx.guild.id},{"$set":{"prefix":symbol}})
        await ctx.reply(f"{self.client.emotes['success']} | Prefix Updated to: `{symbol}`")

async def setup(client):
    await client.add_cog(setprefix(client))