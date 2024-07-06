from discord.ext import commands
import os 
from src.core.validation import is_command_enabled

class superscript(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(usage=f"{os.path.basename(__file__)[:-3]} <Text>", description = "Returns Superscript Of A Given Text", aliases = ['sup'])
    @commands.check(is_command_enabled)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def superscript(self, ctx:commands.Context, *, text:str):
        await ctx.reply(get_super(text))

def get_super(x):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
    res = x.maketrans(''.join(normal), ''.join(super_s))
    return x.translate(res)

async def setup(client):
    await client.add_cog(superscript(client))