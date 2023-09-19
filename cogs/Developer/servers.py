from discord.ext import commands
import os
import discord
import pagination
from validation import is_command_enabled

class servers(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description='Returns Bot Servers', usage=f"{os.path.basename(__file__)[:-3]}", aliases=['s'])
    @commands.check(is_command_enabled)
    async def servers(self, ctx):
        if ctx.author.id not in self.client.config["owner"]: return
        data = sorted(self.client.guilds, key=lambda x: x.member_count, reverse=True)

        embeds = []
        for i in range(0,len(data), 20):
            description = ""
            for j in range(i, min(i+20, len(data))):
                description += f'**{str(j+1)}.** {str(data[j].name)} **|** {str(data[j].id)} **|** {str(data[j].member_count)}\n'
            pagination_embed = discord.Embed(title=f'Bot Servers [{len(self.client.guilds)}]', description=description,color=0xfb7c04)
            pagination_embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
            embeds.append(pagination_embed)
        await pagination_check(self, ctx, data, embeds)

async def pagination_check(self, ctx, data, embeds):
    if len(data)>20:
        await pagination.Simple(timeout=60).start(ctx, pages=embeds)
    elif (len(data)<20 and len(data)>0):
        await ctx.reply(embed=embeds[0])
        
async def setup(client):
    await client.add_cog(servers(client))