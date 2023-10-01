# from discord.ext import commands
# import discord
# import os
# import confirmation
# from types import SimpleNamespace
# from validation import is_command_enabled

# class role(commands.Cog):
#     def __init__(self, client):
#         self.client = client

#     @commands.command(description='Add/Remove Roles', aliases=['r'], usage=f"{os.path.basename(__file__)[:-3]} add/remove <role(s)> <user(s)>\n{os.path.basename(__file__)[:-3]} add/remove all/bots/humans <role(s>)")
#     @commands.check(is_command_enabled)
#     @commands.has_permissions(manage_roles=True)
#     @commands.bot_has_permissions(manage_roles=True)
#     async def role(self, ctx, mode, *ids):
#         if(len(ids)==0):
#             raise commands.MissingRequiredArgument(SimpleNamespace(displayed_name="IDs"))
        
#         if(mode.lower() not in ['add','remove']):
#             raise commands.MissingRequiredArgument(SimpleNamespace(displayed_name ="mode"))
        
#         mode = mode.lower()
#         category = ids[0]

#         ids = await parse_ids(ids)

#         member_list=[]
#         role_list=[]

#         member_string=""
#         role_string=""

#         if(category in ["all","a"]):
#             for member in ctx.guild.members:
#                 member_list.append(str(member.id))
#             role_list.extend(ids)

#         elif(category in ["humans","human",'h']):
#             for member in ctx.message.guild.members:
#                 if member.bot==False: member_list.append(str(member.id))
#             role_list.extend(ids)

#         elif(category in ['bots','bot','b']):
#             for member in ctx.message.guild.members:
#                 if member.bot==True: member_list.append(str(member.id))
#             role_list.extend(ids)

#         else:
#             for id in ids:
#                 member = ctx.guild.get_member(int(id))
#                 role = ctx.guild.get_role(int(id))

#                 if role:
#                     await position_check(self=self, ctx=ctx, role=role)
#                     role_list.append(id)

#                 if member:
#                     member_list.append(id)

#         for r in role_list:
#             role = ctx.guild.get_role(int(r))
#             if(mode=="remove"):
#                 member_list = [str(mem.id) for mem in role.members if str(mem.id) in member_list]
#             else:
#                 member_list = set(member_list) - set([str(mem.id) for mem in role.members])

#         if(len(member_list)==0 or len(role_list)==0):
#             raise commands.MissingRequiredArgument(SimpleNamespace(displayed_name="list"))
        
#         else:
#             if(len(role_list)<=10):
#                 for r in role_list: role_string += f'<@&{ctx.guild.get_role(int(r)).id}>,'
#             else:
#                 role_string =f'`{len(role_list)} roles``'

#             if(len(member_list)<=10):
#                 for m in member_list: member_string += f'<@{ctx.guild.get_member(int(m)).id}>,'
#             else:
#                 member_string = f'`{len(member_list)} members``'

#             view = confirmation.Buttons(ctx)
#             embed = discord.Embed(title=f"{mode.capitalize()}?",description=f"**Roles: {role_string[:-1]}\nMembers: {member_string[:-1]}**",color=0xfb7c04)

#             msg = await ctx.reply(embed=embed,view=view)
#             await view.wait()

#             if view.value == "1":
#                 if msg: await msg.delete()
#                 msg = await ctx.reply(f'{self.client.emotes["loading"]} | Adding Roles!')

#                 role_string = ""
#                 member_string = ""

#                 if(len(role_list)<=10):
#                     for r in role_list: role_string += f'`{ctx.guild.get_role(int(r)).name}`,'
#                 else:
#                     role_string = f'`{len(role_list)} roles``'
#                 if(len(member_list)<=10):
#                     for m in member_list: member_string += f'`{ctx.guild.get_member(int(m)).name}`,'
#                 else:
#                     member_string = f'`{len(member_list)} members``'

#                 match mode:
#                     case 'add':
#                         await give_role(self, ctx, role_list, member_list, role_string, member_string)
#                     case 'remove':
#                         await take_role(self, ctx, role_list, member_list, role_string, member_string)
#                     case _:
#                         ctx.reply(f'{self.client.emotes["failed"]} Not a valid argument!')
                
#                 if msg: msg.delete()

#             if view.value == "2":
#                 if msg: await msg.delete()
#                 return await ctx.message.add_reaction(self.client.emotes['failed'])

# async def parse_ids(ids):
#     parsed_ids = []
#     for id in ids:
#         if "<@&" in id:
#             parsed_ids.append(id[id.index("<@&")+3:id.index(">")])

#         elif "<@" in id:
#             parsed_ids.append(id[id.index("<@")+2:id.index(">")])

#         elif id.isdigit():
#             parsed_ids.append(id)
#     return parsed_ids

# async def position_check(self, ctx, role):
#     if ctx.guild.get_member(self.client.user.id).top_role.position <= role.position:
#         return await ctx.reply(f"{self.client.emotes['failed']} | My Role Isn't High Enough To Assign The Role `{role.name}`!")

#     elif ctx.guild.owner_id != ctx.author.id and ctx.author.top_role.position <= role.position:
#         return await ctx.reply(f"{self.client.emotes['failed']} | Your Role Isn't High Enough To Assign The Role `{role.name}`!")

