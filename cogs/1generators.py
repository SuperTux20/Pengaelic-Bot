import discord
from discord.ext import commands
from random import choice, randint

class Generators(commands.Cog):
    def __init__(self, client):
        self.client = client
    name = "generators"
    name_typable = name
    description = "Ya like randomization?"
    description_long = description + " So do I!"

    @commands.command(name = "name", help = "Generate a random name! They tend to be mystic-sounding :eyes:", aliases = ["generatename", "namegen"], usage = "[number of names to generate (1)] [limit to how many syllables can be used (3)]")
    async def name_generator(self, ctx, amount: int = 1, syllable_limit: int = 3):
        await ctx.send(
            str(
                [
                    "".join(
                        [
                            choice(
                                [
                                    "a",
                                    "ae",
                                    "ag",
                                    "ah",
                                    "al",
                                    "am",
                                    "an",
                                    "art",
                                    "as",
                                    "au",
                                    "av",
                                    "ayn",
                                    "az",
                                    "be",
                                    "bi",
                                    "bo",
                                    "bor",
                                    "burn",
                                    "by",
                                    "ca",
                                    "cai",
                                    "car",
                                    "cat",
                                    "ce",
                                    "cei",
                                    "cer",
                                    "cha",
                                    "ci",
                                    "co",
                                    "cu",
                                    "da",
                                    "dam",
                                    "dan",
                                    "del",
                                    "der",
                                    "des",
                                    "di",
                                    "dil",
                                    "do",
                                    "don",
                                    "dy",
                                    "dyl",
                                    "e",
                                    "el",
                                    "em",
                                    "en",
                                    "ev",
                                    "ex",
                                    "fi",
                                    "fin",
                                    "finn",
                                    "fly",
                                    "fu",
                                    "ga",
                                    "go",
                                    "gor",
                                    "gy",
                                    "he",
                                    "hy",
                                    "i",
                                    "ig",
                                    "il",
                                    "in",
                                    "is",
                                    "iss",
                                    "ja",
                                    "ji",
                                    "jo",
                                    "jor",
                                    "ka",
                                    "kes",
                                    "kev",
                                    "kla",
                                    "ko",
                                    "lan",
                                    "lar",
                                    "ler",
                                    "li",
                                    "lo",
                                    "lu",
                                    "ly",
                                    "ma",
                                    "mar",
                                    "me",
                                    "mel",
                                    "mi",
                                    "mo",
                                    "mol",
                                    "mu",
                                    "mus",
                                    "na",
                                    "nar",
                                    "ne",
                                    "nei",
                                    "no",
                                    "nor",
                                    "nos",
                                    "o",
                                    "ob",
                                    "ok",
                                    "ol",
                                    "om",
                                    "on",
                                    "or",
                                    "os",
                                    "pe",
                                    "pen",
                                    "per",
                                    "pu",
                                    "ra",
                                    "ral",
                                    "ran",
                                    "ras",
                                    "re",
                                    "res",
                                    "rez",
                                    "ri",
                                    "rin",
                                    "rob",
                                    "ry",
                                    "sa",
                                    "sac",
                                    "sam",
                                    "san",
                                    "sans",
                                    "ser",
                                    "sey",
                                    "sha",
                                    "sky",
                                    "son",
                                    "st",
                                    "str",
                                    "ta",
                                    "tam",
                                    "tay",
                                    "ter",
                                    "tha",
                                    "than",
                                    "tif",
                                    "ti",
                                    "tin",
                                    "to",
                                    "tor",
                                    "tur",
                                    "u",
                                    "um",
                                    "un",
                                    "ur",
                                    "va",
                                    "vac",
                                    "van",
                                    "ve",
                                    "vi",
                                    "wa",
                                    "wyn",
                                    "yu",
                                    "za",
                                    "zal",
                                    "ze",
                                    "zi",
                                    "zil",
                                    "zo",
                                    "zu"
                                ]
                            )
                            for _ in range(randint(2, syllable_limit))
                        ]
                    ).capitalize()
                    for _ in range(amount)
                ]
            )[1:-1].replace(
                "'",
                ""
            )
        )

    @commands.command(name = "floridaman", help = "Generate random Florida Man headlines!", aliases = ["florida"], usage = "[other state]")
    async def florida_man(self, ctx, *, state = "florida"):
        headline = [" ".join([name.capitalize() for name in state.split()])]
        objects = ["van", "dog", "cat", "car", "alligator", "chicken nugget", "penguin", "burger", "car salesman"]
        selected_object = choice(objects)
        people = ["man", "woman"]
        events = ["pushed", "thrown", "dropped", "burned", "stabbed", "run over", "slapped"]
        poss2 = ["", "by"]
        timing = ["after", "when"]
        actions = ["pushes", "throws", "drops", "burns", "stabs", "runs over", "slaps"]
        part2 = choice(poss2)
        headline.append(choice(people))
        headline.append(choice(events))
        if part2 != "":
            headline.append(part2)
            headline.append(selected_object)
            objects.remove(selected_object)
            selected_object = choice(objects)
        headline.append(choice(timing))
        headline.append(selected_object)
        objects.remove(selected_object)
        selected_object = choice(objects)
        headline.append(choice(actions))
        headline.append(selected_object)
        await ctx.send(" ".join(headline))

    @name_generator.error
    @florida_man.error
    async def error(self, ctx, error):
        if str(error) == """Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body
In content: Must be 2000 or fewer in length.""":
            await ctx.send(
                "Sorry, you specified numbers that were too large. Sending all that would put me over the 2000-character limit!"
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
    client.add_cog(
        Generators(
            client
        )
    )