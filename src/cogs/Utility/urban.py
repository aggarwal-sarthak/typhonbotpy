import os
import requests
import discord
from discord.ext import commands
from src.core.bot import tether
from src.core.check import command_enabled


class Urban(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(
        description="Returns Urban Dictionary Meaning Of The Query",
        usage=f"{os.path.basename(__file__)[:-3]} <Query>",
    )
    @commands.bot_has_permissions(embed_links=True)
    @command_enabled()
    async def urban(self, ctx: commands.Context, *, query: str):
        url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
        querystring = {"term": query}
        headers = {
            "X-RapidAPI-Key": tether.rapid_token,
            "X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com",
        }

        response = requests.get(url, headers=headers, params=querystring).json()
        if not len(response["list"]):
            msg = "No Meaning Found!"
        else:
            msg = response["list"][0]["definition"]

        embed = discord.Embed(
            title=query,
            description=f"```{msg}```",
            color=discord.Colour.from_str(tether.color),
        )
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar)
        await ctx.reply(embed=embed)


async def setup(client: commands.Bot):
    await client.add_cog(Urban(client))
