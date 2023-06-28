import discord
from discord.ext import commands
import os

class setnick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.command(description='Assigns Given Nickname To Mentioned User',aliases=['nick'], usage=f"{os.path.basename(__file__)[:-3]} <user> [nickname]")
    async def setnick(self, ctx, member:discord.Member=None, *nickname):
        if ctx.guild.owner_id == member.id or ctx.guild.get_member(self.client.user.id).top_role.position <= member.top_role.position:
            await ctx.reply(f"{self.client.emotes['failed']} | My Role Isn't High Enough To Change `{member.name}`'s Nickname!")
        elif ctx.guild.owner_id != ctx.author.id and ctx.author.top_role.position <= member.top_role.position:
            await ctx.reply(f"{self.client.emotes['failed']} | Your Role Isn't High Enough To Change `{member.name}`'s Nickname!")
        
        if not nickname:
            await member.edit(nick=None)
            await ctx.reply(f"{self.client.emotes['success']} | Removed `{member.name}`'s Nickname!")
        else:
            if len(nickname[0])>32:
                ctx.reply(f"{self.client.emotes['failed']} | Nickname Character Limit Exceeded!")
            else:
                await member.edit(nick=nickname[0])
                await ctx.reply(f"{self.client.emotes['success']} | Changed `{member.name}`'s Nickname To `{nickname[0]}`!")

async def setup(client):
    await client.add_cog(setnick(client))