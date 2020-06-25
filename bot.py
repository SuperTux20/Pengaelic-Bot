# bot.py
print("Starting...")

import os
import re
import discord
import platform
from json import load, dump
from random import choice, randint
from discord.ext import commands
from dotenv import load_dotenv
from time import sleep

load_dotenv("../pengaelicbot.env")
TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix="p!")

try:
    with open(r"options.json", "r") as optionsfile:
        allOptions = load(optionsfile)
except:
    try:
        open(r"options.json", "x").close()
    except FileExistsError:
        pass
    allOptions = {"toggles": {"censor": True, "dad": False, "yoMama": True}}
    with open(r"options.json", "w") as optionsfile:
        dump(allOptions, optionsfile, sort_keys=True, indent=4)

try:
    open(r"Bad words (Caution, NSFW).txt", "x").close()
except FileExistsError:
    pass

@bot.event
async def on_ready():
    print("Connected!")
    artist = choice(["Tux Penguin", "Qumu", "Robotic Wisp", "xGravity", "Nick Nitro"])
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=artist))
    print("Status changed to \"Listening to " + artist + "\"")

@bot.event
async def on_message(message):
    global bot
    global allOptions
    if message.author.mention == "<@721092139953684580>" or message.author.mention == "<@503720029456695306>": # that's the ID for Dad Bot, this is to prevent conflict.
        return

    # this section is for Dad Bot-like responses
    if allOptions["toggles"]["dad"] == True:
        dadprefixes = ["I'm ", "Im ", "I am "]
        for dad in range(len(dadprefixes)):
            if dadprefixes[dad] in message.content or dadprefixes[dad].lower() in message.content:
                dadjoke = dadprefixes[dad]
                if dadprefixes[dad].lower() in message.content:
                    dadjoke = dadjoke.lower()
                if dadjoke[0] == message.content[0] and dadjoke[1] == message.content[1]:
                    if "Pengaelic Bot" in message.content or "Pengaelic bot" in message.content or "pengaelic bot" in message.content:
                        await message.channel.send("You're not the Pengaelic Bot, I am!")
                    else:
                        await message.channel.send("Hi " + message.content[len(dadjoke):] + ", I'm the Pengaelic Bot!")

    # this section is to auto-delete messages containing a keyword contained in the text file
    if allOptions["toggles"]["censor"] == True:
        with open(r"Bad words (Caution, NSFW).txt", "r") as bads_file:
            all_bads = bads_file.read().split(" ")
            for bad in range(len(all_bads)):
                if all_bads[bad] in message.content or all_bads[bad].lower() in message.content:
                    await message.delete()

    # this section reprimands people when they're rude to the bots
    insults = ["Your mother was a calculator and your dad ran on Windows Vista", "fuck you", "screw you", "stfu", "shut up"]
    bots = ["MEE6", "Mantaro", "Dyno", "Nadeko", "Dad Bot"]
    for insult in range(len(insults)):
        if insults[insult] in message.content:
            if "pengaelicbot" in message.content or "pengaelic bot" in message.content or "Pengaelic bot" in message.content or "Pengaelic Bot" in message.content:
                await message.channel.send(choice([";-;", ":sob:", ":cry:"]))
            else:
                for bot in range(len(bots)):
                    if bots[bot] in message.content or bots[bot].lower() in message.content:
                        defenseP1 = ["Hey", "Dude", "Whoa"]
                        defenseP2 = ["be nice to " + bots[bot], "be nice", "chill out"]
                        defenseP3 = ["its job", "what it was told", "what it's supposed to"]
                        await message.channel.send(choice(defenseP1) + ", " + choice(defenseP2) + ", it's only doing " + choice(defenseP3) + "!")


    # this section randomizes yo mama jokes
    if allOptions["toggles"]["yoMama"] == True:
        mamatypes = ["fat", "stupid", "short", "hairy", "ugly", "poor"]
        failedtypes = []
        with open(r"Yo Mama Jokes.json", "r") as AllTheJokes:
            jokes = load(AllTheJokes)
        for mom in range(len(mamatypes)):
            if "Yo mama so " in message.content or "yo mama so " in message.content:
                if mamatypes[mom] in message.content or mamatypes[mom] in message.content:
                    await message.channel.send(choice(jokes[mamatypes[mom]]))
                else:
                    failedtypes.append(mamatypes[mom])
        if failedtypes == mamatypes:
            mamatype = choice(mamatypes)
            await message.channel.send("Invalid Yo Mama type detected... Sending a " + mamatype + " joke.")
            await message.channel.send(choice(jokes[mamatype]))
                
    # this lets all the commands below work as normal
    await bot.process_commands(message)

