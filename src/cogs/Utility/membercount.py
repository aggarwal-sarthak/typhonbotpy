import os
import discord
from discord.ext import commands
from src.core.bot import tether
from src.core.check import command_enabled


class membercount(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(
        description="Returns Membercount",
        usage=f"{os.path.basename(__file__)[:-3]}",
        aliases=["members", "mc"],
    )
    @commands.bot_has_permissions(embed_links=True)
    @command_enabled()
    async def membercount(self, ctx: commands.Context):
        embed = discord.Embed(title=None, color=discord.Colour.from_str(tether.color))
        embed.add_field(name="**Members**", value=f"```{ctx.guild.member_count}```")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar)
        embed.timestamp = ctx.message.created_at
        await ctx.reply(embed=embed)


async def setup(client: commands.Bot):
    await client.add_cog(membercount(client))
