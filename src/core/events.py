import asyncio
import datetime
import discord
from discord.ext import commands
import logging

from src.core.buttons import Prompt

logging.basicConfig(level=logging.DEBUG)

class EventHandler:
    def __init__(self, tether_instance):
        self.tether = tether_instance
        self.client = tether_instance.client
        self.db = tether_instance.db
        self.constants = tether_instance.constants

        self.client.add_listener(self.on_ready)
        self.client.add_listener(self.on_command)
        self.client.add_listener(self.on_command_error)
        self.client.add_listener(self.on_guild_join)
        self.client.add_listener(self.on_guild_remove)

    async def on_ready(self):
        logs_channel = self.client.get_channel(int(self.tether.bot_logs))
        if logs_channel:
            await logs_channel.send(f"```{self.constants.success_emoji} Bot Started!```")
        logging.info(f'{self.constants.success_emoji} {self.client.user.name} Is Ready!')

    async def on_command(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            return
        
        guild_id = ctx.guild.id
        guild_db = self.db.guilds.find_one_and_update(
            {"guild_id": guild_id},
            {"$set": {"updated": True}},
            upsert=True,
            return_document=True
        )

        if not guild_db.get('updated', False):
            view = Prompt(ctx.author.id)
            msg = await ctx.send(f"{self.constants.bot} | A New Mail Has Arrived. Click To Read!", view=view, ephemeral=True)
            await view.wait()

            try:
                if view.value:
                    if msg:
                        await msg.delete()
                    embed = discord.Embed.from_dict(self.db.updatelog.find_one({}))
                    await ctx.send(embed=embed)
                    target_channel = self.client.get_channel(self.tether.update_logs)
                    if target_channel:
                        await target_channel.send(f"```{ctx.author.name} - {ctx.author.id} in {ctx.guild.name} - {ctx.guild.id}```")
                elif view.value is False:
                    if msg:
                        await msg.delete()
            except Exception as e:
                await self.tether.handle_error(ctx, e)

    async def on_guild_join(self, guild):
        members_count = len(guild.members)

        invite_link = None
        if guild.me.guild_permissions.create_instant_invite:
            invite = await guild.text_channels[0].create_invite()
            invite_link = invite.url

        icon_url = guild.icon.url if guild.icon else None

        embed = discord.Embed(title="JOINED A SERVER", color=0xfb7c04)
        embed.add_field(name="SERVER NAME:", value=guild.name, inline=False)
        embed.add_field(name="SERVER ID:", value=guild.id, inline=False)
        embed.add_field(name="SERVER MEMBERS: ", value=members_count, inline=False)
        if invite_link: embed.add_field(name="INVITE LINK:", value=invite_link, inline=False)
        if icon_url: embed.set_thumbnail(url=icon_url)

        client_total_servers = len(self.client.guilds)
        client_total_members = sum(len(g.members) for g in self.client.guilds)
        embed.set_footer(text=f"BOT SERVERS: {client_total_servers} | BOT MEMBERS: {client_total_members}")

        target_channel = self.client.get_channel(self.tether.join_logs)
        if target_channel:
            await target_channel.send(embed=embed)

    async def on_guild_remove(self, guild):
        self.db.guilds.delete_one({"guild_id": guild.id})

        members_count = len(guild.members)
        icon_url = guild.icon.url if guild.icon else None

        embed = discord.Embed(title="LEFT A SERVER", color=0xfb7c04)
        embed.add_field(name="SERVER NAME:", value=guild.name, inline=False)
        embed.add_field(name="SERVER ID:", value=guild.id, inline=False)
        embed.add_field(name="SERVER MEMBERS: ", value=members_count, inline=False)
        if icon_url: embed.set_thumbnail(url=icon_url)

        client_total_servers = len(self.client.guilds)
        client_total_members = sum(len(g.members) for g in self.client.guilds)
        embed.set_footer(text=f"BOT SERVERS: {client_total_servers} | BOT MEMBERS: {client_total_members}")

        target_channel = self.client.get_channel(self.tether.leave_logs)
        if target_channel:
            await target_channel.send(embed=embed)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        
        if not isinstance(error, commands.CommandOnCooldown):
            ctx.command.reset_cooldown(ctx)

        if isinstance(error, commands.CommandInvokeError) and isinstance(error.original, asyncio.TimeoutError):
            await ctx.reply(f"{self.constants.failed} Command Timed Out!")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            help_command = self.client.get_command('help')
            parent_name = ctx.command.parent.name if ctx.command.parent else ctx.command.name
            await ctx.invoke(help_command, parent_name, ctx.command.name)
            return

        if isinstance(error, commands.CommandOnCooldown):
            now = datetime.datetime.now()
            retry_time = now + datetime.timedelta(seconds=error.retry_after)
            retry_message = f"{self.constants.failed} Command On Cooldown! Try again <t:{int(retry_time.timestamp())}:R>!"
            reply = await ctx.reply(retry_message)
            await asyncio.sleep(error.retry_after)
            if reply:
                await reply.delete()
            return

        if isinstance(error, (commands.MissingPermissions, commands.BotMissingPermissions)):
            permission_type = "Bot" if isinstance(error, commands.BotMissingPermissions) else "You"
            err = str(error).replace(f'{permission_type} requires ', '').replace(' permission(s) to run this command.', '')
            await ctx.reply(f"{self.constants.failed} {permission_type} Don't Have `{err}` Permission To Run This Command!")
            return
        
        target_channel = self.client.get_channel(self.tether.error_logs)
        if target_channel:
            await target_channel.send(f'```{ctx.command.name} : {error}```')
