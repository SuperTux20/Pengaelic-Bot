# bot.py
import discord
from json import load, dump
from discord.utils import get
from discord.ext import commands
from random import choice
from os import getenv, listdir
from dotenv import load_dotenv

print("Starting")

load_dotenv("../pengaelicbot.data/.env")
TOKEN = getenv("DISCORD_TOKEN")
errorAlreadyHandled = False
# even though I'm removing the default p!help command, I'm leaving the vestigial descriptions in the commands
client = commands.Bot(command_prefix="p!",case_insensitive=True,description="Pengaelic Bot",help_command=None)

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
    helpMenu = discord.Embed(title=client.description, description="Type `p!help <category name>` for a list of commands.", color=cyan)
    cogfiles = [cog[:-3] for cog in listdir("./cogs") if cog.endswith(".py")]
    cogs = [client.get_cog(cog.capitalize()) for cog in cogfiles]
    print(cogs)
    with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
        allOptions = load(optionsfile)
        allCogs = list(allOptions["toggles"]["cogs"].keys())
        enabled = list(allOptions["toggles"]["cogs"].values())
        for cog in range(len(allCogs)):
            if enabled[cog] == False:
                cogs.remove(allCogs[cog])
        for cog in cogs:
            if cog == None:
                pass
            elif cog.name == "options" or cog.name == "noncommands":
                pass
            elif allOptions["toggles"]["cogs"][cog.name] == True:
                helpMenu.add_field(name=cog.name.capitalize(), value=cog.description)
        helpMenu.add_field(name="Options", value=client.get_cog("Options").description)
        helpMenu.add_field(name="Non-commands", value=client.get_cog("Noncommands").description)
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
for cog in listdir("./cogs"):
    if cog.endswith(".py"):
        client.load_extension(f"cogs.{cog[:-3]}")
        print(f'Cog "{cog[:-3]}" loaded')

# this loop auto-reloads if internet connection is lost
while True:
    client.run(TOKEN)