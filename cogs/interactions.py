#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from random import choice, randint
from os import listdir
from pengaelicutils import list2str, unhandling, tux_in_guild, Developers

devs = Developers()


class Interactions(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.teal = 0x007F7F

    name = "interactions"
    name_typable = name
    description = "Interact with other server members!"
    description_long = description
    # SECTION: FUNCTIONS
    def act(self, ctx, act, pastact, actees, violence) -> discord.Embed:
        acted = []
        for actee in actees:
            acted.append(actee.mention)
        acted = list2str(acted, 0, True)
        image = f"https://supertux20.github.io/Pengaelic-Bot/images/interactions/{act}"
        if violence:
            image += ".jpg"
        else:
            image += f"/{randint(1,len(listdir(f'images/interactions/{act}'))-1)}.gif"
        return discord.Embed(
            description=f'**{choice([f"{acted} just got {pastact} by {ctx.author}",f"{ctx.author} {pastact} {acted}",])}**',
            color=self.teal,
        ).set_image(url=image)

    async def nact(self, ctx, act, pastact, actees, selfresponses):
        if len(actees) == 1 and actees[0] == ctx.author:
            await ctx.send(choice(selfresponses))
        else:
            await ctx.send(embed=self.act(ctx, act, pastact, actees, False))

    async def vact(self, ctx, act, pastact, actees):
        if len(actees) == 1 and actees[0] == ctx.author:
            await ctx.send(f"Hey, you can't {act} yourself!")
        elif len(actees) == 1 and actees[0] == self.client.user:
            await ctx.send(f"Hey, you can't {act} me!")
        else:
            await ctx.send(embed=self.act(ctx, act, pastact, actees, True))

    # END SECTION

    # SECTION: INTERACTIONS
    @commands.command(
        name="hug",
        help="Give somebody a hug!",
        usage="<username, nickname, or @mention>",
    )
    async def hug(self, ctx, *hug: discord.Member):
        await self.nact(
            ctx,
            "hug",
            "hugged",
            hug,
            [
                "You wrap your arms tightly around yourself.",
                "Reaching through the 4th dimension, you manage to give yourself a hug.",
                "You hug yourself, somehow.",
            ],
        )

    @commands.command(
        name="boop",
        help="Boop someone's nose :3",
        usage="<username, nickname, or @mention>",
    )
    async def boop(self, ctx, *boop: discord.Member):
        await self.nact(
            ctx,
            "boop",
            "booped",
            boop,
            [
                "You boop your own nose, I guess...? ",
                f"You miss your nose and poke yourself in the eye. {choice(['Ouch', 'Oops', 'Whoops'])}!",
                "Somehow, your hand clips through your nose and appears on the other side of your head.",
            ],
        )

    @commands.command(
        name="pat",
        help="Pat someone on the head!",
        usage="<username, nickname, or @mention>",
    )
    async def pat(self, ctx, *pat: discord.Member):
        await self.nact(
            ctx,
            "pat",
            "patted",
            pat,
            [
                "You pat yourself on the head.",
                "You reach into the mirror and pat your reflection on the head.",
                "You give yourself a pat on the back.",
            ],
        )

    @commands.command(
        name="tickle",
        help="Tickle tickle tickle... >:D",
        usage="<username, nickname, or @mention>",
    )
    async def tickle(self, ctx, *tickle: discord.Member):
        await self.nact(
            ctx,
            "tickle",
            "tickled",
            tickle,
            [
                "You try to tickle yourself, but your body reflexively flinches away.",
                "You try to tickle yourself, and you burst out laughing the moment your finger touches you.",
                "You try to tickle yourself, but nothing happens.",
            ],
        )

    @commands.command(
        name="kiss",
        help="Give somebody a kiss~ :kissing_heart:",
        usage="<username, nickname, or @mention>",
    )
    async def kiss(self, ctx, *kiss: discord.Member):
        await self.nact(
            ctx,
            "kiss",
            "kissed",
            kiss,
            [
                "You... Huh... How does this work...?",
                "You kiss your reflection in the mirror.",
                "You kiss the back of your own hand.",
            ],
        )

    @commands.command(
        name="squish",
        help="Sqweesh someone's face >3<",
        usage="<username, nickname, or @mention>",
    )
    async def squish(self, ctx, *squish: discord.Member):
        await self.nact(
            ctx,
            "squish",
            "squished",
            squish,
            [
                "You squish your own face. You look like a fish.",
                "You reach through the mirror and squish your reflection's face.",
                "For some reason, you curl your arms around your head to squish your own face.",
            ],
        )

    @commands.command(
        name="nom",
        help="**C O N S U M E**",
        usage="<username, nickname, or @mention>",
    )
    async def nom(self, ctx, *nom: discord.Member):
        await self.nact(
            ctx,
            "nom",
            "nommed",
            nom,
            [
                "You break all meaning of Euclidean space and eat yourself.",
                "You pull your reflection out of the mirror and eat them.",
                "You shove your hand into your mouth, then give up.",
            ],
        )

    # END SECTION

    # SECTION: ACTS OF VIOLENCE
    @commands.command(
        name="slap", help="Slap someone!", usage="<username, nickname, or @mention>"
    )
    async def slap(self, ctx, *slap: discord.Member):
        await self.vact(ctx, "slap", "slapped", slap)

    @commands.command(
        name="stab", help="Stab someone!", usage="<username, nickname, or @mention>"
    )
    async def stab(self, ctx, *stab: discord.Member):
        await self.vact(ctx, "stab", "stabbed", stab)

    @commands.command(
        name="shoot", help="Shoot someone!", usage="<username, nickname, or @mention>"
    )
    async def shoot(self, ctx, *shoot: discord.Member):
        await self.vact(ctx, "shoot", "shot", shoot)

    @commands.command(
        name="bonk",
        help="Bonk someone on the head!",
        usage="<username, nickname, or @mention>",
    )
    async def bonk(self, ctx, *bonk: discord.Member):
        await self.vact(ctx, "bonk", "bonked", bonk)

    # END SECTION

    @bonk.error
    @boop.error
    @hug.error
    @kiss.error
    @nom.error
    @pat.error
    @shoot.error
    @slap.error
    @stab.error
    @squish.error
    @tickle.error
    async def error(self, ctx, error):
        error = str(error)
        if (
            error.startswith("Member") and error.endswith("not found.")
        ) or "IndexError" in error:
            await ctx.send("<:winxp_warning:869760947114348604>Invalid user specified!")
        else:
            await ctx.send(
                unhandling(
                    error,
                    tux_in_guild(ctx, self.client),
                )
            )


def setup(client):
    client.add_cog(Interactions(client))
