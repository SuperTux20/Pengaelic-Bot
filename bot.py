# bot.py
print("Starting...")

import os
import re
import fnmatch
import discord
import platform
from json import load, dump
from random import choice, randint
from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv
from asyncio import sleep
from time import sleep as staticsleep

load_dotenv("../pengaelicbot.env")
TOKEN = os.getenv("DISCORD_TOKEN")
client = commands.Bot(command_prefix="p!",case_insensitive=True,description="Pengaelic Bot commands")
# Even though I'm removing the default p!help command, I'm leaving the vestigial descriptions in the commands.
client.remove_command("help")

try:
    with open(r"../options.json", "r") as optionsfile:
        allOptions = load(optionsfile)
except:
    try:
        open(r"../options.json", "x").close()
    except FileExistsError:
        pass
    allOptions = {"toggles": {"censor": True, "dad": False, "yoMama": True}, "numbers": {"rudeness": 0}}
    with open(r"../options.json", "w") as optionsfile:
        dump(allOptions, optionsfile, sort_keys=True, indent=4)

try:
    open(r"Bad words (Caution, NSFW).txt", "x").close()
except FileExistsError:
    pass

@client.event
async def on_ready():
    print("Connected!")
    artist = choice(["Tux Penguin", "Qumu", "Robotic Wisp", "xGravity", "Nick Nitro"])
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=artist))
    print("Status changed to \"Listening to " + artist + "\"")

@client.event
async def on_guild_join(guild):
    welcomeEmbed = discord.Embed(title="Howdy fellas! I'm the Pengaelic Bot!", description="Type `p!help` for a list of commands.", color=32639)
    welcomeEmbed.set_thumbnail(url=client.user.avatar_url)
    allchannels = list(guild.text_channels)
    for channel in range(len(allchannels)):
        allchannels[channel] = str(allchannels[channel])
    generals = [channel for channel in allchannels if "general" in channel]
    for gen in range(len(generals)):
        if "2" in generals[gen]:
            generals.remove(generals[gen])
    if get(guild.text_channels, name="general"):
        await get(guild.text_channels, name="general").send(embed=welcomeEmbed)
    else:
        for channel in range(len(generals)):
            await get(guild.text_channels, name=generals[channel]).send(embed=welcomeEmbed)

