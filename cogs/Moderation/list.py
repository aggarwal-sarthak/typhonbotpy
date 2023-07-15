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

    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(description='Returns List Of Mentioned Argument', usage=f"{os.path.basename(__file__)[:-3]} admins\n{os.path.basename(__file__)[:-3]} bots\n{os.path.basename(__file__)[:-3]} boosters\n{os.path.basename(__file__)[:-3]} roles\n{os.path.basename(__file__)[:-3]} bans\n{os.path.basename(__file__)[:-3]} emojis\n{os.path.basename(__file__)[:-3]} inrole <role>")
    async def list(self, ctx, mode , *role: discord.Role):
        embeds = []
        match mode:
            case "admins" | "admin":
                data = [member for member in ctx.guild.members if member.guild_permissions.administrator and member.bot==False]
                title = f"Admins : {len(data)}"
                await mention_pagination(self,ctx,data,embeds, title)
                
            case "bots" | "bot":
                data = [member for member in ctx.guild.members if member.bot]
                title = f"Bots : {len(data)}"
                await mention_pagination(self,ctx,data,embeds, title)

            case "boosters" | "booster":
                data = [member for member in ctx.guild.premium_subscribers]
                title = f"Boosters : {len(data)}"
                await mention_pagination(self,ctx,data,embeds, title)
            
            case "roles" | "role":
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

            case "bans" | "ban":
                data = [ban.user async for ban in ctx.guild.bans()]
                title = f"Bans : {len(data)}"
                await mention_pagination(self,ctx,data,embeds, title)
            
            case "emojis" | "emoji" | "emo":
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

            case "inrole" | "dump":
                data = [member for member in role[0].members]
                title = f"Members In Role : {len(data)}"
                await mention_pagination(self,ctx,data,embeds, title)

            case _:
                await ctx.invoke(self.client.get_command('help'), f"{os.path.basename(__file__)[:-3]}")

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