from discord.ext import commands
import os

class load(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.command(description='Loads A Given Command', usage=f"{os.path.basename(__file__)[:-3]}")
    async def load(self, ctx, cog: str):
        await self.client.load_extension(f'cogs.{cog}')
        await ctx.reply(f"{self.client.emotes['success']} | Command {cog} Loaded Successfully!")

async def setup(client):
    await client.add_cog(load(client))