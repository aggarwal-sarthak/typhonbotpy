from discord.ext import commands
import os
from validation import is_command_enabled

class load(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.command(description='Loads A Given Command', usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.check(is_command_enabled)
    async def load(self, ctx, cog: str):
        if ctx.author.id not in self.client.config["owner"]: return
        await self.client.load_extension(f'cogs.{cog}')
        await ctx.reply(f"{self.client.emotes['success']} | Command {cog} Loaded Successfully!")

async def setup(client):
    await client.add_cog(load(client))