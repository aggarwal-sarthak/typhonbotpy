from __future__ import annotations
from typing import Optional,Callable, Dict, List, Any
from discord import ButtonStyle,ChannelType, CategoryChannel, Embed, ForumChannel, HTTPException, Interaction, StageChannel, Colour, SelectOption, TextStyle,Embed, Member, Role
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ui import Item, Select, select, Button, button, View, ChannelSelect, Modal, TextInput
from contextlib import suppress
import json
import os
from validation import is_command_enabled
import timeago, datetime
import pytz
import requests

with open('emoji.json', 'r') as f:
    emotes = json.load(f)
with open('config.json', 'r') as f:
    config = json.load(f)

class utilcmd(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.deleted_messages = {}

    @commands.command(description='Custom Embed Builder',aliases = ['embed', 'ann'], usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.check(is_command_enabled)
    @commands.has_guild_permissions(administrator=True)
    @commands.bot_has_guild_permissions(administrator=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def announce(self,ctx):
        global author
        author = ctx.author
        try:
            view = EmbedCreator(bot=self.client)
            await ctx.send(embed=view.get_default_embed, view=view)
        except Exception as e:
            pass
    @commands.command(description='Returns User Avatar', aliases=['av'], usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.check(is_command_enabled)
    @commands.bot_has_permissions(embed_links=True)
    async def avatar(self, ctx, member: Member=None):
        if not member: member = ctx.author
        embed = Embed(title=f"{member}'s Avatar",color=self.client.config['color'])
        embed.set_image(url=member.display_avatar)
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
        await ctx.reply(embed=embed)

    @commands.group(name='banner', description='Returns Banner', usage=f"{os.path.basename(__file__)[:-3]} <user>", invoke_without_command=True)
    @commands.check(is_command_enabled)
    @commands.bot_has_permissions(embed_links=True)
    async def banner(self, ctx, member: Member=None):
        if not member: member = ctx.author
        try:
            embed = Embed(title=f"{member}'s Banner",color=self.client.config['color'])
            user = await self.client.fetch_user(member.id)
            banner_url = user.banner.url
            embed.set_image(url=banner_url)
            embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
            await ctx.reply(embed=embed)
        except:
            await ctx.reply(f"{self.client.emotes['failed']} | `{member}` Does Not Have A Banner!")

    @banner.command(name='server', description='Returns Server Banner', usage=f"{os.path.basename(__file__)[:-3]} server")
    @commands.bot_has_permissions(embed_links=True)
    async def server(self, ctx):
        if ctx.guild.banner :
            embed = Embed(title=f"{ctx.guild}'s Banner",color=self.client.config['color'])
            embed.set_image(url=ctx.guild.banner)
            embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
            await ctx.reply(embed=embed)
        else:
            await ctx.reply(f"{self.client.emotes['failed']} | This Server Does Not Have A Banner!")

    @commands.command(description='Returns First Message In The Channel By The User', usage=f"{os.path.basename(__file__)[:-3]} firstmsg [user]")
    @commands.check(is_command_enabled)
    @commands.bot_has_permissions(embed_links=True, read_message_history=True)
    async def firstmsg(self, ctx, member: Member=None):
        if not member:
            member = ctx.author

        async for message in ctx.channel.history(limit=None, oldest_first=True):
            if message.author == member:
                return await message.reply(f"{self.client.emotes['success']} | Found First Message By `{member.name}`!")
                
        await ctx.reply(f"{self.client.emotes['failed']} | No Message Found By `{member.name}`!")

    @commands.command(description='Returns Membercount', usage=f"{os.path.basename(__file__)[:-3]}", aliases= ['members', 'mc'])
    @commands.check(is_command_enabled)
    async def membercount(self, ctx):
        embed = Embed(title=None,color=self.client.config['color'])
        embed.add_field(name='**Members**', value=ctx.guild.member_count)
        embed.timestamp = ctx.message.created_at
        await ctx.reply(embed=embed)

    @commands.command(description='Returns Information About Mentioned Role', usage=f"{os.path.basename(__file__)[:-3]} <role>")
    @commands.check(is_command_enabled)
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def roleinfo(self, ctx, role: Role=None):
        permissions = ", ".join(sorted([str(perms[0]).replace("_"," ").title() for perms in role.permissions if perms[1] is True]))
        if not permissions: permissions = "None"
        
        embed = Embed(title=None,color=self.client.config['color'])
        embed.add_field(name="**__General Information__**", value=f"**Name :** {role.name}\n**ID :** {role.id}\n**Role Position :** {len(ctx.guild.roles) - role.position}\n**Color :** {role.color}\n**Created At :** {timeago.format(role.created_at.astimezone(pytz.timezone('Asia/Kolkata')).replace(tzinfo=None),datetime.datetime.now())}\n**Mentionable :** {str(role.mentionable).title()}\n**Hoisted :** {str(role.hoist).title()}\n**Managed :** {str(role.managed).title()}", inline=False)
        embed.add_field(name="**__Permissions__**", value=f"{permissions if len(permissions)<=256 else 'Too Many Permissions To Show!'}", inline=False)
        embed.add_field(name=f"**__Members [{len(role.members)}]__**", value=f"{', '.join([member.mention for member in role.members]) if len(', '.join([member.mention for member in role.members]))<256 else 'Too Many Members To Show!'}", inline=False)
        if role.icon: embed.set_thumbnail(url=role.icon)
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
        await ctx.reply(embed=embed)

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

        embed = Embed(title=f"{ctx.guild.name}'s Information",color=self.client.config['color'])
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

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.deleted_messages[message.channel.id] = message

    @commands.command(description='Returns Last Deleted Messaged In The Channel', usage=f"{os.path.basename(__file__)[:-3]}")
    @commands.check(is_command_enabled)
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def snipe(self, ctx):
        if ctx.channel.id not in self.deleted_messages:
            return await ctx.reply(f"{self.client.emotes['failed']} | No Deleted Messages Found In This Channel!")

        embed = Embed(title='Message Found',color=self.client.config['color'])
        embed.add_field(name="**__Information__**", value=f"**Message By :** {self.deleted_messages[ctx.channel.id].author.mention}\n**Channel :** {ctx.channel.mention}\n**Time :** {timeago.format(self.deleted_messages[ctx.channel.id].created_at.astimezone(pytz.timezone('Asia/Kolkata')).replace(tzinfo=None),datetime.datetime.now())}", inline=False)
        embed.add_field(name="**__Content__**", value=f"{self.deleted_messages[ctx.channel.id].content}", inline=False)
        if len(self.deleted_messages[ctx.channel.id].attachments): embed.set_image(url=self.deleted_messages[ctx.channel.id].attachments[0].url)
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
        await ctx.reply(embed=embed)


    @commands.command(usage=f"{os.path.basename(__file__)[:-3]} <Text>", description = "Returns Superscript Of A Given Text", aliases = ['sup'])
    @commands.check(is_command_enabled)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def superscript(self, ctx:commands.Context, *, text:str):
        await ctx.reply(get_super(text))

    @commands.command(description='Returns Urban Dictionary Meaning Of The Query', usage=f"{os.path.basename(__file__)[:-3]} <Query>")
    @commands.check(is_command_enabled)
    async def urban(self, ctx, *, query):
        url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
        querystring = {"term": query}
        headers = {
	        "X-RapidAPI-Key": self.client.config['rapidapi'],
	        "X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring).json()
        if not len(response['list']):
            msg = 'No Meaning Found!'
        else:
            msg = response['list'][0]['definition']

        embed = Embed(title=query, description=msg, color=self.client.config['color'])
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
        await ctx.reply(embed=embed)

    @commands.command(description="Returns Information For The Mentioned User", aliases=['user', 'ui', 'about'], usage=f"{os.path.basename(__file__)[:-3]} [User]")
    @commands.check(is_command_enabled)
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def userinfo(self, ctx, member:Member=None):
        if not member:
            member = ctx.author

        roles = []
        for role in member.roles:
            roles.append(str(role.mention))
        roles.reverse()

        permissions = [str(permission) for permission, value in member.guild_permissions if value]
        permission_list = []
        for permission in permissions:
            words = permission.split("_")
            capitalized_words = [word.capitalize() for word in words]
            formatted_permission = " ".join(capitalized_words)
            permission_list.append(formatted_permission)
        permission_list.sort()

        if ctx.guild.owner_id == member.id: ack = "Server Owner"
        elif "Administrator" in permission_list: ack = "Server Administrator"
        elif "Manage Guild" in permission_list: ack = "Server Moderator"
        else: ack = "Server Member"

        embed = Embed(title=None,color=self.client.config['color'])
        badges = member.public_flags.all()
        badge_text=""
        for badge in badges:
            badge_text += self.client.emotes[f'{badge.name}']+" "
        now = datetime.datetime.now()
        embed.add_field(name="**__General Information__**", value=f"**Name :** {member}\n**ID :** {member.id}\n**Nickname :** {member.nick}\n**Badges :** {badge_text}\n**Account Creation :** {timeago.format(member.created_at.astimezone(pytz.timezone('Asia/Kolkata')).replace(tzinfo=None),now)}\n**Server Joined :** {timeago.format(member.joined_at.astimezone(pytz.timezone('Asia/Kolkata')).replace(tzinfo=None),now)}", inline=False)
        if len(str(", ".join([x.mention for x in member.roles])))>1024:
            embed.add_field(name=f"**__Roles [{len(member.roles)-1}]__**", value="Too Many To Display!", inline=False)
        else:
            embed.add_field(name=f"**__Roles [{len(member.roles)-1}]__**", value=", ".join(roles[:-1]), inline=False)
        if len(", ".join([x for x in permission_list]))>1024:
            embed.add_field(name=f"**__Permissions__**", value="Too Many To Display!", inline=False)
        else:
            embed.add_field(name=f"**__Permissions__**", value=", ".join(permission_list), inline=False)
        embed.add_field(name="**__Acknowledgements__**", value=ack)
        embed.set_thumbnail(url=member.avatar)
        try:
            user = await self.client.fetch_user(member.id)
            banner_url = user.banner.url
            embed.set_image(url=banner_url)
        except:
            pass
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
        await ctx.reply(embed=embed)


def get_super(x):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
    res = x.maketrans(''.join(normal), ''.join(super_s))
    return x.translate(res)


class ChannelSelectPrompt(View):
    """
    This class is a subclass of the `View` class that is intended to be used as a base class for creating a channel select prompt.

    Parameters:
        placeholder (str): The placeholder text that will be displayed in the channel select prompt.
        ephemeral (bool, optional): A boolean indicating whether the select prompt will be sent as an ephemeral message or not. Default is False.
        max_values (int, optional): The maximum number of options that can be selected by the user. Default is 1.
    """
    def __init__(
        self, placeholder: str, ephemeral: bool = False, max_values: int = 1
    ) -> None:
        super().__init__()
        self.values = None
        self.ephemeral = ephemeral
        self.children[0].placeholder, self.children[0].max_values = placeholder, max_values# type: ignore

    @select(cls=ChannelSelect, channel_types=[ChannelType.text, ChannelType.private_thread, ChannelType.public_thread, ChannelType.news])
    async def callback(self, interaction: Interaction, select: ChannelSelect):
        await interaction.response.defer(ephemeral=self.ephemeral)
        if self.ephemeral:
            await interaction.delete_original_response()
        else:
            with suppress(Exception):
                await interaction.message.delete()  # type: ignore
        self.values = [interaction.guild.get_channel(i.id) for i in select.values] # type: ignore
        self.stop()

class CreatorMethods:
    """
    This class contains all the methods for editing an embed. It is intended to be inherited by the main `EmbedCreator` class.

    Attributes:
        embed (discord.Embed): The embed object being edited.

    """

    def __init__(self, embed: Embed) -> None:
        self.embed = embed
        self.callbacks: Dict[str, Callable] = {
            "author": self.edit_author,
            "message": self.edit_message,
            "thumbnail": self.edit_thumbnail,
            "image": self.edit_image,
            "footer": self.edit_footer,
            "color": self.edit_colour,
            "addfield": self.add_field,
            "removefield": self.remove_field,
        }
class ModalInput(Modal):
    """
    This class is a subclass of the `Modal` class that is intended to be used as a base class for creating modals that require user input.

    Parameters:
        title (str): The title of the modal.
        timeout (float, optional): An optional argument that is passed to the parent Modal class. It is used to specify a timeout for the modal in seconds.
        custom_id (str, optional): An optional argument that is passed to the parent Modal class. It is used to specify a custom ID for the modal.
        ephemeral (bool, optional): A boolean indicating whether the modal will be sent as an ephemeral message or not.
    """
    def __init__(
        self,
        *,
        title: str,
        timeout: Optional[float] = None,
        custom_id: str = "modal_input",
        ephemeral: bool = False,
    ) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self.ephemeral = ephemeral

    async def on_submit(self, interaction: Interaction) -> None:
        with suppress(Exception):
            await interaction.response.defer(ephemeral=self.ephemeral)


class SelectPrompt(View):
    """
    This class is a subclass of the `View` class that is intended to be used as a base class for creating a select prompt.

    Parameters:
        placeholder (str): The placeholder text that will be displayed in the select prompt.
        options (List[SelectOption]): A list of `SelectOption` instances that will be displayed as options in the select prompt.
        max_values (int, optional): The maximum number of options that can be selected by the user. Default is 1.
        ephemeral (bool, optional): A boolean indicating whether the select prompt will be sent as an ephemeral message or not. Default is False.
    """
    def __init__(
        self, placeholder: str, options: List[SelectOption], max_values: int = 1, ephemeral: bool = False
    ) -> None:
        super().__init__()
        self.children[0].placeholder, self.children[0].max_values, self.children[0].options = placeholder, max_values, options  # type: ignore
        self.values = None
        self.ephemeral = ephemeral

    @select()
    async def select_callback(self, interaction: Interaction, select: Select):
        await interaction.response.defer(ephemeral=self.ephemeral)
        if self.ephemeral:
            await interaction.delete_original_response()
        else:
            with suppress(Exception):
                await interaction.message.delete()  # type: ignore
        self.values = select.values
        self.stop()

class CreatorMethods:
    """
    This class contains all the methods for editing an embed. It is intended to be inherited by the main `EmbedCreator` class.

    Attributes:
        embed (discord.Embed): The embed object being edited.

    """

    def __init__(self, embed: Embed) -> None:
        self.embed = embed
        self.callbacks: Dict[str, Callable] = {
            "author": self.edit_author,
            "message": self.edit_message,
            "thumbnail": self.edit_thumbnail,
            "image": self.edit_image,
            "footer": self.edit_footer,
            "color": self.edit_colour,
            "addfield": self.add_field,
            "removefield": self.remove_field,
        }

    async def edit_author(self, interaction: Interaction) -> None:
        """This method edits the embed's author"""
        if interaction.user != author:
            await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
            return await interaction.response.defer()
        modal = ModalInput(title="Edit Embed Author")
        modal.add_item(
            TextInput(
                label="Author Name",
                max_length=100,
                default=self.embed.author.name,
                placeholder="Author name to display in the embed",
                required=False,
            )
        )
        modal.add_item(
            TextInput(
                label="Author Icon Url",
                default=self.embed.author.icon_url,
                placeholder="Author icon to display in the embed",
                required=False,
            )
        )
        modal.add_item(
            TextInput(
                label="Author Url",
                default=self.embed.author.url,
                placeholder="URL to set as the embed's author link",
                required=False,
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        try:
            self.embed.set_author(
                name=str(modal.children[0]),
                icon_url=str(modal.children[1]),
                url=str(modal.children[2]),
            )
        except HTTPException:
            self.embed.set_author(
                name=str(modal.children[0])
            )

    async def edit_message(self, interaction: Interaction) -> None:
        """This method edits the embed's message (discord.Embed.title and discord.Embed.description)"""
        if interaction.user != author:
            await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
            return await interaction.response.defer()
        modal = ModalInput(title="Edit Embed Message")
        modal.add_item(
            TextInput(
                label="Embed Title",
                max_length=255,
                default=self.embed.title,
                placeholder="Title to display in the embed",
                required=False,
            )
        )
        modal.add_item(
            TextInput(
                label="Embed Description",
                default=self.embed.description,
                placeholder="Description to display in the embed",
                style=TextStyle.paragraph,
                required=False,
                max_length=2000,
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.embed.title, self.embed.description = str(modal.children[0]), str(
            modal.children[1]
        )

    async def edit_thumbnail(self, interaction: Interaction) -> None:
        """This method edits the embed's thumbnail"""
        if interaction.user != author:
            await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
            return await interaction.response.defer()
        modal = ModalInput(title="Edit Embed Thumbnail")
        modal.add_item(
            TextInput(
                label="Thumbnail Url",
                default=self.embed.thumbnail.url,
                placeholder="Thumbnail you want to display in the embed",
                required=False,
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.embed.set_thumbnail(url=str(modal.children[0]))

    async def edit_image(self, interaction: Interaction) -> None:
        """This method edits the embed's image"""
        if interaction.user != author:
            await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
            return await interaction.response.defer()
        modal = ModalInput(title="Edit Embed Thumbnail")
        modal.add_item(
            TextInput(
                label="Image Url",
                default=self.embed.image.url,
                placeholder="Image you want to display in the embed",
                required=False,
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.embed.set_image(url=str(modal.children[0]))

    async def edit_footer(self, interaction: Interaction) -> None:
        """This method edits the embed's footer (text, icon_url)"""
        if interaction.user != author:
            await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
            return await interaction.response.defer()
        modal = ModalInput(title="Edit Embed Footer")
        modal.add_item(
            TextInput(
                label="Footer Text",
                max_length=255,
                required=False,
                default=self.embed.footer.text,
                placeholder="Text you want to display on embed footer",
            )
        )
        modal.add_item(
            TextInput(
                label="Footer Icon",
                required=False,
                default=self.embed.footer.icon_url,
                placeholder="Icon you want to display on embed footer",
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.embed.set_footer(
            text=str(modal.children[0]), icon_url=str(modal.children[1])
        )

    async def edit_colour(self, interaction: Interaction) -> None:
        """This method is edits the embed's colour"""
        if interaction.user != author:
            await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
            return await interaction.response.defer()
        modal = ModalInput(title="Edit Embed Colour")
        modal.add_item(
            TextInput(
                label="Embed Colour",
                placeholder="The colour you want to display on embed (e.g: #303236)",
                max_length=20
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        try:
            colour = Colour.from_str(str(modal.children[0]))
        except:
            await interaction.followup.send(
                "Please provide a valid hex code.", ephemeral=True
            )
        else:
            self.embed.color = colour

    async def add_field(self, interaction: Interaction) -> None:
        if interaction.user != author:
            await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
            return await interaction.response.defer()
        if len(self.embed.fields) >= 25:
            return await interaction.response.send_message(
                "You can not add more than 25 fields.", ephemeral=True
            )
        modal = ModalInput(title="Add a new field")
        modal.add_item(
            TextInput(
                label="Field Name",
                placeholder="The name you want to display on the field",
                max_length=255,
            )
        )
        modal.add_item(
            TextInput(label="Field Value", max_length=2000, style=TextStyle.paragraph)
        )
        modal.add_item(
            TextInput(
                label="Field Inline (True/False)",
                default="True",
                max_length=5,
                placeholder="The inline for the field either True or False",
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        try:
            inline = False
            if str(modal.children[2]).lower() == "true":
                inline = True
            elif str(modal.children[2]).lower() == "false":
                inline = False
            else:
                raise Exception("Bad Bool Input.")
        except:
            await interaction.followup.send(
                "Please provide a valid input in `inline` either True Or False.",
                ephemeral=True,
            )
        else:
            self.embed.add_field(
                name=str(modal.children[0]), value=str(modal.children[1]), inline=inline
            )

    async def remove_field(self, interaction: Interaction) -> None:
        if interaction.user != author:
            await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
            return await interaction.response.defer()
        if not self.embed.fields:
            return await interaction.response.send_message("There is no fields to remove.", ephemeral=True)
        field_options = list()
        for index, field in enumerate(self.embed.fields):
            field_options.append(
                SelectOption(
                    label=str(field.name)[0:30],
                    value=str(index),
                    emoji="\U0001f5d1"
                )
            )
        select = SelectPrompt(
            placeholder="Select a field to remove...",
            options=field_options,
            max_values=len(field_options),
            ephemeral=True
        )
        await interaction.response.send_message(view=select, ephemeral=True)
        await select.wait()
        
        if vals := select.values:
            for value in vals:
                self.embed.remove_field(int(value))

class EmbedCreator(View):
    """
    This class is a subclass of `discord.ui.View`.
    It is intended to be used as a base class for creating a panel that allows users to create embeds in a specified Discord TextChannel.

    Parameters:
        bot (discord.Client or discord.ext.commands.Bot): An instance of the Discord bot that will be used to access client information such as avatar, name, and ID.
        embed (discord.Embed): An instance of the Discord Embed class that will be used as the main embed.
        timeout (float, optional): An optional argument that is passed to the parent View class. It is used to specify a timeout for the view in seconds.
    """

    def __init__(
        self,
        *,
        bot: Bot,
        embed: Optional[Embed] = None,
        timeout: Optional[float] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(timeout=timeout)
        if not embed:
            embed = self.get_default_embed
        self.bot, self.embed, self.timeout, self._creator_methods = (
            bot,
            embed,
            timeout,
            CreatorMethods(embed),
        )
        self.options_data = [
            {
                "label": kwargs.get("author_label", "Edit Author"),
                "description": kwargs.get(
                    "author_description", "Edits the embed author name, icon."
                ),
                "emoji": kwargs.get("author_emoji", "🔸"),
                "value": "author",
            },
            {
                "label": kwargs.get(
                    "message_label", "Edit Message (title, description)"
                ),
                "description": kwargs.get(
                    "message_description", "Edits the embed title, description."
                ),
                "emoji": kwargs.get("message_emoji", "🔸"),
                "value": "message",
            },
            {
                "label": kwargs.get("thumbnail_label", "Edit Thumbnail"),
                "description": kwargs.get(
                    "thumbnail_description", "Edits the embed thumbnail url."
                ),
                "emoji": kwargs.get("thumbnail_emoji", "🔸"),
                "value": "thumbnail",
            },
            {
                "label": kwargs.get("image_label", "Edit Image"),
                "description": kwargs.get(
                    "image_description", "Edits the embed image url."
                ),
                "emoji": kwargs.get("image_emoji", "🔸"),
                "value": "image",
            },
            {
                "label": kwargs.get("footer_label", "Edit Footer"),
                "description": kwargs.get(
                    "footer_description", "Edits the embed footer text, icon url."
                ),
                "emoji": kwargs.get("footer_emoji", "🔸"),
                "value": "footer",
            },
            {
                "label": kwargs.get("color_label", "Edit Color"),
                "description": kwargs.get(
                    "color_description", "Edits the embed colour."
                ),
                "emoji": kwargs.get("color_emoji", "🔸"),
                "value": "color",
            },
            {
                "label": kwargs.get("addfield_label", "Add Field"),
                "description": kwargs.get(
                    "addfield_description", "Adds a field to the embed."
                ),
                "emoji": kwargs.get("addfield_emoji", "🔸"),
                "value": "addfield",
            },
            {
                "label": kwargs.get("removefield_label", "Remove Field"),
                "description": kwargs.get(
                    "removefield_description", "Removes a field from the embed."
                ),
                "emoji": kwargs.get("removefield_emoji", "🔸"),
                "value": "removefield",
            },
        ]

        self.children[0].options = [SelectOption(  # type: ignore
            **option) for option in self.options_data
        ]
        self.children[1].label, self.children[1].emoji, self.children[1].style = kwargs.get(  # type: ignore
            "send_label", 'Send'), kwargs.get("send_emoji", None), kwargs.get("send_style", ButtonStyle.blurple)
        self.children[2].label, self.children[2].emoji, self.children[2].style = kwargs.get(  # type: ignore
            "cancel_label", 'Cancel'), kwargs.get("cancel_emoji", None), kwargs.get("cancel_style", ButtonStyle.red)  # type: ignore

    async def on_error(self, interaction: Interaction, error: Exception, item: Item[Any]) -> None:
        if isinstance(error, HTTPException) and error.code == 50035:
            # This will save you from the '50035' error, if any user try to remove all the attr of the embed then HTTP exception will raise with the error code `50035`
            self.embed.description = f"_ _"
            await self.update_embed(interaction)

    async def update_embed(self, interaction: Interaction):
        """This function will update the whole embed and edit the message and view."""
        return await interaction.message.edit(embed=self.embed, view=self)  # type: ignore

    @property
    def get_default_embed(self) -> Embed:
        """
        This class method `get_default_embed` returns a pre-configured `discord.Embed` object with
        title, description, color, author, thumbnail, image and footer set to specific values.
        It can be used as a default template for creating the embed builder.

        Returns:
            embed (discord.Embed)
        """
        embed = Embed(title=None,
                      description="Select Options from the Drop down menu!", colour=config['color'])
        return embed

    @select(placeholder="Edit a section")
    async def edit_select_callback(
        self, interaction: Interaction, select: Select
    ) -> None:
        """
        This method is a callback function for the `select` interaction.
        It is triggered when a user selects an option from the select menu. 
        The method uses the `callbacks` attribute of the `CreatorMethods` class to call the appropriate callback function based on the user's selection.

        Parameters:
            interaction (discord.Interaction): The interaction object representing the current interaction.
            select (discord.Select): The select object representing the select menu.

        """
        await self._creator_methods.callbacks[select.values[0]](interaction)
        await self.update_embed(interaction)

    @button()
    async def send_callback(self, interaction: Interaction, button: Button) -> None:
        """
        This method is a callback function for the `button` interaction. It is triggered when a user clicks on the "send" button. 
        The method creates a `ChannelSelectPrompt` object and sends it as an ephemeral message to the user. It then waits for the user to select a channel.
        If a channel is selected, the method sends the embed to the selected channel and deletes the original interaction message.

        Parameters:
            interaction (discord.Interaction): The interaction object representing the current interaction.
            button (discord.Button): The button object representing the "send" button.
        """
        if interaction.user != author:
            await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
            return await interaction.response.defer()
        prompt = ChannelSelectPrompt(
            "Select a channel to send this embed...", True, 1)
        await interaction.response.send_message(view=prompt, ephemeral=True)
        await prompt.wait()
        if prompt.values:
            if not isinstance(prompt.values[0], (StageChannel, ForumChannel, CategoryChannel)):
                await prompt.values[0].send(embed=self.embed)  # type: ignore
                await interaction.message.delete()  # type: ignore

    @button()
    async def cancel_callback(self, interaction: Interaction, button: Button) -> None:
        """
        This method is a callback function for the `button` interaction. It is triggered when a user clicks on the "cancel" button. 
        The method deletes the original interaction message and stops the current interaction.

        Parameters:
            interaction (Interaction): The interaction object representing the current interaction.
            button (Button): The button object representing the "cancel" button.
        """
        if interaction.user != author:
            await interaction.response.send_message(f"{emotes['failed']} | You Cannot Interact With This Button!", ephemeral=True)
            return await interaction.response.defer()
        await interaction.message.delete()  # type: ignore
        self.stop()

async def setup(client):
    await client.add_cog(utilcmd(client)) 