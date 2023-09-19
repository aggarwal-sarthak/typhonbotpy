from discord.ext import commands
import os
import discord
import asyncio
from validation import is_command_enabled

class voicemove(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member == self.client.user and (before.channel and after.channel) != None and before.channel != after.channel:
            oldmem = before.channel.members if before.channel else []
            await self.move(before.channel, after.channel, oldmem)

    async def move(self, old, new, oldmem):
        for member in oldmem:
            await member.move_to(new)
        voice_client = discord.utils.get(self.client.voice_clients, guild=new.guild)
        await voice_client.disconnect()

    @commands.command(description='Voicemoves All Users From Voice Channel To Another',aliases = ['vm', 'vmove'], usage=f"{os.path.basename(__file__)[:-3]} <user>")
    @commands.check(is_command_enabled)
    @commands.has_guild_permissions(move_members=True)
    @commands.bot_has_guild_permissions(move_members=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def voicemove(self, ctx, *id: discord.VoiceChannel):
        if not ctx.author.voice:
            return await ctx.reply(f"{self.client.emotes['failed']} | You Need To Be In A Voice Channel To Use This Command!")
        
        if id:
            mem = ctx.author.voice.channel.members
            for i in mem:
                await i.move_to(id[0])
        
        if not id:
            channel = ctx.author.voice.channel
            try:
                await channel.connect()
                await ctx.reply(f"{self.client.emotes['success']} | Move Me To New Channel To Start Voicemove!")
                await self.client.wait_for('voice_state_update', timeout=30)

            except discord.ClientException:
                await ctx.reply(f"{self.client.emotes['failed']} | I'm Already Connect To A Voice Channel!")

            except asyncio.TimeoutError:
                await ctx.reply(f"{self.client.emotes['failed']} | Command Timed Out!")
                voice_client = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
                await voice_client.disconnect()

            except Exception as e:
                await ctx.reply(f"{self.client.emotes['failed']} | Error Connecting To Voice Channel!")
            
async def setup(client):
    await client.add_cog(voicemove(client))