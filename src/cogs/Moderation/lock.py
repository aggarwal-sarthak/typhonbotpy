from discord.ext import commands
import os
import discord
from src.core.bot import tether
from src.core.check import command_enabled


class Lock(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.group(
        description="Locks Current/Mentioned Channel(s) For Everyone",
        usage=f"{os.path.basename(__file__)[:-3]} [channel(s)]",
        invoke_without_command=True,
    )
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    @command_enabled()
    async def lock(self, ctx: commands.Context):
        channels = ctx.message.channel_mentions or [ctx.channel]
        await self.lock_channels(ctx, channels)

    @lock.command(
        name="all",
        description="Locks All Channels For Everyone",
        usage=f"{os.path.basename(__file__)[:-3]} [channel(s)]",
    )
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def all(self, ctx: commands.Context):
        msg = await ctx.reply(f"{tether.constants.loading} | Locking Channels!")
        channels = [
            c for c in ctx.guild.channels if not isinstance(c, discord.CategoryChannel)
        ]
        count = await self.lock_channels(ctx, channels)
        if msg:
            await msg.edit(
                content=f"{tether.constants.success} | `{count}` Channels Are Locked!"
            )

    @lock.command(
        name="text",
        description="Locks All Text Channel(s) For Everyone",
        aliases=["texts"],
        usage=f"{os.path.basename(__file__)[:-3]}",
    )
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def text(self, ctx: commands.Context):
        msg = await ctx.reply(f"{tether.constants.loading} | Locking Text Channels!")
        count = await self.lock_channels(ctx, ctx.guild.text_channels)
        if msg:
            await msg.edit(
                content=f"{tether.constants.success} | `{count}` Text Channels Locked!"
            )

    @lock.command(
        name="voice",
        description="Locks All Voice Channel(s) For Everyone",
        aliases=["vc", "vcs"],
        usage=f"{os.path.basename(__file__)[:-3]}",
    )
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def voice(self, ctx: commands.Context):
        msg = await ctx.reply(f"{tether.constants.loading} | Locking Voice Channels!")
        count = await self.lock_channels(
            ctx, ctx.guild.voice_channels, lock_voice=True
        )
        if msg:
            await msg.edit(
                content=f"{tether.constants.success} | `{count}` Voice Channels Locked!"
            )

    async def lock_channels(self, ctx: commands.Context, channels, lock_voice=False):
        count = 0
        mentions = ""
        for channel in channels:
            perms = channel.overwrites_for(ctx.guild.default_role)
            perms.send_messages = False
            if lock_voice:
                perms.connect = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
            mentions += f"<#{channel.id}> "
            count += 1
        if not lock_voice and count == 1:
            await ctx.reply(f"{tether.constants.success} | {mentions} Is Locked!")
        return count


async def setup(client: commands.Bot):
    await client.add_cog(Lock(client))
