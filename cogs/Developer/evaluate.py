from discord.ext import commands
import os
from validation import is_command_enabled

class evaluate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.command(description='Evaluates given code',aliases=['eval', 'e'], usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.check(is_command_enabled)
    async def evaluate(self, ctx, *,code: str):
        if ctx.author.id not in self.client.config["owner"]: return
        try:
            result = eval(code)
            
            await ctx.send(f"{self.client.emotes['success']} | Result: {result}")

        except Exception as e:
            await ctx.send(f"{self.client.emotes['failed']} | Error: {e}")
       
async def setup(client):
    await client.add_cog(evaluate(client))