from __future__ import annotations
import discord
from discord.ext import commands
import os
import pagination
from contextlib import suppress
import json
from discord.ui import Item, Select, select, Button, button, View, ChannelSelect, Modal, TextInput
from typing import Optional,Callable, Dict, List, Any
from discord import ButtonStyle,ChannelType, CategoryChannel, Embed, ForumChannel, HTTPException, Interaction, StageChannel, Colour, SelectOption, TextStyle
from discord.ext.commands import Bot
from validation import db_client

with open('emoji.json', 'r') as f:
    emotes = json.load(f)


class devcmd(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command(description='Evaluates given code',aliases=['eval', 'e'], usage=f"{os.path.basename(__file__)[:-3]} <code>")
    async def evaluate(self, ctx, *,code: str):
        if ctx.author.id not in self.client.config["owner"]: return
        try:
            result = eval(code)
            await ctx.send(f"{self.client.emotes['success']} | **Result:** {result}")

        except Exception as e:
            await ctx.send(f"{self.client.emotes['failed']} | Error: {e}")

    @commands.command(description='Generates Invite Link of a Guild',aliases=['invites'], usage=f"{os.path.basename(__file__)[:-3]} <guild_id>")    
    async def invite(self,ctx,guild: discord.Guild):
        if ctx.author.id not in self.client.config["owner"]: return
        try:
            invite = await guild.invites()
        except discord.Forbidden:
            await ctx.reply(f"{self.client.emotes['failed']} | Missing Permission to generate Invite!")
            return
        except discord.HTTPException:
            await ctx.reply(f"{self.client.emotes['failed']} | An error occurred while fetching the information!")
            return
        await ctx.send(f"{invite[0]}")

    @commands.command(description='Leaves The Server With Given ID', usage=f"{os.path.basename(__file__)[:-3]} <serverid>")
    async def leave(self, ctx):
        if ctx.author.id not in self.client.config["owner"]: return
        guild = discord.utils.get(self.client.guilds, id=int(ctx))

        if guild:
            await guild.leave()
            await ctx.reply(f"{self.client.emotes['success']} | Left The server: `{guild.name}`!")
        else:
            await ctx.reply(f"{self.client.emotes['faield']} | No Server Found With Given ID!")
       
    @commands.command(description='Loads A Given Command', usage=f"{os.path.basename(__file__)[:-3]} <cmd>")
    async def load(self, ctx, cog: str):
        if ctx.author.id not in self.client.config["owner"]: return
        await self.client.load_extension(f'cogs.{cog}')
        await ctx.reply(f"{self.client.emotes['success']} | Command {cog} Loaded Successfully!")

    @commands.command(description='Reloads A Given Command', usage=f"{os.path.basename(__file__)[:-3]} <cmd>")
    async def reload(self, ctx, cog: str):
        if ctx.author.id not in self.client.config["owner"]: return
        await self.client.reload_extension(f'cogs.{cog}')
        await ctx.reply(f"{self.client.emotes['success']} | Command {cog} Reloaded Successfully!")

    @commands.command(description='Returns Bot Servers', usage=f"{os.path.basename(__file__)[:-3]}", aliases=['s'])
    async def servers(self, ctx):
        if ctx.author.id not in self.client.config["owner"]: return
        data = sorted(self.client.guilds, key=lambda x: x.member_count, reverse=True)

        embeds = []
        for i in range(0,len(data), 20):
            description = ""
            for j in range(i, min(i+20, len(data))):
                description += f'**{str(j+1)}.** {str(data[j].name)} **|** {str(data[j].id)} **|** {str(data[j].member_count)}\n'
            pagination_embed = discord.Embed(title=f'Bot Servers [{len(self.client.guilds)}]', description=description,color=self.client.config['color'])
            pagination_embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar)
            embeds.append(pagination_embed)
        await pagination_check(self, ctx, data, embeds)
    @commands.command(description='Unloads A Given Command', usage=f"{os.path.basename(__file__)[:-3]} <cmd>")
    async def unload(self, ctx, cog: str):
        if ctx.author.id not in self.client.config["owner"]: return
        await self.client.unload_extension(f'cogs.{cog}')
        await ctx.reply(f"{self.client.emotes['success']} | Command {cog} Unloaded Successfully!")    

    @commands.command(description="Sends the UpdateLog!",aliases=['update'],usage=f"{os.path.basename(__file__)[:-3]}")
    async def updatelog(self,ctx):
        global author
        author = ctx.author
        if ctx.author.id not in self.client.config["owner"]: return
        view = EmbedCreator(bot=self.client)
        await ctx.send(embed=view.get_default_embed, view=view)


async def pagination_check(self, ctx, data, embeds):
    if len(data)>20:
        await pagination.Simple(timeout=60).start(ctx, pages=embeds)
    elif (len(data)<20 and len(data)>0):
        await ctx.reply(embed=embeds[0])


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
                      description="Select Options from the Drop down menu!", colour=0xfb7c04)
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
        dict = self.embed.to_dict()
        updateLog = db_client.typhonbot.updatelog
        if(updateLog is not None):
            updateLog.delete_many({})
        updateLog.insert_one(dict)
        await interaction.message.delete()
        await interaction.message.channel.send(f"{emotes['success']} | Update Log letter Sent!")
        db_client.typhonbot.guilds.update_many({},{"$set":{"updated":False}})
        
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
    await client.add_cog(devcmd(client))