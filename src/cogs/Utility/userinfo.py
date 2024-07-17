import os
import pytz
import discord
from discord.ext import commands
import datetime,timeago
from src.core.bot import tether
from src.core.check import command_enabled

class Userinfo(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(description="Returns Information For The Mentioned User", aliases=['user', 'ui', 'about'], usage=f"{os.path.basename(__file__)[:-3]} [User]")
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @command_enabled()
    async def userinfo(self, ctx: commands.Context, member:discord.Member=None):
        if not member:
            member = ctx.author

        roles = []
        for role in member.roles:
            roles.append(str(role.mention))
        roles.reverse()

        permissions = [str(permission) for permission, value in member.guild_permissions if value]
        permission_list = []
        for permission in permissions:
            words = permission.split("_")
            capitalized_words = [word.capitalize() for word in words]
            formatted_permission = " ".join(capitalized_words)
            permission_list.append(formatted_permission)
        permission_list.sort()

        if ctx.guild.owner_id == member.id: ack = "Server Owner"
        elif "Administrator" in permission_list: ack = "Server Administrator"
        elif "Manage Guild" in permission_list: ack = "Server Moderator"
        else: ack = "Server Member"

        embed = discord.Embed(title=None,color=discord.Colour.from_str(tether.color))
        badges = member.public_flags.all()
        badge_text=""
        for badge in badges:
            badge_text += tether.constants[f'{badge.name}']+" "
        now = datetime.datetime.now()
        embed.add_field(name="**__General Information__**", value=f"**Name :** {member}\n**ID :** {member.id}\n**Nickname :** {member.nick}\n**Badges :** {badge_text}\n**Account Creation :** {timeago.format(member.created_at.astimezone(pytz.timezone('Asia/Kolkata')).replace(tzinfo=None),now)}\n**Server Joined :** {timeago.format(member.joined_at.astimezone(pytz.timezone('Asia/Kolkata')).replace(tzinfo=None),now)}", inline=False)
        if len(str(", ".join([x.mention for x in member.roles])))>1024:
            embed.add_field(name=f"**__Roles [{len(member.roles)-1}]__**", value="Too Many To Display!", inline=False)
        else:
            embed.add_field(name=f"**__Roles [{len(member.roles)-1}]__**", value=", ".join(roles[:-1]), inline=False)
        if len(", ".join([x for x in permission_list]))>1024:
            embed.add_field(name=f"**__Permissions__**", value="Too Many To Display!", inline=False)
        else:
            embed.add_field(name=f"**__Permissions__**", value=", ".join(permission_list), inline=False)
        embed.add_field(name="**__Acknowledgements__**", value=ack)
        embed.set_thumbnail(url=member.avatar)
        try:
            user = await self.client.fetch_user(member.id)
            banner_url = user.banner.url
            embed.set_image(url=banner_url)
        except:
            pass
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
        await ctx.reply(embed=embed)

async def setup(client: commands.Bot):
    await client.add_cog(Userinfo(client))