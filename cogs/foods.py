import discord
from discord.ext import commands
from random import choice, randint
from os import listdir
from json import dumps

class interactions(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.formatChars = "*`~|"
        self.cyan = 32639
    name = "interactions"
    name_typable = name
    description = "Interact with other server members!"
    description_long = description

    async def giveitem(self, ctx, botresponses, item, person2give2):
        persongiving = ctx.author.display_name.replace(
            "_",
            r"\_"
        )
        for char in self.formatChars:
            persongiving = persongiving.replace(
                char,
                "\\" + char
            )
        try:
            persongetting = person2give2.display_name.replace(
                "_",
                r"\_"
            )
            for char in self.formatChars:
                persongetting = persongetting.replace(
                    char,
                    "\\" + char
                )
        except:
            await ctx.send(
                f"""You can't just give a {
                    item
                } to thin air! (Unless you're giving it to a ghost?)"""
            )
            return
        if person2give2 == ctx.author:
            await ctx.send(
                f"""You didn't give the {
                    item
                } to anyone in particular"""
            )
        else:
            await ctx.send(
                embed = discord.Embed(
                    title = f"""{
                            persongiving
                        } gave a {
                            item
                        } to {
                            persongetting
                        }""",
                    color = self.cyan
                )
            )
            if person2give2 == self.client.user:
                await ctx.send(
                    choice(
                        botresponses
                    )
                )

    @commands.command(name = "give", help = "Give someone something to eat!", usage = " < username, nickname, or @mention > < item > ")
    async def give(self, ctx, member: discord.Member = None, *, item = None):
        items = {
            "candies": [
                "3 musketeers",
                "cake",
                "chocolate bar",
                "cookie",
                "kitkat",
                "snickers",
                "truffle"
            ],
            "dinners": [
                "burger",
                "burrito",
                "lasagna",
                "taco"
            ],
            "drinks": [
                "dr. pepper",
                "coke",
                "mcdonald's sprite",
                "pepsi",
                "root beer",
                "sprite",
                "water"
            ],
            "fruits": [
                "apple",
                "banana",
                "handful of berries",
                "orange",
                "peach",
                "pear"
            ],
            "sandwiches": [
                "blt",
                "club sandwich",
                "cuban sandwich",
                "grilled cheese",
                "pb&j",
                "reuben"
            ]
        }
        if member == None or type(item) is not str:
            await ctx.send(f"""Available food items:
```json
{
    dumps(
        items,
        indent = 4
    )
}
```"""
            )
        else:
            tests = {
                typeOfFood: True
                for typeOfFood in items
            }
            for typeOfFood in list(items.keys()):
                if item in items[typeOfFood]:
                    await self.giveitem(
                        ctx,
                        [
                            "Hey, thanks!",
                            "Thanks! :yum:"
                        ],
                        item,
                        member
                    )
                else:
                    tests[typeOfFood] = False
            if True not in list(tests.values()):
                await ctx.send(
                    "That item isn't in the list!"
                )

    @give.error
    async def error(self, ctx, error):
        if "Member" in str(error) and "not found" in str(error):
            await ctx.send(
                "Invalid user specified!"
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
        interactions(
            client
        )
    )