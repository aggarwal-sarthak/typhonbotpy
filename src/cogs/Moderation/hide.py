import os
from discord.ext import commands
from src.core.bot import tether
from src.core.check import command_enabled


class Hide(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.group(
        description="Hides Current/Mentioned Channel(s) For Everyone",
        usage=f"{os.path.basename(__file__)[:-3]} [channel(s)]",
        invoke_without_command=True,
    )
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    @command_enabled()
    async def hide(self, ctx: commands.Context):
        channels = ctx.message.channel_mentions or [ctx.channel]
        mentions = ""
        for c in channels:
            perms = c.overwrites_for(ctx.guild.default_role)
            perms.view_channel = False
            await c.set_permissions(ctx.guild.default_role, overwrite=perms)
            mentions += f"<#{c.id}> "
        await ctx.reply(f"{tether.constants.success} | {mentions} Is Hidden!")

    @hide.command(
        name="text",
        description="Hides All Text Channel(s) For Everyone",
        aliases=["texts"],
        usage=f"{os.path.basename(__file__)[:-3]}",
    )
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def text(self, ctx: commands.Context):
        await self.hide_all_channels(ctx, ctx.guild.text_channels, "Text")

    @hide.command(
        name="voice",
        description="Hides All Voice Channel(s) For Everyone",
        aliases=["vc", "vcs"],
        usage=f"{os.path.basename(__file__)[:-3]}",
    )
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def voice(self, ctx: commands.Context):
        await self.hide_all_channels(ctx, ctx.guild.voice_channels, "Voice")

    async def hide_all_channels(self, ctx: commands.Context, channels, channel_type):
        count = 0
        msg = await ctx.reply(
            f"{tether.constants.loading} | Hiding {channel_type} Channels!"
        )
        for c in channels:
            perms = c.overwrites_for(ctx.guild.default_role)
            perms.view_channel = False
            await c.set_permissions(ctx.guild.default_role, overwrite=perms)
            count += 1
        if msg:
            await msg.edit(
                content=f"{tether.constants.success} | `{count}` {channel_type} Channels Hidden!"
            )


async def setup(client: commands.Bot):
    await client.add_cog(Hide(client))
