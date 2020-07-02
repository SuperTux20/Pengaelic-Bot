# bot.py
import os
import discord
from json import load, dump
from random import choice
from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv

print("Starting")

load_dotenv("../pengaelicbot.data/.env")
TOKEN = os.getenv("DISCORD_TOKEN")
errorAlreadyHandled = False
# even though I'm removing the default p!help command, I'm leaving the vestigial descriptions in the commands
client = commands.Bot(command_prefix="p!",case_insensitive=True,description="Pengaelic Bot commands", help_command=None)
wipecensorconfirm = False

@client.event
async def on_ready():
    print("Connected")
    artist = choice(["Tux Penguin", "Qumu", "Robotic Wisp", "xGravity", "Nick Nitro", "ynk", "KEDD", "Jesse Cook", "musical rock", "SharaX"])
    game = choice(["Minecraft", "OpenRA", "3D Pinball: Space Cadet", "SuperTux", "Project Muse", "Shattered Pixel Dungeon", "Super Hexagon", "osu!", "AstroMenace", "Space Pirates and Zombies"])
    youtuber = choice(["Ethoslab", "MumboJumbo", "Blue Television Games", "The King of Random", "Phoenix SC"])
    movie = choice(["Avengers: Endgame", "Avengers: Infinity War", "Star Wars: A New Hope", "Spiderman: Into the Spiderverse", "Back to the Future"])
    activity = choice([discord.Activity(type=discord.ActivityType.listening, name=artist), discord.Game(name=game), discord.Activity(type=discord.ActivityType.watching, name=choice([youtuber, movie]))])
    await client.change_presence(activity=activity)
    print("Status updated")
    for guild in range(len(client.guilds)):
        # try to read the options file
        try:
            with open(rf"../pengaelicbot.data/configs/{client.guilds[guild].id}.json", "r") as optionsfile:
                allOptions = load(optionsfile)
                print("Options file loaded for " + str(client.guilds[guild].name))
        # if something goes wrong...
        except:
            # ...try creating it
                try:
                    open(rf"../pengaelicbot.data/configs/{client.guilds[guild].id}.json", "x").close()
                except FileExistsError:
                    pass
                with open(r"default_options.json", "r") as defaultsfile:
                    allOptions = load(defaultsfile)
                with open(rf"../pengaelicbot.data/configs/{client.guilds[guild].id}.json", "w") as optionsfile:
                    dump(allOptions, optionsfile, sort_keys=True, indent=4)
                print("Options file created for " + str(client.guilds[guild].name))

@client.event
async def on_guild_join(guild):
    print("Joined " + str(guild.name))
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

    # create fresh options file for new server
    open(rf"../pengaelicbot.data/configs/{guild.id}.json", "x").close()
    with open(r"default_options.json", "r") as defaultsfile:
        allOptions = load(defaultsfile)
    with open(rf"../pengaelicbot.data/configs/{guild.id}.json", "w") as optionsfile:
        dump(allOptions, optionsfile, sort_keys=True, indent=4)
    print("Options file created for " + str(guild.name))

@client.event
async def on_message(message):
    with open(rf"../pengaelicbot.data/configs/{message.guild.id}.json", "r") as optionsfile:
        allOptions = load(optionsfile)
    global client
    if message.author.mention == "<@721092139953684580>" or message.author.mention == "<@503720029456695306>": # that's the ID for Dad Bot, this is to prevent conflict.
        return

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
        try:
            open(rf"../pengaelicbot.data/censorfilters/{message.guild.id}.txt", "x").close()
            print("Censor file created for " + str(message.guild.name))
        except FileExistsError:
            pass
        with open(rf"../pengaelicbot.data/censorfilters/{message.guild.id}.txt", "r") as bads_file:
            all_bads = bads_file.read().split(", ")
            if all_bads == [""]:
                pass
            else:
                for bad in range(len(all_bads)):
                    if all_bads[bad] in message.content or all_bads[bad].lower() in message.content or all_bads[bad] == message.content:
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
            await message.channel.send(f"Yo mama so {mamatype}")

    # this lets all the commands below work as normal
    await client.process_commands(message)

@client.event
async def on_command_error(ctx, error):
    with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
        allOptions = load(optionsfile)
    if errorAlreadyHandled == False:
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