# async def give_role(self, ctx, role_list, member_list, role_string, member_string):
#     for r in role_list:
#         role = ctx.guild.get_role(int(r))
#         for m in list(member_list):
#             await ctx.guild.get_member(int(m)).add_roles(role)
#     await ctx.reply(f"{self.client.emotes['success']} | Added {role_string[:-1]} To {member_string[:-1]}!")

# async def take_role(self, ctx, role_list, member_list, role_string, member_string):
#     for r in role_list:
#         role = ctx.guild.get_role(int(r))
#         for m in member_list:
#             await ctx.guild.get_member(int(m)).remove_roles(role)
#     await ctx.reply(f"{self.client.emotes['success']} | Removed {role_string[:-1]} From {member_string[:-1]}!")

# async def setup(client):
#     await client.add_cog(role(client))


from discord.ext import commands
import discord
import os
import confirmation
from validation import is_command_enabled

class role(commands.Cog):
    def __init__(self, client):
        self.client = client

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
        pass

    @add.command(name='all', description='Manages All Members Of Server', usage = f"{os.path.basename(__file__)[:-3]} add all")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def add_all(self, ctx, *ids: discord.Role):
        mem_dict = {}
        for i in ids:
            mem_dict[i.id] = [m.id for m in ctx.guild.members if not i in m.roles]
        await confirm(self, ctx, mem_dict, 'add')

    @add.command(name='humans', description='Manages Human Members Of Server', usage = f"{os.path.basename(__file__)[:-3]} add humans")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def add_humans(self, ctx, *ids: discord.Role):
        mem_dict = {}
        for i in ids:
            mem_dict[i.id] = [m.id for m in ctx.guild.members if not i in m.roles and not m.bot]
        await confirm(self, ctx, mem_dict, 'add')

    @add.command(name='bots', description='Manages Bot Members Of Server', usage = f"{os.path.basename(__file__)[:-3]} add bots")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def add_bots(self, ctx, *ids: discord.Role):
        mem_dict = {}
        for i in ids:
            mem_dict[i.id] = [m.id for m in ctx.guild.members if not i in m.roles and m.bot]
        await confirm(self, ctx, mem_dict, 'add')

    @role.group(name='remove', description='Removes Role(s) From Members', aliases = ['take', 'r'], usage = f"{os.path.basename(__file__)[:-3]} remove <subcommand>", invoke_without_command=True)
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def remove(self, ctx, cmd):
        pass

    @remove.command(name='all', description='Manages All Members Of Server', usage = f"{os.path.basename(__file__)[:-3]} remove all")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def remove_all(self, ctx, *ids: discord.Role):
        mem_dict = {}
        for i in ids:
            mem_dict[i.id] = [m.id for m in ctx.guild.members if i in m.roles]
        await confirm(self, ctx, mem_dict, 'remove')

    @remove.command(name='humans', description='Manages Human Members Of Server', usage = f"{os.path.basename(__file__)[:-3]} remove humans")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def remove_humans(self, ctx, *ids: discord.Role):
        mem_dict = {}
        for i in ids:
            mem_dict[i.id] = [m.id for m in ctx.guild.members if i in m.roles and not m.bot]
        await confirm(self, ctx, mem_dict, 'remove')

    @remove.command(name='bots', description='Manages Bot Members Of Server', usage = f"{os.path.basename(__file__)[:-3]} remove bots")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def remove_bots(self, ctx, *ids: discord.Role):
        mem_dict = {}
        for i in ids:
            mem_dict[i.id] = [m.id for m in ctx.guild.members if i in m.roles and m.bot]
        await confirm(self, ctx, mem_dict, 'remove')

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
    
    if msg: await msg.delete()
    await ctx.reply(desc)

async def confirm(self, ctx, members, mode):
    desc = ''
    for i in members:
        desc += f'**Role:** `{ctx.guild.get_role(i).name}`, **Members:** `{len(members[i])}`\n'
    
    if mode == 'add': title = 'Do You Want To Add Roles?'
    elif mode == 'remove': title = 'Do You Want To Remove Roles?'

    view = confirmation.Buttons(ctx)
    embed = discord.Embed(title=title,description=desc,color=0xfb7c04)

    msg = await ctx.reply(embed=embed,view=view)
    try:
        await view.wait()
        if view.value == '1':
            if msg: await msg.delete()
            msg = await ctx.reply(f'{self.client.emotes["loading"]} | Command Executing...!')
            await action(self, ctx, members, msg, mode)

        if view.value == '2':
            if msg: await msg.delete()
            await ctx.reply(f'{self.client.emotes["failed"]} | Command Cancelled!')
    except:
        disable = confirmation.Disabled(ctx)
        await msg.edit(embed=embed, view=disable)
        
async def parse_ids(self, ctx, ids, mode):
    mem_dict = {}
    for id in ids:
        if id.isnumeric():
            member = discord.utils.get(ctx.guild.members, id = int(id))
        else:
            member = discord.utils.get(ctx.guild.members, id = int(id.id))
    # parsed_ids = []
    # for id in ids:
    #     if "<@&" in id:
    #         parsed_ids.append(id[id.index("<@&")+3:id.index(">")])

    #     elif "<@" in id:
    #         parsed_ids.append(id[id.index("<@")+2:id.index(">")])

    #     elif id.isdigit():
    #         parsed_ids.append(id)

async def setup(client):
    await client.add_cog(role(client))