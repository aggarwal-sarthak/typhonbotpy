from discord.ext import commands
from src.core.bot import tether

async def is_command_enabled(ctx):
    guild_id = ctx.guild.id
    guild_info = tether.db.guilds.find_one({"guild_id": guild_id, "cmds": {"$in": [ctx.command.name]}})

    if guild_info:
        await ctx.reply(f"{tether.constants.failed} | The Command `{ctx.command.name}` Is Disabled In This Server!")
        return False
    return True

def command_enabled():
    return commands.check(is_command_enabled)