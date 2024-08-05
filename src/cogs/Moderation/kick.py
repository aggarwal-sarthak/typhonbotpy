import discord
from discord.ext import commands
import os
from src.core.buttons import Prompt
from src.core.bot import tether
from src.core.check import command_enabled


class Kick(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(
        description="Kicks the Mentioned User",
        usage=f"{os.path.basename(__file__)[:-3]} <user> [reason]",
    )
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @command_enabled()
    async def kick(self, ctx: commands.Context, user: discord.Member, *reason: str):
        reason = (
            " ".join(reason)
            if reason
            else f"[Kicked By {ctx.author.name}({ctx.author.id})]"
        )

        view = Prompt(ctx.author.id)
        role = user.top_role

        if user == ctx.guild.owner:
            return await ctx.reply(
                f"{tether.constants.failed} | Cannot Kick the Owner!"
            )

        if ctx.guild.get_member(self.client.user.id).top_role.position <= role.position:
            return await ctx.reply(
                f"{tether.constants.failed} | My Role Isn't High Enough To Kick!"
            )

        elif (
            ctx.guild.owner_id != ctx.author.id
            and ctx.author.top_role.position <= role.position
        ):
            return await ctx.reply(
                f"{tether.constants.failed} | Your Role Isn't High Enough To Kick!"
            )

        msg = await ctx.reply(f"You Are About To Kick: `{user}`", view=view)
        await view.wait()

        if view.value:
            if msg:
                await msg.delete()
            await ctx.guild.kick(user=user, reason=reason)
            return await ctx.reply(
                f"{tether.constants.success} | <@{user.id}> Was Kicked Successfully!"
            )

        if view.value is False:
            if msg:
                await msg.delete()
            return await ctx.reply(
                f"{tether.constants.success} | Kick Cancelled Successfully!"
            )


async def setup(client: commands.Bot):
    await client.add_cog(Kick(client))