class Misc(commands.Cog):
    @commands.command(name="os", help="Read out what OS I'm running on!")
    async def showos(self, ctx):
        defaultmsg = "I'm running on " + platform.system() + " "
        if platform.release() == "10":
            await ctx.send(defaultmsg + platform.version())
        else:
            await ctx.send(defaultmsg + platform.release() + " " + platform.version())

class Options(commands.Cog):
    async def updateoptions(self):
        global allOptions
        with open(r"options.json", "w+") as optionsfile:
            dump(allOptions, optionsfile, sort_keys=True, indent=4)

    @commands.command(name="options", help="Show a list of all options.")
    async def showoptions(self, ctx):
        global allOptions
        with open(r"options.json", "r") as optionsfile:
            await ctx.send("```" + f"{str(optionsfile.read())}" + "```")

    @commands.command(name="resetdefaults", help="Reset to the default options.")
    async def resetoptions(self, ctx):
        global allOptions
        allOptions = {"toggles": {"censor": True, "dad": False, "yoMama": True}}
        await self.updateoptions()
        await ctx.send("Options reset to defaults.")
        await self.showoptions(ctx)

    @commands.command(name="togglecensor", help="Toggle the automatic deletion of messages containing specific keywords.")
    async def togglecensor(self, ctx):
        global allOptions
        if allOptions["toggles"]["censor"] == True:
            allOptions["toggles"]["censor"] = False
            await ctx.send("Censorship turned off.")
        elif allOptions["toggles"]["censor"] == False:
            allOptions["toggles"]["censor"] = True
            await ctx.send("Censorship turned on.")
        await self.updateoptions()

    @commands.command(name="toggledad", help="Toggle the automatic Dad Bot-like responses to messages starting with \"I'm\"")
    async def toggledad(self, ctx):
        global allOptions
        if allOptions["toggles"]["dad"] == True:
            allOptions["toggles"]["dad"] = False
            await ctx.send("Bye p!toggledad, I'm the Pengaelic Bot!")
        elif allOptions["toggles"]["dad"] == False:
            allOptions["toggles"]["dad"] = True
            await ctx.send("Hi p!toggledad, I'm the Pengaelic Bot!")
        await self.updateoptions()

    @commands.command(name="togglemama", help="Toggle the automatic Yo Mama jokes")
    async def togglemama(self, ctx):
        global allOptions
        if allOptions["toggles"]["yoMama"] == True:
            allOptions["toggles"]["yoMama"] = False
            await ctx.send("Yo Mama jokes turned off.")
        elif allOptions["toggles"]["yoMama"] == False:
            allOptions["toggles"]["yoMama"] = True
            await ctx.send("Yo Mama jokes turned on.")
        await self.updateoptions()

class Messages(commands.Cog):
    @commands.command(name="hi", help="You say hi, I greet you back!")
    async def say_hi_back(self, ctx, delete=None):
        await ctx.send(choice(["Hi, I'm the Pengaelic Bot!", "Heya!", "What's up?"]))
        if delete:
            await ctx.message.delete()

    @commands.command(name="bye", help="You say bye, I bid you farewell.")
    async def say_bye_back(self, ctx, delete=None):
        await ctx.send(choice(["See you next time!", "Bye!", "So long, Gay Bowser!"]))
        if delete:
            await ctx.message.delete()

    @commands.command(name="say", help="Make me say something!", pass_context=True)
    async def say_back(self, ctx, *, arg):
        await ctx.send(arg)
        await ctx.message.delete()

