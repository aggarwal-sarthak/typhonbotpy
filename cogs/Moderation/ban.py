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
    @commands.command(description="Bans Member from the Server",usage=f"{os.path.basename(__file__)[:-3]} <user> [reason]")
    async def ban(self,ctx,user: discord.Member,*reason: str):
        if(len(reason)!=0):
            reason = " ".join([x for x in reason])
        else:
            reason=None
        view = confirmation.Buttons(ctx)
        role = user.top_role
        if(user==ctx.guild.owner):
            await ctx.reply(f"{self.client.emotes['failed']} | Cannot Ban the Owner!")
            return
        await position_check(self,ctx,role)
        msg = await ctx.reply(f"You are about to ban: {user}",view=view)
        await view.wait()
        if view.value == "1":
            if msg: await msg.delete()
            await ctx.guild.ban(user=user,reason=reason,delete_message_seconds=0)
            await ctx.reply(f"{self.client.emotes['success']} | {user} was banned successfully!")
            return False
        if view.value == "2":
            if msg: await msg.delete()
            await ctx.reply(f"{self.client.emotes['success']} | Ban Cancelled Successfully!")
            return False

async def setup(client):
    await client.add_cog(ban(client))   

async def position_check(self, ctx, role):
    if ctx.guild.get_member(self.client.user.id).top_role.position <= role.position:
        await ctx.reply(f"{self.client.emotes['failed']} | My Role Isn't High Enough To Ban!")
        raise commands.CommandError("Command Cancelled")
    elif ctx.guild.owner_id != ctx.author.id and ctx.author.top_role.position <= role.position:
        await ctx.reply(f"{self.client.emotes['failed']} | Your Role Isn't High Enough To Ban!")
        raise commands.CommandError("Command Cancelled")
