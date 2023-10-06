from discord.ext import commands
import os
import requests
import discord
from validation import is_command_enabled

class urban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description='Returns Urban Dictionary Meaning Of The Query', usage=f"{os.path.basename(__file__)[:-3]} <Query>")
    @commands.check(is_command_enabled)
    async def urban(self, ctx, *, query):
        url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
        querystring = {"term": query}
        headers = {
	        "X-RapidAPI-Key": self.client.config['rapidapi'],
	        "X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring).json()
        if not len(response['list']):
            msg = 'No Meaning Found!'
        else:
            msg = response['list'][0]['definition']

        embed = discord.Embed(title=query, description=msg, color=self.client.config['color'])
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
        await ctx.reply(embed=embed)

async def setup(client):
    await client.add_cog(urban(client))