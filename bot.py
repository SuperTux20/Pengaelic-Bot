import discord
from json import load, dump
from discord.utils import get
from discord.ext import commands
from random import choice, randint
from os import getenv, listdir
from dotenv import load_dotenv
from asyncio import sleep

print("Starting")

load_dotenv("../pengaelicbot.data/.env")
TOKEN = getenv("DISCORD_TOKEN")
connected = False
fail = False
client = commands.Bot(command_prefix="p!",case_insensitive=True,description="Pengaelic Bot",help_command=None)

async def status_switcher():
    global client
    global fail
    await client.wait_until_ready()
    while client.is_ready:
        if fail == False:
            artist = choice(["Tux Penguin", "Qumu", "Robotic Wisp", "xGravity", "Nick Nitro", "ynk", "KEDD", "Jesse Cook", "musical rock", "SharaX"])
            game = choice(["Minecraft", "OpenRA", "3D Pinball: Space Cadet", "SuperTux", "Project Muse", "Shattered Pixel Dungeon", "Super Hexagon", "osu!", "AstroMenace", "Space Pirates and Zombies"])
            youtuber = choice(["Ethoslab", "MumboJumbo", "Blue Television Games", "The King of Random", "Phoenix SC"])
            movie = choice(["Avengers: Endgame", "Avengers: Infinity War", "Star Wars Episode IV: A New Hope", "Spiderman: Into the Spiderverse", "Back to the Future"])
            activities = {"l": discord.Activity(type=discord.ActivityType.listening, name=artist), "p": discord.Game(name=game), "wm": discord.Activity(type=discord.ActivityType.watching, name=movie), "wyt": discord.Activity(type=discord.ActivityType.watching, name=youtuber)}
            activityr = choice(list(activities.keys()))
            activity = activities[activityr]
            await client.change_presence(activity=activity)
            if activityr == "l":
                print(f'Status updated to "Listening to {artist}"')
            if activityr == "p":
                print(f'Status updated to "Playing {game}"')
            if activityr == "wm":
                print(f'Status updated to "Watching {movie}"')
            if activityr == "wyt":
                print(f'Status updated to "Watching {youtuber}"')
            await sleep(randint(1,10)*60) # task runs every few minutes (random 1-10)
        else:
            break

@client.event
async def on_ready():
    global connected
    global fail
    for guild in range(len(client.guilds)):
        if client.guilds[guild].name == None:
            fail = True
            break
        else:
            fail = False
            # try to read the options file
            try:
                with open(rf"../pengaelicbot.data/configs/{client.guilds[guild].id}.json", "r") as optionsfile:
                    allOptions = load(optionsfile)
                    if connected == False:
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
    if fail == True:
        print("Failed to connect to Discord")
        exit()
    else:
        if connected == False:
            connectstatus = f"{client.user.name}#{client.user.discriminator} connected to Discord"
        else:
            connectstatus = "Reconnected"
        print()
        print(connectstatus)
        connected = True

@client.event
async def on_guild_join(guild, ctx=None):
    print("Joined " + str(guild.name))
    welcomeEmbed = discord.Embed(title="Howdy fellas! I'm the Pengaelic Bot!", description="Type `p!help` for a list of commands.", color=32639)
    welcomeEmbed.set_thumbnail(url=client.user.avatar_url)
    allchannels = list(guild.text_channels)
    for channel in range(len(allchannels)):
        allchannels[channel] = str(allchannels[channel])
    if get(guild.text_channels, name="general"):
        await get(guild.text_channels, name="general").send(embed=welcomeEmbed)
    elif channel:
        await ctx.channel.send(embed=welcomeEmbed)

    # create fresh options file for new server
    try:
        open(rf"../pengaelicbot.data/configs/{guild.id}.json", "x").close()
        with open(r"default_options.json", "r") as defaultsfile:
            allOptions = load(defaultsfile)
        with open(rf"../pengaelicbot.data/configs/{guild.id}.json", "w") as optionsfile:
            dump(allOptions, optionsfile, sort_keys=True, indent=4)
        print("Options file created for " + str(guild.name))
    except:
        pass