@client.event
async def on_message(message):
    global client
    global allOptions
    if message.author.mention == "<@721092139953684580>" or message.author.mention == "<@503720029456695306>": # that's the ID for Dad Bot, this is to prevent conflict.
        return

    if message.content == "I want to see the list of all the servers the bot is in.":
        thelistofalltheserversthebotisin = await client.fetch_guilds(limit=150).flatten()
        await message.channel.send(thelistofalltheserversthebotisin)

    # this section is for Dad Bot-like responses
    if allOptions["toggles"]["dad"] == True:
        dadprefixes = ["I'm ", "Im ", "I am "]
        for dad in range(len(dadprefixes)):
            dadprefixes.append(dadprefixes[dad].lower())
        for dad in range(len(dadprefixes)):
            if dadprefixes[dad] == message.content[0:len(dadprefixes[dad])]:
                dadjoke = dadprefixes[dad]
                if dadprefixes[dad].lower() in message.content:
                    dadjoke = dadjoke.lower()
                if dadjoke[0] == message.content[0] and dadjoke[1] == message.content[1]:
                    if "Pengaelic Bot" in message.content or "Pengaelic bot" in message.content or "pengaelic bot" in message.content:
                        await message.channel.send("You're not the Pengaelic Bot, I am!")
                    else:
                        if dadprefixes[dad] + "a " == message.content[0:len(dadprefixes[dad])+2]:
                            await message.channel.send(f"Hi {message.content[len(dadjoke)+2:]}, I'm the Pengaelic Bot!")
                        else:
                            await message.channel.send(f"Hi {message.content[len(dadjoke):]}, I'm the Pengaelic Bot!")

    # this section is to auto-delete messages containing a keyword contained in the text file
    if allOptions["toggles"]["censor"] == True:
        with open(r"Bad words (Caution, NSFW).txt", "r") as bads_file:
            all_bads = bads_file.read().split(" ")
            for bad in range(len(all_bads)):
                if all_bads[bad] + " " in message.content or all_bads[bad].lower() + " " in message.content or " " + all_bads[bad] in message.content or " " + all_bads[bad].lower() in message.content or all_bads[bad] == message.content:
                    await message.delete()

    # this section reprimands people when they're rude to the bots, does not reprimand if rudeness level is above 1
    if allOptions["numbers"]["rudeness"] < 2:
        insults = ["Your mother was a calculator and your dad ran on Windows Vista", "Fuck you", "Screw you", "Stfu", "Shut up"]
        bots = [str(member)[:-5] for member in message.guild.members if member.bot is True]
        if "YAGPDB.xyz" in bots:
            bots.append("YAGPBD")
            bots.append("YAG")
        for insult in range(len(insults)):
            if insults[insult] in message.content or insults[insult].lower() in message.content:
                if "pengaelicbot" in message.content or "pengaelic bot" in message.content or "Pengaelic bot" in message.content or "Pengaelic Bot" in message.content:
                    await message.channel.send(choice([";-;", ":sob:", ":cry:"]))
                else:
                    for bot in range(len(bots)):
                        if bots[bot] in message.content or bots[bot].lower() in message.content:
                            defenseP1 = ["Hey", "Dude", "Whoa"]
                            defenseP2 = ["be nice to " + bots[bot], "be nice", "chill out"]
                            defenseP3 = ["its job", "what it was told", "what it's supposed to"]
                            await message.channel.send(f"{choice(defenseP1)}, {choice(defenseP2)}, it's only doing {choice(defenseP3)}!")

    # this section randomizes yo mama jokes, does not work if
    if allOptions["toggles"]["yoMama"] == True:
        with open(r"Yo Mama Jokes.json", "r") as AllTheJokes:
            jokes = load(AllTheJokes)
            mamatypes = list(jokes.keys())
        failedtypes = []
        for mom in range(len(mamatypes)):
            if "Yo mama so " == message.content[0:11] or "yo mama so " in message.content[0:11]:
                    if mamatypes[mom] in message.content:
                        if allOptions["numbers"]["rudeness"] > 1:
                            await message.channel.send(choice(jokes[mamatypes[mom]]))
                        else:
                            await message.channel.send("Yo Mama jokes are disabled: rudeness level below 2.")
                    else:
                        if "dumb" in message.content or "retarded" in message.content:
                                await message.channel.send(choice(jokes["stupid"]))
                        else:
                            failedtypes.append(mamatypes[mom])
            elif "Yo mama list" == message.content or "yo mama list" in message.content:
                if allOptions["numbers"]["rudeness"] > 1:
                    await message.channel.send(str(mamatypes)[1:-1].replace("'",""))
                else:
                    await message.channel.send("Yo Mama jokes are disabled: rudeness level below 2.")
                break
        if failedtypes == mamatypes:
            mamatype = choice(mamatypes)
            await message.channel.send(f"Invalid Yo Mama type detected... Sending a {mamatype} joke.")
            await message.channel.send("Yo mama so " + mamatype)
            await message.channel.send(choice(jokes[mamatype]))

    # this lets all the commands below work as normal
    await client.process_commands(message)

@client.event
async def on_reaction_add(reaction, user):
    if reaction.emoji == "👄":
        if user.id != 721092139953684580:
            if Actions.isNomming == True:
                Actions.isNomming = False
                Actions.nomSuccess = False

@client.event
async def on_command_error(ctx, error):
    if allOptions["numbers"]["rudeness"] < 3:
        if allOptions["numbers"]["rudeness"] == 0:
            invalidmsg = "Sorry, this command is invalid."
        elif allOptions["numbers"]["rudeness"] == 1:
            invalidmsg = "Invalid command/usage."
        elif allOptions["numbers"]["rudeness"] == 2:
            invalidmsg = "You typed the command wrong!"
        await ctx.send(invalidmsg + " Type `p!help` for a list of commands and their usages.")
    else:
        await ctx.send(file=discord.File("images/thatsnothowitworksyoulittleshit.jpg"))

