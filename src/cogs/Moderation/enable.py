import os
from discord.ext import commands
from src.core.bot import tether
from src.core.check import command_enabled


class Enable(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(
        usage=f"{os.path.basename(__file__)[:-3]} <command>",
        description="Enables The Mentioned Command",
        aliases=["en"],
    )
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @command_enabled()
    async def enable(self, ctx: commands.Context, cmnd: str):
        command = self.client.get_command(cmnd)

        if command is None:
            return await ctx.reply(
                f"{tether.constants.failed} | {cmnd} Is Not A Command!"
            )

        guild_db = tether.db.guilds.find_one({"guild_id": ctx.guild.id})
        if (
            not guild_db
            or "cmds" not in guild_db
            or command.name not in guild_db["cmds"]
        ):
            return await ctx.reply(
                f"{tether.constants.failed} | Command `{command.name}` Is Already Enabled!"
            )

        cmds = guild_db["cmds"]
        cmds.remove(command.name)
        tether.db.guilds.update_one(
            {"guild_id": ctx.guild.id}, {"$set": {"cmds": cmds}}
        )

        await ctx.reply(
            f"{tether.constants.success} | Command `{command.name}` Enabled For This Server!"
        )


async def setup(client: commands.Bot):
    await client.add_cog(Enable(client))
