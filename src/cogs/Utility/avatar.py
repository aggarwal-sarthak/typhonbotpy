from discord.ext import commands
import os
import discord
from src.core.bot import tether
from src.core.check import command_enabled


class Avatar(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(
        description="Returns User Avatar",
        aliases=["av"],
        usage=f"{os.path.basename(__file__)[:-3]}",
    )
    @commands.bot_has_permissions(embed_links=True)
    @command_enabled()
    async def avatar(self, ctx: commands.Context, member: discord.Member = None):
        if not member:
            member = ctx.author
        embed = discord.Embed(
            title=f"{member}'s Avatar", color=discord.Colour.from_str(tether.color)
        )
        embed.set_image(url=member.display_avatar)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar)
        await ctx.reply(embed=embed)


async def setup(client: commands.Bot):
    await client.add_cog(Avatar(client))
