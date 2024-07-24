import discord
from discord.ext import commands
import os
from src.core.bot import tether
from src.core.check import command_enabled


class Config(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(
        name="config",
        usage=f"{os.path.basename(__file__)[:-3]}",
        description="Shows the Bot configuration for the server",
        aliases=["configuration", "settings", "setting"],
    )
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 2, commands.BucketType.member)
    @command_enabled()
    async def config(self, ctx: commands.Context):
        guild_config = tether.db.guilds.find_one({"guild_id": ctx.guild.id})
        prefix = (
            guild_config.get("prefix", tether.prefix) if guild_config else tether.prefix
        )
        disabled_cmds = guild_config.get("cmds", []) if guild_config else []
        disabled = ", ".join(disabled_cmds) if disabled_cmds else "None"

        embed = discord.Embed(
            title="Server Configuration", color=discord.Colour.from_str(tether.color)
        )
        embed.add_field(name="Prefix", value=f"```{prefix}```")
        embed.add_field(
            name="Disabled Commands",
            value=f"```{disabled}```",
            inline=False,
        )

        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar or ""
        )

        await ctx.reply(embed=embed)


async def setup(client: commands.Bot):
    await client.add_cog(Config(client))
