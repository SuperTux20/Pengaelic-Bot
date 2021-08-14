#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from discord.ext import commands
from pengaelicutils import list2str, Stopwatch, syllables
from random import choice, randint
from subprocess import check_output as bash
from time import time


class Generators(commands.Cog):
    def __init__(self, client):
        self.client = client

    name = "generators"
    name_typable = name
    description = "Do ya like randomization?"
    description_long = description + " So do I!"

    @commands.command(
        name="name",
        help="Generate a random name! They tend to be mystic-sounding :eyes:",
        aliases=["namegen"],
        usage="[names to generate (1)]\n[max syllables (3)]\n[min syllables (2)]",
    )
    async def name_generator(
        self, ctx, amount: int = 1, upper_limit: int = 3, lower_limit: int = 2
    ):
        if amount > 0 and upper_limit > 0 and lower_limit > 0:
            if not lower_limit > upper_limit:
                await ctx.send(
                    list2str(
                        [
                            "".join(
                                [
                                    choice(syllables)
                                    for _ in range(randint(lower_limit, upper_limit))
                                ]
                            ).capitalize()
                            for _ in range(amount)
                        ],
                        3,
                    )
                )
            else:
                await ctx.send("The lower limit cannot be higher than the upper limit.")
        else:
            await ctx.send("Values can't be zero.")

    @commands.command(
        name="floridaman",
        help="Generate random Florida Man headlines!",
        aliases=["florida"],
        usage="[other state/country]",
    )
    async def florida_man(self, ctx, *, state="florida"):
        headline = [" ".join([name.capitalize() for name in state.split()])]
        objects = [
            "van",
            "dog",
            "cat",
            "car",
            "house",
            "alligator",
            "chicken nugget",
            "hospital bed",
            "penguin",
            "burger",
            "car salesman",
        ]
        people = ["man", "woman", "boy", "girl"]
        events = [
            "pushed",
            "thrown",
            "dropped",
            "burned",
            "stabbed",
            "run over",
            "slapped",
            "arrested",
        ]
        poss2 = ["", "by"]
        timing = ["after", "when"]
        actions = ["pushes", "throws", "drops", "burns", "stabs", "runs over", "slaps"]
        selected_object = choice(objects)
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
        headline.append(choice(actions))
        headline.append(choice(objects))
        await ctx.send(" ".join(headline))

    # @commands.command(
    #     name="img",
    #     help="[Infinite Monkey Generator](https://codepen.io/justinchan/full/enBFA)",
    #     aliases=["monkeys", "infinitemonkey", "monkeygen"],
    #     usage="<word> [alphabet (abcdefghijklmnopqrstuvwxyz)]",
    # )
    # async def img(self, ctx, word=None, alphabet="abcdefghijklmnopqrstuvwxyz"):
    #     alphabet = list(alphabet)
    #     if word == None:
    #         await ctx.send("You didn't specify a keyword to search for!")
    #     else:
    #         invalid = False
    #         for character in word:
    #             if character not in alphabet:
    #                 invalid = True
    #         if invalid:
    #             await ctx.send(
    #                 f"Your keyword contained characters that weren't in the specified alphabet ({list2str(alphabet, 1)})"
    #             )
    #         else:
    #             status = await ctx.send("Generating...")
    #             starttime = time()
    #             text = ""
    #             success = True
    #             while text.find(word) == -1:
    #                 letter = alphabet[randint(0, len(alphabet) - 1)]
    #                 text = text + letter
    #                 if Stopwatch.monkeywatch(starttime) == "01:00":
    #                     success = False
    #                     break
    #             cutoff = ""
    #             textlen = len(text)
    #             if len(text) > 1000:
    #                 text = f"...{text[-1000:]}"
    #                 cutoff = " (last 1000 shown)"
    #             text = (
    #                 text.replace("\\", "\\\\")
    #                 .replace("*", "\*")
    #                 .replace("_", "\_")
    #                 .replace("`", "\`")
    #                 .replace("~", "\~")
    #                 .replace("|", "\|")
    #             )
    #             if success:
    #                 await status.edit(
    #                     content=f'{text}\nKeyword "{word}" found after {textlen} characters{cutoff} in {Stopwatch.mokneywatch(self, starttime)}'
    #                 )
    #             else:
    #                 await status.edit(
    #                     content=f'Could not find keyword "{word}" within one minute. :frowning:'
    #                 )

    @commands.command(
        name="fortune",
        help="Pipe output from [`fortune`](https://en.wikipedia.org/wiki/Fortune_(Unix))",
        usage="no args",
    )
    async def fortune(self, ctx):
        await ctx.send(f"```{bash('fortune', shell=True).decode()}```")

    @name_generator.error
    @florida_man.error
    # @img.error
    @fortune.error
    async def error(self, ctx, error):
        error = str(error)
        if error.startswith(
            "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body"
        ):
            await ctx.send(
                "<:winxp_critical_error:869760946816553020>Sending all that would put me over the character limit!"
            )
        elif error == 'Unexpected quotation mark (") in non-quoted string':
            await ctx.send(
                '<:winxp_information:869760946808180747>You need to escape your "quotation marks" with backslashes (\\ these things \\\).'
            )
        else:
            await ctx.send(
                f"<:winxp_critical_error:869760946816553020>Unhandled error occurred:\n```\n{error}\n```\nIf my developer (<@!686984544930365440>) is not here, please tell him what the error is so that he can add handling or fix the issue!"
            )


def setup(client):
    client.add_cog(Generators(client))
