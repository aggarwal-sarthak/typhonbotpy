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
    @commands.command(description='Add/Remove Roles', aliases=['r'], usage=f"{os.path.basename(__file__)[:-3]}")
    async def role(self, ctx, mode, *ids):
        ids = await parse_ids(ids)
        member_list=[]
        role_list=[]
        member_string=""
        role_string=""

        match mode:
            case 'add':
                for id in ids:
                    member = ctx.guild.get_member(int(id))
                    role = ctx.guild.get_role(int(id))
                    
                    if role:
                        if await position_check(self=self, ctx=ctx, role=role):
                            pass
                        else: role_list.append(id)
                            
                    if member:
                        member_list.append(id)

                await give_role(self=self, ctx=ctx, role_list=role_list, member_list=member_list, role_string=role_string, member_string=member_string)

            case 'remove':
                print(ids)
            case _:
                print('wrong')

    @role.error
    async def missing_permissions(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            err = str(error).replace('You are missing ','').replace(' permission(s) to run this command.','')
            await ctx.reply(f"{self.client.emotes['failed']} | You Don't Have `{err}` Permission To Use This Command!")

        if isinstance(error, commands.BotMissingPermissions):
            err = str(error).replace('Bot requires ','').replace(' permission(s) to run this command.', '')
            await ctx.reply(f"{self.client.emotes['failed']} | I Don't Have `{err}` Permission To Use This Command!")

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
    elif ctx.guild.owner_id != ctx.author.id and ctx.author.top_role.position <= role.position:
        await ctx.reply(f"{self.client.emotes['failed']} | Your Role Isn't High Enough To Assign The Role `{role.name}`!")
        
async def give_role(self, ctx, role_list, member_list, role_string, member_string):
    for r in role_list:
        for m in member_list:
            await ctx.guild.get_member(int(m)).add_roles(ctx.guild.get_role(int(r)))
                
    for r in role_list: role_string += "`" + ctx.guild.get_role(int(r)).name + "`,"
    for m in member_list: member_string += "`" + ctx.guild.get_member(int(m)).name + "`,"

    await ctx.reply(f"{self.client.emotes['success']} | Added {role_string} To {member_string}!")

async def setup(client):
    await client.add_cog(role(client))