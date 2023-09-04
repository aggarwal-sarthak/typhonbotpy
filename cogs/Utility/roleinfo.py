from discord.ext import commands
import os
import discord
import timeago, datetime
import pytz
from validation import is_command_enabled

class roleinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.command(description='Returns Information About Mentioned Role', usage=f"{os.path.basename(__file__)[:-3]} <role>")
    @commands.check(is_command_enabled)
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def roleinfo(self, ctx, role: discord.Role=None):
        permissions = ", ".join(sorted([str(perms[0]).replace("_"," ").title() for perms in role.permissions if perms[1] is True]))
        if not permissions: permissions = "None"
        embed = discord.Embed(title=None,color=0xfb7c04)
        embed.add_field(name="**__General Information__**", value=f"**Name :** {role.name}\n**ID :** {role.id}\n**Role Position :** {len(ctx.guild.roles) - role.position}\n**Color :** {role.color}\n**Created At :** {timeago.format(role.created_at.astimezone(pytz.timezone('Asia/Kolkata')).replace(tzinfo=None),datetime.datetime.now())}\n**Mentionable :** {str(role.mentionable).title()}\n**Hoisted :** {str(role.hoist).title()}\n**Managed :** {str(role.managed).title()}", inline=False)
        embed.add_field(name="**__Permissions__**", value=f"{permissions if len(permissions)<=256 else 'Too Many Permissions To Show!'}", inline=False)
        embed.add_field(name=f"**__Members [{len(role.members)}]__**", value=f"{', '.join([member.mention for member in role.members]) if len(', '.join([member.mention for member in role.members]))<256 else 'Too Many Members To Show!'}", inline=False)
        if role.icon: embed.set_thumbnail(url=role.icon)
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
        await ctx.reply(embed=embed)
        
async def setup(client):
    await client.add_cog(roleinfo(client))