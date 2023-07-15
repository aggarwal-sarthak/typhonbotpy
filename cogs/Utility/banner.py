from discord.ext import commands
import os
import discord
import requests

class banner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.bot_has_permissions(embed_links=True)
    @commands.command(description='Returns Banner For User/Server', usage=f"{os.path.basename(__file__)[:-3]} user\n{os.path.basename(__file__)[:-3]} server")
    async def banner(self, ctx, mode, *member: discord.Member):
        embed = discord.Embed(title=None,color=0xfb7c04)

        class Buttons(discord.ui.view):
            def __init__(self, client, ctx, *, timeout=60, globalbutton: discord.ui.Button = discord.ui.Button(label="Global Banner", style=discord.ButtonStyle.green), serverbanner: discord.ui.Button = discord.ui.Button(label="Server Banner", style=discord.ButtonStyle.green)):
                self.client = client
                super().__init__(timeout=timeout)
            
            async def global_callback(self, interaction: discord.Interaction):
                if interaction.user != self.ctx.author:
                    return await interaction.response.send_message(f"{self.client.emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
                await interaction.response.defer()

            async def server_callback(self, interaction: discord.Interaction):
                if interaction.user != self.ctx.author:
                    return await interaction.response.send_message(f"{self.client.emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
                await interaction.response.defer()

            async def global_banner(self, ctx):
                headers = {
                'Authorization': f'{self.client.config["token"]}',
                'User-Agent': f'DiscordBot {self.client.user.name}',
                }
                url = f'https://discord.com/api/v9/guilds/{ctx.guild.id}/members/{member.id}'
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    banner = data.get('banner')
                    if banner:
                        return f'https://cdn.discordapp.com/banners/{ctx.guild.id}/{banner}.gif'
                    else:
                        return None

        match mode:
            case "server" | "s":
                if ctx.guild.banner :
                    embed.set_image(url=ctx.guild.banner)
                    embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
                    await ctx.reply(embed=embed)
                else:
                    await ctx.reply(f"{self.client.emotes['failed']} | This Server Does Not Have A Banner!")
            
            case "user" | "u":
                if not member: member = ctx.author
                try:
                    user = await self.client.fetch_user(member.id)
                    banner_url = user.banner.url
                    embed.set_image(url=banner_url)
                    await ctx.reply(embed=embed)
                except:
                    await ctx.reply(f"{self.client.emotes['failed']} | {member} Does Not Have A Banner!")

async def setup(client):
    await client.add_cog(banner(client))