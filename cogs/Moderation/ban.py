import discord
from discord.ext import commands
import os
import json
import confirmation
with open('emoji.json', 'r') as f:
    emotes = json.load(f)

class ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command(description="Bans Member from the Server",aliases=['None'],usage=f"{os.path.basename(__file__)[:-3]} <user> []")
    async def ban(self,ctx,user: discord.Member):
        view = confirmation.Buttons(ctx)
        msg = await ctx.reply(f"You are about to ban: {user}",view=view)
        await view.wait()
        if view.value == "1":
            if msg: await msg.delete()
            await ctx.reply(f"{self.client.emotes['success']} | {user} was banned successfully!")
            return False
        if view.value == "2":
            if msg: await msg.delete()
            await ctx.reply(f"{self.client.emotes['success']} | Ban Cancelled Successfully!")
            return False

async def setup(client):
    await client.add_cog(ban(client)) 