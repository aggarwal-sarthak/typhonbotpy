from discord.ext import commands
import os

class unhide(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.command(description='Unhides Current/Mentioned Channel(s) For Everyone', usage=f"{os.path.basename(__file__)[:-3]}")
    async def unhide(self, ctx):
        channel = ctx.message.channel_mentions
        mentions = ""
        if not channel:
            channel = ctx.channel
        for c in channel:
            await c.set_permissions(ctx.guild.default_role, view_channel=True)
            mentions += "<#"+str(c.id)+"> " 
        await ctx.send(f'{self.client.emotes["success"]} | {mentions} Is Unhidden!')

async def setup(client):
    await client.add_cog(unhide(client))