class Tools(commands.Cog):
    purgeconfirm = False
    @commands.command(name="os", help="Read out what OS I'm running on!", aliases=["getos"])
    async def showos(self, ctx):
        defaultmsg = f"I'm running on {platform.system()} "
        if platform.release() == "10":
            await ctx.send(defaultmsg + platform.version())
        else:
            await ctx.send(defaultmsg + platform.release() + " " + platform.version())

    @commands.command(name="ping", help="How slow am I to respond?", aliases=["ng"])
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

    @commands.command(name="clear", help="Clear some messages away.")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx, msgcount: int=5):
        await ctx.channel.purge(limit=msgcount + 1)
        report = await ctx.send(str(msgcount) + " messages deleted.")
        await sleep(3)
        await report.delete()

    @clear.error
    async def clearError(self, ctx, error):
        await ctx.send(f"Sorry {ctx.author.mention}, you don't have the correct permissions! (Manage Messages)")

    @commands.command(name="purge", help="Purge a channel. :warning:WARNING:warning: This command clears an ENTIRE channel!")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def purge(self, ctx, msgcount: int=5):
        if self.purgeconfirm == False:
            await ctx.send("Are you **really** sure you want to wipe this channel? Type p!purge again to confirm.")
            self.purgeconfirm = True
        elif self.purgeconfirm == True:
            await ctx.channel.clone()
            await ctx.channel.delete()
            self.purgeconfirm = False

    @purge.error
    async def purgeError(self, ctx, error):
        await ctx.send(f"Sorry {ctx.author.mention}, you don't have the correct permissions! (Manage Channels)")

class Options(commands.Cog):
    async def updateoptions(self):
        global allOptions
        with open(r"../options.json", "w+") as optionsfile:
            dump(allOptions, optionsfile, sort_keys=True, indent=4)

    @commands.command(name="options", help="Show a list of all options.", aliases=["showoptions", "prefs", "config", "cfg"])
    async def showoptions(self, ctx):
        global allOptions
        with open(r"../options.json", "r") as optionsfile:
            await ctx.send("```" + f"{str(optionsfile.read())}" + "```")

    @commands.command(name="resetdefaults", help="Reset to the default options.", aliases=["defaultoptions", "reset"])
    async def resetoptions(self, ctx):
        global allOptions
        allOptions = {"toggles": {"censor": True, "dad": False, "yoMama": True}, "numbers": {"rudeness": 0}}
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

    @commands.command(name="toggledad", help="Toggle the automatic Dad Bot-like responses to messages starting with \"I'm\".")
    async def toggledad(self, ctx):
        global allOptions
        if allOptions["toggles"]["dad"] == True:
            allOptions["toggles"]["dad"] = False
            await ctx.send("Bye p!toggledad, I'm the Pengaelic Bot!")
        elif allOptions["toggles"]["dad"] == False:
            allOptions["toggles"]["dad"] = True
            await ctx.send("Hi p!toggledad, I'm the Pengaelic Bot!")
        await self.updateoptions()

    @commands.command(name="togglemama", help="Toggle the automatic Yo Mama jokes.")
    async def togglemama(self, ctx):
        global allOptions
        if allOptions["toggles"]["yoMama"] == True:
            allOptions["toggles"]["yoMama"] = False
            await ctx.send("Yo Mama jokes turned off.")
        elif allOptions["toggles"]["yoMama"] == False:
            allOptions["toggles"]["yoMama"] = True
            await ctx.send("Yo Mama jokes turned on.")
        await self.updateoptions()

    @commands.command(name="rudenesslevel", help="Change how rude the bot can be.")
    async def rudenesslevel(self, ctx, level: int):
        global allOptions
        allOptions["numbers"]["rudeness"] = level
        await ctx.send("Rudeness level set to " + str(level))
        await self.updateoptions()

class Messages(commands.Cog):
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

