import discord
from discord.ext import commands
import os
import confirmation
from validation import is_command_enabled
import pagination
import re
from types import SimpleNamespace
import aiohttp
from io import BytesIO
import json
import asyncio

with open('emoji.json', 'r') as f:
    emotes = json.load(f)


class modcmd(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.embeds = []
        self.mem_dict = {}

    @commands.command(description="Bans Member from the Server",usage=f"{os.path.basename(__file__)[:-3]} <user> [reason]")
    @commands.check(is_command_enabled)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *reason: str):
        if(len(reason)!=0):
            reason = " ".join([x for x in reason])
        else:
            reason=None

        view = confirmation.Buttons(ctx)
        role = user.top_role

        if(user == ctx.guild.owner):
            return await ctx.reply(f"{self.client.emotes['failed']} | Cannot Ban the Owner!")
            
        if ctx.guild.get_member(self.client.user.id).top_role.position <= role.position:
            return await ctx.reply(f"{self.client.emotes['failed']} | My Role Isn't High Enough To Ban!")

        elif ctx.guild.owner_id != ctx.author.id and ctx.author.top_role.position <= role.position:
            return await ctx.reply(f"{self.client.emotes['failed']} | Your Role Isn't High Enough To Ban!")
        
        msg = await ctx.reply(f"You Are About To Ban: `{user}`",view=view)
        await view.wait()
        try:
            if view.value == "1":
                if msg: await msg.delete()
                await ctx.guild.ban(user=user,reason=reason,delete_message_seconds=0)
                return await ctx.reply(f"{self.client.emotes['success']} | <@{user.id}> Was Banned successfully!")

            if view.value == "2":
                if msg: await msg.delete()
                return await ctx.reply(f"{self.client.emotes['success']} | Ban Cancelled Successfully!")
        except:
            disable = confirmation.Disabled(ctx)
            return await msg.edit(content=f"You Are About To Ban: `{user}`",view=disable)

    @commands.command(name = "config",
                    usage=f"{os.path.basename(__file__)[:-3]}",
                    description = "Shows the Bot configuration for the server",
                    aliases=["configuration","settings","setting"])
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def config(self, ctx:commands.Context):
        guild = self.client.db.guilds.find_one({"guild_id":ctx.guild.id})
        if guild and "prefix" in guild:
            prefix = guild['prefix']
        else:
            prefix = self.client.config['prefix']
        embed = discord.Embed(title="Server Configuration",color=self.client.config['color'])
        embed.add_field(name="Prefix:",value=f"`{prefix}`")
        embed.add_field(name="Disabled Commands:",value=f"`{'`,`'.join([cmd for cmd in guild['cmds']]) if guild and len(guild['cmds'])>0 else 'None'}`",inline=False)
        # enabled_command = ""
        # for folder in os.listdir('./cogs'):
        #     if(folder == "Developer"): continue
        #     enabled_command += f"`{'`, `'.join([filename[:-3] for filename in os.listdir(f'./cogs/{folder}') if filename.endswith('.py')])}`"
        # embed.add_field(name="Enabled Commands:",value=enabled_command)
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
        await ctx.reply(embed=embed)

    @commands.command(usage=f"{os.path.basename(__file__)[:-3]} <command>", description = "Disables The Mentioned Command", aliases=["dis"])
    @commands.check(is_command_enabled)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def disable(self, ctx:commands.Context, cmnd: str):
        command = self.client.get_command(cmnd)
        if(command.name=="disable" or command.name=="enable"):
            return await ctx.reply(f"{self.client.emotes['failed']} | Cannot Disable `{command.name}`!")
            
        if command is None: await ctx.reply(f"{self.client.emotes['failed']} | {cmnd} Is Not A Command!")
        guild_db = self.client.db.guilds.find_one({"guild_id":ctx.guild.id})

        if not guild_db:
            self.client.db.guilds.insert_one({
                "guild_id": ctx.guild.id,
                "cmds": [command.name]
            })
            return await ctx.reply(f"{self.client.emotes['success']} | Command `{command.name}` Disabled For This Server!")
        
        if('cmds' in guild_db):
            cmds = guild_db['cmds']
            if(command.name in cmds):
                return await ctx.reply(f"{self.client.emotes['failed']} | Command `{command.name}` Is Already Disabled!")
                
            cmds.append(command.name)
        else:
            cmds = [command.name]

        self.client.db.guilds.update_one({"guild_id":ctx.guild.id},{"$set":{"cmds":cmds}})
        await ctx.reply(f"{self.client.emotes['success']} | Command `{command.name}` Disabled For This Server!")

    @commands.command(usage=f"{os.path.basename(__file__)[:-3]} <command>", description = "Enables The Mentioned Command", aliases=["en"])
    @commands.check(is_command_enabled)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def enable(self, ctx:commands.Context, cmnd: str):
        command = self.client.get_command(cmnd)
        if command is None: await ctx.reply(f"{self.client.emotes['failed']} | {cmnd} Is Not A Command!")
        
        guild_db = self.client.db.guilds.find_one({"guild_id":ctx.guild.id})
        if(not guild_db or 'cmds' not in guild_db):
            await ctx.reply(f"{self.client.emotes['failed']} | Command `{command.name}` Is Already Enabled!")
            
        else:
            cmds = guild_db['cmds']
            if command.name in cmds:
                cmds.remove(command.name)
                self.client.db.guilds.update_one({"guild_id":ctx.guild.id},{"$set":{"cmds":cmds}})
                await ctx.reply(f"{self.client.emotes['success']} | Command `{command.name}` Enabled For This Server!")
            else:
                await ctx.reply(f"{self.client.emotes['failed']} | Command `{command.name}` Is Already Enabled!")

    @commands.group(description='Hides Current/Mentioned Channel(s) For Everyone', usage=f"{os.path.basename(__file__)[:-3]} [channel(s)]", invoke_without_command=True)
    @commands.check(is_command_enabled)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
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

    @hide.command(name='text', description='Hides All Text Channel(s) For Everyone', aliases=['texts'], usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def text(self, ctx):
        count = 0
        msg = await ctx.reply(f'{self.client.emotes["loading"]} | Hiding Text Channels!')
        for c in ctx.guild.text_channels:
            perms = c.overwrites_for(ctx.guild.default_role)
            perms.view_channel = False
            await c.set_permissions(ctx.guild.default_role, overwrite=perms)
            count += 1
        if msg: await msg.edit(content=f'{self.client.emotes["success"]} | `{count}` Text Channels Hidden!')

    @hide.command(name='voice', description='Hides All Voice Channel(s) For Everyone', aliases=['vc','vcs'], usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def text(self, ctx):
        count = 0
        msg = await ctx.reply(f'{self.client.emotes["loading"]} | Hiding Voice Channels!')
        for c in ctx.guild.voice_channels:
            perms = c.overwrites_for(ctx.guild.default_role)
            perms.view_channel = False
            await c.set_permissions(ctx.guild.default_role, overwrite=perms)
            count += 1
        if msg: await msg.edit(content=f'{self.client.emotes["success"]} | `{count}` Voice Channels Hidden!')

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


    @commands.group(name='list', description='Returns List', usage=f'{os.path.basename(__file__)[:-3]} <subcommand>', aliases=['dump'], invoke_without_command=True)
    @commands.check(is_command_enabled)
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def list(self, ctx, role: discord.Role):
        data = [member for member in role.members]
        title = f"Members In Role : {len(data)}"
        await mention_pagination(self, ctx, data, self.embeds, title)
    
    @list.command(name='admins', description='Returns List of Admins', aliases=['admin', 'administrator'])
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def admins(self, ctx):
        data = [member for member in ctx.guild.members if member.guild_permissions.administrator and member.bot==False]
        title = f"Admins : {len(data)}"
        await mention_pagination(self, ctx, data, self.embeds, title)

    @list.command(name='bans', description='Returns List of Banned Members', aliases=['ban', 'banned'])
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True, ban_members=True)
    async def bans(self, ctx):
        data = [ban.user async for ban in ctx.guild.bans()]
        title = f"Bans : {len(data)}"
        await mention_pagination(self, ctx, data, self.embeds, title)

    @list.command(name='boosters', description='Returns List of Server Boosters', aliases=['booster', 'premium'])
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def boosters(self, ctx):
        data = [member for member in ctx.guild.premium_subscribers]
        title = f"Boosters : {len(data)}"
        await mention_pagination(self, ctx, data, self.embeds, title)

    @list.command(name='bots', description='Returns List of Bots', aliases=['bot'])
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def bots(self, ctx):
        data = [member for member in ctx.guild.members if member.bot]
        title = f"Bots : {len(data)}"
        await mention_pagination(self, ctx, data, self.embeds, title)

    @list.command(name='emojis', description='Returns List of Server Emojis', aliases=['emoji', 'emo'])
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def emojis(self, ctx):
        data = [emoji for emoji in ctx.guild.emojis]
        title = f"Emojis : {len(data)}"
        for i in range(0,len(data), 20):
            description = ""
            for j in range(i, min(i+20, len(data))):
                description += f"**{str(j+1)}** : {data[j]} : `{data[j].name}`\n"
            pagination_embed = discord.Embed(title=title, description=description,color=self.client.config['color'])
            pagination_embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
            self.embeds.append(pagination_embed)
        await pagination_check(self, ctx, data, self.embeds)

    @list.command(name='roles', description='Returns List of Roles', aliases=['role'])
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def roles(self, ctx):
        data = [roles for roles in ctx.guild.roles]
        data.reverse()
        title = f"Roles : {len(data)}"
        for i in range(0,len(data), 20):
            description = ""
            for j in range(i, min(i+20, len(data))):
                description += "**" + str(j+1) + "** : " + str(data[j].mention) + " `" + str(data[j].id) + "`" + "\n"
            pagination_embed = discord.Embed(title=title, description=description,color=self.client.config['color'])
            pagination_embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
            self.embeds.append(pagination_embed)
        await pagination_check(self, ctx, data, self.embeds)

    @list.command(name='vc', description='Returns List of Voice Channels', aliases=['vcs', 'voice'])
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def vc(self, ctx):
        data = [chan for chan in ctx.guild.voice_channels]
        title = f"Voice Channels : {len(data)}"
        await mention_pagination(self, ctx, data, self.embeds, title)

    @list.command(name='text', description='Returns List of Text Channels', aliases=['texts'])
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def text(self, ctx):
        data = [chan for chan in ctx.guild.text_channels]
        title = f"Text Channels : {len(data)}"
        await mention_pagination(self, ctx, data, self.embeds, title)

    @commands.group(description='Locks Current/Mentioned Channel(s) For Everyone', usage=f"{os.path.basename(__file__)[:-3]} [channel(s)]", invoke_without_command=True)
    @commands.check(is_command_enabled)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def lock(self, ctx):
        channel = ctx.message.channel_mentions
        mentions = ""
        if not channel:
            channel = [ctx.channel]
            
        for c in channel:
            perms = c.overwrites_for(ctx.guild.default_role)
            perms.send_messages=False
            await c.set_permissions(ctx.guild.default_role, overwrite=perms)
            mentions += "<#"+str(c.id)+"> " 
        await ctx.reply(f'{self.client.emotes["success"]} | {mentions} Is Locked!')

    @lock.command(name='all', description='Locks All Channels For Everyone', usage=f"{os.path.basename(__file__)[:-3]} [channel(s)]")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(administrator=True)
    async def all(self, ctx):
        count = 0
        msg = await ctx.reply(f'{self.client.emotes["loading"]} | Locking Channels!')
        for channel in ctx.guild.channels:
            if not isinstance(channel, discord.CategoryChannel):
                perms = channel.overwrites_for(ctx.guild.default_role)
                perms.send_messages=False
                await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
                count += 1
        if msg: await msg.edit(content=f'{self.client.emotes["success"]} | `{count}` Channels Are Locked!')

    @lock.command(name='text', description='Locks All Text Channel(s) For Everyone', aliases=['texts'], usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def text(self, ctx):
        count = 0
        msg = await ctx.reply(f'{self.client.emotes["loading"]} | Locking Text Channels!')
        for c in ctx.guild.text_channels:
            perms = c.overwrites_for(ctx.guild.default_role)
            perms.send_messages=False
            await c.set_permissions(ctx.guild.default_role, overwrite=perms)
            count += 1
        if msg: await msg.edit(content=f'{self.client.emotes["success"]} | `{count}` Text Channels Locked!')

    @lock.command(name='voice', description='Locks All Voice Channel(s) For Everyone', aliases=['vc','vcs'], usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def text(self, ctx):
        count = 0
        msg = await ctx.reply(f'{self.client.emotes["loading"]} | Locking Voice Channels!')
        for c in ctx.guild.voice_channels:
            perms = c.overwrites_for(ctx.guild.default_role)
            perms.send_messages=False
            await c.set_permissions(ctx.guild.default_role, overwrite=perms)
            count += 1
        if msg: await msg.edit(content=f'{self.client.emotes["success"]} | `{count}` Voice Channels Locked!')


    @commands.group(name='maintenance', description='Enables/Disables Maintenance Mode For Server', aliases=['mm', 'mmode'], invoke_without_command=True)
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

    @commands.group(name='purge', description='Clears Messages For Given Parameters', aliases = ['clear'], usage = f"{os.path.basename(__file__)[:-3]} <amount>", invoke_without_command=True)
    @commands.check(is_command_enabled)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        def check(message):
            return not message.pinned
        await delete(self, ctx, amount, check)

    @purge.command(name='bots', description='Clears Messages For Bots', aliases = ['bot', 'b'], usage = f"{os.path.basename(__file__)[:-3]} bots <amount>")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def bots(self, ctx, amount: int):
        def check(message):
            return not message.pinned and message.author.bot
        await delete(self, ctx, amount, check)

    @purge.command(name='humans', description='Clears Messages For Humans', aliases = ['human', 'h'], usage = f"{os.path.basename(__file__)[:-3]} humans <amount>")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def humans(self, ctx, amount: int):
        def check(message):
            return not message.pinned and not message.author.bot
        await delete(self, ctx, amount, check)

    @purge.command(name='embeds', description='Clears Embeds', aliases = ['embed', 'e'], usage = f"{os.path.basename(__file__)[:-3]} embeds <amount>")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def embeds(self, ctx, amount: int):
        def check(message):
            return not message.pinned and message.embeds
        await delete(self, ctx, amount, check)

    @purge.command(name='images', description='Clears Images', aliases = ['image', 'img', 'imgs'], usage = f"{os.path.basename(__file__)[:-3]} images <amount>")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def images(self, ctx, amount: int):
        def check(message):
            return not message.pinned and (message.attachments or ('.jpg' or '.jpeg' or '.png' or '.webp') in message.content)
        await delete(self, ctx, amount, check)
        

    @commands.group(description='Role Management', usage=f"{os.path.basename(__file__)[:-3]} <subcommand>", invoke_without_command=True)
    @commands.check(is_command_enabled)
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def role(self, ctx, mode):
        pass

    @role.group(name='add', description='Add Role(s) To Members', aliases = ['give', 'a'], usage = f"{os.path.basename(__file__)[:-3]} add <subcommand>", invoke_without_command=True)
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def add(self, ctx, *ids):
        await parse_ids(self, ctx, ids, 'add')

    @add.command(name='all', description='Add Role To All Members Of Server', usage = f"{os.path.basename(__file__)[:-3]} add all")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def add_all(self, ctx, *ids: discord.Role):
        for i in ids:
            self.mem_dict[i.id] = [m.id for m in ctx.guild.members if not i in m.roles]
        await confirm(self, ctx, self.mem_dict, 'add')

    @add.command(name='humans', description='Add Role To Human Members Of Server', usage = f"{os.path.basename(__file__)[:-3]} add humans")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def add_humans(self, ctx, *ids: discord.Role):
        for i in ids:
            self.mem_dict[i.id] = [m.id for m in ctx.guild.members if not i in m.roles and not m.bot]
        await confirm(self, ctx, self.mem_dict, 'add')

    @add.command(name='bots', description='Add Role To Bot Members Of Server', usage = f"{os.path.basename(__file__)[:-3]} add bots")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def add_bots(self, ctx, *ids: discord.Role):
        for i in ids:
            self.mem_dict[i.id] = [m.id for m in ctx.guild.members if not i in m.roles and m.bot]
        await confirm(self, ctx, self.mem_dict, 'add')

    @role.group(name='remove', description='Removes Role(s) From Members', aliases = ['take', 'r'], usage = f"{os.path.basename(__file__)[:-3]} remove <subcommand>", invoke_without_command=True)
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def remove(self, ctx, *ids):
        await parse_ids(self, ctx, ids, 'remove')

    @remove.command(name='all', description='Remove Role From All Members Of Server', usage = f"{os.path.basename(__file__)[:-3]} remove all")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def remove_all(self, ctx, *ids: discord.Role):
        for i in ids:
            self.mem_dict[i.id] = [m.id for m in ctx.guild.members if i in m.roles]
        await confirm(self, ctx, self.mem_dict, 'remove')

    @remove.command(name='humans', description='Remove Role From Human Members Of Server', usage = f"{os.path.basename(__file__)[:-3]} remove humans")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def remove_humans(self, ctx, *ids: discord.Role):
        for i in ids:
            self.mem_dict[i.id] = [m.id for m in ctx.guild.members if i in m.roles and not m.bot]
        await confirm(self, ctx, self.mem_dict, 'remove')

    @remove.command(name='bots', description='Remove Role From Bot Members Of Server', usage = f"{os.path.basename(__file__)[:-3]} remove bots")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def remove_bots(self, ctx, *ids: discord.Role):
        for i in ids:
            self.mem_dict[i.id] = [m.id for m in ctx.guild.members if i in m.roles and m.bot]
        await confirm(self, ctx, self.mem_dict, 'remove')

    @commands.command(description='Assigns Given Nickname To Mentioned User',aliases=['nick'], usage=f"{os.path.basename(__file__)[:-3]} <user> [nickname]")
    @commands.check(is_command_enabled)
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    async def setnick(self, ctx, member:discord.Member, *nickname):
        if ctx.guild.owner_id == member.id or ctx.guild.get_member(self.client.user.id).top_role.position <= member.top_role.position:
            return await ctx.reply(f"{self.client.emotes['failed']} | My Role Isn't High Enough To Change `{member.name}`'s Nickname!")

        elif ctx.guild.owner_id != ctx.author.id and ctx.author.top_role.position <= member.top_role.position:
            return await ctx.reply(f"{self.client.emotes['failed']} | Your Role Isn't High Enough To Change `{member.name}`'s Nickname!")
        
        if not nickname:
            await member.edit(nick=None)
            await ctx.reply(f"{self.client.emotes['success']} | Removed `{member.name}`'s Nickname!")
        else:
            if len(nickname[0])>32:
                ctx.reply(f"{self.client.emotes['failed']} | Nickname Character Limit Exceeded!")
            else:
                await member.edit(nick=nickname[0])
                await ctx.reply(f"{self.client.emotes['success']} | Changed `{member.name}`'s Nickname To `{nickname[0]}`!")

    @commands.command(description= "Sets The Mentioned Symbol As Server Prefix", aliases=['set','sp','setpre','prefix'], usage=f"{os.path.basename(__file__)[:-3]} <Symbol>" )
    @commands.check(is_command_enabled)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def setprefix(self, ctx, symbol:str):
        guild_db = self.client.db.guilds.find_one({"guild_id":ctx.guild.id})
        
        if(len(symbol)>4):
            return await ctx.reply(f"{self.client.emotes['failed']} | Prefix Cannot Be Longer Than 4 Characters!")
        
        if not guild_db and symbol != self.client.config["prefix"]:
            self.client.db.guilds.insert_one({
                "guild_id": ctx.guild.id,
                "prefix": symbol
            })
        elif symbol != self.client.config["prefix"]:
            self.client.db.guilds.update_one({"guild_id":ctx.guild.id},{"$set":{"prefix":symbol}})
        else:
            self.client.db.guilds.update_one({"guild_id":ctx.guild.id},{"$unset":{"prefix":""}})
        await ctx.reply(f"{self.client.emotes['success']} | Prefix Updated To: `{symbol}`")

    @commands.command(description="Add Emotes and Stickers to Server",aliases=['add'],usage=f"{os.path.basename(__file__)[:-3]} <emote>")
    @commands.check(is_command_enabled)
    @commands.has_permissions(manage_expressions=True)
    @commands.bot_has_permissions(manage_expressions=True)
    async def steal(self, ctx,*args):
        emoji = []
        if(ctx.message.reference is not None):
            msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            if(len(msg.stickers)>0):
                sticker = msg.stickers[0]
            else:
                emoji = msg.content.split()     #needs emoji verification
        else:
            if(len(args)>0):
                for em in args:
                    emoji.append(em)            #needs verif
            elif(len(ctx.message.stickers)>0):
                sticker = ctx.message.stickers[0]
            else:
                await ctx.reply(f"{self.client.emotes['failed']}| No emojis or stickers found!")
                return
        
        if(len(emoji)>0):
            for emote in emoji:
                if('<' not in emote or '>' not in emote or ':' not in emote):
                    emoji.remove(emote)
            if(len(emoji)>0):
                name, url = await get_name_url(emoji)
                await send_view(self,ctx,emoji,name,url)
            else:
                await ctx.reply(f"{self.client.emotes['failed']}| No emojis or stickers found!")
                return
        elif(sticker):
            sticker_list = [sticker]
            name = [sticker.name]
            url = [sticker.url]
            await send_view(self,ctx,sticker_list,name,url)
        else:
            pass

    @commands.group(name='unban', description="Unbans Member from the Server",usage=f"{os.path.basename(__file__)[:-3]} <user> [reason]", invoke_without_command=True)
    @commands.check(is_command_enabled)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, user: int, *reason: str):
        banned = [entry.user.id async for entry in ctx.guild.bans()]
        if user not in banned:
            return await ctx.reply(f"{self.client.emotes['failed']} | {user} Was Not Found In Ban list!")
            
        if(len(reason)!=0):
            reason = " ".join([x for x in reason])
        else:
            reason = None

        view = confirmation.Buttons(ctx)
        user = await self.client.fetch_user(user)

        msg = await ctx.reply(f"You Are About To Unban: `{user}`",view=view)
        await view.wait()

        try:
            if view.value == "1":
                if msg: await msg.delete()
                await ctx.guild.unban(user=user,reason=reason)
                return await ctx.reply(f"{self.client.emotes['success']} | <@{user.id}> Was Unbanned Successfully!")
    
            if view.value == "2":
                if msg: await msg.delete()
                return await ctx.reply(f"{self.client.emotes['success']} | Unban Cancelled Successfully!")
        except:
            disable = confirmation.Disabled(ctx)
            return await msg.edit(content=f"You Are About To Unban: `{user}`",view=disable)
        
    @unban.command(name='all', description="Unbans Member from the Server",usage=f"{os.path.basename(__file__)[:-3]} all [reason]")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(ban_members=True)
    async def all(self, ctx, *reason: str):
        banned = [entry.user.id async for entry in ctx.guild.bans()]
        if len(banned) < 0:
            await ctx.reply(f"{self.client.emotes['failed']} | No Banned Members Found!")
        if(len(reason) != 0):
            reason = " ".join([x for x in reason])
        else:
            reason = None

        view = confirmation.Buttons(ctx)
        msg = await ctx.reply(f"You Are About To Unban: `{len(banned)}` Members",view=view)
        await view.wait()
        
        try:
            if view.value == "1":
                if msg: await msg.delete()
                msg = await ctx.reply(f'{self.client.emotes["loading"]} | Unbanning `{len(banned)}` Members!')

                for user in banned:
                    user = await self.client.fetch_user(user)
                    await ctx.guild.unban(user=user,reason=reason)
                if msg: await msg.delete()
                return await ctx.reply(f"{self.client.emotes['success']} | `{len(banned)}` Members Were Unbanned Successfully!")
    
            if view.value == "2":
                if msg: await msg.delete()
                return await ctx.reply(f"{self.client.emotes['success']} | Unban Cancelled Successfully!")
        except:
            disable = confirmation.Disabled(ctx)
            return await msg.edit(content=f"You Are About To Unban: `{len(banned)}` Members",view=disable)
    
    @commands.group(description='Unhides Current/Mentioned Channel(s) For Everyone', usage=f"{os.path.basename(__file__)[:-3]} [channel(s)]", invoke_without_command=True)
    @commands.check(is_command_enabled)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def unhide(self, ctx):
        channel = ctx.message.channel_mentions
        mentions = ""
        if not channel:
            channel = [ctx.channel]
            
        for c in channel:
            perms = c.overwrites_for(ctx.guild.default_role)
            perms.view_channel = True
            await c.set_permissions(ctx.guild.default_role, overwrite=perms)
            mentions += "<#"+str(c.id)+"> " 
        await ctx.reply(f'{self.client.emotes["success"]} | {mentions} Is Unhidden!')

    @unhide.command(name='text', description='Unhides All Text Channel(s) For Everyone', usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def text(self, ctx):
        count = 0
        msg = await ctx.reply(f'{self.client.emotes["loading"]} | Unhiding Text Channels!')
        for c in ctx.guild.text_channels:
            perms = c.overwrites_for(ctx.guild.default_role)
            perms.view_channel = True
            await c.set_permissions(ctx.guild.default_role, overwrite=perms)
            count += 1
        if msg: await msg.edit(content=f'{self.client.emotes["success"]} | `{count}` Text Channels Unhidden!')

    @unhide.command(name='voice', description='Unhides All Voice Channel(s) For Everyone', aliases=['vc','vcs'], usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def voice(self, ctx):
        count = 0
        msg = await ctx.reply(f'{self.client.emotes["loading"]} | Unhiding Voice Channels!')
        for c in ctx.guild.voice_channels:
            perms = c.overwrites_for(ctx.guild.default_role)
            perms.view_channel = True
            await c.set_permissions(ctx.guild.default_role, overwrite=perms)
            count += 1
        if msg: await msg.edit(content=f'{self.client.emotes["success"]} | `{count}` Voice Channels Unhidden!')

    @commands.group(description='Unlocks Current/Mentioned Channel(s) For Everyone', usage=f"{os.path.basename(__file__)[:-3]} [channel(s)]", invoke_without_command=True)
    @commands.check(is_command_enabled)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        channel = ctx.message.channel_mentions
        mentions = ""
        if not channel:
            channel = [ctx.channel]
            
        for c in channel:
            perms = c.overwrites_for(ctx.guild.default_role)
            perms.send_messages=True
            await c.set_permissions(ctx.guild.default_role, overwrite=perms)
            mentions += "<#"+str(c.id)+"> " 
        await ctx.replys(f'{self.client.emotes["success"]} | {mentions} Is Unlocked!')

    @unlock.command(name='all', description='Unlocks All Channels For Everyone', usage=f"{os.path.basename(__file__)[:-3]} [channel(s)]")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(administrator=True)
    async def all(self, ctx):
        count = 0
        msg = await ctx.reply(f'{self.client.emotes["loading"]} | Unlocking Channels!')
        for channel in ctx.guild.channels:
            if not isinstance(channel, discord.CategoryChannel):
                perms = channel.overwrites_for(ctx.guild.default_role)
                perms.send_messages=True
                await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
                count += 1
        if msg: await msg.edit(content=f'{self.client.emotes["success"]} | `{count}` Channels Are Unlocked!')

    @unlock.command(name='text', description='Unlocks All Text Channel(s) For Everyone', aliases=['texts'], usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def text(self, ctx):
        count = 0
        msg = await ctx.reply(f'{self.client.emotes["loading"]} | Unlocking Text Channels!')
        for c in ctx.guild.text_channels:
            perms = c.overwrites_for(ctx.guild.default_role)
            perms.send_messages=False
            await c.set_permissions(ctx.guild.default_role, overwrite=perms)
            count += 1
        if msg: await msg.edit(content=f'{self.client.emotes["success"]} | `{count}` Text Channels Unlocked!')

    @unlock.command(name='voice', description='Unlocks All Voice Channel(s) For Everyone', aliases=['vc','vcs'], usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def text(self, ctx):
        count = 0
        msg = await ctx.reply(f'{self.client.emotes["loading"]} | Unlocking Voice Channels!')
        for c in ctx.guild.voice_channels:
            perms = c.overwrites_for(ctx.guild.default_role)
            perms.send_messages=False
            await c.set_permissions(ctx.guild.default_role, overwrite=perms)
            count += 1
        if msg: await msg.edit(content=f'{self.client.emotes["success"]} | `{count}` Voice Channels Unlocked!')

    @commands.command(description='Voicekick A User From Voice Channel',aliases = ['vk', 'vkick'], usage=f"{os.path.basename(__file__)[:-3]} <user>")
    @commands.check(is_command_enabled)
    @commands.has_guild_permissions(move_members=True)
    @commands.bot_has_guild_permissions(move_members=True)
    async def voicekick(self, ctx, member: discord.Member):
        vcstate = member.voice
        if not vcstate or not vcstate.channel:
            return await ctx.reply(f"{self.client.emotes['failed']} | `{member}` Is Not In Any Voice Channel!")
        
        try:
            await member.move_to(None)
            await ctx.reply(f"{self.client.emotes['success']} | `{member}` Kicked From Voice Channel!")
        except Exception as e:
            await ctx.reply(f"{self.client.emotes['failed']} | `{member}` Cannot Be Kicked From Voice Channel!")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member == self.client.user and (before.channel and after.channel) != None and before.channel != after.channel:
            oldmem = before.channel.members if before.channel else []
            await self.move(before.channel, after.channel, oldmem)

    async def move(self, old, new, oldmem):
        for member in oldmem:
            await member.move_to(new)
        voice_client = discord.utils.get(self.client.voice_clients, guild=new.guild)
        await voice_client.disconnect()

    @commands.command(description='Voicemoves All Users From Voice Channel To Another',aliases = ['vm', 'vmove'], usage=f"{os.path.basename(__file__)[:-3]} <user>")
    @commands.check(is_command_enabled)
    @commands.has_guild_permissions(move_members=True)
    @commands.bot_has_guild_permissions(move_members=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def voicemove(self, ctx, *id: discord.VoiceChannel):
        if not ctx.author.voice:
            return await ctx.reply(f"{self.client.emotes['failed']} | You Need To Be In A Voice Channel To Use This Command!")
        
        if id:
            mem = ctx.author.voice.channel.members
            for i in mem:
                await i.move_to(id[0])
        
        if not id:
            channel = ctx.author.voice.channel
            try:
                await channel.connect()
                await ctx.reply(f"{self.client.emotes['success']} | Move Me To New Channel To Start Voicemove!")
                await self.client.wait_for('voice_state_update', timeout=30)

            except discord.ClientException:
                await ctx.reply(f"{self.client.emotes['failed']} | I'm Already Connect To A Voice Channel!")

            except asyncio.TimeoutError:
                await ctx.reply(f"{self.client.emotes['failed']} | Command Timed Out!")
                voice_client = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
                await voice_client.disconnect()

            except Exception as e:
                await ctx.reply(f"{self.client.emotes['failed']} | Error Connecting To Voice Channel!")

async def action(self, ctx, members, msg, mode):
    dict = {}
    for value in members:
        success, failed = 0, 0
        try:
            for mem in members[value]:
                if mode == 'add':
                    await ctx.guild.get_member(mem).add_roles(ctx.guild.get_role(value))
                elif mode == 'remove':
                    await ctx.guild.get_member(mem).remove_roles(ctx.guild.get_role(value))
                success += 1
        except discord.HTTPException:
            failed += 1
        dict[ctx.guild.get_role(value).name] = [success, failed]

    desc = ''
    for i in dict:
        desc += f'{self.client.emotes["success"]} | **Role:** `{i}`, **Success:** `{dict[i][0]}`, **Failed:** `{dict[i][1]}`\n'
    
    if msg: await msg.edit(content=desc)

async def confirm(self, ctx, members, mode):
    if not members: raise commands.MissingRequiredArgument(SimpleNamespace(displayed_name="ids"))
    
    for role in members:
        role = ctx.guild.get_role(role)
        if ctx.guild.get_member(self.client.user.id).top_role.position <= role.position:
            return await ctx.reply(f"{self.client.emotes['failed']} | My Role Isn't High Enough To Assign The Role `{role.name}`!")

        elif ctx.guild.owner_id != ctx.author.id and ctx.author.top_role.position <= role.position:
            return await ctx.reply(f"{self.client.emotes['failed']} | Your Role Isn't High Enough To Assign The Role `{role.name}`!")

    desc = ''
    for i in members:
        desc += f'**Role:** `{ctx.guild.get_role(i).name}`, **Members:** `{len(members[i])}`\n'
    
    if mode == 'add': title = 'Do You Want To Add Roles?'
    elif mode == 'remove': title = 'Do You Want To Remove Roles?'

    view = confirmation.Buttons(ctx)
    embed = discord.Embed(title=title,description=desc,color=self.client.config['color'])

    msg = await ctx.reply(embed=embed,view=view)
    await view.wait()

    try:
        if view.value == '1':
            if msg: await msg.delete()
            msg = await ctx.reply(f'{self.client.emotes["loading"]} | Command Executing...!')
            await action(self, ctx, members, msg, mode)

        elif view.value == '2':
            if msg: await msg.delete()
            await ctx.reply(f'{self.client.emotes["failed"]} | Command Cancelled!')
    except:
        disable = confirmation.Disabled(ctx)
        return await msg.edit(embed=embed, view=disable)
    
    self.mem_dict = {}
        
async def parse_ids(self, ctx, ids, mode):
    mem_dict = {}
    members = []
    roles = []
    matches = re.findall(r'\d+', str(ids))

    ids = [int(match) for match in matches]

    for id in ids:
        member = ctx.guild.get_member(id)
        if member:
            members.append(id)
        role = ctx.guild.get_role(id)
        if role:
            roles.append(id)

    if mode == 'add':
        for r in roles:
            mem_dict[r] = [m for m in members if ctx.guild.get_role(r) not in ctx.guild.get_member(m).roles]
    elif mode == 'remove':
        for r in roles:
            mem_dict[r] = [m for m in members if ctx.guild.get_role(r) in ctx.guild.get_member(m).roles]
    await confirm(self, ctx, mem_dict, mode)


async def delete(self, ctx, amount, check):
    await ctx.message.delete()
    msgs = await ctx.channel.purge(limit=amount, check=check)
    await ctx.channel.send(f'{self.client.emotes["success"]} | {len(msgs)} Messages Deleted Successfully!')

async def mention_pagination(self, ctx, data, embeds, title):
    for i in range(0,len(data), 20):
        description = ""
        for j in range(i, min(i+20, len(data))):
            description += "**" + str(j+1) + "** : " +  str(data[j]) + " [" + str(data[j].mention) + "]" + "\n"
        pagination_embed = discord.Embed(title=title, description=description,color=self.client.config['color'])
        pagination_embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
        embeds.append(pagination_embed)
    await pagination_check(self,ctx,data, embeds)

async def pagination_check(self,ctx,data,embeds):
    if len(data)>20:
        await pagination.Simple(timeout=60).start(ctx, pages=embeds)
    elif (len(data)<20 and len(data)>0):
        await ctx.reply(embed=embeds[0])
    else:
        await ctx.reply(f"{self.client.emotes['failed']} | No Members To Show!")
    self.embeds = []

async def send_view(self,ctx,emoji,name,url,page=0):
    if(len(emoji)==0): return
    guild = ctx.guild
    embed = await create_embed(url,page)
    view = Buttons(ctx)
    msg = await ctx.reply(embed=embed,view=view)
    await view.wait()
    if view.value == "1":
        if msg: await msg.delete()
        if(page==0):
            await ctx.reply("Cannot go back!")
            await send_view(self,ctx,emoji,name,url,page)
        else:
            page -= 1
            await send_view(self,ctx,emoji,name,url,page)
        return False
    if view.value == "2":
        if msg: await msg.delete()
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url[page]) as r:
                try:
                    img_or_gif = BytesIO(await r.read())
                    b_value = img_or_gif.getvalue()
                    if r.status in range(200, 299):
                        emj = await guild.create_custom_emoji(image=b_value, name=name[page].replace(' ','_'))
                        await ctx.send(f'{self.client.emotes["success"]} | Successfully created emoji: <{"a" if emj.animated else ""}:{emj.name}:{emj.id}>')
                        emoji.pop(page)
                        name.pop(page)
                        url.pop(page)
                        if(page==len(emoji)): page = page-1
                        await ses.close()
                    else:
                        await ctx.send(f'Error when making request | {r.status} response.')
                        await ses.close()
                        
                except discord.HTTPException as e:
                    if(e.code==30008): await ctx.send(f"{self.client.emotes['failed']} | Emoji Slots are full!")
                    else: await ctx.send(f"{self.client.emotes['failed']} | {e.text}")
        await send_view(self,ctx,emoji,name,url,page)

    if view.value == "3":
        if msg: await msg.delete()
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url[page]) as resp:
                file = discord.File(fp=BytesIO(await resp.read()), filename="sticker.png") 
                try:
                    sticker = await guild.create_sticker(name=name[page],description="",file=file,emoji="👌")
                    await ctx.send(f'{self.client.emotes["success"]} | Successfully created Sticker:',stickers=[sticker])
                    emoji.pop(page)
                    name.pop(page)
                    url.pop(page)
                    if(page==len(emoji)): page = page-1
                except discord.HTTPException as e:
                    if(e.code==30039): await ctx.send(f"{self.client.emotes['failed']} | Sticker Slots are full!")
                    else: await ctx.send(f"{self.client.emotes['failed']} | {e.text}")
                    
                await ses.close()
        await send_view(self,ctx,emoji,name,url,page)

    
        
    if view.value == '4':
        if msg: await msg.delete()
        if(page==len(emoji)-1):
            await ctx.reply("Cannot go ahead!")
            await send_view(self,ctx,emoji,name,url,page)
        else:
            page+=1 
            await send_view(self,ctx,emoji,name,url,page)

async def get_name_url(emoji):
    name  = []
    url = []
    for emote in emoji:
        if emote[1]=='a':
            index = emote.find(":",5)
            name.append(emote[3:index])
            url.append("https://cdn.discordapp.com/emojis/" +f"{emote[index+1:-1]}.gif")
        else:
            index = emote.find(":",4)
            name.append(emote[2:index])
            url.append("https://cdn.discordapp.com/emojis/" +f"{emote[index+1:-1]}.png")
    return name,url

async def create_embed(url,pgno):
    embed = discord.Embed(title=f"Emoji {pgno+1}/{len(url)}",color=0xfb7c04)
    embed.set_image(url=url[pgno])
    return embed



class Buttons(discord.ui.View):
    def __init__ (self, ctx, *, timeout=60):
        super().__init__(timeout=timeout)
        self.ctx = ctx
    @discord.ui.button(emoji="◀", style=discord.ButtonStyle.green, row=0)
    async def button1_call(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
        self.value = "1"
        self.stop()
        await interaction.response.defer()
    @discord.ui.button(label="Add as Emote", style=discord.ButtonStyle.primary, row=1)
    async def button2_call(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
        self.value = "2"
        self.stop()
        await interaction.response.defer()
    @discord.ui.button(label="Add as Sticker", style=discord.ButtonStyle.primary, row=1)
    async def button3_call(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
        self.value = "3"
        self.stop()
        await interaction.response.defer()
    @discord.ui.button(emoji="▶", style=discord.ButtonStyle.green, row=0)
    async def button4_call(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
        self.value = "4"
        self.stop()
        await interaction.response.defer()

async def setup(client):
    await client.add_cog(modcmd(client))       