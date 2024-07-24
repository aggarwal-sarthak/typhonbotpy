import os
import discord
from discord.ext import commands
import timeago
import datetime
import pytz
from src.core.bot import tether
from src.core.check import command_enabled


class Serverinfo(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(
        description="Returns Information About Server",
        aliases=["server", "si"],
        usage=f"{os.path.basename(__file__)[:-3]}",
    )
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @command_enabled()
    async def serverinfo(self, ctx: commands.Context):
        banned_count = [entry async for entry in ctx.guild.bans()]

        roles = [role.mention for role in reversed(ctx.guild.roles)]
        features = "\n".join(
            f"{tether.constants.success}: {feature.replace('_', ' ').title()}"
            for feature in ctx.guild.features
        )

        system_welcome_messages = (
            tether.constants.success
            if ctx.guild.system_channel_flags.join_notifications
            else tether.constants.failed
        )
        system_boost_messages = (
            tether.constants.success
            if ctx.guild.system_channel_flags.premium_subscriptions
            else tether.constants.failed
        )
        afk_timeout = (
            f"{ctx.guild.afk_timeout / 60} minutes" if ctx.guild.afk_timeout else "None"
        )

        embed = discord.Embed(
            title=f"{ctx.guild.name}'s Information",
            color=discord.Colour.from_str(tether.color),
        )
        embed.add_field(
            name="**__About__**",
            value=f"**Name:** {ctx.guild.name}\n**ID:** {ctx.guild.id}\n**Owner {tether.constants.owner}:** {ctx.guild.owner} [{ctx.guild.owner.mention}]\n**Created At:** {timeago.format(ctx.guild.created_at.astimezone(pytz.timezone('Asia/Kolkata')).replace(tzinfo=None), datetime.datetime.now())}\n**Members :** {ctx.guild.member_count}\n**Banned :** {len(banned_count)}",
            inline=False,
        )
        embed.add_field(
            name="**__Extras__**",
            value=f"**Verification Level:** {ctx.guild.verification_level}\n**Upload Limit:** {ctx.guild.filesize_limit / 1048576}MB\n**Inactive Channel:** {ctx.guild.afk_channel.mention if ctx.guild.afk_channel else tether.constants.failed}\n**Inactive Timeout:** {afk_timeout}\n**System Messages Channel:** {ctx.guild.system_channel.mention if ctx.guild.system_channel else tether.constants.failed}\n**System Welcome Messages:** {system_welcome_messages}\n**System Boost Messages:** {system_boost_messages}\n**Default Notifications:** {str(ctx.guild.default_notifications).replace('NotificationLevel.','').replace('_',' ').title()}\n**Explicit Media Content Filter:** {str(ctx.guild.explicit_content_filter).replace('_',' ').title()}\n**2FA Requirement:** {tether.constants.success if str(ctx.guild.mfa_level).replace('MFALevel.','')=='require_2fa' else tether.constants.failed}\n**Boost Bar Enabled:** {tether.constants.success if ctx.guild.premium_progress_bar_enabled else tether.constants.failed}",
            inline=False,
        )
        embed.add_field(
            name="**__Description__**",
            value=f"```{ctx.guild.description}```",
            inline=False,
        )
        embed.add_field(name="**__Features__**", value=f"{features}")
        embed.add_field(
            name="**__Channels__**",
            value=f"**Total:** {len(ctx.guild.channels)}\n**Channels:** {tether.constants.text} {len(ctx.guild.text_channels)} | {tether.constants.voice} {len(ctx.guild.voice_channels)}\n**Rules Channel:** {ctx.guild.rules_channel.mention if ctx.guild.rules_channel else tether.constants.failed}",
            inline=False,
        )
        embed.add_field(
            name="**__Emojis__**",
            value=f"**Regular:** {sum(1 for emoji in ctx.guild.emojis if not emoji.animated)}\n**Animated:** {sum(1 for emoji in ctx.guild.emojis if emoji.animated)}",
            inline=False,
        )
        embed.add_field(
            name="**__Boosts__**",
            value=f"**Level:** {ctx.guild.premium_tier} [{tether.constants.premium} {ctx.guild.premium_subscription_count} Boosts]\n**Server Booster:** {ctx.guild.premium_subscriber_role.mention if ctx.guild.premium_subscriber_role else tether.constants.failed}",
            inline=False,
        )
        embed.add_field(
            name=f"**__Roles [{len(roles)-1}]__**",
            value=(
                ", ".join(roles[:-1]) if len(roles) < 40 else "Too Many Roles To Show!"
            ),
            inline=False,
        )
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        if ctx.guild.banner:
            embed.set_image(url=ctx.guild.banner.url)
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
        )

        await ctx.reply(embed=embed)


async def setup(client: commands.Bot):
    await client.add_cog(Serverinfo(client))
