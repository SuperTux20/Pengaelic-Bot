import discord
from discord.ext import commands
from random import choice, shuffle

class converters(commands.Cog):
    def __init__(self, client):
        self.client = client
    name = "converters"
    name_typable = name
    description = "Run some text through a converter to make it look funny!"
    description_long = description

    async def testIfNoContent(self, ctx, arg):
        if not arg:
            return list(
                await ctx.channel.history(
                    limit = 2
                ).flatten()
            )[1].content
        else:
            return arg

    @commands.command(name = "owo", help = "Convert whatever text into owo-speak... oh god why did i make this", aliases = ["uwu", "furry"])
    async def owoConverter(self, ctx, *, arg = None):
        arg = await self.testIfNoContent(
            ctx,
            arg
        )
        await ctx.send(
            arg.replace(
                "l",
                "w"
            ).replace(
                "r",
                "w"
            ).replace(
                "t",
                "tw"
            ).replace(
                "twh",
                "thw"
            ) + " " + choice(
                [
                    "OwO",
                    "UwU",
                    "owo",
                    "uwu",
                    "O3O",
                    "U3U",
                    "o3o",
                    "u3u",
                    "^w^",
                    "nya~",
                    "rawr"
                ]
            )
        )

    @commands.command(name = "blockify", help = "Convert text into\n:regional_indicator_b: :regional_indicator_i: :regional_indicator_g: letters.", aliases = ["bigtext", "big"])
    async def bigText(self, ctx, *, arg = None):
        arg = await self.testIfNoContent(
            ctx,
            arg
        )
        alphabet = "qwertyuiopasdfghjklzxcvbnm ?!1234567890"
        textlist = []
        finaltext = ""
        for char in arg:
            for letter in alphabet:
                if letter == char or letter.upper() == char:
                    if char == " ":
                        textlist.append("\n"
                        )
                    elif char == "?":
                        textlist.append(
                            ":question: "
                        )
                    elif char == "!":
                        textlist.append(
                            ":exclamation: "
                        )
                    elif char == "1":
                        textlist.append(
                            ":one: "
                        )
                    elif char == "2":
                        textlist.append(
                            ":two: "
                        )
                    elif char == "3":
                        textlist.append(
                            ":three: "
                        )
                    elif char == "4":
                        textlist.append(
                            ":four: "
                        )
                    elif char == "5":
                        textlist.append(
                            ":five: "
                        )
                    elif char == "6":
                        textlist.append(
                            ":six: "
                        )
                    elif char == "7":
                        textlist.append(
                            ":seven: "
                        )
                    elif char == "8":
                        textlist.append(
                            ":eight: "
                        )
                    elif char == "9":
                        textlist.append(
                            ":nine: "
                        )
                    elif char == "0":
                        textlist.append(
                            ":zero: "
                        )
                    else:
                        textlist.append(
                            f""":regional_indicator_{
                                char.lower()
                            }: """
                        )
        for big in textlist:
            finaltext = finaltext + big
        await ctx.send(
            finaltext
        )

    @commands.command(name = "greekify", help = "Make words *look* Greek, but the pronunciation is still almost the same as in English.")
    async def greekify(self, ctx, *, arg = None):
        arg = await self.testIfNoContent(
            ctx,
            arg
        )
        alphabet = [
            "CH",
            "PS",
            "AV",
            "AF",
            "EV",
            "EF",
            "OO",
            "EH",
            "TH",
            "YE",
            "YI",
            "YU",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z"
        ]
        greekAlphabet = [
            "Χ",
            "Ψ",
            "ΑΥ",
            "ΑΥ",
            "ΕΥ",
            "ΕΥ",
            "ΟΥ",
            "ΑΙ",
            "Θ",
            "Γ",
            "Γ",
            "Γ",
            "Α",
            "Β",
            "K",
            "Δ",
            "Ε",
            "Φ",
            "Γ",
            "",
            "Ι",
            "Γ",
            "Κ",
            "Λ",
            "Μ",
            "Ν",
            "Ο",
            "Π",
            "Κ",
            "Ρ",
            "Σ",
            "Τ",
            "Ω",
            "Φ",
            "ΟΥ",
            "Ξ",
            "Υ",
            "Ζ"
        ]
        alphabet = alphabet + [
            letter.lower()
            for letter in alphabet
        ]
        greekAlphabet = greekAlphabet + [
            letter.lower()
            for letter in greekAlphabet
        ]
        toConvert = arg
        for letter in range(len(alphabet)):
            toConvert = toConvert.replace(
                alphabet[letter],
                greekAlphabet[letter]
            )
        await ctx.send(
            toConvert
        )

    @commands.command(name = "stroke", help = "Shuffle a message", aliases = ["shuffle", "mixup"])
    async def shuffle(self, ctx, *, arg = None):
        arg = await self.testIfNoContent(
            ctx,
            arg
        )
        if arg == "Pengaelic Bot":
            await ctx.send(
                "OwO you pet me??? *purrs softly*"
            )
        else:
            toShuffle = list(
                arg
            )
            shuffle(
                toShuffle
            )
            await ctx.send(
                "".join(
                    toShuffle
                )
            )

    @commands.command(name = "strokebyword", help = "Shuffle the individual words instead of the entire message.")
    async def shufflebyword(self, ctx, *, arg = None):
        arg = await self.testIfNoContent(
            ctx,
            arg
        )
        wordsToShuffle = arg.split()
        for toShuffle in range(len(wordsToShuffle)):
            wordsToShuffle[toShuffle] = list(
                wordsToShuffle[toShuffle]
            )
            shuffle(
                wordsToShuffle[toShuffle]
            )
            wordsToShuffle[toShuffle] = "".join(
                wordsToShuffle[toShuffle]
            )
        await ctx.send(
            " ".join(
                wordsToShuffle
            )
        )

    @commands.command(name = "spacer", help = "Insert spaces between every character", aliases = ["space", "gaps"])
    async def spacer(self, ctx, *, arg = None):
        arg = await self.testIfNoContent(
            ctx,
            arg
        )
        await ctx.send(
            " ".join(
                arg[i:i + 1]
                for i in range(0, len(arg), 1)
            )
        )

    @commands.command(name = "wingdings", help = "You heard what the River Person said.", aliases = ["dings", "gaster", "wd"])
    async def dings(self, ctx, *, arg = None):
        arg = await self.testIfNoContent(
            ctx,
            arg
        )
        alphabet = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
            " "
        ]
        dingAlphabet = [
            ":v:",
            ":ok_hand:",
            ":thumbsup:",
            ":thumbsdown:",
            ":point_left:",
            ":point_right:", ":point_up_2:",
            ":point_down:",
            ":raised_hand:",
            ":slight_smile:",
            ":neutral_face:", ":frowning:", ":bomb:", ":skull_crossbones:", ":flag_white:",
            ":triangular_flag_on_post:",
            ":airplane:",
            ":sunny:",
            ":droplet:",
            ":snowflake:",
            ":cross:", ":orthodox_cross:",
            ":atom:",
            ":diamond_shape_with_a_dot_inside:",
            ":star_of_david:",
            ":star_and_crescent:",
            " < :empty:725132670056661023 > "
        ]
        toConvert = arg.upper()
        for letter in range(len(alphabet)):
            toConvert = toConvert.replace(
                alphabet[letter],
                dingAlphabet[letter]
            )
        await ctx.send(
            toConvert
        )

    @owoConverter.error
    @bigText.error
    @greekify.error
    @shuffle.error
    @shufflebyword.error
    @spacer.error
    @dings.error
    async def overcharlimit(self, ctx, error):
        if str(error) == """Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body
In content: Must be 2000 or fewer in length.""":
            await ctx.send("Sending all that would put me over the 2000-character limit!")
        elif str(error) == "arg is a required argument that is missing.":
            await ctx.send(
                "You didn't specify any text to convert!"
            )
        else:
            await ctx.send(
                f"""Unhandled error occurred:
        {
            error
        }
If my developer (<@!686984544930365440>) is not here, please tell him what the error is so that he can add handling or fix the issue!"""
                )

def setup(client):
    client.add_cog(converters(client))