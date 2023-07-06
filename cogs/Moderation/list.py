from discord.ext import commands
import os
import discord
import pagination

class list(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.command(description='Returns List Of Mentioned Argument', usage=f"{os.path.basename(__file__)[:-3]}")
    async def list(self, ctx, mode , *msg):
        embeds = []
        match mode:
            case "admins":
                data = [member for member in ctx.guild.members if member.guild_permissions.administrator and member.bot==False]
                title = f"Admins : {len(data)}"
                await mention_pagination(self,ctx,data,embeds, title)
                
            case "bots":
                data = [member for member in ctx.guild.members if member.bot]
                title = f"Bots : {len(data)}"
                await mention_pagination(self,ctx,data,embeds, title)

            case "boosters":
                data = [member for member in ctx.guild.premium_subscribers]
                title = f"Boosters : {len(data)}"
                await mention_pagination(self,ctx,data,embeds, title)
            
            case "roles":
                data = [roles for roles in ctx.guild.roles]
                data.reverse()
                title = f"Roles : {len(data)}"
                for i in range(0,len(data), 20):
                    description = ""
                    for j in range(i, min(i+20, len(data))):
                        description += "**" + str(j+1) + "** : " + str(data[j].mention) + " `" + str(data[j].id) + "`" + "\n"
                    pagination_embed = discord.Embed(title=title, description=description,color=0xfb7c04)
                    pagination_embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
                    embeds.append(pagination_embed)
                await pagination_check(self,ctx,data, embeds)

            case "bans":
                data = [ban.user async for ban in ctx.guild.bans()]
                title = f"Bans : {len(data)}"
                await mention_pagination(self,ctx,data,embeds, title)
            
            case "emojis":
                data = [emoji for emoji in ctx.guild.emojis]
                title = f"Emojis : {len(data)}"
                for i in range(0,len(data), 20):
                    description = ""
                    for j in range(i, min(i+20, len(data))):
                        description += f"**{str(j+1)}** : {data[j]} : `{data[j].name}`\n"
                    pagination_embed = discord.Embed(title=title, description=description,color=0xfb7c04)
                    pagination_embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
                    embeds.append(pagination_embed)
                await pagination_check(self,ctx,data, embeds)

async def mention_pagination(self, ctx, data, embeds, title):
    for i in range(0,len(data), 20):
        description = ""
        for j in range(i, min(i+20, len(data))):
            description += "**" + str(j+1) + "** : " +  str(data[j]) + " [" + str(data[j].mention) + "]" + "\n"
        pagination_embed = discord.Embed(title=title, description=description,color=0xfb7c04)
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

async def setup(client):
    await client.add_cog(list(client))