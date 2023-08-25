from discord.ext import commands
import discord
import os
import discord
import json

with open('emoji.json', 'r') as f:
    emotes = json.load(f)

class announce(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    @commands.command(description="Embed Builder",aliases=['embed','ann'],usage=f"{os.path.basename(__file__)[:-3]} <Channel>")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def announce(self, ctx, channel: discord.TextChannel):
        embed_dict = dict()
        embed_dict['title'] = await get_title(self,ctx)
        embed_dict['description'] = await get_description(self,ctx)
        embed_dict['color'] = await get_color(self,ctx)
        user_embed = await create_embed(self,ctx,embed_dict)
        await get_thumbnail(self,ctx,user_embed)
        await get_image(self,ctx,user_embed)
        await get_footer(self,ctx,user_embed)
        await send_view(self,ctx,channel,user_embed,embed_dict)

class Buttons(discord.ui.View):
    def __init__ (self, ctx, *, timeout=60):
        super().__init__(timeout=timeout)
        self.ctx = ctx
    @discord.ui.button(label="Send", style=discord.ButtonStyle.green)
    async def button1_call(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
        self.value = "1"
        self.stop()
        await interaction.response.defer()
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def button2_call(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
        self.value = "2"
        self.stop()
        await interaction.response.defer()
    @discord.ui.button(label="Edit")
    async def button3_call(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
        self.value = "3"
        self.stop()
        await interaction.response.defer()
        
async def get_title(self,ctx):
    bot_embed = discord.Embed(title='Embed Builder : Title',description="Enter The Title Of The Announcement\n[Note] : The Title Must Not Exceed 256 Character Limit\n\n[None] : Type None For No Title\n[Cancel] : Type Cancel To Cancel Embed Builder",color=0xfb7c04)
    await ctx.reply(embed=bot_embed)
    title = await self.client.wait_for("message",timeout=60,check=lambda message:message.author==ctx.author and message.channel==ctx.channel)
    if(title.content.lower()=="cancel"):
        await ctx.reply(f"{self.client.emotes['success']} | Embed Builder Cancelled Successfully!")
        raise commands.CommandError("Command Cancelled")
    else:
        title = await parse_input(title)
    return title

async def get_description(self,ctx):
    bot_embed = discord.Embed(title='Embed Builder : Description',description="Enter The Description Of The Announcement\n[Note] : The Description Must Not Exceed 4096 Character Limit\n\n[None] : Type None For No Description\n[Cancel] : Type Cancel To Cancel Embed Builder",color=0xfb7c04)
    await ctx.reply(embed=bot_embed)
    description = await self.client.wait_for("message",timeout=60,check=lambda message:message.author==ctx.author and message.channel==ctx.channel)
    if(description.content.lower()=="cancel"):
        await ctx.reply(f"{self.client.emotes['success']} | Embed Builder Cancelled Successfully!")
        raise commands.CommandError("Command Cancelled")
    else:
        description=await parse_input(description)
    return description

async def get_color(self,ctx):
    bot_embed = discord.Embed(title='Embed Builder : Color',description="Enter The Color Of The Announcement\n[Note] : The Color Must Be In HexCode Format\n\n[None] : Type None For No Color\n[Cancel] : Type Cancel To Cancel Embed Builder",color=0xfb7c04)
    await ctx.reply(embed=bot_embed)
    color = await self.client.wait_for("message",timeout=60,check=lambda message:message.author==ctx.author and message.channel==ctx.channel)
    if(color.content.lower()=="cancel"):
        await ctx.reply(f"{self.client.emotes['success']} | Embed Builder Cancelled Successfully!")
        raise commands.CommandError("Command Cancelled")
    else:
        color = await parse_input(color)
        if(color):
            method = getattr(discord.Color, color.lower()   , None)
            if method and callable(method):
                color = method()
            elif(color.startswith("#")):
                color = int(color[1:],16)
            elif(color.startswith("0x")):
                color = int(color,16)
            else:
                await ctx.reply(f"{self.client.emotes['failed']} | Invalid Color! Enter Correct Color Again!")
                color = await get_color(self,ctx)
        return color

async def get_thumbnail(self,ctx,user_embed):
    bot_embed = discord.Embed(title='Embed Builder : Thumbnail',description="Enter The Thumbnail Of The Announcement\n[Note] : Must Be an Attachment or In Link Format\n\n[None] : Type None For No Thumbnail\n[Cancel] : Type Cancel To Cancel Embed Builder",color=0xfb7c04)
    await ctx.reply(embed=bot_embed)
    thumbnail = await self.client.wait_for("message",timeout=60,check=lambda message:message.author==ctx.author and message.channel==ctx.channel)
    if(len(thumbnail.attachments)!=0):
        user_embed.set_thumbnail(url=thumbnail.attachments[0].proxy_url)

    elif(thumbnail.content.lower()=="cancel"):
        await ctx.reply(f"{self.client.emotes['success']} | Embed Builder Cancelled Successfully!")
        raise commands.CommandError("Command Cancelled")
    else:
        thumbnail = await parse_input(thumbnail)
        if(thumbnail!=None):
            if(await verif_url(thumbnail)):
                user_embed.set_thumbnail(url=thumbnail)
            else:
                await ctx.reply(f"{self.client.emotes['failed']} | Invalid Thumbnail Link! Enter Correct Link For Thumbnail Again!")
                await get_thumbnail(self,ctx,user_embed)
        else:
            return

async def verif_url(url):
    if(url.startswith("http://") or url.startswith("https://")):
        for i in ['.jpg','.jpeg','.png','.webp']:
            if i in url:
                return True
    return False

async def get_image(self,ctx,user_embed):
    bot_embed = discord.Embed(title='Embed Builder : Image',description="Enter The Image Of The Announcement\n[Note] : Must Be an Attachment or In Link Format\n\n[None] : Type None For No Image\n[Cancel] : Type Cancel To Cancel Embed Builder",color=0xfb7c04)
    await ctx.reply(embed=bot_embed)
    image = await self.client.wait_for("message",timeout=60,check=lambda message:message.author==ctx.author and message.channel==ctx.channel)
    if(len(image.attachments)!=0):
        user_embed.set_image(url=image.attachments[0].proxy_url)
    
    elif(image.content.lower()=="cancel"):
        await ctx.reply(f"{self.client.emotes['success']} | Embed Builder Cancelled Successfully!")
        raise commands.CommandError("Command Cancelled")
    else:
        image = await parse_input(image)
        if(image!=None):
            if(await verif_url(image)):
                user_embed.set_image(url=image)
            else:
                await ctx.reply(f"{self.client.emotes['failed']} | Invalid Image Link! Enter Correct Link For Image Again!")
                await get_image(self,ctx,user_embed)
        else:
            return  

async def get_footer(self,ctx,user_embed):
    bot_embed = discord.Embed(title='Embed Builder : Footer',description="Enter The Footer Of The Announcement\n[Note] : The Footer Must Not Exceed 2048 Character Limit\n\n[None] : Type None For No Footer\n[Cancel] : Type Cancel To Cancel Embed Builder",color=0xfb7c04)
    await ctx.reply(embed=bot_embed)
    footer = await self.client.wait_for("message",timeout=60,check=lambda message:message.author==ctx.author and message.channel==ctx.channel)
    if(footer.content.lower()=="cancel"):
        await ctx.reply(f"{self.client.emotes['success']} | Embed Builder Cancelled Successfully!")
        raise commands.CommandError("Command Cancelled")
    else:
        footer = await parse_input(footer)
        user_embed.set_footer(text=footer)

async def parse_input(input):
    if(input.content.lower()=="none"):
        input = None
    else:
        input = input.content
    return input

async def create_embed(self,ctx,dict):
    user_embed=discord.Embed(title=dict['title'],description=dict['description'],color=dict['color'])
    return user_embed

async def send_view(self,ctx,channel,user_embed,embed_dict):
    view = Buttons(ctx)
    msg = await ctx.reply(embed=user_embed, view=view)
    await view.wait()
    if view.value == "1":
        if msg: await msg.delete()
        await ctx.reply(f"{self.client.emotes['success']} | Message Announced Successfully!")
        await channel.send(embed=user_embed)
        return False
    if view.value == "2":
        if msg: await msg.delete()
        await ctx.reply(f"{self.client.emotes['success']} | Message Cancelled Successfully!")
        return False
    if view.value == '3':
        if msg: await msg.delete()
        await ctx.reply(f"{self.client.emotes['success']} | Enter The Field To Edit!")
        field = await self.client.wait_for("message",timeout=60,check=lambda message:message.author==ctx.author and message.channel==ctx.channel)
        match field.content.lower():
            case "title":
                title = await get_title(self,ctx)
                embed_dict['title'] = title
                user_embed = await create_embed(self,ctx,embed_dict)
                await send_view(self,ctx,channel,user_embed,embed_dict)
            case "description":
                description = await get_description(self,ctx)
                embed_dict['description'] = description
                user_embed = await create_embed(self,ctx,embed_dict)
                await send_view(self,ctx,channel,user_embed,embed_dict)
            case "color":
                color = await get_color(self,ctx)
                embed_dict['color'] = color
                user_embed = await create_embed(self,ctx,embed_dict)
                await send_view(self,ctx,channel,user_embed,embed_dict)
            case "thumbnail":
                await get_thumbnail(self,ctx,user_embed)
                await send_view(self,ctx,channel,user_embed,embed_dict) 
            case "image":
                await get_image(self,ctx,user_embed)
                await send_view(self,ctx,channel,user_embed,embed_dict) 
            case "footer":
                await get_footer(self,ctx,user_embed)
                await send_view(self,ctx,channel,user_embed,embed_dict) 
            case _:
                await ctx.reply(f"{self.client.emotes['failed']} | Invalid Field To Edit!")

async def setup(client):
    await client.add_cog(announce(client)) 