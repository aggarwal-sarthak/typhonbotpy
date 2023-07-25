import discord
from discord.ext import commands
import os
import json

with open('emoji.json', 'r') as f:
    emotes = json.load(f)


class ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command(description="Bans Member from the Server",aliases=['None'],usage=f"{os.path.basename(__file__)[:-3]} <user> []")
    async def ban(self,ctx,user: discord.Member):
        view = Buttons(ctx)
        msg = await ctx.reply(f"You are about to ban: {user}",view=view)
        await view.wait()
        if view.value == "1":
            if msg: await msg.delete()
            await ctx.reply(f"{self.client.emotes['success']} | {user} was banned successfully!")
            return False
        if view.value == "2":
            if msg: await msg.delete()
            await ctx.reply(f"{self.client.emotes['success']} | Ban Cancelled Successfully!")
            return False







class Buttons(discord.ui.View):
    def __init__ (self, ctx, *, timeout=60):
        super().__init__(timeout=timeout)
        self.ctx = ctx
    @discord.ui.button(label="Ban", style=discord.ButtonStyle.green)
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


async def setup(client):
    await client.add_cog(ban(client)) 
