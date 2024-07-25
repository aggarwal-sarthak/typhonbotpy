import os
import discord
from discord.ext import commands
from src.core.bot import tether
from src.core.check import command_enabled


class Help(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(
        description="Returns Help Menu For The Bot Commands",
        usage=f"{os.path.basename(__file__)[:-3]} [command]",
    )
    @commands.bot_has_permissions(embed_links=True)
    @command_enabled()
    async def help(self, ctx: commands.Context, *args: str):
        guild_info = tether.db.guilds.find_one({"guild_id": ctx.guild.id})
        prefix = (
            guild_info["prefix"]
            if guild_info and "prefix" in guild_info
            else tether.prefix
        )

        if not args:
            embed = discord.Embed(color=discord.Colour.from_str((tether.color)))
            embed.add_field(
                name="",
                value=f"[Invite Me](https://discord.com/api/oauth2/authorize?client_id=756052319417925633&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.com%2Finvite%2F5UqVvZj&response_type=code&scope=bot%20guilds.join%20applications.commands) **|** [Support Server](https://discord.com/invite/5UqVvZj) **|** [Vote Me](https://top.gg/bot/756052319417925633/vote)",
                inline=False,
            )
            for folder in os.listdir("./src/cogs"):
                if ctx.author.id not in tether.owner_ids and folder == "Developer":
                    continue
                commands_list = [
                    filename[:-3]
                    for filename in os.listdir(f"./src/cogs/{folder}")
                    if filename.endswith(".py")
                ]
                embed.add_field(
                    name=f"{folder}",
                    value=f"`{'`, `'.join(commands_list)}`",
                    inline=False,
                )

            embed.set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
            )
            return await ctx.reply(embed=embed)

        cmd = self.client.get_command(args[0].lower())
        if not cmd:
            return await ctx.reply(f"{tether.constants.failed} | Command Not Found!")

        for subcmd_name in args[1:]:
            if isinstance(cmd, commands.Group):
                subcmd = cmd.get_command(subcmd_name.lower())
                if subcmd:
                    cmd = subcmd
                else:
                    break

        desc = (
            f'**Description:** ```{cmd.description or "None"}```\n'
            f'**Usage:** ```{cmd.usage or "None"}```\n'
            f'**Aliases:** ```{"`, `".join(cmd.aliases) if cmd.aliases else "None"}```\n'
            f'**Cooldown:** ```{str(int(cmd.cooldown.per)) + "s" if cmd.cooldown else "None"}```'
        )

        if isinstance(cmd, commands.Group):
            subs = "\n".join([f"{prefix}{cmd} {sub.name}" for sub in cmd.commands])
            desc += f"\n**Subcommands:**\n```{subs}```"

        embed = discord.Embed(
            title=f"Command: {cmd.name}",
            color=discord.Colour.from_str((tether.color)),
            description=desc,
        )
        await ctx.reply(embed=embed)


async def setup(client: commands.Bot):
    await client.add_cog(Help(client))
