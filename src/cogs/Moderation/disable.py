import os
from discord.ext import commands
from src.core.bot import tether
from src.core.check import command_enabled


class Disable(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(
        usage=f"{os.path.basename(__file__)[:-3]} <command>",
        description="Disables The Mentioned Command",
        aliases=["dis"],
    )
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @command_enabled()
    async def disable(self, ctx: commands.Context, cmnd: str):
        command = self.client.get_command(cmnd)

        if command is None:
            return await ctx.reply(
                f"{tether.constants.failed} | {cmnd} Is Not A Command!"
            )

        if command.name in ["disable", "enable"]:
            return await ctx.reply(
                f"{tether.constants.failed} | Cannot Disable `{command.name}`!"
            )

        guild_db = tether.db.guilds.find_one({"guild_id": ctx.guild.id})

        if not guild_db:
            tether.db.guilds.insert_one(
                {"guild_id": ctx.guild.id, "cmds": [command.name]}
            )
            return await ctx.reply(
                f"{tether.constants.success} | Command `{command.name}` Disabled For This Server!"
            )

        disabled_cmds = guild_db.get("cmds", [])

        if command.name in disabled_cmds:
            return await ctx.reply(
                f"{tether.constants.failed} | Command `{command.name}` Is Already Disabled!"
            )

        disabled_cmds.append(command.name)
        tether.db.guilds.update_one(
            {"guild_id": ctx.guild.id}, {"$set": {"cmds": disabled_cmds}}
        )

        await ctx.reply(
            f"{tether.constants.success} | Command `{command.name}` Disabled For This Server!"
        )


async def setup(client: commands.Bot):
    await client.add_cog(Disable(client))
