from discord.ext import commands
import os

class role(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.command(description='Add/Remove Roles', aliases=['r'], usage=f"{os.path.basename(__file__)[:-3]}")
    async def role(self, ctx, mode, *ids):
        match mode:
            case 'add':
                member_list=[]
                role_list=[]
                for id in ids:
                    member = ctx.guild.get_member(int(id))
                    role = ctx.guild.get_role(int(id))
                    if role:
                        if ctx.guild.get_member(self.client.user.id).top_role.position <= role.position:
                            await ctx.reply(f"{self.client.emotes['failed']} | My Role Isn't High Enough To Assign The Role `{role.name}`!")
                        elif ctx.guild.owner_id != ctx.author.id and ctx.author.top_role.position <= role.position:
                            await ctx.reply(f"{self.client.emotes['failed']} | Your Role Isn't High Enough To Assign The Role `{role.name}`!")
                        else:
                            role_list.append(id)
                            
                    if member:
                        member_list.append(id)

                print(role_list, member_list)

            case 'remove':
                print(ids)
            case _:
                print('wrong')

async def setup(client):
    await client.add_cog(role(client))