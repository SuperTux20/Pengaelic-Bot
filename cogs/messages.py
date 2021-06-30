# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from pengaelicutils import jsoncheck
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

    @commands.command(name="credits", help="See who helped me come to exist!")
    async def credits(self, ctx):
        bot_credits = {
            "Main Developer and Creator": "Tux Penguin (your local comfort OC dealer#7140)",
            "Original Host": "Hy Asencion (Hyperfresh#8080)",
            "Current Host": "Cherry Rain (Dichromatic Cherry Blossom#0356)",
        }
        if jsoncheck(ctx.guild.id):
            bot_credits = {cred.lower(): bot_credits[cred] for cred in bot_credits}
            await ctx.send(
                f"""
```json
"credits": {str(dumps(bot_credits, indent=4))}
```
"""
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
