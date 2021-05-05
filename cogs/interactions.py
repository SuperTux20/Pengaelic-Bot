# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from random import choice, randint
from os import listdir
from json import dumps
from pengaelicutils import getops

class Interactions(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.formatChars = "*`~|"
        self.teal = 0x007f7f
    name = "interactions"
    name_typable = name
    description = "Interact with other server members!"
    description_long = description

    async def act(self, ctx, selfresponses, act, pastact, acting, actee: discord.Member = None):
        if actee:
            if not actee.bot:
                actor = ctx.author.display_name.replace("_", r"\_")
                for char in self.formatChars:
                    actor = actor.replace(char, "\\" + char)
                acted = actee.display_name.replace("_", r"\_")
                for char in self.formatChars:
                    acted = acted.replace(char, "\\" + char)
                responses = [
                    f"{acted} just got {pastact} by {actor}",
                    f"{actor} {pastact} {acted}"
                ]
                if actee == ctx.author:
                    await ctx.send(choice(selfresponses))
                else:
                    await ctx.send(
                        embed=discord.Embed(
                            title=choice(responses),
                            color=self.teal
                        ).set_image(url=f"https://supertux20.github.io/Pengaelic-Bot/images/interactions/{act}/{randint(1,len(listdir(f'../Pengaelic-Bot/images/interactions/{act}'))-1)}.gif"))
            else:
                await ctx.send(f"Sorry, you can't {act} bots...")
                if actee.id == self.client.user.id:
                    await ctx.send(f"Thanks anyway.")
        else:
            await ctx.send(f"You can't just {act} thin air! (Unless you're {acting} a ghost?)")

    async def vact(self, ctx, act, pastact, acting, actee: discord.Member = None, image: str = None):
        if actee:
            actor = ctx.author.display_name
            factor = actor.replace("_", r"\_")
            for char in self.formatChars:
                factor = factor.replace(char, "\\" + char)
                acted = actee.display_name
                facted = acted.replace("_", r"\_")
                for char in self.formatChars:
                    facted = facted.replace(char, "\\" + char)
            responses = [
                f"{facted} just got {pastact} by {factor}",
                f"{factor} {pastact} {facted}"
            ]
            if actee == ctx.author:
                await ctx.send(f"Hey, you can't {act} yourself!")
            elif actee == self.client.user:
                await ctx.send(f"Hey, you can't {act} me!")
            else:
                embed = discord.Embed(
                    title=choice(responses),
                    color=self.teal
                ).set_image(url=f"https://supertux20.github.io/Pengaelic-Bot/images/interactions/{act}.jpg")
                await ctx.send(embed=embed)
        else:
            await ctx.send(f"You can't just {act} thin air! (Unless you're {acting} a ghost?)")

    @commands.command(name="hug", help="Give somebody a hug!", usage="<username or nickname or @mention>")
    async def hug(self, ctx, *, hug: discord.Member = None):
        await self.act(
            ctx,
            [
                "You wrap your arms tightly around yourself.",
                "Reaching through the 4th dimension, you manage to give yourself a hug.",
                "You hug yourself, somehow."
            ],
            "hug",
            "hugged",
            "hugging",
            hug
        )

    @commands.command(name="boop", help="Boop someone's nose :3", usage="<username or nickname or @mention>")
    async def boop(self, ctx, *, boop: discord.Member = None):
        await self.act(
            ctx,
            [
                "You boop your own nose, I guess...? ",
                f"You miss your nose and poke yourself in the eye. {choice(['Ouch', 'Oops', 'Whoops'])}!",
                "Somehow, your hand clips through your nose and appears on the other side of your head."
            ],
            "boop",
            "booped",
            "booping",
            boop
        )

    @commands.command(name="pat", help="Pat someone on the head!", usage="<username or nickname or @mention>")
    async def pat(self, ctx, *, pat: discord.Member = None):
        await self.act(
            ctx,
            [
                "You pat yourself on the head.",
                "You reach into the mirror and pat your reflection on the head.",
                "You give yourself a pat on the back."
            ],
            "pat",
            "patted",
            "patting",
            pat
        )

    @commands.command(name="tickle", help="Tickle tickle tickle... >:D", usage="<username or nickname or @mention>")
    async def tickle(self, ctx, *, tickle: discord.Member = None):
        await self.act(
            ctx,
            [
                "You try to tickle yourself, but your body reflexively flinches away.",
                "You try to tickle yourself, and you burst out laughing the moment your finger touches you.",
                "You try to tickle yourself, but nothing happens."
            ],
            "tickle",
            "tickled",
            "tickling",
            tickle
        )

    @commands.command(name="kiss", help="Give somebody a kiss~ :kissing_heart:", usage="<username or nickname or @mention>")
    async def kiss(self, ctx, *, kiss: discord.Member = None):
        await self.act(
            ctx,
            [
                "You... Huh... How does this work...?",
                "You kiss your reflection in the mirror.",
                "You kiss the back of your own hand."
            ],
            "kiss",
            "kissed",
            "kissing",
            kiss
        )

    @commands.command(name="squish", help="Sqweesh someone's face >3<", usage="<username or nickname or @mention>")
    async def squish(self, ctx, *, squish: discord.Member = None):
        await self.act(
            ctx,
            [
                "You squish your own face. You look like a fish.",
                "You reach through the mirror and squish your reflection's face.",
                "For some reason, you curl your arms around your head to squish your own face."
            ],
            "squish",
            "squished",
            "squishing",
            squish
        )

    async def giveitem(self, ctx, item, person2give2):
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
            await ctx.send(f"You can't just give a {item} to thin air! (Unless you're giving it to a ghost?)")
            return
        if person2give2 == ctx.author:
            await ctx.send(f"You didn't give the {item} to anyone in particular")
        else:
            await ctx.send(
                embed=discord.Embed(
                    title=f"{persongiving} gave a {item} to {persongetting}",
                    color=self.teal
                )
            )
            if person2give2.bot:
                await ctx.send(f"Sorry, you can't give foods to bots...")
                if person2give2.id == self.client.user.id:
                    await ctx.send(f"Thanks anyway.")

    @commands.command(name="give", help="Give someone something to eat!", usage=" <username, nickname, or @mention> <item>")
    async def give(self, ctx, member: discord.Member = None, *, item=None):
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
            if getops(ctx.guild.id, "toggles", "jsonMenus"):
                await ctx.send(f"""availableFoodItems:
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
                embed = discord.Embed(
                    color=self.teal,
                    title="Available food items"
                )
                for food_type in items:
                    embed.add_field(
                        name=food_type,
                        value=items[food_type]
                    )
                await ctx.send(embed)
        else:
            tests = {
                food_type: True
                for food_type in items
            }
            for food_type in list(items.keys()):
                if item in items[food_type]:
                    await self.giveitem(
                        ctx,
                        item,
                        member
                    )
                else:
                    tests[food_type] = False
            if True not in list(tests.values()):
                await ctx.send("That item isn't in the list!")

    @commands.command(name="slap", help="Slap someone!", usage="<username or nickname or @mention>")
    async def slap(self, ctx, *, slap: discord.Member = None):
        await self.vact(
            ctx,
            "slap",
            "slapped",
            "slapping",
            slap
        )

    @commands.command(name="stab", help="Stab someone!", usage="<username or nickname or @mention>")
    async def stab(self, ctx, *, stab: discord.Member = None):
        await self.vact(
            ctx,
            "stab",
            "stabbed",
            "stabbing",
            stab
        )

    @commands.command(name="shoot", help="Shoot someone!", usage="<username or nickname or @mention>")
    async def shoot(self, ctx, *, shoot: discord.Member = None):
        await self.vact(
            ctx,
            "shoot",
            "shot",
            "shooting",
            shoot
        )

    @commands.command(name="bonk", help="Bonk someone on the head!", usage="<username or nickname or @mention>")
    async def bonk(self, ctx, *, bonk: discord.Member = None):
        await self.vact(
            ctx,
            "bonk",
            "bonked",
            "bonking",
            bonk
        )

    @slap.error
    @stab.error
    @shoot.error
    @bonk.error
    @boop.error
    @hug.error
    @pat.error
    @tickle.error
    @kiss.error
    @squish.error
    @give.error
    async def error(self, ctx, error):
        if "Member" in str(error) and "not found" in str(error):
            await ctx.send("Invalid user specified!")
        else:
            await ctx.send(f"Unhandled error occurred:\n```{error}```\nIf my developer (<@!686984544930365440>) is not here, please tell him what the error is so that he can add handling or fix the issue!")

def setup(client):
    client.add_cog(Interactions(client))