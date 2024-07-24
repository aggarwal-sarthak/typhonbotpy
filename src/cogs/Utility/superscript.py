import os
from discord.ext import commands
from src.core.check import command_enabled


class Superscript(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(
        usage=f"{os.path.basename(__file__)[:-3]} <Text>",
        description="Returns Superscript Of A Given Text",
        aliases=["sup"],
    )
    @commands.cooldown(1, 10, commands.BucketType.member)
    @command_enabled()
    async def superscript(self, ctx: commands.Context, *, text: str):
        normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
        super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
        res = text.maketrans("".join(normal), "".join(super_s))
        await ctx.reply(text.translate(res))


async def setup(client: commands.Bot):
    await client.add_cog(Superscript(client))
