# bot.py
import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
from time import sleep

load_dotenv("../pengaelicbot.env")
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="p!")

try:
    open(r"Bad words to auto-delete.txt", "x").close()
except FileExistsError:
    pass

@bot.event
async def on_ready():
    print("Connected!")
    song = random.choice(["Pinballovania", "Zakarralovania", "Bone Travel", "Hall of the Mountain Dude (Pengaelic Remix)"]) # I made all these songs myself :D find me on SoundCloud @ Tux Penguin
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=song))
    print("Status changed to \"" + song + "\"")

@bot.event
async def on_message(message):
    dadprefixes = ["I'm ", "Im ", "i'm ", "im ", "I Am ", "I am ", "i am "]
    if message.author == bot.user or message.author.mention == "<@503720029456695306>": # that's the ID for Dad Bot, this is to prevent conflict.
        return

    for dad in range(len(dadprefixes)):
        if dadprefixes[dad] in message.content:
            await message.channel.send("Hi " + message.content[len(dadprefixes[dad]):] + ", I'm the Pengaelic Bot!")
            
    # this section is to auto-delete messages containing a keyword contained in the text file
    with open(r"Bad words to auto-delete.txt", "r") as bads_file:
        all_bads = bads_file.read().split(" ")
        for bad in range(len(all_bads)):
            if all_bads[bad] in message.content:
                await message.delete()

    # this lets all the commands below work as normal
    await bot.process_commands(message)

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
        await ctx.send("You didn't roll any dice.")
    elif sides == "0":
        if dice == "1":
            await ctx.send("Hey, you can't roll a zero-sided die!")
        if dice > "1":
            await ctx.send("Hey, you can't roll zero-sided dice!")
    elif dice < "0":
        await ctx.send("You rolled NaN dice and got [REDACTED]")
    elif sides < "0":
        if dice == "1":
            await ctx.send("You rolled a [ERROR]-sided die and got `404`")
        if dice > "1":
            await ctx.send("You rolled " + dice + " `err`-sided dice and got [NULL]")
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

@bot.command(name="slap", help="Slap someone...?", command_category="Interactions")
async def slap(ctx, slap: discord.User=""):
    slapper = str(ctx.author.mention)
    try:
        slapped = "<@" + str(slap.id) + ">"
    except:
        await ctx.send("You can't just slap thin air! (Unless you're slapping a ghost?)")
        return
    responses = [slapped + " just got slapped by " + slapper, slapper + " slapped " + slapped]
    selfresponses = ["Hey, you can't slap yourself!", "Please don't", "y tho"]
    botresponses = [";-;", "ow! ;-;", "ow!"]
    if slap == ctx.author:
        await ctx.send(random.choice(selfresponses) + " :(")
    else:
        await ctx.send(random.choice(responses))
        if str(slap.id) == "721092139953684580":
            await ctx.send(random.choice(botresponses))

@bot.command(name="hug", help="Give somebody a hug!")
async def hug(ctx, hug: discord.User=""):
    hugger = str(ctx.author.mention)
    try:
        hugged = "<@" + str(hug.id) + ">"
    except:
        await ctx.send("You can't just hug thin air! (Unless you're hugging a ghost?)")
        return
    responses = [hugged + " just got hugged by " + hugger, hugger + " hugged " + hugged, hugger + " gave a hug to " + hugged]
    selfresponses = ["You wrap your arms tightly around yourself.", "Reaching through the 4th dimension, you manage to give yourself a hug.", "You hug yourself, somehow."]
    botresponses = ["aww!", "thanks <:happy:708534449310138379>", "*gasp*"]
    if hug == ctx.author:
        await ctx.send(random.choice(selfresponses))
    else:
        await ctx.send(random.choice(responses))
        if str(hug.id) == "721092139953684580":
            await ctx.send(random.choice(botresponses))

@bot.command(name="boop", help="Boop someone's nose :3")
async def boop(ctx, boop: discord.User=""):
    booper = str(ctx.author.mention)
    try:
        booped = "<@" + str(boop.id) + ">"
    except:
        await ctx.send("You can't just boop thin air! (Unless you're booping a ghost?)")
        return
    responses = [booped + " just got booped by " + booper, booper + " booped " + booped, booper + " booped " + booped + "'s nose!"]
    selfresponses = ["You boop your own nose, I guess...? ", "You miss your nose and poke yourself in the eye. ", "Somehow, your hand clips through your nose and appears on the other side of your head. "]
    botresponses = ["<:happy:708534449310138379>", "<:uwu:708534448949559328>", "thaaanks :3"]
    if booped == "":
        await ctx.send("You can't just boop thin air! (Unless you're booping a ghost?)")
    elif boop == ctx.author:
        choice = random.choice(selfresponses)
        if choice == selfresponses[1]:
            await ctx.send(choice + random.choice(["Ouch", "Oops", "Whoops"]) + "!")
        else:
            await ctx.send(choice)
    else:
        await ctx.send(random.choice(responses))
        if str(boop.id) == "721092139953684580":
            await ctx.send(random.choice(botresponses))

@bot.command(name="pat", help="Pat someone on the head!")
async def pat(ctx, pat: discord.User="", *, bodypart="head"):
    patter = str(ctx.author.mention)
    try:
        patted = "<@" + str(pat.id) + ">"
    except:
        await ctx.send("You can't just pat thin air! (Unless you're patting a ghost?)")
        return
    responses = [patted + " just got patted on the " + bodypart + " by " + patter, patter + " patted " + patted + " on the " + bodypart + "."]
    botresponses = ["<:happy:708534449310138379>", "hehe", "aw, you're cute :3"]
    if pat == ctx.author:
        await ctx.send("You pat yourself on the " + bodypart + ".")
    else:
        await ctx.send(random.choice(responses))
        if str(pat.id) == "721092139953684580":
            await ctx.send(random.choice(botresponses))

bot.run(TOKEN)
