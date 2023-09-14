# from discord.ext import commands
# import discord
# import os
# import confirmation
# from types import SimpleNamespace
# from validation import is_command_enabled

# class role(commands.Cog):
#     def __init__(self, client):
#         self.client = client

#     @commands.Cog.listener()
#     async def on_ready(self):
#         print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

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
#                     if await position_check(self=self, ctx=ctx, role=role):
#                         pass
#                     else: role_list.append(id)

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
#                 for r in role_list: role_string += "<@&" + str(ctx.guild.get_role(int(r)).id) + ">,"
#             else:
#                 role_string = "`"+str(len(role_list)) + " roles``"
#             if(len(member_list)<=10):
#                 for m in member_list: member_string += "<@"+str(ctx.guild.get_member(int(m)).id) + ">,"
#             else:
#                 member_string = "`"+str(len(member_list)) + " members``"
#             view = confirmation.Buttons(ctx)
#             embed = discord.Embed(title=f"{mode.capitalize()}?",description=f"**Roles: {role_string[:-1]}\nMembers: {member_string[:-1]}**",color=0xfb7c04)
#             msg = await ctx.reply(embed=embed,view=view)
#             await view.wait()
#             if view.value == "1":
#                 if msg: await msg.delete()
#                 await ctx.message.add_reaction(self.client.emotes['success'])
#                 role_string = ""
#                 member_string = ""
#                 if(len(role_list)<=10):
#                     for r in role_list: role_string += "`" + str(ctx.guild.get_role(int(r)).name) + "`,"
#                 else:
#                     role_string = "`"+str(len(role_list)) + " roles``"
#                 if(len(member_list)<=10):
#                     for m in member_list: member_string += "`"+str(ctx.guild.get_member(int(m)).name) + "`,"
#                 else:
#                     member_string = "`"+str(len(member_list)) + " members``"

#                 match mode:
#                     case 'add':
#                         await give_role(self=self, ctx=ctx, role_list=role_list, member_list=member_list,role_string=role_string,member_string=member_string)
#                     case 'remove':
#                         await take_role(self=self, ctx=ctx, role_list=role_list, member_list=member_list,role_string=role_string,member_string=member_string)
#                     case _:
#                         ctx.reply(f'{self.client.emotes["failed"]} Not a valid argument!')
#             if view.value == "2":
#                 if msg: await msg.delete()
#                 await ctx.message.add_reaction(self.client.emotes['failed'])
#                 raise commands.CommandError("Command Cancelled")

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
#         await ctx.reply(f"{self.client.emotes['failed']} | My Role Isn't High Enough To Assign The Role `{role.name}`!")
#         raise commands.CommandError("Command Cancelled")
#     elif ctx.guild.owner_id != ctx.author.id and ctx.author.top_role.position <= role.position:
#         await ctx.reply(f"{self.client.emotes['failed']} | Your Role Isn't High Enough To Assign The Role `{role.name}`!")
#         raise commands.CommandError("Command Cancelled")

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
#             await ctx.guild.get_member(int(m)).remove_roles(ctx.guild.get_role(int(r)))
#     await ctx.reply(f"{self.client.emotes['success']} | Removed {role_string[:-1]} From {member_string[:-1]}!")

# async def setup(client):
#     await client.add_cog(role(client))


from discord.ext import commands
import discord
import os
import confirmation
from types import SimpleNamespace
from validation import is_command_enabled

class Mode(commands.Converter):
    def mode_check(arg):
        if arg not in ['add', 'remove']:
            raise commands.BadArgument("Argument Must be Add or Remove!")
        return arg.lower()

class role(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.group(name='role', description='Add/Remove Roles', aliases=['r'], usage=f"{os.path.basename(__file__)[:-3]} add/remove", invoke_without_command=True)
    @commands.check(is_command_enabled)
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def role(self, ctx, mode: Mode, *ids):
        await ctx.send("role")
        print("\n\n\n\n\nrole")

    @role.command(name='add', description='Add Roles', aliases=['+'])
    @commands.check(is_command_enabled)
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def add(self, ctx, mode: Mode):
        await ctx.send("add")
        print("\n\n\n\n\nadd")

    # @add.command (name='all', description='Add Roles To Everyone', aliases=['a'])
    # @commands.check(is_command_enabled)
    # @commands.has_permissions(manage_roles=True)
    # @commands.bot_has_permissions(manage_roles=True)
    # async def all(self, ctx):
    #     await ctx.send("all")
    #     print("\n\n\n\n\nall")

async def parse_ids(ids):
    parsed_ids = []
    for id in ids:
        if "<@&" in id:
            parsed_ids.append(id[id.index("<@&")+3:id.index(">")])
        elif "<@" in id:
            parsed_ids.append(id[id.index("<@")+2:id.index(">")])
        elif id.isdigit():
            parsed_ids.append(id)

    return parsed_ids

async def position_check(self, ctx, role):
    if ctx.guild.get_member(self.client.user.id).top_role.position <= role.position:
        await ctx.reply(f"{self.client.emotes['failed']} | My Role Isn't High Enough To Assign The Role `{role.name}`!")
        raise commands.CommandError("Command Cancelled")
    elif ctx.guild.owner_id != ctx.author.id and ctx.author.top_role.position <= role.position:
        await ctx.reply(f"{self.client.emotes['failed']} | Your Role Isn't High Enough To Assign The Role `{role.name}`!")
        raise commands.CommandError("Command Cancelled")

async def give_role(self, ctx, role_list, member_list, role_string, member_string):
    for r in role_list:
        role = ctx.guild.get_role(int(r))
        for m in list(member_list):
            await ctx.guild.get_member(int(m)).add_roles(role)
    await ctx.reply(f"{self.client.emotes['success']} | Added {role_string[:-1]} To {member_string[:-1]}!")

async def take_role(self, ctx, role_list, member_list, role_string, member_string):
    for r in role_list:
        role = ctx.guild.get_role(int(r))
        for m in member_list:
            await ctx.guild.get_member(int(m)).remove_roles(role)
    await ctx.reply(f"{self.client.emotes['success']} | Removed {role_string[:-1]} From {member_string[:-1]}!")

async def setup(client):
    await client.add_cog(role(client))