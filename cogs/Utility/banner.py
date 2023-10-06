from discord.ext import commands
import os
import discord
from validation import is_command_enabled

class banner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(name='banner', description='Returns Banner', usage=f"{os.path.basename(__file__)[:-3]} <user>", invoke_without_command=True)
    @commands.check(is_command_enabled)
    @commands.bot_has_permissions(embed_links=True)
    async def banner(self, ctx, member: discord.Member=None):
        if not member: member = ctx.author
        try:
            embed = discord.Embed(title=f"{member}'s Banner",color=self.client.config['color'])
            user = await self.client.fetch_user(member.id)
            banner_url = user.banner.url
            embed.set_image(url=banner_url)
            embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
            await ctx.reply(embed=embed)
        except:
            await ctx.reply(f"{self.client.emotes['failed']} | `{member}` Does Not Have A Banner!")

    @banner.command(name='server', description='Returns Server Banner', usage=f"{os.path.basename(__file__)[:-3]} server")
    @commands.bot_has_permissions(embed_links=True)
    async def server(self, ctx):
        if ctx.guild.banner :
            embed = discord.Embed(title=f"{ctx.guild}'s Banner",color=self.client.config['color'])
            embed.set_image(url=ctx.guild.banner)
            embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
            await ctx.reply(embed=embed)
        else:
            await ctx.reply(f"{self.client.emotes['failed']} | This Server Does Not Have A Banner!")

async def setup(client):
    await client.add_cog(banner(client))