import discord
from discord.ext import commands


class superscript(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(name = "superscript",
                    usage=";superscript <Text>",
                    description = "Returns Superscript Of A Given Text",
                    aliases = ['sup'])
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