from discord.ext import commands
import os

class unlock(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.command(description='Unlocks Current/Mentioned Channel(s) For Everyone', usage=f"{os.path.basename(__file__)[:-3]} [channel(s)]")
    async def unlock(self, ctx):
        channel = ctx.message.channel_mentions
        mentions = ""
        if not channel:
            channel = [ctx.channel]
        for c in channel:
            perms = c.overwrites_for(ctx.guild.default_role)
            perms.send_messages=True
            await c.set_permissions(ctx.guild.default_role, overwrite=perms)
            mentions += "<#"+str(c.id)+"> " 
        await ctx.replys(f'{self.client.emotes["success"]} | {mentions} Is Unlocked!')

async def setup(client):
    await client.add_cog(unlock(client))