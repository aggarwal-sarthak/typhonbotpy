import discord
from discord.ext import commands
import os
from src.core.buttons import Prompt
from core.check import is_command_enabled

class ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Bans Member from the Server",usage=f"{os.path.basename(__file__)[:-3]} <user> [reason]")
    @commands.check(is_command_enabled)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *reason: str):
        if(len(reason)!=0):
            reason = " ".join([x for x in reason])
        else:
            reason=None

        view = Prompt(ctx)
        role = user.top_role

        if(user == ctx.guild.owner):
            return await ctx.reply(f"{self.client.emotes['failed']} | Cannot Ban the Owner!")
            
        if ctx.guild.get_member(self.client.user.id).top_role.position <= role.position:
            return await ctx.reply(f"{self.client.emotes['failed']} | My Role Isn't High Enough To Ban!")

        elif ctx.guild.owner_id != ctx.author.id and ctx.author.top_role.position <= role.position:
            return await ctx.reply(f"{self.client.emotes['failed']} | Your Role Isn't High Enough To Ban!")
        
        msg = await ctx.reply(f"You Are About To Ban: `{user}`",view=view)
        await view.wait()
        try:
            if view.value == "1":
                if msg: await msg.delete()
                await ctx.guild.ban(user=user,reason=reason,delete_message_seconds=0)
                return await ctx.reply(f"{self.client.emotes['success']} | <@{user.id}> Was Banned successfully!")

            if view.value == "2":
                if msg: await msg.delete()
                return await ctx.reply(f"{self.client.emotes['success']} | Ban Cancelled Successfully!")
        except:
            disable = buttons.Disabled(ctx)
            return await msg.edit(content=f"You Are About To Ban: `{user}`",view=disable)

async def setup(client):
    await client.add_cog(ban(client))       