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
    try:
        with open(rf"../pengaelicbot.data/configs/{message.guild.id}.json", "r") as optionsfile:
            allOptions = load(optionsfile)
    except:
        pass
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

    # this section randomizes yo mama jokes, does not work if rudeness is below 2
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

# @client.event
# async def on_command_error(ctx, error):
#     with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
#         allOptions = load(optionsfile)
#     if errorAlreadyHandled == False:
#         if allOptions["numbers"]["rudeness"] < 3:
#             if allOptions["numbers"]["rudeness"] == 0:
#                 invalidmsg = "Sorry, this command is invalid."
#             elif allOptions["numbers"]["rudeness"] == 1:
#                 invalidmsg = "Invalid command/usage."
#             elif allOptions["numbers"]["rudeness"] == 2:
#                 invalidmsg = "You typed the command wrong!"
#             await ctx.send(invalidmsg + " Type `p!help` for a list of commands and their usages.")
#         else:
#             await ctx.send(file=discord.File("images/thatsnothowitworksyoulittleshit.jpg"))

@client.command(name="welcome", help="Show the welcome message if it doesn't show up automatically")
async def redoWelcome(ctx):
    await on_guild_join(ctx.guild)
    await ctx.message.delete()

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
        cog = client.get_cog("Actions")
        for command in cog.get_commands():
            helpMenu.add_field(name=f"{command} <@mention>", value=command.help)
    elif selectedCategory == "Converters" or selectedCategory == "converters":
        helpMenu = discord.Embed(title="Converters", description="Run some text through a converter to make it look funny!", color=cyan)
        cog = client.get_cog("Converters")
        for command in cog.get_commands():
            command.activations = [command.name]
            for alias in command.aliases:
                command.activations.append(alias)
            helpMenu.add_field(name="(" + str(command.activations)[1:-1].replace("'","").replace(", ","/") + ")\n<text to convert>", value=command.help)
    elif selectedCategory == "Games" or selectedCategory == "games":
        helpMenu = discord.Embed(title="Games", description="All sorts of fun stuff!", color=cyan)
        cog = client.get_cog("Games")
        for command in cog.get_commands():
            command.activations = [command.name]
            for alias in command.aliases:
                command.activations.append(alias)
            if command.usage:
                helpMenu.add_field(name="(" + str(command.activations)[1:-1].replace("'","").replace(", ","/") + ")\n" + str(command.usage), value=command.help)
            else:
                helpMenu.add_field(name="(" + str(command.activations)[1:-1].replace("'","").replace(", ","/") + ")", value=command.help)
    elif selectedCategory == "Messages" or selectedCategory == "messages":
        helpMenu = discord.Embed(title="Messages", description="M a k e   m e   s a y   t h i n g s", color=cyan)
        cog = client.get_cog("Messages")
        for command in cog.get_commands():
            command.activations = [command.name]
            for alias in command.aliases:
                command.activations.append(alias)
            if command.usage:
                helpMenu.add_field(name="(" + str(command.activations)[1:-1].replace("'","").replace(", ","/") + ")\n" + str(command.usage), value=command.help)
            else:
                helpMenu.add_field(name="(" + str(command.activations)[1:-1].replace("'","").replace(", ","/") + ")", value=command.help)
    elif selectedCategory == "Options" or selectedCategory == "options":
        with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
            allOptions = load(optionsfile)
            helpMenu = discord.Embed(title="Options", description="Settings for the bot. Different settings need different permissions.", color=cyan)
            cog = client.get_cog("Options")
            for command in cog.get_commands():
                command.activations = [command.name]
                for alias in command.aliases:
                    command.activations.append(alias)
                if command.usage:
                    helpMenu.add_field(name="(" + str(command.activations)[1:-1].replace("'","").replace(", ","/") + ")\n" + str(command.usage), value=command.help)
                else:
                    helpMenu.add_field(name="(" + str(command.activations)[1:-1].replace("'","").replace(", ","/") + ")", value=command.help)
    elif selectedCategory == "Tools" or selectedCategory == "tools":
        helpMenu = discord.Embed(title="Tools", description="Various tools and info.", color=cyan)
        cog = client.get_cog("Tools")
        for command in cog.get_commands():
            command.activations = [command.name]
            for alias in command.aliases:
                command.activations.append(alias)
            if command.usage:
                helpMenu.add_field(name="(" + str(command.activations)[1:-1].replace("'","").replace(", ","/") + ")\n" + str(command.usage), value=command.help)
            else:
                helpMenu.add_field(name="(" + str(command.activations)[1:-1].replace("'","").replace(", ","/") + ")", value=command.help)
    elif selectedCategory == "Non-commands" or selectedCategory == "Non-Commands" or selectedCategory == "non-commands" or selectedCategory == "noncommands" or selectedCategory == "Noncommands" or selectedCategory == "NonCommands":
        helpMenu = discord.Embed(title="Non-commands", description="Automatic message responses that aren't commands.", color=cyan)
        helpMenu.add_field(name="I'm <message>", value="It's like Dad Bot. 'Nuff said.")
        helpMenu.add_field(name="Yo mama so <mama type>", value="Automatic Yo Mama jokes!")
        helpMenu.add_field(name="Yo mama list", value="Show the list of mama types to use in the auto-joker.")
    helpMenu.set_footer(text="Command prefix is `p!`, <arg> = required, [arg] = optional, [arg (value)] = default option, (command/command/command) = all keywords to run the command")
    await ctx.send(embed=helpMenu)

# load all the cogs
for cog in os.listdir("./cogs"):
    if cog.endswith(".py"):
        client.load_extension(f"cogs.{cog[:-3]}")
        print(f"Cog {cog[:-3]} loaded")

# this loop auto-reloads if internet connection is lost
while True:
    client.run(TOKEN)