class Converters(commands.Cog):
    @commands.command(name="novowels", help="Remove all vowels from whatever text you put in.", aliases=["vowelremover", "removevowels"])
    async def vowelRemover(self, ctx, *, arg):
        vowels = "aeiouAEIOU"
        outputString = arg
        for vowel in range(len(vowels)):
                outputString = outputString.replace(vowels[vowel],"")
        await ctx.send(outputString.replace("  ", " ")) # fix doubled spaces

    @commands.command(name="owo", help="Convert whatever text into owo-speak... oh god why did i make this", aliases=["furry"])
    async def owoConverter(self, ctx, *, arg):
        await ctx.send(arg.replace("l","w").replace("r","w") + " " + choice(["OwO","UwU","owo","uwu","ewe","O3O","U3U","o3o","u3u","^w^","nya~","rawr"]))
        await ctx.message.delete()

    @commands.command(name="beegtext", help="Convert text into regional indicator letters, the big blue ones.", aliases=["bigtext", "big", "beeg"])
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
                        textlist.append(":regional_indicator_" + arg[char].lower() + ": ")
        for beeg in range(len(textlist)):
            finaltext = finaltext + textlist[beeg]
        await ctx.send(finaltext)

class Games(commands.Cog):
    @commands.command(name="8ball", help="Ask the ball a yes-or-no question!", aliases=["magic8ball"])
    async def _8ball(self, ctx, *, question = None):
        global allOptions
        with open(rf"8ball_level_{allOptions['numbers']['rudeness']}.txt", "r") as responsefile:
            ballResponses = responsefile.read().split(", ")
        if question:
            await ctx.send(":8ball:" + choice(ballResponses))
        else:
            await ctx.send(":8ball:You didn't ask the 8-ball anything.")

    @commands.command(name="roll", help="Roll some dice!", aliases=["dice", "rolldice", "diceroll"])
    async def rollem(self, ctx, dice: int=1, sides: int=6):
        if dice == 0:
            await ctx.send(":game_die:You didn't roll any dice.")
        elif sides == 0:
            await ctx.send(":game_die:You rolled thin air.")
        elif dice < 0:
            await ctx.send(":game_die:You rolled NaN dice and got [REDACTED]")
        elif sides < 0:
            if dice == 1:
                await ctx.send(":game_die:You rolled a [ERROR]-sided die and got `DivideByZeroError`")
            if dice > 1:
                await ctx.sendf(f":game_die:You rolled {dice} `err`-sided dice and got [NULL]")
        else:
            sideList = []
            rollResults = []
            for side in range(sides):
                sideList.append(side + 1)
            for _ in range(dice):
                rollResults.append(sideList[randint(0, sideList[-1])-1])
            total = sum(rollResults)
            if dice > 1:
                response = f":game_die:You rolled {str(rollResults[:-1])[1:-1]}, and {rollResults[-1]}, totalling {total}"
            else:
                response = f":game_die:You rolled {total}"
            await ctx.send(response)

    @commands.command(name="flip", help="Flip some coins!", aliases=["coin", "coinflip", "coins", "flipcoin", "flipcoins"])
    async def flipem(self, ctx, coins: int=1):
        results = []
        if coins == 1:
            await ctx.send(f":moneybag:You flipped a {choice(['head','tail'])}")
        elif coins == 0:
            await ctx.send(":moneybag:You flicked your thumb in the air.")
        elif coins == -1:
            await ctx.send(":moneybag:You flipped a [REDACTED]")
        elif coins < -1:
            await ctx.semd(":moneybag:You flipped NaN heads and [ERROR] tails.")
        else:
            if coins > 1000000:
                await ctx.send(f":moneybag:{coins} coins? That's just silly.")
            else:
                for _ in range(int(str(coins))):
                    result = randint(0,2)
                    if result == 2:
                        result = randint(0,2)
                        if result == 2:
                            result = randint(0,2)
                            if result == 2:
                                result = randint(0,2)
                                if result == 2:
                                    result = randint(0,2)
                                    if result == 2:
                                        result = randint(0,2)
                    results.append(result)
                if results.count(2) > 0:
                    if results.count(2) == 1:
                        await ctx.send(f":moneybag:You flipped {results.count(0)} heads and {results.count(1)} tails, and a coin even landed on its edge.")
                    else:
                        await ctx.send(f":moneybag:You flipped {results.count(0)} heads and {results.count(1)} tails, and {results.count(2)} coins landed on their edges.")
                else:
                    await ctx.send(f":moneybag:You flipped {results.count(0)} heads and {results.count(1)} tails.")

    @commands.command(name="draw", help="Draw some cards!", aliases=["drawcard", "drawcards", "card", "cards"])
    async def drawem(self, ctx, cards: int=1, replaceCards: str="no"):
        suits = ["Diamonds", "Spades", "Hearts", "Clubs"]
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        allCards = []
        faces = []
        nums = []
        drawn = []
        if replaceCards == "no":
            for suit in range(int(len(suits)/1)):
                for value in range(len(values)):
                    if values[value] == 10:
                        length = 2
                    elif values[value] == 1:
                        length = 3
                    elif values[value] == 11 or values[value] == 13:
                        length = 4
                    elif values[value] == 12:
                        length = 5
                    else:
                        length = 1
                    allCards.append(str(values[value]) + (" " * (6 - length) + "of ") + suits[suit])
            if cards > 52:
                await ctx.send(":black_joker:You can't draw more than the entire deck!")
                return
            elif cards == 52:
                await ctx.send(":black_joker:You picked up the entire deck. What was the point of that?")
                return
            else:
                for _ in range(cards):
                    card = choice(allCards)
                    if card[1] == "0" or card[1] == "1" or card[1] == "2" or card[1] == "3":
                        faces.append(card)
                    else:
                        nums.append(card)
                    allCards.remove(card)
                faces = sorted(faces, reverse=True)
                nums = sorted(nums, reverse=True)
                drawn = faces + nums
        else:
            for _ in range(cards):
                chosenValue = str(choice(values))
                card = str(chosenValue + (" " * (len(chosenValue) - 6) + "of ") + choice(suits))
                if card[1] == "0" or card[1] == "1" or card[1] == "2" or card[1] == "3":
                    faces.append(card)
                else:
                    nums.append(card)
            faces = sorted(faces, reverse=True)
            nums = sorted(nums, reverse=True)
            drawn = faces + nums
        for card in range(len(drawn)):
            drawn[card] = drawn[card].replace("11","Jack").replace("12","Queen").replace("13","King").replace("1 ", "Ace ")
        if cards == 1:
            while "  " in drawn[0]:
                drawn[0] = drawn[0].replace("  "," ")
            await ctx.send(":black_joker:You drew " + drawn[0])
        else:
            await ctx.send(":black_joker:You drew...```" + str(drawn)[1:-1].replace("'","").replace(", ","\n") + "```")

    @commands.command(name="pop", help="Get a sheet of bubble wrap! Click to pop.", aliases=["bubblewrap", "bubble", "wrap" "bubbles"])
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
    isNomming = True
    nomSuccess = False
    global allOptions
    @commands.command(name="slap", help="Slap someone...?")
    async def slap(self, ctx, slap: discord.User=""):
        if allOptions["counters"]["rudeness"] == 0:
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
        else:
            await ctx.send("Slapping is disabled: Rudeness level is 0")

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

    """@commands.command(name="nom", help="Give someone a good nom >:3")
    async def nom(self, ctx, nom: discord.User=""):
        nommer = str(ctx.author.mention)
        try:
            nommed = "<@" + str(nom.id) + ">"
        except:
            await ctx.send("You can't just nom thin air! (Unless you're nomming a ghost?)")
            return
        responses = [nommed + " just got nommed by " + nommer, nommer + " nommed " + nommed, nommer + " ate " + nommed]
        selfresponses = ["You eat yourself and create a black hole. Thanks a lot.", "You chew on your finger. Why...?", "Uh..."]
        botresponses = ["mmmph!", "mmmmmmmmph!", "mmmmmnnnn!!"]
        if nom == ctx.author:
            await ctx.send(choice(selfresponses))
        else:
            if str(nom.id) == "721092139953684580":
                await ctx.send(choice(responses))
                await ctx.send(choice(botresponses))
            else:
                Actions.isNomming = True
                Actions.nomSuccess = False
                NoNomSense = await ctx.send(f"{nommer} is trying to eat you, {nommed}! Quick, react to get away!")
                await NoNomSense.add_reaction("👄")
                for i in range(5):
                    staticsleep(1)
                    print(i)
                    if Actions.isNomming == False:
                        await ctx.send("loop broken")
                        break
                if Actions.isNomming == True:
                    await ctx.send("success undetermined")
                    Actions.isNomming = False
                    Actions.nomSuccess = True
                if Actions.nomSuccess == True:
                    # await ctx.send(choice(responses))
                    await ctx.send("success successful")
                else:
                    # await ctx.send(nommed + " got away!")
                    await ctx.send("success unsuccessful")"""

    @commands.command(name="tickle", help="Tickle tickle tickle... >:D")
    async def tickle(self, ctx, tickle: discord.User=""):
        tickler = str(ctx.author.mention)
        try:
            tickled = "<@" + str(tickle.id) + ">"
        except:
            await ctx.send("You can't just tickle thin air! (Unless you're tickling a ghost?)")
            return
        responses = [tickled + " just got tickled by " + tickler, tickler + " tickled " + tickled]
        selfresponses = ["You try to tickle yourself, but your body reflexively flinches away.", "You tickle yourself, and you burst out laughing the moment your finger touches that sweet spot of ticklishness..", "You try to tickle yourself, but nothing happens."]
        botresponses = ["hahahahahahahaha", "eeeeeehahahahaha", "aaaaaahahahahahaahaSTAHPhahahaha"]
        if tickle == ctx.author:
            await ctx.send(choice(selfresponses))
        else:
            await ctx.send(choice(responses))
            if str(tickle.id) == "721092139953684580":
                await ctx.send(choice(botresponses))