class Converters(commands.Cog):
    @commands.command(name="novowels", help="Remove all vowels from whatever text you put in.")
    async def vowelRemover(self, ctx, *, arg):
        vowels = "aeiouAEIOU"
        outputString = arg
        for vowel in range(len(vowels)):
                outputString = outputString.replace(vowels[vowel],"")
        await ctx.send(outputString.replace("  ", " ")) # fix doubled spaces

    @commands.command(name="owo", help="Convert whatever text into owo-speak... oh god why did i make this")
    async def owoConverter(self, ctx, *, arg):
        await ctx.send(arg.replace("l","w").replace("r","w") + " " + choice(["OwO","UwU","owo","uwu","ewe","O3O","U3U","o3o","u3u","^w^","nya~","rawr"]))
        await ctx.message.delete()

    @commands.command(name="beegtext", help="Convert text into regional indicator letters, the big blue ones.")
    async def embiggener(self, ctx, *, arg):
        alphabet = "QWERTYUIOPASDFGHJKLZXCVBNM ?!"
        textlist = []
        finaltext = ""
        for char in range(len(arg)):
            for letter in range(len(alphabet)):
                if alphabet[letter] == arg[char] or alphabet[letter].lower() == arg[char]:
                    if arg[char] == " ":
                        textlist.append("\n")
                    elif arg[char] == "!":
                        textlist.append(":exclamation: ")
                    elif arg[char] == "?":
                        textlist.append(":question: ")
                    else:
                        textlist.append(":regional_indicator_" + arg[char] + ": ")
        for beeg in range(len(textlist)):
            finaltext = finaltext + textlist[beeg]
        await ctx.send(finaltext)

class Games(commands.Cog):
    @commands.command(name="roll", help="Roll some dice!")
    async def rollem(self, ctx, dice: int=1, sides: int=6):
        if dice == 0:
            await ctx.send("You didn't roll any dice.")
        elif sides == 0:
            await ctx.send("You rolled thin air.")
        elif dice < 0:
            await ctx.send("You rolled NaN dice and got [REDACTED]")
        elif sides < 0:
            if dice == 1:
                await ctx.send("You rolled a [ERROR]-sided die and got `404`")
            if dice > 1:
                await ctx.send("You rolled " + str(dice) + " `err`-sided dice and got [NULL]")
        else:
            sideList = []
            rollResults = []
            for side in range(sides):
                sideList.append(side + 1)
            for _ in range(dice):
                rollResults.append(sideList[randint(0, sideList[-1])-1])
            total = sum(rollResults)
            if dice > 1:
                response = "You rolled " + str(rollResults[:-1])[1:-1] + ", and " + str(rollResults[-1]) + ", totalling " + str(total)
            else:
                response = "You rolled " + str(total)
            await ctx.send(response)

    @commands.command(name="flip", help="Flip some coins!")
    async def flipem(self, ctx, coins: int=1):
        results = []
        if coins == 1:
            await ctx.send("You flipped a " + choice(["head","tail"]))
        elif coins == 0:
            await ctx.send("You flicked your thumb in the air.")
        elif coins == -1:
            await ctx.send("You flipped a [REDACTED]")
        elif coins < -1:
            await ctx.semd("You flipped NaN heads and [ERROR] tails.")
        else:
            for _ in range(int(str(coins))):
                results.append(choice(["h","t"]))
            await ctx.send("You flipped " + str(results.count("h")) + " heads and " + str(results.count("t")) + " tails.")
            

    @commands.command(name="draw", help="Draw some cards!")
    async def drawem(self, ctx, cards: int=1, replaceCards: str="no"):
        suits = ['Diamonds', 'Spades', 'Hearts', 'Clubs']
        values = ['Ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King']
        allCards = []
        drawn = []
        if replaceCards == "no":
            for suit in range(len(suits)):
                for value in range(len(values)):
                    allCards.append(str(values[value]) + " of " + suits[suit])
            if cards == 52:
                await ctx.send("You picked up the entire deck. What was the point of that?")
                return
            elif cards > 52:
                await ctx.send("You can't draw more than the entire deck!")
                return
            else:
                for _ in range(cards):
                    drawn.append(str(choice(allCards)))
        else:
            for _ in range(cards):
                drawn.append(str(choice(values)) + " of " + choice(suits))
        await ctx.send("You drew " + str(drawn))

    @commands.command(name="pop", help="Get a sheet of bubble wrap! Click to pop.")
    async def summonsheet(self, ctx, width: int=5, height: int=5):
        if width == 1 and height == 1:
            await ctx.send(r"""```
 ____   ___  ____
|  _ \ / _ \|  _ \
| |_) | | | | |_) |
|  __/| |_| |  __/
|_|    \___/|_|
```""")
        else:
            sheet = ""
            for _ in range(height):
                row = ""
                for _ in range(width):
                    if width < 5 and height < 5:
                        if width == 2 and height == 2:
                            row = row + "||:regional_indicator_p: :regional_indicator_o: :regional_indicator_p:||"
                        else:
                            row = row + "||POP||"
                    else:
                        row = row + "||pop||"
                sheet = sheet + row + "\n"
            await ctx.send(sheet)

