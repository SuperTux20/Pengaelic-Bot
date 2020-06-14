# bot.py
import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(".env")
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

bot = commands.Bot(command_prefix="p!")

@bot.command(name="hi", help="You say hi, I greet you back!")
async def say_hi_back(ctx):
    responses = ["Hi, I'm the Pengaelic Bot!", "Heya!", "What's up?"]
    response = random.choice(responses)
    await ctx.send(response)

@bot.command(name="bye", help="You say bye, I bid you farewell.")
async def say_bye_back(ctx):
    responses = ["See you next time!", "Bye!", "So long, gay bowser!"]
    response = random.choice(responses)
    await ctx.send(response)

@bot.command(name="repeat", help="You say something, I repeat it.")
async def say_back(ctx, *, arg):
    await ctx.send(arg)

@bot.command(name="roll", help="Roll some dice! Be sure to specify the number of dice, then the number of sides they have (all dice have the same number of sides).\nThe currently known limits are...\n\t- 658 dice with 1 side\n\t- 657 dice with 2-9 sides\n\t- 616 dice with 10 sides")
async def rollem(ctx, dice: int, sides: int):
    if dice == "0":
        await ctx.send("Hey, you can't roll zero dice!")
    elif sides == "0":
        if dice == "1":
            await ctx.send("Hey, you can't roll a zero-sided die!")
        if dice > "1":
            await ctx.send("Hey, you can't roll zero-sided dice!")
    elif dice < "0":
        await ctx.send("Hey, you can't roll negative dice!")
    elif sides < "0":
        if dice == "1":
            await ctx.send("Hey, you can't roll a negative-sided die!")
        if dice > "1":
            await ctx.send("Hey, you can't roll negative-sided dice!")
    else:
        sideList = []
        rollResults = []
        for side in range(sides):
            sideList.append(side + 1)
        for result in range(dice):
            rollResults.append(sideList[random.randint(0, sideList[-1])-1])
        total = sum(rollResults)
        if dice > 1:
            response = "You rolled `" + str(rollResults) + "`, totalling " + str(total)
        else:
            response = "You rolled " + str(total)
        await ctx.send(response)

@bot.command()
async def slap(ctx, members: commands.Greedy[discord.Member], *, reason="no reason"):
    slapped = ", ".join(x.name for x in members)
    await ctx.send(members)
    if slapped == " ":
        await ctx.send("{0} just got slapped by {1.author} for {2}".format(slapped, ctx, reason))
    else:
        await ctx.send("You can't just slap thin air!")
bot.run(TOKEN)
