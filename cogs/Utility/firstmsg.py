from discord.ext import commands
import os
import discord

class firstmsg(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.bot_has_permissions(embed_links=True, read_message_history=True)
    @commands.command(description='Returns First Message In The Channel By The User', usage=f"{os.path.basename(__file__)[:-3]} firstmsg [user]")
    async def firstmsg(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author

        async for message in ctx.channel.history(limit=None, oldest_first=True):
            if message.author == member:
                await message.reply(f"{self.client.emotes['success']} | Found First Message By `{member.name}`!")
                return
        
        await ctx.reply(f"{self.client.emotes['failed']} | No Message Found By `{member.name}`!")

    @firstmsg.error
    async def missing_permissions(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            err = str(error).replace('Bot requires ','').replace(' permission(s) to run this command.', '')
            await ctx.reply(f"{self.client.emotes['failed']} | I Don't Have `{err}` Permission To Use This Command!")

async def setup(client):
    await client.add_cog(firstmsg(client))