async def updateoptions(guild_id, options2dump):
    with open(rf"../pengaelicbot.data/configs/{guild_id}.json", "w+") as optionsfile:
        dump(options2dump, optionsfile, sort_keys=True, indent=4)

@client.command(name="resetdefaults", help="Reset to the default options.", aliases=["defaultoptions", "reset"])
@commands.has_permissions(kick_members=True)
async def resetoptions(ctx):
    with open(r"default_options.json", "r") as defaultoptions:
        await updateoptions(ctx.guild.id, load(defaultoptions))
        await ctx.send("Options reset to defaults.")
        await ctx.send(defaultoptions.read())

@client.command(name="togglecensor", help="Toggle the automatic deletion of messages containing specific keywords.")
@commands.has_permissions(kick_members=True)
async def togglecensor(ctx):
    with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
        allOptions = load(optionsfile)
    if allOptions["toggles"]["censor"] == True:
        allOptions["toggles"]["censor"] = False
        await ctx.send("Censorship turned off.")
    elif allOptions["toggles"]["censor"] == False:
        allOptions["toggles"]["censor"] = True
        await ctx.send("Censorship turned on.")
    await updateoptions(ctx.guild.id, allOptions)

@client.command(name="toggledad", help="Toggle the automatic Dad Bot-like responses to messages starting with \"I'm\".")
@commands.has_permissions(kick_members=True)
async def toggledad(ctx):
    with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
        allOptions = load(optionsfile)
    if allOptions["toggles"]["dad"] == True:
        allOptions["toggles"]["dad"] = False
        await ctx.send("Bye p!toggledad, I'm the Pengaelic Bot!")
    elif allOptions["toggles"]["dad"] == False:
        allOptions["toggles"]["dad"] = True
        await ctx.send("Hi p!toggledad, I'm the Pengaelic Bot!")
    await updateoptions(ctx.guild.id, allOptions)

@client.command(name="togglemama", help="Toggle the automatic Yo Mama jokes.")
@commands.has_permissions(kick_members=True)
async def togglemama(ctx):
    with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
        allOptions = load(optionsfile)
    if allOptions["toggles"]["yoMama"] == True:
        allOptions["toggles"]["yoMama"] = False
        await ctx.send("Yo Mama jokes turned off.")
    elif allOptions["toggles"]["yoMama"] == False:
        allOptions["toggles"]["yoMama"] = True
        await ctx.send("Yo Mama jokes turned on.")
    await updateoptions(ctx.guild.id, allOptions)

@client.command(name="rudenesslevel", help="Change how rude the bot can be.", aliases=["rudeness"])
@commands.has_permissions(manage_messages=True)
async def rudenesslevel(ctx, level: int=-1):
    with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
        allOptions = load(optionsfile)
    if level == -1:
        await ctx.send("Current rudeness level is " + str(allOptions["numbers"]["rudeness"]))
    else:
        if level < 0:
            await ctx.send("Wait- What would negative rudeness even mean?")
        else:
            if level > 3:
                await ctx.send("Sorry pal, 3 is the highest it can go.")
                allOptions["numbers"]["rudeness"] = 3
                await ctx.send("Rudeness level set to 3")
                await updateoptions(ctx.guild.id, allOptions)
            else:
                allOptions["numbers"]["rudeness"] = level
                await ctx.send("Rudeness level set to " + str(level))
                await updateoptions(ctx.guild.id, allOptions)

@client.command(name="showcensor", help="Display the contents of the censorship filter.", aliases=["showfilter", "getcensor", "getfilter", "censorlist", "filterlist"])
@commands.has_permissions(manage_messages=True)
async def showfilter(ctx):
    with open(rf"../pengaelicbot.data/censorfilters/{ctx.guild.id}.txt", "r") as bads_file:
        all_bads = bads_file.read()
        if all_bads.split(', ') == ['']:
            await ctx.send("Filter is empty.")
        else:
            await ctx.send(f"```{str(all_bads)}```")

@client.command(name="addcensor", help="Add a word to the censorship filter.", aliases=["addfilter"])
@commands.has_permissions(manage_messages=True)
async def addfilter(ctx, word2add):
    with open(rf"../pengaelicbot.data/censorfilters/{ctx.guild.id}.txt", "r") as bads_file:
        all_bads = bads_file.read()
        oneword = []
        if ", " in all_bads:
            all_bads = all_bads.split(", ")
        else:
            oneword.append(all_bads)
            all_bads = oneword
        if all_bads == [""]:
            all_bads = []
        if word2add in all_bads:
            await ctx.send("That word is already in the filter.")
        else:
            all_bads.append(word2add)
            all_bads.sort()
            finalbads = str(all_bads)[1:-1].replace("'","")
            with open(rf"../pengaelicbot.data/censorfilters/{ctx.guild.id}.txt", "w") as bads_file_to:
                bads_file_to.write(finalbads)
                await ctx.send("Word added to the filter.")

