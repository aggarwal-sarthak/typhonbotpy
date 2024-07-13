from discord.ext import commands
import os
import discord
from core.check import is_command_enabled

class lock(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(description='Locks Current/Mentioned Channel(s) For Everyone', usage=f"{os.path.basename(__file__)[:-3]} [channel(s)]", invoke_without_command=True)
    @commands.check(is_command_enabled)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def lock(self, ctx):
        channel = ctx.message.channel_mentions
        mentions = ""
        if not channel:
            channel = [ctx.channel]
            
        for c in channel:
            perms = c.overwrites_for(ctx.guild.default_role)
            perms.send_messages=False
            await c.set_permissions(ctx.guild.default_role, overwrite=perms)
            mentions += "<#"+str(c.id)+"> " 
        await ctx.reply(f'{self.client.emotes["success"]} | {mentions} Is Locked!')

    @lock.command(name='all', description='Locks All Channels For Everyone', usage=f"{os.path.basename(__file__)[:-3]} [channel(s)]")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(administrator=True)
    async def all(self, ctx):
        count = 0
        msg = await ctx.reply(f'{self.client.emotes["loading"]} | Locking Channels!')
        for channel in ctx.guild.channels:
            if not isinstance(channel, discord.CategoryChannel):
                perms = channel.overwrites_for(ctx.guild.default_role)
                perms.send_messages=False
                await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
                count += 1
        if msg: await msg.edit(content=f'{self.client.emotes["success"]} | `{count}` Channels Are Locked!')

    @lock.command(name='text', description='Locks All Text Channel(s) For Everyone', aliases=['texts'], usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def text(self, ctx):
        count = 0
        msg = await ctx.reply(f'{self.client.emotes["loading"]} | Locking Text Channels!')
        for c in ctx.guild.text_channels:
            perms = c.overwrites_for(ctx.guild.default_role)
            perms.send_messages=False
            await c.set_permissions(ctx.guild.default_role, overwrite=perms)
            count += 1
        if msg: await msg.edit(content=f'{self.client.emotes["success"]} | `{count}` Text Channels Locked!')

    @lock.command(name='voice', description='Locks All Voice Channel(s) For Everyone', aliases=['vc','vcs'], usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def text(self, ctx):
        count = 0
        msg = await ctx.reply(f'{self.client.emotes["loading"]} | Locking Voice Channels!')
        for c in ctx.guild.voice_channels:
            perms = c.overwrites_for(ctx.guild.default_role)
            perms.send_messages=False
            await c.set_permissions(ctx.guild.default_role, overwrite=perms)
            count += 1
        if msg: await msg.edit(content=f'{self.client.emotes["success"]} | `{count}` Voice Channels Locked!')

async def setup(client):
    await client.add_cog(lock(client))