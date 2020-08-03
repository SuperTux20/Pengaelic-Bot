import discord
from discord.ext import commands
from random import choice

class actsofviolence(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.formatChars = "*`~|"
    name = "acts of violence"
    name_typable = "actsofviolence"
    description = "Interact with other server members, but with **anger**"
    description_long = description

    async def act(self, ctx, act, pastact, acting, actee: discord.Member=None, image: str=None):
        actor = ctx.author.display_name
        factor = actor.replace(
            "_",
            r"\_"
        )
        for char in self.formatChars:
            factor = factor.replace(
                char,
                "\\" + char
            )
        try:
            acted = actee.display_name
            facted = acted.replace(
                "_",
                r"\_"
            )
            for char in self.formatChars:
                facted = facted.replace(
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
                facted
            } just got {
                pastact
            } by {
                factor
            }""",

            f"""{
                factor
            } {
                pastact
            } {
                facted
            }"""
            ]
        if actee == ctx.author:
            await ctx.send(
                f"""Hey, you can't {
                    act
                } yourself!"""
            )
        elif actee == self.client.user:
            await ctx.send(
                f"""Hey, you can't {
                    act
                } me!"""
            )
        else:
            embed = discord.Embed(
                title=choice(responses),
                color=32639
            )
            if image:
                embed.set_image(
                    url=image
                )
            await ctx.send(
                embed=embed
            )

    @commands.command(name="slap", help="Slap someone!")
    async def slap(self, ctx, *, slap: discord.Member=None):
        await self.act(
            ctx,
            "slap",
            "slapped",
            "slapping",
            slap
        )

    @commands.command(name="stab", help="Stab someone!")
    async def stab(self, ctx, *, stab: discord.Member=None):
        await self.act(
            ctx,
            "stab",
            "stabbed",
            "stabbing",
            stab
        )

    @commands.command(name="shoot", help="Shoot someone!")
    async def shoot(self, ctx, *, shoot: discord.Member=None):
        await self.act(
            ctx,
            "shoot",
            "shot",
            "shooting",
            shoot
        )

    @commands.command(name="bonk", help="Bonk someone on the head!")
    async def bonk(self, ctx, *, bonk: discord.Member=None):
        await self.act(
            ctx,
            "bonk",
            "bonked",
            "bonking",
            bonk,
            "https://supertux20.github.io/Pengaelic-Bot/images/bonk.jpg"
        )

    @slap.error
    @stab.error
    @shoot.error
    @bonk.error
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
        actsofviolence(
            client
        )
    )