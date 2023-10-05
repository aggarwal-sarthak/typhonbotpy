from discord.ext import commands
import discord
import os
import confirmation
from types import SimpleNamespace
from validation import is_command_enabled

class role(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.mem_dict = {}

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
    embed = discord.Embed(title=title,description=desc,color=0xfb7c04)

    msg = await ctx.reply(embed=embed,view=view)
    await view.wait()
    if not view.value:
        disable = confirmation.Disabled(ctx)
        return await msg.edit(embed=embed, view=disable)

    elif view.value == '1':
        if msg: await msg.delete()
        msg = await ctx.reply(f'{self.client.emotes["loading"]} | Command Executing...!')
        await action(self, ctx, members, msg, mode)

    elif view.value == '2':
        if msg: await msg.delete()
        await ctx.reply(f'{self.client.emotes["failed"]} | Command Cancelled!')
        
    self.mem_dict = {}
        
async def parse_ids(self, ctx, ids, mode):
    mem_dict = {}
    members = []
    roles = []
    for i in ids:
        if i.isnumeric():
            id = int(i)
        else:
            id = int(i.strip('<@!&>'))

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

async def setup(client):
    await client.add_cog(role(client))