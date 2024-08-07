import os
import discord
from discord.ext import commands
import datetime, timeago
import pytz
from src.core.bot import tether
from src.core.check import command_enabled


class Snipe(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.deleted_messages = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.deleted_messages[message.channel.id] = message

    @commands.command(
        description="Returns Last Deleted Messaged In The Channel",
        usage=f"{os.path.basename(__file__)[:-3]}",
    )
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @command_enabled()
    async def snipe(self, ctx: commands.Context):
        if (
            ctx.channel.id not in self.deleted_messages
            or not self.deleted_messages[ctx.channel.id]
        ):
            return await ctx.reply(
                f"{tether.constants.failed} | No Deleted Messages Found In This Channel!"
            )

        embed = discord.Embed(
            title="Message Found", color=discord.Colour.from_str(tether.color)
        )
        embed.add_field(
            name="**__Information__**",
            value=f"**Message By :** {self.deleted_messages[ctx.channel.id].author.mention}\n**Time :** {timeago.format(self.deleted_messages[ctx.channel.id].created_at.astimezone(pytz.timezone('Asia/Kolkata')).replace(tzinfo=None), datetime.datetime.now())}",
            inline=False,
        )
        embed.add_field(
            name="**__Content__**",
            value=f"```{self.deleted_messages[ctx.channel.id].content}```",
            inline=False,
        )
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar)
        await ctx.reply(embed=embed)


async def setup(client: commands.Bot):
    await client.add_cog(Snipe(client))
