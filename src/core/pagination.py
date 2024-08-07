from __future__ import annotations
import discord
from discord.ext import commands
from src.core.bot import tether


class Simple(discord.ui.View):
    def __init__(
        self,
        *,
        timeout: int = 60,
        PreviousButton: discord.ui.Button = discord.ui.Button(
            emoji=discord.PartialEmoji(name="\U000025c0")
        ),
        NextButton: discord.ui.Button = discord.ui.Button(
            emoji=discord.PartialEmoji(name="\U000025b6")
        ),
        PageCounterStyle: discord.ButtonStyle = discord.ButtonStyle.grey,
        InitialPage: int = 0,
        ephemeral: bool = False,
    ) -> None:
        super().__init__(timeout=timeout)
        self.PreviousButton = PreviousButton
        self.NextButton = NextButton
        self.PageCounterStyle = PageCounterStyle
        self.InitialPage = InitialPage
        self.ephemeral = ephemeral

        self.pages = []
        self.ctx = None
        self.message = None
        self.current_page = InitialPage

        self.PreviousButton.callback = self.previous_button_callback
        self.NextButton.callback = self.next_button_callback

    async def start(
        self, ctx: discord.Interaction | commands.Context, pages: list[discord.Embed]
    ):
        if isinstance(ctx, discord.Interaction):
            ctx = await commands.Context.from_interaction(ctx)
        self.pages = pages
        self.ctx = ctx

        page_counter = SimplePaginatorPageCounter(
            style=self.PageCounterStyle,
            TotalPages=len(pages),
            InitialPage=self.InitialPage,
        )
        self.add_item(self.PreviousButton)
        self.add_item(page_counter)
        self.add_item(self.NextButton)

        self.message = await ctx.reply(
            embed=pages[self.InitialPage], view=self, ephemeral=self.ephemeral
        )

    async def previous(self):
        if self.current_page == 0:
            self.current_page = len(self.pages) - 1
        else:
            self.current_page -= 1
        await self.update_message()

    async def next(self):
        if self.current_page == len(self.pages) - 1:
            self.current_page = 0
        else:
            self.current_page += 1
        await self.update_message()

    async def update_message(self):
        self.children[1].label = f"{self.current_page + 1}/{len(self.pages)}"
        await self.message.edit(embed=self.pages[self.current_page], view=self)

    async def previous_button_callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(
                f"{tether.constants.failed} | You Cannot Interact With This Button!",
                ephemeral=True,
            )
        else:
            await self.previous()
            await interaction.response.defer()

    async def next_button_callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(
                f"{tether.constants.failed} | You Cannot Interact With This Button!",
                ephemeral=True,
            )
        else:
            await self.next()
            await interaction.response.defer()


class SimplePaginatorPageCounter(discord.ui.Button):
    def __init__(self, style: discord.ButtonStyle, TotalPages: int, InitialPage: int):
        super().__init__(
            label=f"{InitialPage + 1}/{TotalPages}", style=style, disabled=True
        )
