#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from pengaelicutils import jsoncheck, Developers
from json import dumps


class Messages(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.teal = 0x007F7F

    name = "messages"
    name_typable = name
    description = "Make me say all sorts of things."
    description_long = description + " And possibly make me die inside."

    @commands.command(
        name="say",
        help="I'll repeat whatever you tell me.",
        pass_context=True,
        aliases=["repeat", "parrot"],
        usage="<message>",
    )
    async def say_back(self, ctx, *, arg):
        await ctx.send(arg)
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.message.delete()

    @commands.command(
        name="credits", help="See who helped me come to exist!", usage="no args"
    )
    async def credits(self, ctx):
        bot_credits = {
            "Main Developer and Creator": f"Tux Penguin ({self.client.get_user(Developers.get(None, 'tux'))})",
            "Current Host": f"Hy Asencion ({self.client.get_user(Developers.get(None, 'hy'))} or {self.client.get_user(Developers.get(None, 'ly'))})",
            "Side Developer and Backup Host": f"Cherry Rain ({self.client.get_user(Developers.get(None, 'cherry'))})",
        }
        if jsoncheck(ctx.guild.id):
            bot_credits = {cred.lower(): bot_credits[cred] for cred in bot_credits}
            await ctx.send(
                "```json"
                + f'\n"credits": {str(dumps(bot_credits, indent=4))}\n'
                + "```"
            )
        else:
            embed = discord.Embed(
                color=self.teal,
                title="Credits",
                description="All the people on Discord who helped me become what I am today.",
            )
            for cred in bot_credits:
                embed.add_field(name=cred, value=bot_credits[cred])
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Messages(client))
