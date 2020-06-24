# bot.py
import os
import re
import discord
import platform
from random import choice, randint
from discord.ext import commands
from dotenv import load_dotenv
from time import sleep

print("Starting...")

load_dotenv("../pengaelicbot.env")
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="p!")

try:
    with open(r"options.txt", "r") as optionsfile:
        censorToggle = bool(optionsfile.readlines()[0])
except FileNotFoundError:
    open(r"options.txt", "x").close()
    censorToggle = False

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
    dadprefixes = ["I'm ", "Im ", "I am "]
    if message.author.mention == "<@721092139953684580>" or message.author.mention == "<@503720029456695306>": # that's the ID for Dad Bot, this is to prevent conflict.
        return

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
    global censorToggle
    if censorToggle == True:
        with open(r"Bad words (Caution, NSFW).txt", "r") as bads_file:
            all_bads = bads_file.read().split(" ")
            for bad in range(len(all_bads)):
                if all_bads[bad] in message.content:
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


    # this section randomizes "yo mama" jokes lol
    mamatypes = ["fat", "stupid", "dumb", "short", "hairy", "ugly", "poor"]
    fatjokes = ["She doesn't need internet, she's already **W O R L D W I D E .**", "Half of her is in another dimension!", "She wakes up on BOTH sides of the bed!", "She got arrested for carrying ten pounds of CRACK!"]
    stupidjokes = ["She sold her car for *gas money.*", "When she heard it was \"chili\" outside, she went and got a bowl.", "She brought a giant spoon to the Super Bowl!", "She got tickets to XBOX LIVE."]
    shortjokes = ["She does backflips *under the bed,*", "When she smokes weed, she can't even get high!!"]
    hairyjokes = ["She shaves with a weedeater!", "She stars in Donkey Kong games!"]
    uglyjokes = ["When she played GTA V, she got an instant 5 stars! ...and then the cops ran away the moment they saw her.", "Her reflection said \"I quit.\"", "She wears a steak around her neck to get dogs to play with her.", "She makes *onions* cry!"]
    poorjokes = ["She runs after the garbage truck with a shopping list!", "She goes to KFC to lick people's fingers.", "The ducks throw bread at *her!*"]
    for mom in range(len(mamatypes)):
        if "Yo mama so " + mamatypes[mom] in message.content or "yo mama so " + mamatypes[mom] in message.content:
            if mamatypes[mom] == "fat":
                await message.channel.send(choice(fatjokes))
            if mamatypes[mom] == "stupid" or mamatypes[mom] == "dumb":
                await message.channel.send(choice(stupidjokes))
            if mamatypes[mom] == "short":
                await message.channel.send(choice(shortjokes))
            if mamatypes[mom] == "hairy":
                await message.channel.send(choice(hairyjokes))
            if mamatypes[mom] == "ugly":
                await message.channel.send(choice(uglyjokes))
            if mamatypes[mom] == "poor":
                await message.channel.send(choice(poorjokes))
                
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

    @commands.command(name="togglecensor", help="Toggle the automatic deletion of messages containing specific keywords.")
    async def togglecensor(self, ctx):
        global censorToggle
        if censorToggle == True:
            censorToggle = False
            await ctx.send("Censorship turned off.")
        elif censorToggle == False:
            censorToggle = True
            await ctx.send("Censorship turned on.")
        with open(r"options.txt", "w+") as optionsfile:
            optionsfile.write(str(censorToggle))

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
            for result in range(dice):
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
            for flip in range(int(str(coins))):
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
                for card in range(cards):
                    drawn.append(str(choice(allCards)))
        else:
            for card in range(cards):
                drawn.append(str(choice(values)) + " of " + choice(suits))
        await ctx.send("You drew " + str(drawn))

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
bot.add_cog(Messages(bot))
bot.add_cog(Converters(bot))
bot.add_cog(Games(bot))
bot.add_cog(Actions(bot))

bot.run(TOKEN)
