
import discord
from discord.ext import commands
import os
import Paginator

class steal(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.command(description="Add Emotes and Stickers to Server",aliases=['add'],usage=f"{os.path.basename(__file__)[:-3]} <emote>")
    async def steal(self, ctx,*args):
        if(ctx.message.reference.reference_id is not None):
            msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            if(msg.stickers is not None):
                sticker = msg.stickers[0]
            else:
                emoji = msg.content.split()
                print(emoji)
        else:
            pass






async def get_name_id(emoji):
    pass
# WARNING: Decompyle incomplete


async def create_embed(emoji):
    pass
# WARNING: Decompyle incomplete


async def setup(client):
    pass
# WARNING: Decompyle incomplete


async def setup(client):
    await client.add_cog(steal(client)) 