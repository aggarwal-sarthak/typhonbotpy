from discord.ext import commands
import os
import discord

class voicemove(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member == self.client.user and before.channel != after.channel:
            oldmem = before.channel.members if before.channel else []
            await self.move(before.channel, after.channel, oldmem)

    async def move(self, old, new, oldmem):
        for member in oldmem:
            await member.move_to(new)
        voice_client = discord.utils.get(self.client.voice_clients, guild=old.guild)
        await voice_client.disconnect()

    @commands.has_guild_permissions(move_members=True)
    @commands.bot_has_guild_permissions(move_members=True)
    @commands.command(description='Voicemoves All Users From Voice Channel To Another',aliases = ['vm', 'vmove'], usage=f"{os.path.basename(__file__)[:-3]} <user>")
    async def voicemove(self, ctx, *id: discord.VoiceChannel):
        try:
            if not ctx.author.voice:
                return await ctx.reply(f"{self.client.emotes['failed']} | You Need To Be In A Voice Channel To Use This Command!")
            
            if id:
                mem = ctx.author.voice.channel.members
                for i in mem:
                    await i.move_to(id[0])
            
            if len(id)==0:
                print("run")
                channel = ctx.author.voice.channel
                try:
                    vc = await channel.connect()
                    await ctx.reply(f"{self.client.emotes['success']} | Move Me To New Channel To Start Voicemove!")
                except discord.ClientException:
                    await ctx.reply(f"{self.client.emotes['failed']} | I'm Already Connect To A Voice Channel!")
                except Exception as e:
                    print("\n\n\n\n\n\n",e)
                    await ctx.reply(f"{self.client.emotes['failed']} | Error Connecting To Voice Channel!")
        except Exception as e:
            print("\n\n\n\n\n\n",e)        
async def setup(client):
    await client.add_cog(voicemove(client))