import discord
from discord.ext import commands
from random import choice, randint

class NSFW(commands.Cog):
    def __init__(self, client):
        self.client = client
    name = "nsfw"
    name_typable = name
    description = "Shhhhh..."
    description_long = description

    @commands.command(name = "sauce", help = "Generate NHentai sauce.", usage = "[number of sauces (1)]\n[auto-link (False)]")
    async def sauce(self, ctx, sauces: int = 1, autolink: bool = False):
        if sauces < 1:
            response = "You didn't generate any sauce."
        elif sauces > 100:
            response = f"{sauces} sacues? That's just silly."
        else:
            if autolink == True:
                response = str(["https://nhentai.net/g/" + str(randint(0,500000)) for _ in range(sauces)])[1:-1].replace("'","")
            elif autolink == False:
                response = str([randint(0,500000) for _ in range(sauces)])[1:-1]
        await ctx.send(response)

    @sauce.error
    async def error(self, ctx, error):
        if str(error) == """Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body
In content: Must be 2000 or fewer in length.""":
            await ctx.send(
                "Sorry, you specified numbers that were too large. Sending all that would put me over the 2000-character limit!"
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
        NSFW(
            client
        )
    )