# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from random import randint
from os import listdir

class Actions(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.formatChars = "*`~|"
        self.teal = 0x007f7f
    name = "actions"
    name_typable = name
    description = "Emote actions!"
    description_long = description

    async def act(self, ctx, act, acting):
        actor = ctx.author.display_name.replace(
            "_",
            r"\_"
        )
        for char in self.formatChars:
            actor = actor.replace(
                char,
                "\\" + char
            )
        await ctx.send(
            embed=discord.Embed(
                title=f"{actor} is {acting}",
                color=self.teal
            )#.set_image(url = f"https://supertux20.github.io/Pengaelic-Bot/images/gifs/actions/{act}/{randint(1,len(listdir(f'../Pengaelic-Bot/images/actions/{act}'))-1)}.gif")
        )

    @commands.command(name="cry")
    async def cry(self, ctx):
        await self.act(
            ctx,
            "cry",
            "crying..."
        )

    @commands.command(name="laugh")
    async def laugh(self, ctx):
        await self.act(
            ctx,
            "laugh",
            "laughing!"
        )

    @commands.command(name="sleep")
    async def snore(self, ctx):
        await self.act(
            ctx,
            "sleep",
            "sleeping..."
        )

def setup(client):
    client.add_cog(Actions(client))
