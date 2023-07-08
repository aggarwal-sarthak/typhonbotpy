from discord.ext import commands
import os
import discord
import datetime,timeago
import pytz

class snipe(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.deleted_messages = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.deleted_messages[message.channel.id] = message

    @commands.bot_has_permissions(embed_links=True)
    @commands.command(description='Returns Last Deleted Messaged In The Channel', usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def snipe(self, ctx):
        if ctx.channel.id not in self.deleted_messages:
            await ctx.reply(f"{self.client.emotes['failed']} | No Deleted Messages Found In This Channel!")
            return

        embed = discord.Embed(title='Message Found',color=0xfb7c04)
        embed.add_field(name="**__Information__**", value=f"**Message By :** {self.deleted_messages[ctx.channel.id].author.mention}\n**Channel :** {ctx.channel.mention}\n**Time :** {timeago.format(self.deleted_messages[ctx.channel.id].created_at.astimezone(pytz.timezone('Asia/Kolkata')).replace(tzinfo=None),datetime.datetime.now())}", inline=False)
        embed.add_field(name="**__Content__**", value=f"{self.deleted_messages[ctx.channel.id].content}", inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
        await ctx.reply(embed=embed)

    @snipe.error
    async def missing_permissions(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            err = str(error).replace('Bot requires ','').replace(' permission(s) to run this command.', '')
            await ctx.reply(f"{self.client.emotes['failed']} | I Don't Have `{err}` Permission To Use This Command!")

async def setup(client):
    await client.add_cog(snipe(client))