@client.command(name="delcensor", help="Remove a word from the censorship filter.", aliases=["delfilter"])
@commands.has_permissions(manage_messages=True)
async def delfilter(ctx, word2del):
    with open(rf"../pengaelicbot.data/censorfilters/{ctx.guild.id}.txt", "r") as bads_file:
        all_bads = bads_file.read()
        oneword = []
        if ", " in all_bads:
            all_bads = all_bads.split(", ")
        else:
            oneword.append(all_bads)
            all_bads = oneword
        if all_bads == [""]:
            all_bads = []
        if word2del not in all_bads:
            await ctx.send("That word is not in the filter.")
        else:
            all_bads.remove(word2del)
            all_bads.sort()
            finalbads = str(all_bads)[1:-1].replace("'","")
            with open(rf"../pengaelicbot.data/censorfilters/{ctx.guild.id}.txt", "w") as bads_file_to:
                bads_file_to.write(finalbads)
                await ctx.send("Word removed from the filter.")

@client.command(name="wipecensor", help="Clear the censor file.", aliases=["wipefilter", "clearcensor", "clearfilter"])
@commands.has_permissions(manage_messages=True)
async def wipefilter(ctx):
    global wipecensorconfirm
    if wipecensorconfirm == False:
        await ctx.send("Are you **really** sure you want to clear the censor filter? Type p!wipecensor again to confirm.")
        wipecensorconfirm = True
    else:
        open(rf"../pengaelicbot.data/censorfilters/{ctx.guild.id}.txt", "w").close()
        await ctx.send("Filter cleared.")
        wipecensorconfirm = False

@client.command(name="welcome", help="Show the welcome message if it doesn't show up automatically")
async def redoWelcome(ctx):
    await on_guild_join(ctx.guild)
    await ctx.message.delete()

@client.command(name="load", help="Load a cog")
@commands.has_permissions(kick_members=True)
async def loadcog(ctx, cog2load=None):
    activecogs = []
    inactivecogs = []
    with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
        allOptions = load(optionsfile)
        cogs = list(allOptions["toggles"]["cogs"].keys())
        enabled = list(allOptions["toggles"]["cogs"].values())
        for cog in range(len(cogs)):
            if enabled[cog] == True:
                activecogs.append(cogs[cog])
            else:
                inactivecogs.append(cogs[cog])

    if len(inactivecogs) == 0:
        await ctx.send("All cogs are already loaded, you can't load any more.")
    else:
        if cog2load:
            try:
                with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
                    allOptions = load(optionsfile)
                    _ = allOptions["toggles"]["cogs"][cog2load]
                    allOptions["toggles"]["cogs"][cog2load] = True
                    await updateoptions(ctx.guild.id, allOptions)
                await ctx.send(f"Cog '{cog2load}' loaded. Type `p!help {cog2load}` to see how it works.")
            except:
                await ctx.send(f"Invalid cog '{cog2load}'")
        else:
            await ctx.send("Please specify a cog to load. Avaliable options are " + str(inactivecogs)[1:-1].replace("\'",""))

@client.command(name="unload", help="Unload a cog")
@commands.has_permissions(kick_members=True)
async def unloadcog(ctx, cog2unload=None):
    activecogs = []
    with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
        allOptions = load(optionsfile)
        cogs = list(allOptions["toggles"]["cogs"].keys())
        enabled = list(allOptions["toggles"]["cogs"].values())
        for cog in range(len(cogs)):
            if enabled[cog] == True:
                activecogs.append(cogs[cog])

    if len(activecogs) == 0:
        await ctx.send("No cogs are loaded, you can't unload any more.")
    else:
        if cog2unload:
            try:
                with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
                    allOptions = load(optionsfile)
                    _ = allOptions["toggles"]["cogs"][cog2unload]
                    allOptions["toggles"]["cogs"][cog2unload] = False
                    await updateoptions(ctx.guild.id, allOptions)
                await ctx.send(f"Cog '{cog2unload}' unloaded.")
            except:
                await ctx.send(f"Invalid cog '{cog2unload}'")
        else:
            await ctx.send("Please specify a cog to unload. Avaliable options are " + str(activecogs).lower()[1:-1].replace("\'",""))

