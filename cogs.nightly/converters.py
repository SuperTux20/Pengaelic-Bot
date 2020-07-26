import discord
from discord.ext import commands
from random import choice, shuffle

class Converters(commands.Cog):
    name = "converters"
    description = "Run some text through a converter to make it look funny!"
    def __init__(self, client):
        self.client = client

    async def ifnocontent(self, ctx, arg):
        if not arg:
            return list(await ctx.channel.history(limit=2).flatten())[1].content
        else:
            return arg

    @commands.command(name="owo", help="Convert whatever text into owo-speak... oh god why did i make this", aliases=["uwu", "furry"])
    async def owoConverter(self, ctx, *, arg=None):
        arg = await self.ifnocontent(ctx, arg)
        await ctx.send(arg.replace("l","w").replace("r","w").replace("t","tw").replace("twh","thw") + " " + choice(["OwO","UwU","owo","uwu","ewe","O3O","U3U","o3o","u3u","^w^","nya~","rawr"]))
        await ctx.message.delete()

    @commands.command(name="beegtext", help="Convert text into regional indicator letters, the big blue ones.", aliases=["bigtext", "big", "beeg", "blockify"])
    async def embiggener(self, ctx, *, arg=None):
        arg = await self.ifnocontent(ctx, arg)
        alphabet = "qwertyuiopasdfghjklzxcvbnm ?!1234567890"
        textlist = []
        finaltext = ""
        for char in range(len(arg)):
            for letter in range(len(alphabet)):
                if alphabet[letter] == arg[char] or alphabet[letter].upper() == arg[char]:
                    if arg[char] == " ":
                        textlist.append("\n")
                    elif arg[char] == "!":
                        textlist.append(":exclamation: ")
                    elif arg[char] == "?":
                        textlist.append(":question: ")
                    elif arg[char] == "1":
                        textlist.append(":one: ")
                    elif arg[char] == "2":
                        textlist.append(":two: ")
                    elif arg[char] == "3":
                        textlist.append(":three: ")
                    elif arg[char] == "4":
                        textlist.append(":four: ")
                    elif arg[char] == "5":
                        textlist.append(":five: ")
                    elif arg[char] == "6":
                        textlist.append(":six: ")
                    elif arg[char] == "7":
                        textlist.append(":seven: ")
                    elif arg[char] == "8":
                        textlist.append(":eight: ")
                    elif arg[char] == "9":
                        textlist.append(":nine: ")
                    elif arg[char] == "0":
                        textlist.append(":zero: ")
                    else:
                        textlist.append(f":regional_indicator_{arg[char].lower()}: ")
        for beeg in range(len(textlist)):
            finaltext = finaltext + textlist[beeg]
        await ctx.send(finaltext)

    @commands.command(name="greekify", help="Make words *look* Greek, but the pronunciation is still almost the same as in English.")
    async def greekify(self, ctx, *, arg=None):
        arg = await self.ifnocontent(ctx, arg)
        alphabet = ["CH","PS","AV","AF","EV","EF","OO","EH","TH","YE","YI","YU","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W", "X","Y","Z"]
        greekphabet = ["Χ","Ψ","ΑΥ","ΑΥ","ΕΥ","ΕΥ","ΟΥ","ΑΙ","Θ","Γ", "Γ", "Γ", "Α","Β","K","Δ","Ε","Φ","Γ","", "Ι","Γ","Κ","Λ","Μ","Ν","Ο","Π","Κ","Ρ","Σ","Τ","Ω","Φ","ΟΥ","Ξ","Υ","Ζ"]
        alphabet = alphabet + [letter.lower() for letter in alphabet]
        greekphabet = greekphabet + [letter.lower() for letter in greekphabet]
        toconvert = arg
        for letter in range(len(alphabet)):
            toconvert = toconvert.replace(alphabet[letter], greekphabet[letter])
        await ctx.send(toconvert)
    
    @commands.command(name="stroke", help="Just freakin' shuffle it dude", aliases=["shuffle", "mixup"])
    async def shuffle(self, ctx, *, arg=None):
        arg = await self.ifnocontent(ctx, arg)
        if arg == "Pengaelic Bot":
            await ctx.send("OwO you pet me??? *purrs softly*")
        else:
            toshuf = list(arg)
            shuffle(toshuf)
            await ctx.send("".join(toshuf))

    @commands.command(name="strokebyword", help="Shuffle the individual words instead of the entire message.")
    async def shufflebyword(self, ctx, *, arg=None):
        arg = await self.ifnocontent(ctx, arg)
        wordstoshuf = arg.split()
        for toshuf in range(len(wordstoshuf)):
            wordstoshuf[toshuf] = list(wordstoshuf[toshuf])
            shuffle(wordstoshuf[toshuf])
            wordstoshuf[toshuf] = "".join(wordstoshuf[toshuf])
        await ctx.send(" ".join(wordstoshuf))

    @commands.command(name="spacer", help="Insert spaces between every character", aliases=["space", "gaps"])
    async def spacer(self, ctx, *, arg=None):
        arg = await self.ifnocontent(ctx, arg)
        await ctx.send(" ".join(arg[i:i + 1] for i in range(0, len(arg), 1)))

    @commands.command(name="wingdings", help="You heard what the River Person said.", aliases=["dings", "gaster", "wd"])
    async def dings(self, ctx, *, arg=None):
        arg = await self.ifnocontent(ctx, arg)
        arg = arg.upper()
        alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"," "]
        dingphabet = [":v:",":ok_hand:",":thumbsup:",":thumbsdown:",":point_left:",":point_right:",":point_up_2:",":point_down:",":raised_hand:",":slight_smile:",":neutral_face:",":frowning:",":bomb:",":skull_crossbones:",":flag_white:",":triangular_flag_on_post:",":airplane:",":sunny:",":droplet:",":snowflake:",":cross:",":orthodox_cross:",":atom:",":diamond_shape_with_a_dot_inside:",":star_of_david:",":star_and_crescent:","<:empty:725132670056661023>"]
        toconvert = arg
        for letter in range(len(alphabet)):
            toconvert = toconvert.replace(alphabet[letter], dingphabet[letter])
        await ctx.send(toconvert)

    @owoConverter.error
    @embiggener.error
    @greekify.error
    @shuffle.error
    @shufflebyword.error
    @spacer.error
    @dings.error
    async def overcharlimit(self, ctx, error):
        if str(error)== """Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body
In content: Must be 2000 or fewer in length.""":
            await ctx.send("Sending all that would put me over the 2000-character limit!")
        elif str(error)== "arg is a required argument that is missing.":
            await ctx.send("You didn't specify any text to convert!")
        else:
            await ctx.send(f"Unhandled error occurred:\n{error}\nIf my developer (chickenmeister#7140) is not here, please tell him what the error is so that he can add handling or fix the issue!")

def setup(client):
    client.add_cog(Converters(client))