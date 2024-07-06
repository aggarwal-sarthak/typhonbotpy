from discord.ext import commands
import os
import discord
import timeago, datetime
import pytz
from src.core.validation import is_command_enabled

class serverinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description='Returns Information About Server', aliases=['server', 'si'], usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.check(is_command_enabled)
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def serverinfo(self, ctx):
        roles = []
        for role in ctx.guild.roles:
            roles.append(str(role.mention))
        roles.reverse()

        banned = [entry async for entry in ctx.guild.bans()]
        features = ""
        for feature in ctx.guild.features:
            features += self.client.emotes['success'] + ":" + str(feature.replace("_"," ")).title() + "\n"

        embed = discord.Embed(title=f"{ctx.guild.name}'s Information",color=self.client.config['color'])
        embed.add_field(name="**__About__**", value=f"**Name:** {ctx.guild.name}\n**ID:** {ctx.guild.id}\n**Owner {self.client.emotes['owner']}:** {ctx.guild.owner} [{ctx.guild.owner.mention}]\n**Created At:** {timeago.format(ctx.guild.created_at.astimezone(pytz.timezone('Asia/Kolkata')).replace(tzinfo=None),datetime.datetime.now())}\n**Members :** {ctx.guild.member_count}\n**Banned :** {len(banned)}", inline=False)
        flag = [flags for flags in ctx.guild.system_channel_flags]
        embed.add_field(name="**__Extras__**", value=f"**Verification Level:** {str(ctx.guild.verification_level).title()}\n**Upload Limit:** {ctx.guild.filesize_limit/1048576}MB\n**Inactive Channel:** {ctx.guild.afk_channel.mention if ctx.guild.afk_channel else self.client.emotes['failed']}\n**Inactive Timeout:** {str(int(ctx.guild.afk_timeout/60))+' Minutes' if ctx.guild.afk_timeout else 'None'}\n**System Messages Channel:** {ctx.guild.system_channel.mention if ctx.guild.system_channel else self.client.emotes['failed']}\n**System Welcome Messages:** {self.client.emotes['success'] if flag[0][1]==True else self.client.emotes['failed']}\n**System Boost Messages:** {self.client.emotes['success'] if flag[1][1]==True else self.client.emotes['failed']}\n**Default Notifications:** {str(ctx.guild.default_notifications).replace('NotificationLevel.','').replace('_',' ').title()}\n**Explicit Media Content Filter:** {str(ctx.guild.explicit_content_filter).replace('_',' ').title()}\n**2FA Requirement:** {self.client.emotes['success'] if str(ctx.guild.mfa_level).replace('MFALevel.','')=='require_2fa' else self.client.emotes['failed']}\n**Boost Bar Enabled:** {self.client.emotes['success'] if ctx.guild.premium_progress_bar_enabled==True else self.client.emotes['failed']}", inline=False)
        embed.add_field(name="**__Description__**", value=f"{ctx.guild.description}", inline=False)
        embed.add_field(name="**__Features__**", value=f"{features}")
        embed.add_field(name="**__Channels__**", value=f"**Total:** {len(ctx.guild.channels)}\n**Channels:** {self.client.emotes['text']} {len(ctx.guild.text_channels)} | {self.client.emotes['voice']} {len(ctx.guild.voice_channels)}\n**Rules Channel:** {ctx.guild.rules_channel.mention if ctx.guild.rules_channel else self.client.emotes['failed'] }", inline=False)
        embed.add_field(name="**__Emojis__**", value=f"**Regular:** {[emoji.animated for emoji in ctx.guild.emojis].count(False)}\n**Animated:** {[emoji.animated for emoji in ctx.guild.emojis].count(True)}", inline=False)
        embed.add_field(name="**__Boosts__**", value=f"**Level:** {ctx.guild.premium_tier} [{self.client.emotes['premium']} {ctx.guild.premium_subscription_count} Boosts]\n**Server Booster:** {ctx.guild.premium_subscriber_role.mention if ctx.guild.premium_subscriber_role else self.client.emotes['failed']}", inline=False)
        embed.add_field(name=f"**__Roles [{len(ctx.guild.roles)-1}]__**", value=", ".join(roles[:-1]) if len(roles)<40 else "Too Many Roles To Show!", inline=False)
        if ctx.guild.icon: embed.set_thumbnail(url=ctx.guild.icon)
        if ctx.guild.banner : embed.set_image(url=ctx.guild.banner)
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
        await ctx.reply(embed=embed)

async def setup(client):
    await client.add_cog(serverinfo(client))