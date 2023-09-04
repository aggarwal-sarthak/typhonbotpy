import discord
from discord.ext import commands
import os
import json
import aiohttp
from io import BytesIO
from validation import is_command_enabled

with open('emoji.json', 'r') as f:
    emotes = json.load(f)

class steal(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.command(description="Add Emotes and Stickers to Server",aliases=['add'],usage=f"{os.path.basename(__file__)[:-3]} <emote>")
    @commands.check(is_command_enabled)
    @commands.has_permissions(manage_expressions=True)
    @commands.bot_has_permissions(manage_expressions=True)
    async def steal(self, ctx,*args):
        try:
            emoji = []
            if(ctx.message.reference is not None):
                msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                if(len(msg.stickers)>0):
                    sticker = msg.stickers[0]
                else:
                    emoji = msg.content.split()     #needs emoji verification
            else:
                if(len(args)>0):
                    for em in args:
                        emoji.append(em)            #needs verif
                elif(len(ctx.message.stickers)>0):
                    sticker = ctx.message.stickers[0]
                else:
                    await ctx.reply(f"{self.client.emotes['failed']}| No emojis or stickers found!")
            if(len(emoji)>0):
                name, url = await get_name_url(emoji)
                await send_view(self,ctx,emoji,name,url)
                # page = 0 
                # name, url = await get_name_url(emoji)
                # embed = await create_embed(url,page)
                # view = Buttons(ctx)
                # message = await ctx.reply(embed=embed,view=view)
                # await view.wait()
            else:
                pass
        except Exception as e:
            print("\n\n\n\n\n\n",e)

async def send_view(self,ctx,emoji,name,url,page=0):
    embed = await create_embed(url,page)
    view = Buttons(ctx)
    msg = await ctx.reply(embed=embed,view=view)
    await view.wait()
    if view.value == "1":
        if msg: await msg.delete()
        if(page==0):
            await ctx.reply("Cannot go back!")
            await send_view(self,ctx,emoji,name,url,page)
        else:
            page -= 1
            await send_view(self,ctx,emoji,name,url,page)
        return False
    if view.value == "2":
        if msg: await msg.delete()
        # print("\n\n\n\n\n ctx guild",ctx.guild,url[page])
        # image = urllib.request.urlopen(url[page]).read()
        # image = base64.b64encode(image)
        # print(image)
        # await ctx.guild.create_custom_emoji(name=name,image=url[page])
        # return False
        guild = ctx.guild
        if ctx.author.guild_permissions.manage_emojis:
            async with aiohttp.ClientSession() as ses:
                async with ses.get(url[page]) as r:
                    try:
                        img_or_gif = BytesIO(await r.read())
                        b_value = img_or_gif.getvalue()
                        if r.status in range(200, 299):
                            emj = await guild.create_custom_emoji(image=b_value, name=name[page])
                            print(f'Successfully created emoji: <:{emj.name}:{emj.id}>')
                            await ctx.send(f'Successfully created emoji: <:{emj.name}:{emj.id}>')
                            await ses.close()
                            print("\n\n\n\n\n\nadded emote")
                        else:
                            await ctx.send(f'Error when making request | {r.status} response.')
                            await ses.close()
                            
                    except discord.HTTPException as e:
                        await ctx.send('File size is too big!')
            await send_view(self,ctx,emoji,name,url,page)

    if view.value == "3":
        if msg: await msg.delete()
        return False
    if view.value == '4':
        if msg: await msg.delete()
        if(page==len(emoji)-1):
            await ctx.reply("Cannot go ahead!")
            await send_view(self,ctx,emoji,name,url,page)
        else:
            page+=1 
            await send_view(self,ctx,emoji,name,url,page)

async def get_name_url(emoji):
    name  = []
    url = []
    for emote in emoji:
        print(emoji,emote)
        if emote[1]=='a':
            index = emote.find(":",5)
            name.append(emote[3:index])
            url.append("https://cdn.discordapp.com/emojis/" +f"{emote[index+1:-1]}.gif")
        else:
            index = emote.find(":",4)
            name.append(emote[2:index])
            url.append("https://cdn.discordapp.com/emojis/" +f"{emote[index+1:-1]}.png")
    return name,url

async def create_embed(url,pgno):
    embed = discord.Embed(title="Emoji")
    embed.set_image(url=url[pgno])
    return embed


async def setup(client):
    await client.add_cog(steal(client)) 


class Buttons(discord.ui.View):
    def __init__ (self, ctx, *, timeout=60):
        super().__init__(timeout=timeout)
        self.ctx = ctx
    @discord.ui.button(label="Previous", style=discord.ButtonStyle.green)
    async def button1_call(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
        self.value = "1"
        self.stop()
        await interaction.response.defer()
    @discord.ui.button(label="Add as Emote", style=discord.ButtonStyle.red)
    async def button2_call(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
        self.value = "2"
        self.stop()
        await interaction.response.defer()
    @discord.ui.button(label="Add as Sticker", style=discord.ButtonStyle.red)
    async def button3_call(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
        self.value = "3"
        self.stop()
        await interaction.response.defer()
    @discord.ui.button(label="Next")
    async def button4_call(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
        self.value = "4"
        self.stop()
        await interaction.response.defer()