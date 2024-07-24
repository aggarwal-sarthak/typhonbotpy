import discord
from discord.ext import commands
import os
import datetime
from src.core.check import command_enabled
from src.core.bot import tether


class Info(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.start_time = datetime.datetime.now()

    @commands.command(
        description="Returns Information About Bot",
        aliases=["botinfo"],
        usage=f"{os.path.basename(__file__)[:-3]}",
    )
    @commands.bot_has_permissions(embed_links=True)
    @command_enabled()
    async def info(self, ctx: commands.Context):
        owner_mentions = "\n".join(
            [
                f"[{await self.client.fetch_user(owner_id)}](https://discord.com/users/{owner_id}) [<@!{owner_id}>]"
                for owner_id in tether.owner_ids
            ]
        )

        total_users = sum(guild.member_count for guild in self.client.guilds)
        td = datetime.datetime.now() - self.start_time
        days = td.days
        hours, remainder = divmod(td.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime = f"{days}d {hours}hr {minutes}min {seconds}sec"

        embed = discord.Embed(
            title=f"{self.client.user.name}",
            color=discord.Colour.from_str(tether.color),
        )
        embed.add_field(
            name="Discord.py", value=f"```{discord.__version__}```", inline=False
        )
        embed.add_field(name="Owner", value=owner_mentions, inline=False)
        embed.add_field(
            name="Total Servers", value=f"```{len(self.client.guilds)}```", inline=False
        )
        embed.add_field(name="Total Users", value=f"```{total_users}```", inline=False)
        embed.add_field(name="Uptime", value=f"```{uptime}```", inline=False)
        embed.add_field(
            name="",
            value="[Invite Me](https://discord.com/api/oauth2/authorize?client_id=756052319417925633&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.com%2Finvite%2F5UqVvZj&response_type=code&scope=bot%20guilds.join%20applications.commands) **|** [Support Server](https://discord.com/invite/5UqVvZj) **|** [Vote Me](https://top.gg/bot/756052319417925633/vote)",
            inline=False,
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
        )
        await ctx.reply(embed=embed)


async def setup(client: commands.Bot):
    await client.add_cog(Info(client))
