from discord.ext import commands
import os

class reload(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.command(description='Reloads A Given Command', usage=f"{os.path.basename(__file__)[:-3]}")
    async def reload(self, ctx, cog: str):
        await self.client.reload_extension(f'cogs.{cog}')
        await ctx.reply(f"{self.client.emotes['success']} | Command {cog} Reloaded Successfully!")

async def setup(client):
    await client.add_cog(reload(client))