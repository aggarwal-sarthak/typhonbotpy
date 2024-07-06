from discord.ext import commands
import os
import discord
from src.core import pagination
from src.core.validation import is_command_enabled

class list(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.embeds = []

    @commands.group(name='list', description='Returns List', usage=f'{os.path.basename(__file__)[:-3]} <subcommand>', aliases=['dump'], invoke_without_command=True)
    @commands.check(is_command_enabled)
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def list(self, ctx, role: discord.Role):
        data = [member for member in role.members]
        title = f"Members In Role : {len(data)}"
        await mention_pagination(self, ctx, data, self.embeds, title)
    
    @list.command(name='admins', description='Returns List of Admins', aliases=['admin', 'administrator'])
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def admins(self, ctx):
        data = [member for member in ctx.guild.members if member.guild_permissions.administrator and member.bot==False]
        title = f"Admins : {len(data)}"
        await mention_pagination(self, ctx, data, self.embeds, title)

    @list.command(name='bans', description='Returns List of Banned Members', aliases=['ban', 'banned'])
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True, ban_members=True)
    async def bans(self, ctx):
        data = [ban.user async for ban in ctx.guild.bans()]
        title = f"Bans : {len(data)}"
        await mention_pagination(self, ctx, data, self.embeds, title)

    @list.command(name='boosters', description='Returns List of Server Boosters', aliases=['booster', 'premium'])
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def boosters(self, ctx):
        data = [member for member in ctx.guild.premium_subscribers]
        title = f"Boosters : {len(data)}"
        await mention_pagination(self, ctx, data, self.embeds, title)

    @list.command(name='bots', description='Returns List of Bots', aliases=['bot'])
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def bots(self, ctx):
        data = [member for member in ctx.guild.members if member.bot]
        title = f"Bots : {len(data)}"
        await mention_pagination(self, ctx, data, self.embeds, title)

    @list.command(name='emojis', description='Returns List of Server Emojis', aliases=['emoji', 'emo'])
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def emojis(self, ctx):
        data = [emoji for emoji in ctx.guild.emojis]
        title = f"Emojis : {len(data)}"
        for i in range(0,len(data), 20):
            description = ""
            for j in range(i, min(i+20, len(data))):
                description += f"**{str(j+1)}** : {data[j]} : `{data[j].name}`\n"
            pagination_embed = discord.Embed(title=title, description=description,color=self.client.config['color'])
            pagination_embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
            self.embeds.append(pagination_embed)
        await pagination_check(self, ctx, data, self.embeds)

    @list.command(name='roles', description='Returns List of Roles', aliases=['role'])
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def roles(self, ctx):
        data = [roles for roles in ctx.guild.roles]
        data.reverse()
        title = f"Roles : {len(data)}"
        for i in range(0,len(data), 20):
            description = ""
            for j in range(i, min(i+20, len(data))):
                description += "**" + str(j+1) + "** : " + str(data[j].mention) + " `" + str(data[j].id) + "`" + "\n"
            pagination_embed = discord.Embed(title=title, description=description,color=self.client.config['color'])
            pagination_embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
            self.embeds.append(pagination_embed)
        await pagination_check(self, ctx, data, self.embeds)

    @list.command(name='vc', description='Returns List of Voice Channels', aliases=['vcs', 'voice'])
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def vc(self, ctx):
        data = [chan for chan in ctx.guild.voice_channels]
        title = f"Voice Channels : {len(data)}"
        await mention_pagination(self, ctx, data, self.embeds, title)

    @list.command(name='text', description='Returns List of Text Channels', aliases=['texts'])
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def text(self, ctx):
        data = [chan for chan in ctx.guild.text_channels]
        title = f"Text Channels : {len(data)}"
        await mention_pagination(self, ctx, data, self.embeds, title)

async def mention_pagination(self, ctx, data, embeds, title):
    for i in range(0,len(data), 20):
        description = ""
        for j in range(i, min(i+20, len(data))):
            description += "**" + str(j+1) + "** : " +  str(data[j]) + " [" + str(data[j].mention) + "]" + "\n"
        pagination_embed = discord.Embed(title=title, description=description,color=self.client.config['color'])
        pagination_embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
        embeds.append(pagination_embed)
    await pagination_check(self,ctx,data, embeds)

async def pagination_check(self,ctx,data,embeds):
    if len(data)>20:
        await pagination.Simple(timeout=60).start(ctx, pages=embeds)
    elif (len(data)<20 and len(data)>0):
        await ctx.reply(embed=embeds[0])
    else:
        await ctx.reply(f"{self.client.emotes['failed']} | No Members To Show!")
    self.embeds = []

async def setup(client):
    await client.add_cog(list(client))