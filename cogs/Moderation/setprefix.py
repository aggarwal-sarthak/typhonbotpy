import discord
from discord.ext import commands


class setprefix(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client

    @commands.has_permissions(administrator=True)
    @commands.command(name = "setprefix",
                    usage=";setprefix <Symbol>",
                    description = "Sets The Mentioned Symbol As Server Prefix",
                    aliases=['set','sp','setpre'])
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def setprefix(self, ctx:commands.Context,symbol:str):
        if(len(symbol)>4):
            await ctx.reply(f"{self.client.emotes['failed']}Prefix Cannot be longer than 4 Characters!")
            return

        self.client.db.guilds.update_one({"guild_id":ctx.guild.id},{"$set":{"prefix":symbol}})
        await ctx.reply(f"{self.client.emotes['success']} Prefix Updated to: `{symbol}`")

async def setup(client):
    await client.add_cog(setprefix(client))