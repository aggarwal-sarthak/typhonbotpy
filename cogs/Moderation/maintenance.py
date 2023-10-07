from discord.ext import commands
import os
import discord
import confirmation
from validation import is_command_enabled
    
class maintenance(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(name='maintenance', description='Enables/Disables Maintenance Mode For Server', aliases=['mm', 'mmode'])
    @commands.check(is_command_enabled)
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def maintenance(self, ctx, mode):
        pass

    @maintenance.command(name='on', description='Enables Maintenance Mode For Server', usage=f"{os.path.basename(__file__)[:-3]} on [role]", aliases=['enable'])
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def on(self, ctx, *role: discord.Role):
        if not role: 
            role = ctx.guild.default_role
        else:
            role = discord.utils.get(ctx.guild.roles, id=role[0].id)

        view = confirmation.Buttons(ctx)
        msg = await ctx.reply(f'Enable Maintenance Mode: `{role}`?', view=view)
        await view.wait()
        
        try:
            if view.value == "1":
                if msg: await msg.delete()
                msg = await ctx.reply(f'{self.client.emotes["loading"]} | Enabling Maintenance Mode: `{role}`!')

                for channel in ctx.guild.channels:
                    if not isinstance(channel, discord.CategoryChannel):
                        perms = channel.overwrites_for(role)
                        perms.view_channel = False
                        await channel.set_permissions(role, overwrite=perms)
                if msg: return await msg.edit(content=f'{self.client.emotes["success"]} | Maintenance Mode Enabled: `{role}`!')
                
            if view.value == "2":
                if msg: await msg.delete()
                return await ctx.reply(f"{self.client.emotes['success']} | Maintenance Cancelled Successfully!")
        except:
            disable = confirmation.Disabled(ctx)
            return await msg.edit(content=f'Enable Maintenance Mode: `{role}`?',view=disable)

    @maintenance.command(name='off', description='Disables Maintenance Mode For Server', usage=f"{os.path.basename(__file__)[:-3]} off [role]", aliases=['disable'])
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def off(self, ctx, *role: discord.Role):
        if not role: 
            role = ctx.guild.default_role
        else:
            role = discord.utils.get(ctx.guild.roles, id=role[0].id)

        view = confirmation.Buttons(ctx)
        msg = await ctx.reply(f'Disable Maintenance Mode: `{role}`?', view=view)
        await view.wait()
        
        if view.value == "1":
            if msg: await msg.delete()
            msg = await ctx.reply(f'{self.client.emotes["loading"]} | Disabling Maintenance Mode: `{role}`!')

            for channel in ctx.guild.channels:
                if not isinstance(channel, discord.CategoryChannel):
                    perms = channel.overwrites_for(role)
                    perms.view_channel = True
                    await channel.set_permissions(role, overwrite=perms)
            if msg: return await msg.edit(content=f'{self.client.emotes["success"]} | Maintenance Mode Disabled: `{role}`!')
            
        if view.value == "2":
            if msg: await msg.delete()
            return await ctx.reply(f"{self.client.emotes['success']} | Maintenance Cancelled Successfully!")

async def setup(client):
    await client.add_cog(maintenance(client))