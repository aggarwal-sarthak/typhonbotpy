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
        if not member: member = ctx.author

        roles = [role.mention for role in member.roles]
        if not roles: roles = "None"
        roles.reverse()

        permissions = [perm[0].replace("_", " ").title() for perm in member.guild_permissions if perm[1]]
        if not permissions: permissions = "None"
        permissions.sort()

        if ctx.guild.owner_id == member.id: ack = "Server Owner"
        elif "Administrator" in permissions: ack = "Server Administrator"
        elif "Manage Guild" in permissions: ack = "Server Moderator"
        else: ack = "Server Member"

        embed = discord.Embed(title=None,color=discord.Colour.from_str(tether.color))
        badges = member.public_flags.all()
        badge_text = " ".join(getattr(tether.constants, badge.name, None) for badge in badges)
        now = datetime.datetime.now()

        embed.add_field(name="**__General Information__**", value=f"**Name :** {member}\n**ID :** {member.id}\n**Nickname :** {member.nick}\n**Badges :** {badge_text}\n**Account Creation :** {timeago.format(member.created_at.astimezone(pytz.timezone('Asia/Kolkata')).replace(tzinfo=None),now)}\n**Server Joined :** {timeago.format(member.joined_at.astimezone(pytz.timezone('Asia/Kolkata')).replace(tzinfo=None),now)}", inline=False)
        embed.add_field(name=f"**__Roles [{len(member.roles)-1}]__**",value=", ".join(roles[:-1]) if len(str(roles)) < 1024 else "Too Many Roles To Display!", inline=False)
        embed.add_field(name=f"**__Permissions__**", value=f'```{", ".join(permissions) if len(str(permissions)) < 1024 else "Too Many Permissions To Display!"}```', inline=False)
        embed.add_field(name="**__Acknowledgements__**", value=ack)
        embed.set_thumbnail(url=member.avatar)
        
        user = await self.client.fetch_user(member.id)
        if user.banner: embed.set_image(url=user.banner.url)

        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
        await ctx.reply(embed=embed)

async def setup(client: commands.Bot):
    await client.add_cog(Userinfo(client))