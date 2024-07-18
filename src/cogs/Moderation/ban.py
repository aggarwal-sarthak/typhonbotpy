import os
import discord
from discord.ext import commands
from src.core.buttons import Prompt
from src.core.bot import tether
from src.core.check import command_enabled

class Ban(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(description="Bans Member from the Server",usage=f"{os.path.basename(__file__)[:-3]} <user> [reason]")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @command_enabled()
    async def ban(self, ctx: commands.Context, user: discord.Member, *reason: str):
        reason = " ".join(reason) if reason else f"[Banned By {user.name}({user.id})]"
        view = Prompt(ctx.author.id)
        role = user.top_role

        if(user == ctx.guild.owner):
            return await ctx.reply(f"{tether.constants.failed} | Cannot Ban the Owner!")
            
        if ctx.guild.get_member(self.client.user.id).top_role.position <= role.position:
            return await ctx.reply(f"{tether.constants.failed} | My Role Isn't High Enough To Ban!")

        elif ctx.guild.owner_id != ctx.author.id and ctx.author.top_role.position <= role.position:
            return await ctx.reply(f"{tether.constants.failed} | Your Role Isn't High Enough To Ban!")
        
        msg = await ctx.reply(f"You Are About To Ban: `{user}`", view=view)
        await view.wait()

        if view.value:
            if msg: await msg.delete()
            await ctx.guild.ban(user=user, reason=reason, delete_message_seconds = 0)
            return await ctx.reply(f"{tether.constants.success} | <@{user.id}> Was Banned successfully!")

        if view.value is False:
            if msg: await msg.delete()
            return await ctx.reply(f"{tether.constants.success} | Ban Cancelled Successfully!")
        
        if msg:
            await msg.delete()

async def setup(client: commands.Bot):
    await client.add_cog(Ban(client))       