class Actions(commands.Cog):
    @commands.command(name="slap", help="Slap someone...?", command_category="Interactions")
    async def slap(self, ctx, slap: discord.User=""):
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
            await ctx.send(choice(selfresponses) + " :(")
        else:
            await ctx.send(choice(responses))
            if str(slap.id) == "721092139953684580":
                await ctx.send(choice(botresponses))

    @commands.command(name="hug", help="Give somebody a hug!")
    async def hug(self, ctx, hug: discord.User=""):
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
            await ctx.send(choice(selfresponses))
        else:
            await ctx.send(choice(responses))
            if str(hug.id) == "721092139953684580":
                await ctx.send(choice(botresponses))

    @commands.command(name="boop", help="Boop someone's nose :3")
    async def boop(self, ctx, boop: discord.User=""):
        booper = str(ctx.author.mention)
        try:
            booped = "<@" + str(boop.id) + ">"
        except:
            await ctx.send("You can't just boop thin air! (Unless you're booping a ghost?)")
            return
        responses = [booped + " just got booped by " + booper, booper + " booped " + booped, booper + " booped " + booped + "'s nose!", booper + " booped " + booped + " on the nose!"]
        selfresponses = ["You boop your own nose, I guess...? ", "You miss your nose and poke yourself in the eye. ", "Somehow, your hand clips through your nose and appears on the other side of your head. "]
        botresponses = ["<:happy:708534449310138379>", "<:uwu:708534448949559328>", "thaaanks :3"]
        if booped == "":
            await ctx.send("You can't just boop thin air! (Unless you're booping a ghost?)")
        elif boop == ctx.author:
            oops = choice(selfresponses)
            if oops == selfresponses[1]:
                await ctx.send(oops + choice(["Ouch", "Oops", "Whoops"]) + "!")
            else:
                await ctx.send(oops)
        else:
            await ctx.send(choice(responses))
            if str(boop.id) == "721092139953684580":
                await ctx.send(choice(botresponses))

    @commands.command(name="pat", help="Pat someone on the head!")
    async def pat(self, ctx, pat: discord.User="", *, bodypart="head"):
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
            await ctx.send(choice(responses))
            if str(pat.id) == "721092139953684580":
                await ctx.send(choice(botresponses))

bot.add_cog(Misc(bot))
bot.add_cog(Options(bot))
bot.add_cog(Messages(bot))
bot.add_cog(Converters(bot))
bot.add_cog(Games(bot))
bot.add_cog(Actions(bot))

try:
    bot.run(TOKEN)
except:
    print("Unable to connect to Discord. Check your internet connection!")