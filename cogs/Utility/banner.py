from discord.ext import commands
import os
import discord
import requests

class banner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.bot_has_permissions(embed_links=True)
    @commands.command(description='Returns Banner For User/Server', usage=f"{os.path.basename(__file__)[:-3]} user\n{os.path.basename(__file__)[:-3]} server")
    async def banner(self, ctx, mode, member: discord.Member=None):
        match mode:
            case "server" | "s":
                if ctx.guild.banner :
                    embed = discord.Embed(title=f"{ctx.guild}'s Banner",color=0xfb7c04)
                    embed.set_image(url=ctx.guild.banner)
                    embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
                    await ctx.reply(embed=embed)
                else:
                    await ctx.reply(f"{self.client.emotes['failed']} | This Server Does Not Have A Banner!")
            
            case "user" | "u":
                if not member: member = ctx.author
                try:
                    embed = discord.Embed(title=f"{member}'s Banner",color=0xfb7c04)
                    user = await self.client.fetch_user(member.id)
                    banner_url = user.banner.url
                    embed.set_image(url=banner_url)
                    embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
                    await ctx.reply(embed=embed)
                except:
                    await ctx.reply(f"{self.client.emotes['failed']} | {member} Does Not Have A Banner!")

async def setup(client):
    await client.add_cog(banner(client))