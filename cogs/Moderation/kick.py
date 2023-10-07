import discord
from discord.ext import commands
import os
import confirmation
from validation import is_command_enabled

class kick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Kicks the Mentioned User",usage=f"{os.path.basename(__file__)[:-3]} <user> [reason]")
    @commands.check(is_command_enabled)
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self,ctx,user:discord.Member,*reason: str):
        if(len(reason)!=0):
            reason = " ".join([x for x in reason])
        else:
            reason=None

        view = confirmation.Buttons(ctx)
        role = user.top_role

        if(user==ctx.guild.owner):
            return await ctx.reply(f"{self.client.emotes['failed']} | Cannot Kick the Owner!")
            
        if ctx.guild.get_member(self.client.user.id).top_role.position <= role.position:
            return await ctx.reply(f"{self.client.emotes['failed']} | My Role Isn't High Enough To Kick!")

        elif ctx.guild.owner_id != ctx.author.id and ctx.author.top_role.position <= role.position:
            return await ctx.reply(f"{self.client.emotes['failed']} | Your Role Isn't High Enough To Kick!")
        
        msg = await ctx.reply(f"You are about to kick: `{user}`",view=view)
        await view.wait()

        try:
            if view.value == "1":
                if msg: await msg.delete()
                await ctx.guild.kick(user=user,reason=reason)
                return await ctx.reply(f"{self.client.emotes['success']} | <@{user.id}> was kicked successfully!")

            if view.value == "2":
                if msg: await msg.delete()
                return await ctx.reply(f"{self.client.emotes['success']} | Kick Cancelled Successfully!")
        except:
            disable = confirmation.Disabled(ctx)
            return await msg.edit(content=f"You Are About To Kick: `{user}`",view=disable)

async def setup(client):
    await client.add_cog(kick(client))   