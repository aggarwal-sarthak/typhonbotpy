import os
import discord
from discord.ext import commands
import timeago, datetime
import pytz
from src.core.bot import tether
from src.core.check import command_enabled


class Roleinfo(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(
        description="Returns Information About Role",
        usage=f"{os.path.basename(__file__)[:-3]} <role>",
    )
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @command_enabled()
    async def roleinfo(self, ctx: commands.Context, role: discord.Role = None):
        permissions = ", ".join(
            sorted(
                [
                    str(perm[0]).replace("_", " ").title()
                    for perm in role.permissions
                    if perm[1]
                ]
            )
        )
        if not permissions:
            permissions = "None"

        members = ", ".join([member.mention for member in role.members])
        if not members:
            members = "```None```"

        embed = discord.Embed(title=None, color=discord.Colour.from_str(tether.color))
        embed.add_field(
            name="**__General Information__**",
            value=f"**Name :** {role.name}\n**ID :** {role.id}\n**Role Position :** {len(ctx.guild.roles) - role.position}\n**Color :** {role.color}\n**Created At :** {timeago.format(role.created_at.astimezone(pytz.timezone('Asia/Kolkata')).replace(tzinfo=None), datetime.datetime.now())}\n**Mentionable :** {role.mentionable}\n**Hoisted :** {role.hoist}\n**Managed :** {role.managed}",
            inline=False,
        )
        embed.add_field(
            name="**__Permissions__**",
            value=f"```{"Too Many To Show!" if len(permissions) > 1024 else permissions}```",
            inline=False,
        )
        embed.add_field(
            name=f"**__Members [{len(role.members)}]__**",
            value=f"{"```Too Many To Show!```" if len(members) > 1024 else members}",
            inline=False,
        )
        if role.icon:
            embed.set_thumbnail(url=role.icon.url)
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
        )

        await ctx.reply(embed=embed)


async def setup(client: commands.Bot):
    await client.add_cog(Roleinfo(client))
