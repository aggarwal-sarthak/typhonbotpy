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
                for id in ids:
                    member = ctx.guild.get_member(int(id))
                    role = ctx.guild.get_role(int(id))

            case 'remove':
                print(ids)
            case _:
                print('wrong')

async def setup(client):
    await client.add_cog(role(client))