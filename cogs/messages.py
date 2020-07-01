import discord
from discord.ext import commands
from random import choice

class Messages(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="hi", help="You say hi, I greet you back!", aliases=["hello", "sup", "howdy"])
    async def say_hi_back(self, ctx, delete=None):
        await ctx.send(choice(["Hi, I'm the Pengaelic Bot!", "Heya!", "What's up?"]))
        if delete:
            await ctx.message.delete()

    @commands.command(name="bye", help="You say bye, I bid you farewell.", aliases=["seeya", "cya", "goodbye"])
    async def say_bye_back(self, ctx, delete=None):
        await ctx.send(choice(["See you next time!", "Bye!", "So long, Gay Bowser!"]))
        if delete:
            await ctx.message.delete()

    @commands.command(name="say", help="Make me say something!", pass_context=True, aliases=["repeat", "parrot"])
    async def say_back(self, ctx, *, arg):
        await ctx.send(arg)
        await ctx.message.delete()

def setup(client):
    client.add_cog(Messages(client))