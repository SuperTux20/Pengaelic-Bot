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

    @commands.command(name="owo", help="Convert whatever text into owo-speak... oh god why did i make this", aliases=["uwu", "furry"])
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

    @commands.command(name="greekify", help="Make words *look* Greek, but the pronunciation is still almost the same as in English.")
    async def greekify(self, ctx, *, arg):
        alphabet = ["CH","PS","AV","AF","EV","EF","OO","EH","TH","YE","YI","YU","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W", "X","Y","Z"]
        greekphabet = ["Χ","Ψ","ΑΥ","ΑΥ","ΕΥ","ΕΥ","ΟΥ","ΑΙ","Θ","Γ", "Γ", "Γ", "Α","Β","K","Δ","Ε","Φ","Γ","", "Ι","Γ","Κ","Λ","Μ","Ν","Ο","Π","Κ","Ρ","Σ","Τ","Ω","Φ","ΟΥ","Ξ","Υ","Ζ"]
        alphabet = alphabet + [letter.lower() for letter in alphabet]
        greekphabet = greekphabet + [letter.lower() for letter in greekphabet]
        toconvert = arg
        for letter in range(len(alphabet)):
            toconvert = toconvert.replace(alphabet[letter], greekphabet[letter])
        await ctx.send(toconvert)

def setup(client):
    client.add_cog(Converters(client))