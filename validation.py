from pymongo import MongoClient
import json
with open('emoji.json', 'r') as f:
    emotes = json.load(f)


try:
    uri = "mongodb+srv://TyphonBotDB:sarthak13@typhonbotcluster.dxwct.mongodb.net/?retryWrites=true&w=majority"
    db_client = MongoClient(uri)


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
