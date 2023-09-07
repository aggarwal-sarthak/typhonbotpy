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
                return
        
        if(len(emoji)>0):
            for emote in emoji:
                if('<' not in emote or '>' not in emote or ':' not in emote):
                    emoji.remove(emote)
            if(len(emoji)>0):
                name, url = await get_name_url(emoji)
                await send_view(self,ctx,emoji,name,url)
            else:
                await ctx.reply(f"{self.client.emotes['failed']}| No emojis or stickers found!")
                return
        elif(sticker):
            sticker_list = [sticker]
            name = [sticker.name]
            url = [sticker.url]
            await send_view(self,ctx,sticker_list,name,url)
        else:
            pass
    

async def send_view(self,ctx,emoji,name,url,page=0):
    if(len(emoji)==0): return
    guild = ctx.guild
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
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url[page]) as r:
                try:
                    img_or_gif = BytesIO(await r.read())
                    b_value = img_or_gif.getvalue()
                    if r.status in range(200, 299):
                        emj = await guild.create_custom_emoji(image=b_value, name=name[page].replace(' ','_'))
                        await ctx.send(f'{self.client.emotes["success"]} | Successfully created emoji: <{"a" if emj.animated else ""}:{emj.name}:{emj.id}>')
                        emoji.pop(page)
                        name.pop(page)
                        url.pop(page)
                        if(page==len(emoji)): page = page-1
                        await ses.close()
                    else:
                        await ctx.send(f'Error when making request | {r.status} response.')
                        await ses.close()
                        
                except discord.HTTPException as e:
                    if(e.code==30008): await ctx.send(f"{self.client.emotes['failed']} | Emoji Slots are full!")
                    else: await ctx.send(f"{self.client.emotes['failed']} | {e.text}")
        await send_view(self,ctx,emoji,name,url,page)

    if view.value == "3":
        if msg: await msg.delete()
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url[page]) as resp:
                file = discord.File(fp=BytesIO(await resp.read()), filename="sticker.png") 
                try:
                    sticker = await guild.create_sticker(name=name[page],description="",file=file,emoji="👌")
                    await ctx.send(f'{self.client.emotes["success"]} | Successfully created Sticker:',stickers=[sticker])
                    emoji.pop(page)
                    name.pop(page)
                    url.pop(page)
                    if(page==len(emoji)): page = page-1
                except discord.HTTPException as e:
                    if(e.code==30039): await ctx.send(f"{self.client.emotes['failed']} | Sticker Slots are full!")
                    else: await ctx.send(f"{self.client.emotes['failed']} | {e.text}")
                    
                await ses.close()
        await send_view(self,ctx,emoji,name,url,page)

    
        
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
    embed = discord.Embed(title=f"Emoji {pgno+1}/{len(url)}",color=0xfb7c04)
    embed.set_image(url=url[pgno])
    return embed


async def setup(client):
    await client.add_cog(steal(client)) 


class Buttons(discord.ui.View):
    def __init__ (self, ctx, *, timeout=60):
        super().__init__(timeout=timeout)
        self.ctx = ctx
    @discord.ui.button(emoji="◀", style=discord.ButtonStyle.green, row=0)
    async def button1_call(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
        self.value = "1"
        self.stop()
        await interaction.response.defer()
    @discord.ui.button(label="Add as Emote", style=discord.ButtonStyle.primary, row=1)
    async def button2_call(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
        self.value = "2"
        self.stop()
        await interaction.response.defer()
    @discord.ui.button(label="Add as Sticker", style=discord.ButtonStyle.primary, row=1)
    async def button3_call(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
        self.value = "3"
        self.stop()
        await interaction.response.defer()
    @discord.ui.button(emoji="▶", style=discord.ButtonStyle.green, row=0)
    async def button4_call(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
        self.value = "4"
        self.stop()
        await interaction.response.defer()