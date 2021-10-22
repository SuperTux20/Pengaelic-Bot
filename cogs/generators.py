#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from asyncio.events import get_event_loop
from concurrent.futures import ThreadPoolExecutor
from discord.ext import commands
from pengaelicutils import (
    list2str,
    unhandling,
    tux_in_guild,
    Developers,
    Stopwatch,
    syllables,
    eldritch_syllables,
)
from random import choice, randint
from subprocess import check_output as bash
from time import time

devs = Developers()


class Generators(commands.Cog):
    def __init__(self, client):
        self.client = client

    name = "generators"
    name_typable = name
    description = "Do ya like randomization?"
    description_long = description + " So do I!"

    # SECTION: FUNCTIONS
    def MonkeyBusiness(
        self,
        word: str,
        alphabet: str,
        starttime: float,
        success: bool = True,
        timer: Stopwatch = Stopwatch(),
        text: str = "",
    ) -> tuple:
        while text.find(word) == -1:
            letter = choice(alphabet)
            text = text + letter
            if timer.monkeywatch(starttime) == "01:00":
                success = False
                break
        cutoff = ""
        textlen = len(text)
        if len(text) > 1000:
            text = f"...{text[-1000:]}"
            cutoff = " (last 1000 shown)"
        text = (
            text.replace("\\", "\\\\")
            .replace("*", "\*")
            .replace("_", "\_")
            .replace("`", "\`")
            .replace("~", "\~")
            .replace("|", "\|")
        )
        return text, cutoff, textlen, success, timer.monkeywatch(starttime)

    def gen(
        self,
        amount: int = 1,
        upper_limit: int = 3,
        lower_limit: int = 2,
        eldritch: bool = False,
    ) -> str:
        if eldritch:
            syls = eldritch_syllables()
        else:
            syls = syllables
        if amount > 0 and upper_limit > 0 and lower_limit > 0:
            if not lower_limit > upper_limit:
                return list2str(
                    [
                        "".join(
                            [
                                choice(syls)
                                for _ in range(randint(lower_limit, upper_limit))
                            ]
                        ).capitalize()
                        for _ in range(amount)
                    ],
                    3,
                )
            else:
                return "The lower limit cannot be higher than the upper limit."
        else:
            return "Values can't be zero."

    # END SECTION

    @commands.command(
        name="name",
        help="Generate a random name! They tend to be mystic-sounding :eyes:",
        aliases=["namegen"],
        usage="[names to generate (1)]\n[max syllables (3)]\n[min syllables (2)]",
    )
    async def name_generator(
        self, ctx, amount: int = 1, upper_limit: int = 3, lower_limit: int = 2
    ):
        await ctx.send(self.gen(amount, upper_limit, lower_limit))

    @commands.command(
        name="ename",
        help="Generate an eldritch name that sounds straight out of an H. P. Lovecraft novel.",
        aliases=["eldritchname"],
        usage="[names to generate (1)]\n[max syllables (3)]\n[min syllables (2)]",
    )
    async def eldritch_name_generator(
        self, ctx, amount: int = 1, upper_limit: int = 3, lower_limit: int = 2
    ):
        await ctx.send(self.gen(amount, upper_limit, lower_limit, True))

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

    @commands.command(
        name="img",
        help="[Infinite Monkey Generator](https://codepen.io/justinchan/full/enBFA)",
        aliases=["monkeys", "infinitemonkey", "monkeygen"],
        usage="<word> [alphabet (abcdefghijklmnopqrstuvwxyz)]",
    )
    async def img(self, ctx, word=None, alphabet="abcdefghijklmnopqrstuvwxyz"):
        alphabet = list(alphabet)
        if word == None:
            await ctx.send("You didn't specify a keyword to search for!")
        else:
            invalid = False
            for character in word:
                if character not in alphabet:
                    invalid = True
            if invalid:
                await ctx.send(
                    f"Your keyword contained characters that weren't in the specified alphabet ({list2str(alphabet, 1)})"
                )
            else:
                status = await ctx.send("Generating...")
                async with ctx.typing():
                    (
                        text,
                        cutoff,
                        textlen,
                        success,
                        elapsed,
                    ) = await get_event_loop().run_in_executor(
                        ThreadPoolExecutor(),
                        self.MonkeyBusiness,
                        word,
                        alphabet,
                        time(),
                    )
                if success:
                    await status.edit(content=text)
                    await ctx.send(
                        f'Keyword "{word}" found after {textlen} characters{cutoff} in {elapsed}'
                    )
                else:
                    await ctx.send(
                        content=f'Could not find keyword "{word}" within one minute. :frowning:'
                    )

    @commands.command(
        name="fortune",
        help="Pipe output from [`fortune`](https://en.wikipedia.org/wiki/Fortune_(Unix))\nNote: I am not responsible for any offensive output it may generate.",
    )
    async def fortune(self, ctx):
        await ctx.send(f"```{bash('fortune')}```")

    @name_generator.error
    @florida_man.error
    @img.error
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
                unhandling(
                    error,
                    tux_in_guild(ctx, self.client),
                )
            )


def setup(client):
    client.add_cog(Generators(client))
