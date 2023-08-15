from discord.ext import commands
import os
import discord

class voicekick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.has_guild_permissions(move_members=True)
    @commands.bot_has_guild_permissions(move_members=True)
    @commands.command(description='Voicekick A User From Voice Channel',aliases = ['vk', 'vkick'], usage=f"{os.path.basename(__file__)[:-3]} <user>")
    async def voicekick(self, ctx, member: discord.Member=None):
        vcstate = member.voice
        if not vcstate or not vcstate.channel:
            return await ctx.reply(f"{self.client.emotes['failed']} | `{member}` Is Not In Any Voice Channel!")
        
        try:
            await member.move_to(None)
            await ctx.reply(f"{self.client.emotes['success']} | `{member}` Kicked From Voice Channel!")
        except Exception as e:
            await ctx.reply(f"{self.client.emotes['failed']} | `{member}` Cannot Be Kicked From Voice Channel!")

async def setup(client):
    await client.add_cog(voicekick(client))