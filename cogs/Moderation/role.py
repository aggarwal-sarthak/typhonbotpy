from discord.ext import commands
import os

class role(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.command(description='Add/Remove Roles', aliases=['r'], usage=f"{os.path.basename(__file__)[:-3]} add/remove <role(s)> <user(s)>\n{os.path.basename(__file__)[:-3]} add/remove all/bots/humans <role(s>)")
    async def role(self, ctx, mode=None, *ids):
        ids = await parse_ids(ids)
        if(len(ids)==0):
            await ctx.invoke(self.client.get_command('help'), f"{os.path.basename(__file__)[:-3]}")
            return
        member_list=[]
        role_list=[]
        member_string=""
        role_string="" 
        
        if(ids[0] in ["all","a"]):
            for member in ctx.message.guild.members:
                member_list.append(str(member.id))
            role_list.extend(ids[1:])    
        elif(ids[0] in ["humans","human",'h']):
            for member in ctx.message.guild.members:
                if member.bot==False: member_list.append(str(member.id))
            role_list.extend(ids[1:])   

        elif(ids[0] in ['bots','bot','b']):
            for member in ctx.message.guild.members:
                if member.bot==True: member_list.append(str(member.id))
            role_list.extend(ids[1:])   

        else:
            for id in ids:
                member = ctx.guild.get_member(int(id))
                role = ctx.guild.get_role(int(id))
                
                if role:
                    if await position_check(self=self, ctx=ctx, role=role):
                        pass
                    else: role_list.append(id)

                if member:
                    member_list.append(id)
    
        if(len(member_list)==0 or len(role_list)==0):
            await ctx.invoke(self.client.get_command('help'), f"{os.path.basename(__file__)[:-3]}")
        else:
            match mode:
                case 'add':
                    await give_role(self=self, ctx=ctx, role_list=role_list, member_list=member_list, role_string=role_string, member_string=member_string)
                case 'remove':
                    await take_role(self=self, ctx=ctx, role_list=role_list, member_list=member_list, role_string=role_string, member_string=member_string)
                case _:
                    await ctx.invoke(self.client.get_command('help'), f"{os.path.basename(__file__)[:-3]}")

async def parse_ids(ids):
    parsed_ids = []
    for id in ids:
        if "<@&" in id:
            parsed_ids.append(id[3:-1])

        elif "<@" in id:
            parsed_ids.append(id[2:-1])
        
        else:
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
    await ctx.message.add_reaction(self.client.emotes['success'])
    for r in role_list:
        role = ctx.guild.get_role(int(r))
        member_list = set(member_list) - set([str(mem.id) for mem in role.members])
        for m in list(member_list):
            await ctx.guild.get_member(int(m)).add_roles(role)
    if(len(role_list)<=10):            
        for r in role_list: role_string += "`" + ctx.guild.get_role(int(r)).name + "`,"
    else:
        role_string = "`"+str(len(role_list)) + " roles``"
    if(len(member_list)<=10):
        for m in member_list: member_string += "`" + ctx.guild.get_member(int(m)).name + "`,"
    else:
        member_string = "`"+str(len(member_list)) + " members``"

    await ctx.reply(f"{self.client.emotes['success']} | Added {role_string[:-1]} To {member_string[:-1]}!")

async def take_role(self, ctx, role_list, member_list, role_string, member_string):
    await ctx.message.add_reaction(self.client.emotes['success'])
    for r in role_list:
        role = ctx.guild.get_role(int(r))
        member_list = [str(mem.id) for mem in role.members if str(mem.id) in member_list]
        for m in member_list:
            await ctx.guild.get_member(int(m)).remove_roles(ctx.guild.get_role(int(r)))
    if(len(role_list)<=10):            
        for r in role_list: role_string += "`" + ctx.guild.get_role(int(r)).name + "`,"
    else:
        role_string = "`"+str(len(role_list)) + " roles``"
    if(len(member_list)<=10):
        for m in member_list: member_string += "`" + ctx.guild.get_member(int(m)).name + "`,"
    else:
        member_string = "`"+str(len(member_list)) + " members``"

    await ctx.reply(f"{self.client.emotes['success']} | Removed {role_string[:-1]} From {member_string[:-1]}!")

async def setup(client):
    await client.add_cog(role(client))