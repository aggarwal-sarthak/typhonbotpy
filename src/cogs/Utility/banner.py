import os
import discord
from discord.ext import commands
from src.core.bot import tether
from src.core.check import command_enabled

class Banner(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.group(name='banner', description='Returns Banner', usage=f"{os.path.basename(__file__)[:-3]} <user>", invoke_without_command=True)
    @commands.bot_has_permissions(embed_links=True)
    @command_enabled()
    async def banner(self, ctx: commands.Context, member: discord.Member=None):
        if not member: member = ctx.author
        user = await self.client.fetch_user(member.id)

        if not user.banner:
            return await ctx.reply(f"{tether.constants.failed} | `{member}` Does Not Have A Banner!")

        embed = discord.Embed(title=f"{member}'s Banner",color=discord.Colour.from_str(tether.color))
        embed.set_image(url=user.banner.url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar)
        await ctx.reply(embed=embed)

    @banner.command(name='server', description='Returns Server Banner', usage=f"{os.path.basename(__file__)[:-3]} server")
    @commands.bot_has_permissions(embed_links=True)
    async def server(self, ctx: commands.Context):
        if not ctx.guild.banner:
            return await ctx.reply(f"{tether.constants.failed} | This Server Does Not Have A Banner!")

        embed = discord.Embed(title=f"{ctx.guild}'s Banner",color=discord.Colour.from_str(tether.color))
        embed.set_image(url=ctx.guild.banner)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar)
        await ctx.reply(embed=embed)


async def setup(client: commands.Bot):
    await client.add_cog(Banner(client))