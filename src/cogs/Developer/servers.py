import os
import discord
from discord.ext import commands
from src.core import pagination
from src.core.bot import tether
from src.core.check import command_enabled


class Servers(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(
        description="Returns Bot Servers",
        usage=f"{os.path.basename(__file__)[:-3]}",
        aliases=["s"],
    )
    @command_enabled()
    async def servers(self, ctx: commands.Context):
        if ctx.author.id not in tether.owner_ids:
            return

        data = sorted(self.client.guilds, key=lambda x: x.member_count, reverse=True)
        embeds = []

        for i in range(0, len(data), 20):
            description = "\n".join(
                f"{j + 1}. {data[j].name} - {data[j].id} - {data[j].member_count}"
                for j in range(i, min(i + 20, len(data)))
            )
            embed = discord.Embed(
                title=f"Bot Servers [{len(self.client.guilds)}]",
                description=f"```{description}```",
                color=discord.Colour.from_str(tether.color),
            )
            embed.set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar
            )
            embeds.append(embed)

        if len(data) > 20:
            await pagination.Simple(timeout=60).start(ctx, pages=embeds)
        elif data:
            await ctx.reply(embed=embeds[0])


async def setup(client: commands.Bot):
    await client.add_cog(Servers(client))
