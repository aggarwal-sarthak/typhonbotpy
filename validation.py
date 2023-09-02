from pymongo import MongoClient
import json

with open('emoji.json', 'r') as f:
    emotes = json.load(f)
with open('config.json', 'r') as f:
    config = json.load(f)

try:
    db_client = MongoClient(config["mongodb"])

    print("✅ | Successfully Connected to MongoDB!")
except Exception as e:
    print(e)

async def is_command_enabled(ctx):
    guild_info = db_client.typhonbot.guilds.find_one({"guild_id":ctx.guild.id})
    if(guild_info and 'cmds' in guild_info):
        disabled_commands = guild_info['cmds']
        if(ctx.command.name in disabled_commands):
            await ctx.reply(f"{emotes['failed']} | The command `{ctx.command.name}` is Disabled in this Server!")
            return False
    return True
