import discord
from discord.ext import commands
from random import choice, randint
from os import listdir

class interactions(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.formatChars = "*`~|"
        self.cyan = 32639
    name = "interactions"
    name_typable = name
    description = "Interact with other server members!"
    description_long = description

    async def act(self, ctx, selfresponses, botresponses, act, pastact, acting, actee: discord.Member = None):
        actor = ctx.author.display_name.replace(
            "_",
            r"\_"
        )
        for char in self.formatChars:
            actor = actor.replace(
                char,
                "\\" + char
            )
        try:
            acted = actee.display_name.replace(
                "_",
                r"\_"
            )
            for char in self.formatChars:
                acted = acted.replace(
                    char,
                    "\\" + char
                )
        except:
            await ctx.send(
                f"""You can't just {
                    act
                } thin air! (Unless you're {
                    acting
                } a ghost?)"""
            )
            return
        responses = [
            f"""{
                acted
            } just got {
                pastact
            } by {
                actor
            }""",

            f"""{
                actor
            } {
                pastact
            } {
                acted
            }"""
        ]
        if actee == ctx.author:
            await ctx.send(choice(selfresponses)
            )
        else:
            await ctx.send(
                embed = discord.Embed(
                    title = choice(
                        responses
                    ),
                    color = self.cyan
                ).set_image(
                    url = f"""https://supertux20.github.io/Pengaelic-Bot/images/gifs/{
                        act
                    }/{
                        randint(
                            1,
                            len(
                                listdir(
                                    f'''../Pengaelic-Bot/images/gifs/{
                                        act
                                    }'''
                                )
                            )-1
                        )
                    }.gif"""
                )
            )
            if actee == self.client.user:
                await ctx.send(
                    choice(
                        botresponses
                    )
                )

    @commands.command(name = "hug", help = "Give somebody a hug!")
    async def hug(self, ctx, *, hug: discord.Member = None):
        await self.act(
            ctx,
            [
                "You wrap your arms tightly around yourself.",
                "Reaching through the 4th dimension, you manage to give yourself a hug.",
                "You hug yourself, somehow."
            ], [
                "aww!",
                "thanks<:happy:708534449310138379>",
                "*gasp*"
            ],
            "hug", "hugged",
            "hugging",
            hug
        )

    @commands.command(name = "boop", help = "Boop someone's nose :3")
    async def boop(self, ctx, *, boop: discord.Member = None):
        await self.act(
            ctx,
            [
                "You boop your own nose, I guess...? ",
                f"""You miss your nose and poke yourself in the eye. {
                    choice(
                        [
                            'Ouch',
                            'Oops',
                            'Whoops'
                        ]
                    )
                }!""",
                "Somehow, your hand clips through your nose and appears on the other side of your head. "
            ], [
                "<:happy:708534449310138379>", "<:uwu:708534448949559328>", "thaaanks :3"
            ],
            "boop",
            "booped",
            "booping",
            boop
        )

    @commands.command(name = "pat", help = "Pat someone on the head!")
    async def pat(self, ctx, *, pat: discord.Member = None):
        await self.act(
            ctx,
            [
                "You pat yourself on the head.",
                "You reach into the mirror and pat your reflection on the head."
            ], [
                "<:happy:708534449310138379>",
                "hehe",
                "aw, you're cute :3"
            ],
            "pat",
            "patted",
            "patting",
            pat
        )

    @commands.command(name = "tickle", help = "Tickle tickle tickle... >:D")
    async def tickle(self, ctx, *, tickle: discord.Member = None):
        await self.act(
            ctx,
            [
                "You try to tickle yourself, but your body reflexively flinches away.",
                "You try to tickle yourself, and you burst out laughing the moment your finger touches you.",
                "You try to tickle yourself, but nothing happens."
            ], [
                "hahahahahahahaha",
                "eeeeeehahahahaha",
                "aaaaaahahahahahaahaSTAHPhahahaha"
            ],
            "tickle",
            "tickled",
            "tickling",
            tickle
        )

    @commands.command(name = "kiss", help = "Give somebody a kiss~ :kissing_heart:")
    async def kiss(self, ctx, *, kiss: discord.Member = None):
        await self.act(
            ctx,
            [
                "You... Huh... How does this work...?",
                "You kiss your reflection in the mirror.",
                "You kiss the back of your own hand."
            ], [
                ":flushed:",
                "<:happy:708534449310138379>",
                "*gasp*"
            ],
            "kiss"
            "kissed",
            "kissing",
            kiss
        )

    @commands.command(name = "squish", help = "Sqweesh someone's face >3<")
    async def squish(self, ctx, *, squish: discord.Member = None):
        await self.act(
            ctx,
            [
                "You squish your own face. You look like a fish.",
                "You reach through the mirror and squish your reflection's face.",
                "For some reason, you curl your arms around your head to squish your own face."
            ], [
                "hehehe",
                "squish...",
                "<:hmmph:708534447217180702>"
            ],
            "squish",
            "squished",
            "squishing",
            squish
        )

    @boop.error
    @hug.error
    @pat.error
    @tickle.error
    @kiss.error
    @squish.error
    async def error(self, ctx, error):
        if "Member" in str(error) and "not found" in str(error):
            await ctx.send("Invalid user specified!")
        else:
            await ctx.send(f"""Unhandled error occurred:
        {
            error
        }
If my developer (<@!686984544930365440>) is not here, please tell him what the error is so that he can add handling or fix the issue!""")

def setup(client):
    client.add_cog(
        interactions(
            client
        )
    )