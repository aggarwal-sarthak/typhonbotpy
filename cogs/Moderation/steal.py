
import discord
from discord.ext import commands
from discord import Button
import os
import json

with open('emoji.json', 'r') as f:
    emotes = json.load(f)

class steal(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.command(description="Add Emotes and Stickers to Server",aliases=['add'],usage=f"{os.path.basename(__file__)[:-3]} <emote>")
    async def steal(self, ctx,*args):
        try:
            emoji = []
            if(ctx.message.reference is not None):
                msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                if(len(msg.stickers)>0):
                    sticker = msg.stickers[0]
                    print(sticker.url)
                else:
                    emoji = msg.content.split()     #needs emoji verification
            else:
                if(len(args)>0):
                    for em in args:
                        emoji.append(em)            #needs verif
                    print("emote")
                elif(len(ctx.message.stickers)>0):
                    sticker = ctx.message.stickers[0]
                    print("stickers")
                else:
                    await ctx.reply(f"{self.client.emotes['failed']}| No emojis or stickers found!")
            if(len(emoji)>0):
                await send_view(self,ctx,emoji)
                page = 0 
                name, url = await get_name_url(emoji)
                embed = await create_embed(url,page)
                view = Buttons(ctx)
                message = await ctx.reply(embed=embed,view=view)
                await view.wait()
            else:
                pass
        except Exception as e:
            print("\n\n\n\n\n\n",e)

async def send_view(self,ctx,emoji,page=0):
    name, url = await get_name_url(emoji)
    embed = await create_embed(url,page)
    view = Buttons(ctx)
    msg = await ctx.reply(embed=embed,view=view)
    await view.wait()
    if view.value == "1":
        if msg: await msg.delete()
        if(page==0):
            await ctx.reply("Cannot go back!")
            await send_view(self,ctx,emoji)
        else:
            page -= 1
            await send_view(self,ctx,emoji,page)
        return False
    if view.value == "2":
        if msg: await msg.delete()
        await ctx.reply(f"{self.client.emotes['success']} | Message Cancelled Successfully!")
        return False
    if view.value == '3':
        if msg: await msg.delete()
        if(page==len(emoji)-1):
            await ctx.reply("Cannot go ahead!")
            await send_view(self,ctx,emoji,page)
        else:
            page+=1
            await send_view(self,ctx,emoji,page)

async def get_name_url(emoji):
    name  = []
    url = []
    for emote in emoji:
        if emote[1]=='a':
            index = emote.find(":",5)
            name.append(emote[3:index])
            print(emote)
            url.append("https://cdn.discordapp.com/emojis/" +f"{emote[index+1:-1]}.gif")
        else:
            index = emote.find(":",4)
            name.append(emote[2:index])
            print(emote)
            url.append("https://cdn.discordapp.com/emojis/" +f"{emote[index+1:-1]}.png")
    return name,url

async def create_embed(url,pgno):
    print(url)
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
    @discord.ui.button(label="Add", style=discord.ButtonStyle.red)
    async def button2_call(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
        self.value = "2"
        self.stop()
        await interaction.response.defer()
    @discord.ui.button(label="Next")
    async def button3_call(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
        self.value = "3"
        self.stop()
        await interaction.response.defer()