@client.event
async def on_command_error(ctx, error):
    # this checks if the individual commands have their own error handling. if not...
    if hasattr(ctx.command, 'on_error'):
        return
    # ...send the global error, which differs depending on rudeness level
    errormsgs = ["Sorry, this command is invalid.", "Invalid command/usage.", "You typed the command wrong!"]
    with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
        allOptions = load(optionsfile)
    if allOptions["numbers"]["rudeness"] < 3:
        await ctx.send(errormsgs[allOptions["numbers"]["rudeness"]] + " Type `p!help` for a list of commands and their usages.")
    else:
        await ctx.send(file=discord.File("images/thatsnothowitworksyoulittleshit.jpg"))
    if "is not found" not in str(error):
        print(error)
    try:
        print("Invalid command p!{} sent in {} in #{} by {}#{}".format(str(error).split('"')[1], ctx.guild, ctx.channel, ctx.message.author.name, ctx.message.author.discriminator))
    except:
        print(error)

@client.command(name="join", help="Show the join message if it doesn't show up automatically")
async def redoWelcome(ctx):
    await on_guild_join(ctx.guild, ctx)
    await ctx.message.delete()

@client.command(name="help", help="Show this message", aliases=["info", "commands", "h"])
async def help(ctx, category=None, subcategory=None):
    cyan = 32639
    helpMenu = discord.Embed(title=client.description, description="Type `p!help <category name>` for more info on each category.", color=cyan)
    cogfiles = [cog[:-3] for cog in listdir("./cogs") if cog.endswith(".py")]
    cogs = [client.get_cog(cog.capitalize()) for cog in cogfiles]
    with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
        allOptions = load(optionsfile)
        allCogs = allOptions["toggles"]["cogs"]
        enabledCogs = {}
        for cog in allCogs:
            if allCogs[cog] == True:
                enabledCogs[cog] = cog
        for cog in cogs:
            if cog == None:
                pass
            elif cog.name == "options" or cog.name == "noncommands":
                pass
            elif allOptions["toggles"]["cogs"][cog.name] == True:
                helpMenu.add_field(name=cog.name.capitalize(), value=cog.description)
        helpMenu.add_field(name="Options", value=client.get_cog("Options").description)
        helpMenu.add_field(name="Non-commands", value=client.get_cog("Noncommands").description)
    if category == "Actions" or category == "actions":
        helpMenu = discord.Embed(title="Actions", description="Interact with other server members!", color=cyan)
        for command in client.get_cog("Actions").get_commands():
            helpMenu.add_field(name=f"{command} <username or nickname or @mention>", value=command.help)
    elif category == "Converters" or category == "converters":
        helpMenu = discord.Embed(title="Converters", description="Run some text through a converter to make it look funny!", color=cyan)
        for command in client.get_cog("Converters").get_commands():
            command.activations = [command.name]
            for alias in command.aliases:
                command.activations.append(alias)
            helpMenu.add_field(name="(" + str(command.activations)[1:-1].replace("'","").replace(", ","/") + ")\n<text to convert>", value=command.help)
    elif category == "Games" or category == "games":
        helpMenu = discord.Embed(title="Games", description="All sorts of fun stuff!", color=cyan)
        for command in client.get_cog("Games").get_commands():
            command.activations = [command.name]
            for alias in command.aliases:
                command.activations.append(alias)
            if command.usage:
                helpMenu.add_field(name="(" + str(command.activations)[1:-1].replace("'","").replace(", ","/") + ")\n" + str(command.usage), value=command.help)
            else:
                helpMenu.add_field(name="(" + str(command.activations)[1:-1].replace("'","").replace(", ","/") + ")", value=command.help)
    elif category == "Messages" or category == "messages":
        helpMenu = discord.Embed(title="Messages", description="M a k e   m e   s a y   t h i n g s", color=cyan)
        for command in client.get_cog("Messages").get_commands():
            command.activations = [command.name]
            for alias in command.aliases:
                command.activations.append(alias)
            if command.usage:
                helpMenu.add_field(name="(" + str(command.activations)[1:-1].replace("'","").replace(", ","/") + ")\n" + str(command.usage), value=command.help)
            else:
                helpMenu.add_field(name="(" + str(command.activations)[1:-1].replace("'","").replace(", ","/") + ")", value=command.help)
    elif category == "Options" or category == "options":
        with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
            allOptions = load(optionsfile)
            if subcategory == None:
                helpMenu = discord.Embed(title="Options", description="Settings for the bot. Different settings need different permissions.\nType `p!help options [option]` for more info on each subcategory.", color=cyan)
                helpMenu.add_field(name="Censor", value="Automatic deletion of messages based on keywords in a text file.")
                helpMenu.add_field(name="Cogs", value="I'm modular! You can enable or disable whatever cog you want.")
                helpMenu.add_field(name="Other", value="Settings that don't fit into any other categories.")
            else:
                if subcategory == "Censor" or subcategory == "censor":
                    helpMenu = discord.Embed(title="Censorship", desctiption="Automatic deletion of messages based on keywords in a text file.", color=cyan)
                    helpMenu.add_field(name="(togglecensor/togglefilter)", value="Toggle the entire censorship function.")
                    helpMenu.add_field(name="(censorlist/filterlist)", value="Show the list of censored words.")
                    helpMenu.add_field(name="(wipecensor/wipefilter)", value="Clear the list.")
                    helpMenu.add_field(name="(addcensor/addfilter)\n<word>", value="Add a word to the list.")
                    helpMenu.add_field(name="(delcensor/delfilter)\n<word>", value="Delete a word from the list.")
                if subcategory == "Cogs" or subcategory == "cogs":
                    helpMenu = discord.Embed(title="Cogs", description="I'm modular! You can enable or disable whatever cog you want.", color=cyan)
                    helpMenu.add_field(name="cogs", value="See a list of all cogs and their statuses.")
                    helpMenu.add_field(name="load\n[cog]", value="Load a cog.")
                    helpMenu.add_field(name="unload\n[cog]", value="Unload a cog.")
                if subcategory == "Other" or subcategory == "other":
                    helpMenu = discord.Embed(title="Other", description="Settings that don't fit into any other categories.", color=cyan)
                    helpMenu.add_field(name="(reset/defaults)", value="Reset all options to their default values.")
                    helpMenu.add_field(name="togglemama", value="Toggle the Yo Mama jokes.")
                    helpMenu.add_field(name="toggledad", value="Toggle the dad jokes.")
                    helpMenu.add_field(name="(rudeness/rudenesslevel) <level>", value="Change how rude the bot can be.")
    elif category == "Tools" or category == "tools":
        helpMenu = discord.Embed(title="Tools", description="Various tools and info.", color=cyan)
        for command in client.get_cog("Tools").get_commands():
            command.activations = [command.name]
            for alias in command.aliases:
                command.activations.append(alias)
            if command.usage:
                helpMenu.add_field(name="(" + str(command.activations)[1:-1].replace("'","").replace(", ","/") + ")\n" + str(command.usage), value=command.help)
            else:
                helpMenu.add_field(name="(" + str(command.activations)[1:-1].replace("'","").replace(", ","/") + ")", value=command.help)
    elif category == "Non-commands" or category == "Non-Commands" or category == "non-commands" or category == "noncommands" or category == "Noncommands" or category == "NonCommands":
        helpMenu = discord.Embed(title="Non-commands", description="Automatic message responses that aren't commands.", color=cyan)
        helpMenu.add_field(name="I'm <message>", value="It's like Dad Bot. 'Nuff said.")
        helpMenu.add_field(name="Yo mama so <mama type>", value="Automatic Yo Mama jokes!")
        helpMenu.add_field(name="Yo mama list", value="Show the list of mama types to use in the auto-joker.")
    helpMenu.set_footer(text="Command prefix is `p!`\n<arg> = required parameter\n[arg] = optional parameter\n[arg (value)] = default value for optional parameter\n(command/command/command) = all aliases you can run the command with")
    await ctx.send(embed=helpMenu)

# load all the cogs
for cog in listdir("./cogs"):
    if cog.endswith(".py"):
        client.load_extension(f"cogs.{cog[:-3]}")
        print(f"Loaded cog {cog[:-3]}")

client.loop.create_task(status_switcher()) # as defined above

# this loop auto-reloads if internet connection is lost
while True:
    try:
        client.run(TOKEN)
    except KeyboardInterrupt:
        print("Disconnected")
        break
    except:
        print("Unable to connect to Discord")
        break
print("Quit")
exit()