from discord.ext import commands
import os
from core.check import is_command_enabled

class unhide(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(description='Unhides Current/Mentioned Channel(s) For Everyone', usage=f"{os.path.basename(__file__)[:-3]} [channel(s)]", invoke_without_command=True)
    @commands.check(is_command_enabled)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def unhide(self, ctx):
        channel = ctx.message.channel_mentions
        mentions = ""
        if not channel:
            channel = [ctx.channel]
            
        for c in channel:
            perms = c.overwrites_for(ctx.guild.default_role)
            perms.view_channel = True
            await c.set_permissions(ctx.guild.default_role, overwrite=perms)
            mentions += "<#"+str(c.id)+"> " 
        await ctx.reply(f'{self.client.emotes["success"]} | {mentions} Is Unhidden!')

    @unhide.command(name='text', description='Unhides All Text Channel(s) For Everyone', usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def text(self, ctx):
        count = 0
        msg = await ctx.reply(f'{self.client.emotes["loading"]} | Unhiding Text Channels!')
        for c in ctx.guild.text_channels:
            perms = c.overwrites_for(ctx.guild.default_role)
            perms.view_channel = True
            await c.set_permissions(ctx.guild.default_role, overwrite=perms)
            count += 1
        if msg: await msg.edit(content=f'{self.client.emotes["success"]} | `{count}` Text Channels Unhidden!')

    @unhide.command(name='voice', description='Unhides All Voice Channel(s) For Everyone', aliases=['vc','vcs'], usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def voice(self, ctx):
        count = 0
        msg = await ctx.reply(f'{self.client.emotes["loading"]} | Unhiding Voice Channels!')
        for c in ctx.guild.voice_channels:
            perms = c.overwrites_for(ctx.guild.default_role)
            perms.view_channel = True
            await c.set_permissions(ctx.guild.default_role, overwrite=perms)
            count += 1
        if msg: await msg.edit(content=f'{self.client.emotes["success"]} | `{count}` Voice Channels Unhidden!')

async def setup(client):
    await client.add_cog(unhide(client))