from discord.ext import commands
import os
from src.core.buttons import Prompt
from src.core.check import is_command_enabled
from src.core.bot import tether 

class unban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(name='unban', description="Unbans Member from the Server",usage=f"{os.path.basename(__file__)[:-3]} <user> [reason]", invoke_without_command=True)
    @commands.check(is_command_enabled)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, user: int, *reason: str):
        banned = [entry.user.id async for entry in ctx.guild.bans()]
        if user not in banned:
            return await ctx.reply(f"{tether.constants.failed} | {user} Was Not Found In Ban list!")
            
        if(len(reason)!=0):
            reason = " ".join([x for x in reason])
        else:
            reason = None

        view = Prompt(ctx.author.id)
        user = await self.client.fetch_user(user)

        msg = await ctx.reply(f"You Are About To Unban: `{user}`",view=view)
        await view.wait()

        try:
            if view.value:
                if msg: await msg.delete()
                await ctx.guild.unban(user=user,reason=reason)
                return await ctx.reply(f"{tether.constants.success} | <@{user.id}> Was Unbanned Successfully!")
    
            if view.value == "2":
                if msg: await msg.delete()
                return await ctx.reply(f"{tether.constants.success} | Unban Cancelled Successfully!")
        except:
            disable = Prompt(ctx)
            return await msg.edit(content=f"You Are About To Unban: `{user}`",view=disable)
        
    @unban.command(name='all', description="Unbans Member from the Server",usage=f"{os.path.basename(__file__)[:-3]} all [reason]")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(ban_members=True)
    async def all(self, ctx, *reason: str):
        banned = [entry.user.id async for entry in ctx.guild.bans()]
        if len(banned) < 0:
            await ctx.reply(f"{tether.constants.failed} | No Banned Members Found!")
        if(len(reason) != 0):
            reason = " ".join([x for x in reason])
        else:
            reason = None

        view = Prompt(ctx.author.id)
        msg = await ctx.reply(f"You Are About To Unban: `{len(banned)}` Members",view=view)
        await view.wait()
        
        
        if view.value:
            if msg: await msg.delete()
            msg = await ctx.reply(f'{tether.constants.loading} | Unbanning `{len(banned)}` Members!')

            for user in banned:
                user = await self.client.fetch_user(user)
                await ctx.guild.unban(user=user,reason=reason)
            if msg: await msg.delete()
            return await ctx.reply(f"{tether.constants.success} | `{len(banned)}` Members Were Unbanned Successfully!")

        if view.value is False:
            if msg: await msg.delete()
            return await ctx.reply(f"{tether.constants.success} | Unban Cancelled Successfully!")

async def setup(client):
    await client.add_cog(unban(client))   