@client.command(name="help", help="Show this message")
async def help(ctx, selectedCategory=None):
    cyan = 32639
    if not selectedCategory:
        rootHelpMenu = discord.Embed(title="Pengaelic Bot", description="Type `p!help <category name>` for a list of commands.", color=cyan)
        rootHelpMenu.add_field(name="Actions", value="Interact with other server members!")
        rootHelpMenu.add_field(name="Converters", value="Run some text through a converter to make it look funny!")
        rootHelpMenu.add_field(name="Games", value="All sorts of fun stuff!")
        rootHelpMenu.add_field(name="Messages", value="Make the bot say things!")
        rootHelpMenu.add_field(name="Options", value="Settings for the bot. (WIP but functional)")
        rootHelpMenu.add_field(name="Tools", value="Various tools and info.")
        rootHelpMenu.add_field(name="Non-commands", value="Automatic message responses that aren't commands.")
        rootHelpMenu.set_footer(text="Command prefix: `p!`")
        await ctx.send(content=None, embed=rootHelpMenu)
    else:
        if selectedCategory == "Actions" or selectedCategory == "actions":
            helpMenu = discord.Embed(title="Actions", description="Interact with other server members!", color=cyan)
            helpMenu.add_field(name="boop <@mention>", value="Boop someone's nose :3")
            helpMenu.add_field(name="hug <@mention>", value="Give somebody a hug!")
            helpMenu.add_field(name="nom <@mention>", value="Command temporarily disabled: haven't gotten reactions to work right :(")
            helpMenu.add_field(name="pat <@mention>", value="Pat someone on the head -w-")
            helpMenu.add_field(name="slap <@mention>", value="Slap someone...?")
            helpMenu.add_field(name="tickle <@mention>", value="Tickle tickle tickle... >:D")
        if selectedCategory == "Converters" or selectedCategory == "converters":
            helpMenu = discord.Embed(title="Converters", description="Run some text through a converter to make it look funny!", color=cyan)
            helpMenu.add_field(name="novowels\n<input string>", value="Remove all vowels from whatever text you put in.")
            helpMenu.add_field(name="owo\n<input string>", value="Convert whatever text into owo-speak... oh god why did i make this")
            helpMenu.add_field(name="beegtext\nbigtext\nbeeg\nbig\n<input string>", value="Turn text into\n:regional_indicator_b: :regional_indicator_e: :regional_indicator_e: :regional_indicator_g:\n:regional_indicator_t: :regional_indicator_e: :regional_indicator_x: :regional_indicator_t: :exclamation:")
        if selectedCategory == "Games" or selectedCategory == "games":
            helpMenu = discord.Embed(title="Games", description="All sorts of fun stuff!", color=cyan)
            helpMenu.add_field(name="8ball\n[question]", value="Ask the ball a yes-or-no question, and it shall respond...")
            helpMenu.add_field(name="pop\nbubblewrap\n[width of sheet (5)]\n[height of sheet (5)]", value="Pop some bubble wrap!")
            helpMenu.add_field(name="draw\ncard\n[number of cards (1)]\n[replace cards? yes/no (no)]", value="Draw some cards!")
            helpMenu.add_field(name="flip\ncoin\n[number of coins (1)]", value="Flip some coins!")
            helpMenu.add_field(name="roll\ndice\n[number of dice (1)]\n[number of sides (6)]", value="Roll some dice!")
        if selectedCategory == "Messages" or selectedCategory == "messages":
            helpMenu = discord.Embed(title="Messages", description="M a k e   m e   s a y   t h i n g s", color=cyan)
            helpMenu.add_field(name="hi\nhello\nsup\n[delete your command message?]", value="You say hi, I greet you back!")
            helpMenu.add_field(name="bye\ncya\ngoodbye\n[delete your command message?]", value="You say bye, I bid you farewell.")
            helpMenu.add_field(name="say\nrepeat\nparrot\n<input string>", value="Make me say whatever you say, and I might die inside in the process.")
        if selectedCategory == "Options" or selectedCategory == "options":
            helpMenu = discord.Embed(title="Options", description="Settings for the bot. (I need to figure out how to make them different on different servers :grimacing:)", color=cyan)
            helpMenu.add_field(name="options\nconfig\nprefs\ncfg", value="Show a list of all options.")
            helpMenu.add_field(name="resetdefaults\ndefaultoptions\nreset", value="Reset all options to their defaults.")
            helpMenu.add_field(name="togglecensor", value="Toggle the automatic deletion of messages containing specific keywords.")
            helpMenu.add_field(name="toggledad", value="Toggle the automatic Dad Bot-like responses to messages starting with \"I'm\".")
            helpMenu.add_field(name="togglemama", value="Toggle the automatic Yo Mama jokes.")
            helpMenu.add_field(name="rudenesslevel <value from 0 to 3>", value="Set how rude the bot can be, and open up more commands.")
        if selectedCategory == "Tools" or selectedCategory == "tools":
            helpMenu = discord.Embed(title="Tools", description="Various tools and info.", color=cyan)
            helpMenu.add_field(name="os\ngetos", value="Read out what OS I'm running on!")
            helpMenu.add_field(name="ping\nng", value="How slow am I to respond?")
            helpMenu.add_field(name="clear [number of messages]", value="Clear away some messages. (Requires Manage Messages permission)")
            helpMenu.add_field(name="purge", value="Clear an entire channel. (Requires Manage Channels permission)")
            helpMenu.add_field(name="help [category]", value="Show the message from earlier!")
        if selectedCategory == "Non-commands" or selectedCategory == "Non-Commands" or selectedCategory == "non-commands" or selectedCategory == "noncommands" or selectedCategory == "Noncommands" or selectedCategory == "NonCommands":
            helpMenu = discord.Embed(title="Non-commands", description="Automatic message responses that aren't commands.", color=cyan)
            helpMenu.add_field(name="I'm <message>", value="It's like Dad Bot. 'Nuff said.")
            helpMenu.add_field(name="Yo mama so <mama type>", value="Automatic Yo Mama jokes!")
            helpMenu.add_field(name="Yo mama list", value="Show the list of mama types to use in the auto-joker.")
        helpMenu.set_footer(text="Command prefix is `p!`, <arg> = required, [arg] = optional, [arg (value)] = default option")
        await ctx.send(content=None, embed=helpMenu)

client.add_cog(Tools(client))
client.add_cog(Options(client))
client.add_cog(Messages(client))
client.add_cog(Converters(client))
client.add_cog(Games(client))
client.add_cog(Actions(client))

while True:
    client.run(TOKEN)