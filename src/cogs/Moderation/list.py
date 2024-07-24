import os
from discord.ext import commands
import discord
from src.core import pagination
from src.core.bot import tether
from src.core.check import command_enabled


class List(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.group(
        name="list",
        description="Returns List",
        usage=f"{os.path.basename(__file__)[:-3]} <subcommand>",
        aliases=["dump"],
        invoke_without_command=True,
    )
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    @command_enabled()
    async def list(self, ctx: commands.Context, role: discord.Role):
        data = role.members
        await self.mention_pagination(ctx, data, f"Members In Role : {len(data)}")

    @list.command(
        name="admins",
        description="Returns List of Admins",
        aliases=["admin", "administrator"],
    )
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def admins(self, ctx):
        data = [
            member
            for member in ctx.guild.members
            if member.guild_permissions.administrator and not member.bot
        ]
        await self.mention_pagination(ctx, data, f"Admins : {len(data)}")

    @list.command(
        name="bans",
        description="Returns List of Banned Members",
        aliases=["ban", "banned"],
    )
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True, ban_members=True)
    async def bans(self, ctx):
        data = [ban.user async for ban in ctx.guild.bans()]
        await self.mention_pagination(ctx, data, f"Bans : {len(data)}")

    @list.command(
        name="boosters",
        description="Returns List of Server Boosters",
        aliases=["booster", "premium"],
    )
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def boosters(self, ctx):
        data = ctx.guild.premium_subscribers
        await self.mention_pagination(ctx, data, f"Boosters : {len(data)}")

    @list.command(name="bots", description="Returns List of Bots", aliases=["bot"])
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def bots(self, ctx):
        data = [member for member in ctx.guild.members if member.bot]
        await self.mention_pagination(ctx, data, f"Bots : {len(data)}")

    @list.command(
        name="emojis",
        description="Returns List of Server Emojis",
        aliases=["emoji", "emo"],
    )
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def emojis(self, ctx):
        data = ctx.guild.emojis
        await self.mention_pagination(
            ctx, data, f"Emojis : {len(data)}", show_name=True
        )

    @list.command(name="roles", description="Returns List of Roles", aliases=["role"])
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def roles(self, ctx):
        data = ctx.guild.roles[::-1]
        await self.mention_pagination(
            ctx, data, f"Roles : {len(data)}", mention_format=True
        )

    @list.command(
        name="vc",
        description="Returns List of Voice Channels",
        aliases=["vcs", "voice"],
    )
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def vc(self, ctx):
        data = ctx.guild.voice_channels
        await self.mention_pagination(ctx, data, f"Voice Channels : {len(data)}")

    @list.command(
        name="text", description="Returns List of Text Channels", aliases=["texts"]
    )
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def text(self, ctx):
        data = ctx.guild.text_channels
        await self.mention_pagination(ctx, data, f"Text Channels : {len(data)}")

    async def mention_pagination(
        self, ctx, data, title, show_name=False, mention_format=False
    ):
        embeds = []
        for i in range(0, len(data), 20):
            description = ""
            for j in range(i, min(i + 20, len(data))):
                item = data[j]
                if mention_format:
                    description += f"**{j + 1}** : {item.mention} `{item.id}`\n"
                elif show_name:
                    description += f"**{j + 1}** : {item} : `{item.name}`\n"
                else:
                    description += f"**{j + 1}** : {item} [{item.mention}]\n"
            embed = discord.Embed(
                title=title,
                description=description,
                color=discord.Colour.from_str(tether.color),
            )
            embed.set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar
            )
            embeds.append(embed)
        await self.pagination_check(ctx, data, embeds)

    async def pagination_check(self, ctx, data, embeds):
        if len(data) > 20:
            await pagination.Simple(timeout=60).start(ctx, pages=embeds)
        elif data:
            await ctx.reply(embed=embeds[0])
        else:
            await ctx.reply(f"{tether.constants.failed} | No Data To Show!")


async def setup(client: commands.Bot):
    await client.add_cog(List(client))
