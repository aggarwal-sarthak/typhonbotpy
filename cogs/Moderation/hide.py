from discord.ext import commands
import os

class hide(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.command(description='Hides Current/Mentioned Channel(s) For Everyone', usage=f"{os.path.basename(__file__)[:-3]} [channel(s)]", pass_context= True)
    async def hide(self, ctx):
        channels = ctx.message.channel_mentions
        mentions = ""
        if not channels:
            channels = [ctx.channel]
        for c in channels:
            perms = c.overwrites_for(ctx.guild.default_role)
            perms.view_channel = False
            await c.set_permissions(ctx.guild.default_role, overwrite=perms)
            mentions += "<#"+str(c.id)+"> " 
        await ctx.reply(f'{self.client.emotes["success"]} | {mentions} Is Hidden!')

    @hide.error
    async def missing_permissions(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            err = str(error).replace('You are missing ','').replace(' permission(s) to run this command.','')
            await ctx.reply(f"{self.client.emotes['failed']} | You Don't Have `{err}` Permission To Use This Command!")

        if isinstance(error, commands.BotMissingPermissions):
            err = str(error).replace('Bot requires ','').replace(' permission(s) to run this command.', '')
            await ctx.reply(f"{self.client.emotes['failed']} | I Don't Have `{err}` Permission To Use This Command!")

async def setup(client):
    await client.add_cog(hide(client))