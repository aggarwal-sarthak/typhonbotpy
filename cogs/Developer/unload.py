from discord.ext import commands
import os

class unload(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.command(description='Unloads A Given Command', usage=f"{os.path.basename(__file__)[:-3]}")
    async def unload(self, ctx, cog: str):
        await self.client.unload_extension(f'cogs.{cog}')
        await ctx.reply(f"{self.client.emotes['success']} | Command {cog} Unloaded Successfully!")

async def setup(client):
    await client.add_cog(unload(client))