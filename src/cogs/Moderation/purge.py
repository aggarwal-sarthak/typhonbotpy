from discord.ext import commands
import os
from core.check import is_command_enabled

class purge(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(name='purge', description='Clears Messages For Given Parameters', aliases = ['clear'], usage = f"{os.path.basename(__file__)[:-3]} <amount>", invoke_without_command=True)
    @commands.check(is_command_enabled)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        def check(message):
            return not message.pinned
        await delete(self, ctx, amount, check)

    @purge.command(name='bots', description='Clears Messages For Bots', aliases = ['bot', 'b'], usage = f"{os.path.basename(__file__)[:-3]} bots <amount>")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def bots(self, ctx, amount: int):
        def check(message):
            return not message.pinned and message.author.bot
        await delete(self, ctx, amount, check)

    @purge.command(name='humans', description='Clears Messages For Humans', aliases = ['human', 'h'], usage = f"{os.path.basename(__file__)[:-3]} humans <amount>")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def humans(self, ctx, amount: int):
        def check(message):
            return not message.pinned and not message.author.bot
        await delete(self, ctx, amount, check)

    @purge.command(name='embeds', description='Clears Embeds', aliases = ['embed', 'e'], usage = f"{os.path.basename(__file__)[:-3]} embeds <amount>")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def embeds(self, ctx, amount: int):
        def check(message):
            return not message.pinned and message.embeds
        await delete(self, ctx, amount, check)

    @purge.command(name='images', description='Clears Images', aliases = ['image', 'img', 'imgs'], usage = f"{os.path.basename(__file__)[:-3]} images <amount>")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def images(self, ctx, amount: int):
        def check(message):
            return not message.pinned and (message.attachments or ('.jpg' or '.jpeg' or '.png' or '.webp') in message.content)
        await delete(self, ctx, amount, check)
        
async def delete(self, ctx, amount, check):
    await ctx.message.delete()
    msgs = await ctx.channel.purge(limit=amount, check=check)
    await ctx.channel.send(f'{self.client.emotes["success"]} | {len(msgs)} Messages Deleted Successfully!')

async def setup(client):
    await client.add_cog(purge(client))