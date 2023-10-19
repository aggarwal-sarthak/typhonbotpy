from discord.ext import commands
import os
import discord
from validation import is_command_enabled

class avatar(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description='Returns User Avatar', aliases=['av'], usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.check(is_command_enabled)
    @commands.bot_has_permissions(embed_links=True)
    async def avatar(self, ctx, member: discord.Member=None):
        if not member: member = ctx.author
        embed = discord.Embed(title=f"{member}'s Avatar",color=self.client.config['color'])
        embed.set_image(url=member.display_avatar)
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
        await ctx.reply(embed=embed)

async def setup(client):
    await client.add_cog(avatar(client))