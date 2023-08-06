import discord
from discord.ext import commands
import os
import json
import confirmation
with open('emoji.json', 'r') as f:
    emotes = json.load(f)

class unban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command(description="Unbans Banned Member from the Server",usage=f"{os.path.basename(__file__)[:-3]} <user> [reason]")
    async def unban(self,ctx,user:int,*reason: str):
        banned = [entry.user.id async for entry in ctx.guild.bans()]
        print(banned)
        if(user in banned):
            print("he is banned fosho fosho\n\n\n\n")
        if(len(reason)!=0):
            reason = " ".join([x for x in reason])
        else:
            reason=None
        view = confirmation.Buttons(ctx)
        msg = await ctx.reply(f"You are about to unban: {user}",view=view)
        await view.wait()
        if view.value == "1":
            if msg: await msg.delete()
            await ctx.guild.unban(user=user,reason=reason)
            await ctx.reply(f"{self.client.emotes['success']} | {user} was unbanned successfully!")
            return False
        if view.value == "2":
            if msg: await msg.delete()
            await ctx.reply(f"{self.client.emotes['success']} | Unban Cancelled Successfully!")
            return False

async def setup(client):
    await client.add_cog(unban(client))   