@client.command(name="help", help="Show this message")
async def help(ctx, selectedCategory=None):
    cyan = 32639
    helpMenu = discord.Embed(title="Pengaelic Bot", description="Type `p!help <category name>` for a list of commands.", color=cyan)
    with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
        allOptions = load(optionsfile)
        if allOptions["toggles"]["cogs"]["actions"] == True:
            helpMenu.add_field(name="Actions", value="Interact with other server members!")
        if allOptions["toggles"]["cogs"]["converters"] == True:
            helpMenu.add_field(name="Converters", value="Run some text through a converter to make it look funny!")
        if allOptions["toggles"]["cogs"]["games"] == True:
            helpMenu.add_field(name="Games", value="All sorts of fun stuff!")
        if allOptions["toggles"]["cogs"]["messages"] == True:
            helpMenu.add_field(name="Messages", value="M a k e   m e   s a y   t h i n g s")
        helpMenu.add_field(name="Options", value="My settings.")
        if allOptions["toggles"]["cogs"]["tools"] == True:
            helpMenu.add_field(name="Tools", value="Various tools and info.")
        helpMenu.add_field(name="Non-commands", value="Automatic message responses that aren't commands.")
    if selectedCategory == "Actions" or selectedCategory == "actions":
        helpMenu = discord.Embed(title="Actions", description="Interact with other server members!", color=cyan)
        helpMenu.add_field(name="boop <@mention>", value="Boop someone's nose :3")
        helpMenu.add_field(name="hug <@mention>", value="Give somebody a hug! :D")
        helpMenu.add_field(name="kiss <@mention>", value="Gib someone a lil kiss ~3~")
        helpMenu.add_field(name="nom <@mention>", value="Try to eat someone, but they can get away if they're quick enough :eyes:")
        helpMenu.add_field(name="pat <@mention>", value="Pat someone on the head -w-")
        helpMenu.add_field(name="slap <@mention>", value="Slap someone...?")
        helpMenu.add_field(name="tickle <@mention>", value="Tickle tickle tickle... >:D")
    elif selectedCategory == "Converters" or selectedCategory == "converters":
        helpMenu = discord.Embed(title="Converters", description="Run some text through a converter to make it look funny!", color=cyan)
        helpMenu.add_field(name="novowels\n<input string>", value="Remove all vowels from whatever text you put in.")
        helpMenu.add_field(name="(owo/uwu/furry)\n<input string>", value="Convert whatever text into owo-speak... oh god why did i make this")
        helpMenu.add_field(name="(beegtext/bigtext/beeg/big)\n<input string>", value="Turn text into\n:regional_indicator_b: :regional_indicator_e: :regional_indicator_e: :regional_indicator_g:\n:regional_indicator_t: :regional_indicator_e: :regional_indicator_x: :regional_indicator_t: :exclamation:")
    elif selectedCategory == "Games" or selectedCategory == "games":
        helpMenu = discord.Embed(title="Games", description="All sorts of fun stuff!", color=cyan)
        helpMenu.add_field(name="(8ball/magic8ball)\n[question]", value="Ask the ball a yes-or-no question, and it shall respond...")
        helpMenu.add_field(name="(pop/bubblewrap)\n[width of sheet (5)]\n[height of sheet (5)]", value="Pop some bubble wrap!")
        helpMenu.add_field(name="(draw/card)\n[number of cards (1)]\n[replace cards? yes/no (no)]", value="Draw some cards!")
        helpMenu.add_field(name="(flip/coin)\n[number of coins (1)]", value="Flip some coins!")
        helpMenu.add_field(name="(roll/dice)\n[number of dice (1)]\n[number of sides (6)]", value="Roll some dice!")
    elif selectedCategory == "Messages" or selectedCategory == "messages":
        helpMenu = discord.Embed(title="Messages", description="M a k e   m e   s a y   t h i n g s", color=cyan)
        helpMenu.add_field(name="(hi/hello/sup)\n[delete your command message?]", value="You say hi, I greet you back!")
        helpMenu.add_field(name="(bye/cya/goodbye)\n[delete your command message?]", value="You say bye, I bid you farewell.")
        helpMenu.add_field(name="(say/repeat/parrot)\n<input string>", value="Make me say whatever you say, and I might die inside in the process.")
    elif selectedCategory == "Options" or selectedCategory == "options":
        with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
            allOptions = load(optionsfile)
            helpMenu = discord.Embed(title="Options", description="Settings for the bot. Different settings need different permissions.", color=cyan)
            helpMenu.add_field(name="togglecensor", value=f"Toggle the automatic deletion of messages containing specific keywords.\n(Current value: `{allOptions['toggles']['censor']}`)")
            helpMenu.add_field(name="toggledad", value=f"Toggle the automatic Dad Bot-like responses to messages starting with \"I'm\".\n(Current value: `{allOptions['toggles']['dad']}`)")
            helpMenu.add_field(name="togglemama", value=f"Toggle the automatic Yo Mama jokes.\n(Current value: `{allOptions['toggles']['yoMama']}`)")
            helpMenu.add_field(name="(rudenesslevel/rudeness)\n<value from 0 to 3>", value=f"Set how rude the bot can be, and open up more commands.\n(Current value: `{allOptions['numbers']['rudeness']}`)")
            helpMenu.add_field(name="load [module name]", value="Load a module. Leave blank to see unloaded modules.")
            helpMenu.add_field(name="unload [module name]", value="Unload a module. Leave blank to see loaded modules.")
            helpMenu.add_field(name="(getcensor/getfilter)", value="Retrieve the list of censored words.")
            helpMenu.add_field(name="(wipecensor/wipefilter)", value="Clear the list of censored words.")
            helpMenu.add_field(name="(addcensor/addfilter) <word to add>", value="Add a word to the censor list.")
            helpMenu.add_field(name="(delcensor/delfilter) <word to delete>", value="Remove a word from the censor list.")
            helpMenu.add_field(name="(resetdefaults/defaultoptions/reset)", value="Reset all options to their defaults.")
    elif selectedCategory == "Tools" or selectedCategory == "tools":
        helpMenu = discord.Embed(title="Tools", description="Various tools and info.", color=cyan)
        helpMenu.add_field(name="(os/getos)", value="Read out what OS I'm running on!")
        helpMenu.add_field(name="(ping/ng)", value="How slow am I to respond?")
        helpMenu.add_field(name="clear [number of messages]", value="Clear away some messages. (Requires Manage Messages permission)")
        helpMenu.add_field(name="purge", value="Clear an entire channel. (Requires Manage Channels permission)")
        helpMenu.add_field(name="help\n[category]", value="Show the message from earlier!")
    elif selectedCategory == "Non-commands" or selectedCategory == "Non-Commands" or selectedCategory == "non-commands" or selectedCategory == "noncommands" or selectedCategory == "Noncommands" or selectedCategory == "NonCommands":
        helpMenu = discord.Embed(title="Non-commands", description="Automatic message responses that aren't commands.", color=cyan)
        helpMenu.add_field(name="I'm <message>", value="It's like Dad Bot. 'Nuff said.")
        helpMenu.add_field(name="Yo mama so <mama type>", value="Automatic Yo Mama jokes!")
        helpMenu.add_field(name="Yo mama list", value="Show the list of mama types to use in the auto-joker.")
    helpMenu.set_footer(text="Command prefix is `p!`, <arg> = required, [arg] = optional, [arg (value)] = default option, (command/command/command) = all keywords to run the command")
    await ctx.send(embed=helpMenu)

@resetoptions.error
@togglecensor.error
@toggledad.error
@togglemama.error
@loadcog.error
@unloadcog.error
async def kickError(ctx, error):
    global errorAlreadyHandled
    await ctx.send(f"{ctx.author.mention}, you have insufficient permissions (Kick Members)")
    errorAlreadyHandled = True

@showfilter.error
@addfilter.error
@delfilter.error
@wipefilter.error
@rudenesslevel.error
async def messageError(ctx, error):
    global errorAlreadyHandled
    await ctx.send(f"{ctx.author.mention}, you have insufficient permissions (Manage Messages)")
    errorAlreadyHandled = True

# load all the cogs
for cog in os.listdir("./cogs"):
    if cog.endswith(".py"):
        client.load_extension(f"cogs.{cog[:-3]}")

# this loop auto-reconnects if internet is lost
while True:
    client.run(TOKEN)