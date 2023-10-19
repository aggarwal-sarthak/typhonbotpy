from discord.ext import commands
import os
from validation import is_command_enabled

class ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description='Returns Bot Ping', usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.check(is_command_enabled)
    async def ping(self, ctx):
        latency = self.client.latency
        await ctx.reply(f'{self.client.emotes["success"]} | {round(latency * 1000)}ms!')

async def setup(client):
    await client.add_cog(ping(client))