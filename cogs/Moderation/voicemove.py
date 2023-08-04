from discord.ext import commands
import os
import discord

class voicemove(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.has_guild_permissions(move_members=True)
    @commands.bot_has_guild_permissions(move_members=True)
    @commands.command(description='Voicemoves All Users From Voice Channel To Another',aliases = ['vm', 'vmove'], usage=f"{os.path.basename(__file__)[:-3]} <user>")
    async def voicemove(self, ctx):
        if not ctx.author.voice:
            return await ctx.reply(f"{self.client.emotes['failed']} | You Need To Be In A Voice Channel To Use This Command!")
        
        channel = ctx.author.voice.channel
        try:
            await channel.connect()
            await ctx.reply(f"{self.client.emotes['success']} | Move Me To New Channel To Start Voicemove!")
        except discord.ClientException:
            await ctx.reply(f"{self.client.emotes['failed']} | I'm Already Connect To A Voice Channel!")
        except Exception as e:
            print("\n\n\n\n\n\n",e)
            await ctx.reply(f"{self.client.emotes['failed']} | Error Connecting To Voice Channel!")

async def setup(client):
    await client.add_cog(voicemove(client))