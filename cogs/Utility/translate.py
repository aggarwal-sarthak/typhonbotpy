import discord
from discord.ext import commands
import os
from googletrans import Translator
translator = Translator()



class translate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")
        
    @commands.command(description="Translates A Messages In Given Language",usage=f"{os.path.basename(__file__)[:-3]} <Language> <Text>")
    async def translate(self, ctx, lang:str, *text:str):
        text = " ".join([x for x in text])
        res = translator.translate(text=text,dest=lang)
        embed = discord.Embed(title="Translator", description=f"**Result**: \n{res.text}\n\n**Pronunciation**: \n{res.pronunciation}",color=0xfb7c04)
        embed.set_footer(text=f"Translation from {res.src.upper()} to {lang.upper()}")
        await ctx.reply(embed=embed)

async def setup(client):
    await client.add_cog(translate(client))   
