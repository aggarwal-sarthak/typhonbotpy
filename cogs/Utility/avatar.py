from discord.ext import commands
import os
import discord

class avatar(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.bot_has_permissions(embed_links=True)
    @commands.command(description='Returns User Avatar', usage=f"{os.path.basename(__file__)[:-3]}")
    async def avatar(self, ctx, member: discord.Member=None):
        if not member: member = ctx.author
        embed = discord.Embed(title=f"{member}'s Avatar",color=0xfb7c04)
        embed.set_image(url=member.display_avatar)
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
        await ctx.reply(embed=embed)

async def setup(client):
    await client.add_cog(avatar(client))