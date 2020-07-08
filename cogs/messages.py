import discord
from discord.ext import commands
from random import choice

class Messages(commands.Cog):
    name = "messages"
    description = "M a k e   m e   s a y   t h i n g s"
    def __init__(self, client):
        self.client = client

    @commands.command(name="hi", help="You say hi, I greet you back!", aliases=["hello", "sup", "howdy", "hey", "heya"])
    async def say_hi_back(self, ctx):
        await ctx.send(choice(["Hi, I'm the Pengaelic Bot!", "Heya!", "What's up?"]))
        await ctx.message.delete()

    @commands.command(name="bye", help="You say bye, I bid you farewell.", aliases=["seeya", "cya", "goodbye"])
    async def say_bye_back(self, ctx):
        await ctx.send(choice(["See you next time!", "Bye!", "So long, Gay Bowser!"]))
        await ctx.message.delete()

    @commands.command(name="say", help="Make me say something! And possibly make me die inside!", pass_context=True, aliases=["repeat", "parrot"], usage="<message>")
    async def say_back(self, ctx, *, arg):
        await ctx.send(arg)
        await ctx.message.delete()

    @commands.command(name="youknowtherules", help="...and so do I.", pass_context=True)
    async def andsodoi(self, ctx):
        responses = []
        death_threats = ["It's time to die <:handgun:706698375592149013>", "And so do I :pensive:\nSay goodbye <:handgun:706698375592149013>"]
        for _ in range(3):
            responses.append("And so do I :pensive:")
        responses.append(choice(death_threats))
        await ctx.send(choice(responses))

def setup(client):
    client.add_cog(Messages(client))