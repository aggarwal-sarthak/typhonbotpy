from discord.ext import commands
import os
from core.check import is_command_enabled

class hide(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(description='Hides Current/Mentioned Channel(s) For Everyone', usage=f"{os.path.basename(__file__)[:-3]} [channel(s)]", invoke_without_command=True)
    @commands.check(is_command_enabled)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def hide(self, ctx):
        channels = ctx.message.channel_mentions
        mentions = ""
        if not channels:
            channels = [ctx.channel]
            
        for c in channels:
            perms = c.overwrites_for(ctx.guild.default_role)
            perms.view_channel = False
            await c.set_permissions(ctx.guild.default_role, overwrite=perms)
            mentions += "<#"+str(c.id)+"> " 
        await ctx.reply(f'{self.client.emotes["success"]} | {mentions} Is Hidden!')

    @hide.command(name='text', description='Hides All Text Channel(s) For Everyone', aliases=['texts'], usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def text(self, ctx):
        count = 0
        msg = await ctx.reply(f'{self.client.emotes["loading"]} | Hiding Text Channels!')
        for c in ctx.guild.text_channels:
            perms = c.overwrites_for(ctx.guild.default_role)
            perms.view_channel = False
            await c.set_permissions(ctx.guild.default_role, overwrite=perms)
            count += 1
        if msg: await msg.edit(content=f'{self.client.emotes["success"]} | `{count}` Text Channels Hidden!')

    @hide.command(name='voice', description='Hides All Voice Channel(s) For Everyone', aliases=['vc','vcs'], usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def text(self, ctx):
        count = 0
        msg = await ctx.reply(f'{self.client.emotes["loading"]} | Hiding Voice Channels!')
        for c in ctx.guild.voice_channels:
            perms = c.overwrites_for(ctx.guild.default_role)
            perms.view_channel = False
            await c.set_permissions(ctx.guild.default_role, overwrite=perms)
            count += 1
        if msg: await msg.edit(content=f'{self.client.emotes["success"]} | `{count}` Voice Channels Hidden!')

async def setup(client):
    await client.add_cog(hide(client))