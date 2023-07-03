from discord.ext import commands
import discord
import os
import discord

class announce(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.command()
    async def announce(self, ctx, channel: discord.TextChannel=None):
        if not channel:
            await ctx.invoke(self.client.get_command('help'), f"{os.path.basename(__file__)[:-3]}")

        bot_embed = discord.Embed(title='Embed Builder : Title',description="Enter The Title Of The Announcement\n[Note] : The Title Must Not Exceed 256 Character Limit\n\n[None] : Type None For No Title\n[Cancel] : Type Cancel To Cancel Embed Builder",color=0xfb7c04)
        await ctx.reply(embed=bot_embed)
        title = await self.client.wait_for("message",timeout=60,check=lambda message:message.author==ctx.author and message.channel==ctx.channel)
        if(title.content.lower()=="cancel"):return
        else:
            title = await parse_input(title)

        bot_embed = discord.Embed(title='Embed Builder : Description',description="Enter The Description Of The Announcement\n[Note] : The Description Must Not Exceed 4096 Character Limit\n\n[None] : Type None For No Description\n[Cancel] : Type Cancel To Cancel Embed Builder",color=0xfb7c04)
        await ctx.reply(embed=bot_embed)
        description = await self.client.wait_for("message",timeout=60,check=lambda message:message.author==ctx.author and message.channel==ctx.channel)
        if(description.content.lower()=="cancel"):return
        else:
            description=await parse_input(description)

        bot_embed = discord.Embed(title='Embed Builder : Color',description="Enter The Color Of The Announcement\n[Note] : The Color Must Be In HexCode Format\n\n[None] : Type None For No Color\n[Cancel] : Type Cancel To Cancel Embed Builder",color=0xfb7c04)
        await ctx.reply(embed=bot_embed)
        color = await get_color(self,ctx)

        bot_embed = discord.Embed(title='Embed Builder : Thumbnail',description="Enter The Thumbnail Of The Announcement\n[Note] : The Thumbnail Must Be In Link Format\n\n[None] : Type None For No Thumbnail\n[Cancel] : Type Cancel To Cancel Embed Builder",color=0xfb7c04)
        await ctx.reply(embed=bot_embed)
        thumbnail = await self.client.wait_for("message",timeout=60,check=lambda message:message.author==ctx.author and message.channel==ctx.channel)
        if(thumbnail.content.lower()=="cancel"):return
        else:
            thumbnail = await parse_input(thumbnail)

        bot_embed = discord.Embed(title='Embed Builder : Image',description="Enter The Image Of The Announcement\n[Note] : The Image Must Be In Link Format\n\n[None] : Type None For No Image\n[Cancel] : Type Cancel To Cancel Embed Builder",color=0xfb7c04)
        await ctx.reply(embed=bot_embed)
        image = await self.client.wait_for("message",timeout=60,check=lambda message:message.author==ctx.author and message.channel==ctx.channel)
        if(image.content.lower()=="cancel"):return
        else:
            image = await parse_input(image)

        bot_embed = discord.Embed(title='Embed Builder : Footer',description="Enter The Footer Of The Announcement\n[Note] : The Footer Must Not Exceed 2048 Character Limit\n\n[None] : Type None For No Footer\n[Cancel] : Type Cancel To Cancel Embed Builder",color=0xfb7c04)
        await ctx.reply(embed=bot_embed)
        footer = await self.client.wait_for("message",timeout=60,check=lambda message:message.author==ctx.author and message.channel==ctx.channel)
        if(footer.content.lower()=="cancel"):return
        else:
            footer = await parse_input(footer)
        try:
            user_embed=discord.Embed(title=title,description=description,color=color)
        except Exception as e:
            print('\n\n\n\n\n\n\n\n\n',e)
        user_embed.set_thumbnail(url=thumbnail)
        user_embed.set_image(url=image)
        user_embed.set_footer(text=footer)
        self.send_channel = channel
        self.send_embed = user_embed
        view = Buttons()

        msg = await ctx.reply(embed=user_embed, view=view)
        await view.wait()
        if view.value == "1":
            if msg: await msg.delete()
            await ctx.reply(f"{self.client.emotes['success']} | Message Announced Successfully!")
            await channel.send(embed=user_embed)
        if view.value == "2":
            await ctx.reply(f"{self.client.emotes['failed']} | Message Cancelled Successfully!")

class Buttons(discord.ui.View):
    def __init__ (self, *, timeout=60):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Send", style=discord.ButtonStyle.green)
    async def button1_call(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "1"
        self.stop()
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def button2_call(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "2"
        self.stop()
    @discord.ui.button(label="Edit")
    async def button3_call(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "3"
        self.stop()
        
async def get_color(self,ctx):
    color = await self.client.wait_for("message",timeout=60,check=lambda message:message.author==ctx.author and message.channel==ctx.channel)
    if(color.content.lower()=="cancel"):return
    else:
        color = await parse_input(color)
        if(color):
            method = getattr(discord.Color, color, None)
            if method and callable(method):
                color = method()
            elif(color.startswith("#")):
                color = int(color[1:],16)
            elif(color.startswith("0x")):
                color = int(color,16)
            else:
                await ctx.reply("Invalid color! Enter correct Color again!")
                color = await get_color(self,ctx)
        return color

async def setup(client):
    await client.add_cog(announce(client)) 

async def parse_input(input):
    if(input.content.lower()=="none"):
        input = None
    else:
        input = input.content
    return input