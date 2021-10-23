#!/usr/bin/python
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from random import randint
from os import listdir


class Actions(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.formatChars = "*`~|"
        self.teal = 0x007F7F

    name = "actions"
    name_typable = name
    description = "Emote actions!"
    description_long = description

    async def act(self, ctx, act, punct="..."):
        actor = ctx.author.display_name.replace("_", r"\_")
        for char in self.formatChars:
            actor = actor.replace(char, "\\" + char)
        await ctx.send(
            embed=discord.Embed(
                title=f"{actor} is {act}ing{punct}", color=self.teal
            ).set_image(
                url=f"https://supertux20.github.io/Pengaelic-Bot/images/actions/{act}/{randint(1,len(listdir(f'images/actions/{act}'))-1)}.gif"
            )
        )

    @commands.command(name="cry")
    async def cry(self, ctx):
        await self.act(ctx, "cry")

    @commands.command(name="glare")
    async def glare(self, ctx):
        await self.act(ctx, "glar")

    @commands.command(name="laugh")
    async def laugh(self, ctx):
        await self.act(ctx, "laugh", "!")

    @commands.command(name="shrug")
    async def shrug(self, ctx):
        await self.act(ctx, "shrugg", ".")

    @commands.command(name="sleep")
    async def sleep(self, ctx):
        await self.act(ctx, "sleep")


def setup(client):
    client.add_cog(Actions(client))
