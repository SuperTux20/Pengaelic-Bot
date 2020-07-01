import discord
from discord.ext import commands
from random import choice

class Converters(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="novowels", help="Remove all vowels from whatever text you put in.", aliases=["vowelremover", "removevowels"])
    async def vowelRemover(self, ctx, *, arg):
        vowels = "aeiouAEIOU"
        outputString = arg
        for vowel in range(len(vowels)):
                outputString = outputString.replace(vowels[vowel],"")
        await ctx.send(outputString.replace("  ", " ")) # fix doubled spaces

    @commands.command(name="owo", help="Convert whatever text into owo-speak... oh god why did i make this", aliases=["furry"])
    async def owoConverter(self, ctx, *, arg):
        await ctx.send(arg.replace("l","w").replace("r","w") + " " + choice(["OwO","UwU","owo","uwu","ewe","O3O","U3U","o3o","u3u","^w^","nya~","rawr"]))
        await ctx.message.delete()

    @commands.command(name="beegtext", help="Convert text into regional indicator letters, the big blue ones.", aliases=["bigtext", "big", "beeg"])
    async def embiggener(self, ctx, *, arg):
        alphabet = "QWERTYUIOPASDFGHJKLZXCVBNM ?!"
        textlist = []
        finaltext = ""
        for char in range(len(arg)):
            for letter in range(len(alphabet)):
                if alphabet[letter] == arg[char] or alphabet[letter].lower() == arg[char]:
                    if arg[char] == " ":
                        textlist.append("\n")
                    elif arg[char] == "!":
                        textlist.append(":exclamation: ")
                    elif arg[char] == "?":
                        textlist.append(":question: ")
                    else:
                        textlist.append(":regional_indicator_" + arg[char].lower() + ": ")
        for beeg in range(len(textlist)):
            finaltext = finaltext + textlist[beeg]
        await ctx.send(finaltext)

def setup(client):
    client.add_cog(Converters(client))