import discord
from discord.ext import commands
from random import choice, randint
from os import listdir
from json import load
from time import sleep

class interactions(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.isNomming = True
        self.nomSuccess = False
        self.formatChars = "*`~|"
        self.cyan = 32639
    name = "interactions"
    name_typable = name
    description = "Interact with other server members!"
    description_long = description

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.emoji == "👄":
            if user.id != 721092139953684580:
                if self.isNomming == True:
                    self.isNomming = False
                    self.nomSuccess = False

    async def act(self, ctx, selfresponses, botresponses, act, pastact, acting, actee: discord.Member=None):
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
                embed=discord.Embed(
                    title=choice(
                        responses
                    ),
                    color=self.cyan
                ).set_image(
                    url=f"""https://supertux20.github.io/Pengaelic-Bot/images/gifs/{
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

    @commands.command(name="hug", help="Give somebody a hug!")
    async def hug(self, ctx, *, hug: discord.Member=None):
        await self.act(
            ctx,
            [
                "You wrap your arms tightly around yourself.",
                "Reaching through the 4th dimension, you manage to give yourself a hug.",
                "You hug yourself, somehow."
            ], [
                "aww!",
                "thanks <:happy:708534449310138379>",
                "*gasp*"
            ],
            "hug", "hugged",
            "hugging",
            hug
        )

    @commands.command(name="boop", help="Boop someone's nose :3")
    async def boop(self, ctx, *, boop: discord.Member=None):
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

    @commands.command(name="pat", help="Pat someone on the head!")
    async def pat(self, ctx, *, pat: discord.Member=None):
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

    @commands.command(name="tickle", help="Tickle tickle tickle... >:D")
    async def tickle(self, ctx, *, tickle: discord.Member=None):
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

    @commands.command(name="kiss", help="Give somebody a kiss~ :kissing_heart:")
    async def kiss(self, ctx, *, kiss: discord.Member=None):
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

    @commands.command(name="squish", help="Sqweesh someone's face >3<")
    async def squish(self, ctx, *, squish: discord.Member=None):
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

    @commands.command(name="nom", help="Possibly eat someone >:3\nThey can get away if they're fast enough :eyes:", aliases=["eat","omnomnom"])
    async def nom(self, ctx, *, nom: discord.Member=None):
        nommer = ctx.author.display_name
        for char in self.formatChars:
            nommer = nommer.replace(
                char,
                "\\" + char
            )
        try:
            nommed = nom.display_name
            for char in self.formatChars:
                nommed = nommed.replace(
                    char,
                    "\\" + char
                )
        except:
            await ctx.send(
                "You can't just nom thin air! (Unless you're nomming a ghost?)"
            )
            return
        responses = [
            nommed + " just got nommed by " + nommer,
            nommer + " nommed " + nommed
        ]
        selfresponses = [
            "You eat yourself and create a black hole. Thanks a lot.",
            "You chew on your own finger. Why...?",
            "Uh... what?"
        ]
        botresponses = [
            "mmmph!",
            "nmmmmmmmph!",
            "hmmmnnnnn!!"
        ]
        embed = discord.Embed(
            title=choice(
                responses
            ),
            color=self.cyan
        ).set_image(
            url=f"""https://supertux20.github.io/Pengaelic-Bot/images/gifs/nom/{
                randint(
                    1,
                    len(
                        listdir(
                            '../Pengaelic-Bot/images/gifs/nom'
                        )
                    ) - 1
                )
            }.gif"""
        )
        if nom == ctx.author:
            await ctx.send(
                choice(
                    selfresponses
                )
            )
        else:
            if str(nom.id) == "721092139953684580":
                await ctx.send(
                    embed=embed
                )
                await ctx.send(
                    choice(
                        botresponses
                    )
                )
            else:
                self.isNomming = True
                self.nomSuccess = False
                stupidchannel = await ctx.guild.create_text_channel(
                    name="nom-command-stupidity",
                    overwrites={
                        ctx.guild.default_role: discord.PermissionOverwrite(
                            read_messages=False
                        ),
                        ctx.guild.me: discord.PermissionOverwrite(
                            read_messages=True
                        )
                    }
                )
                NoNomSense = await ctx.send(
                    f"""{
                        nommer
                    } is trying to eat you, {
                        nommed
                    }! Quick, click on the reaction to get away!"""
                )
                await NoNomSense.add_reaction(
                    "👄"
                )
                for _ in range(5):
                    sleep(
                        1
                    )
                    await stupidchannel.send(
                        "The command doesn't work without this message for some stupid reason."
                    )
                    if self.isNomming == False:
                        break
                if self.isNomming == True:
                    self.isNomming = False
                    self.nomSuccess = True
                await NoNomSense.delete()
                if self.nomSuccess == True:
                    await ctx.send(
                        embed=embed
                    )
                else:
                    await ctx.send(
                        f"""{
                            nommed
                        } got away!"""
                    )
                await stupidchannel.delete()

    @boop.error
    @hug.error
    @pat.error
    @tickle.error
    @kiss.error
    @squish.error
    @nom.error
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