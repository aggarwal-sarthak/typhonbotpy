from discord.ext import commands
import os
from types import SimpleNamespace
import asyncio
from validation import is_command_enabled

class purge(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.command(description='Clears Messages For Given Parameters', usage=f"{os.path.basename(__file__)[:-3]} <amount>\n{os.path.basename(__file__)[:-3]} <Member> <amount>\n{os.path.basename(__file__)[:-3]} bots <amount>\n{os.path.basename(__file__)[:-3]} embeds <amount>\n{os.path.basename(__file__)[:-3]} humans <amount>\n{os.path.basename(__file__)[:-3]} images <amount>\n{os.path.basename(__file__)[:-3]} images <amount>")
    @commands.check(is_command_enabled)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, *args):
        mode = [str(x) for x in args if not x.isdigit()][0] if len([str(x) for x in args if not x.isdigit()]) else []
        amount = [int(x) for x in args if x.isdigit()][0] if len([int(x) for x in args if x.isdigit()]) else 50
        if amount <=0: raise commands.MissingRequiredArgument(SimpleNamespace(displayed_name="amount"))
        await ctx.message.delete()
        if len(mode) and not (mode.startswith("<@") or mode.endswith(">")):
            match mode[0]:
                case "bots" | "bot" | "b":
                    def check(message):
                        asyncio.sleep(0.5)
                        return not message.pinned and message.author.bot
                    
                case "embeds" | "embed" | "e":
                    def check(message):
                        asyncio.sleep(0.5)
                        return not message.pinned and message.embeds

                case "humans" | "human" | "h":
                    def check(message):
                        asyncio.sleep(0.5)
                        return not message.pinned and not message.author.bot
                    
                case "images" | "image" | "i":
                    def check(message):
                        asyncio.sleep(0.5)
                        return not message.pinned and (message.attachments or ('.jpg' or '.jpeg' or '.png' or '.webp') in message.content)
                    
                case _:
                    raise commands.MissingRequiredArgument(SimpleNamespace(displayed_name="mode"))
        else:
            if mode.startswith("<@") and mode.endswith(">"):
                def check(message):
                    return not message.pinned and str(message.author.id) == str(mode[mode.index("<@")+2:mode.index(">")])
            else:
                def check(message):
                    return not message.pinned
                
        msgs = await ctx.channel.purge(limit=amount, check=check)
        await ctx.channel.send(f'{self.client.emotes["success"]} | {len(msgs)} Messages Deleted Successfully!')

async def setup(client):
    await client.add_cog(purge(client))