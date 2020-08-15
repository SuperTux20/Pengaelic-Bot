print(
    "Loading"
)
import discord
print(
    "Imported discord"
)
import sys
print(
    "Imported sys"
)
import os
print(
    "Imported os"
)
from json import load, dump
print(
    "Imported load and dump from json"
)
from fnmatch import filter
print(
    "Imported filter from fnmatch"
)
from discord.utils import get
print(
    "Imported get from discord.utils"
)
from discord.ext import commands
print(
    "Imported commands from discord.ext"
)
from random import choice, randint
print(
    "Imported choice and randint from random"
)
from dotenv import load_dotenv as dotenv
print(
    "Imported dotenv"
)
from asyncio import sleep
print(
    "Imported sleep from asyncio"
)
from time import sleep as realsleep
print(
    "Imported sleep from time"
)

dotenv(
    "data/.env"
)
print(
    "Loaded bot token"
)

connected = False
fail = False
client = commands.Bot(
    command_prefix = "p!",
    case_insensitive = True,
    description = "Pengaelic Bot",
    help_command = None
)
print(
    "Defined client"
)

async def statusSwitcher():
    global client
    global fail
    await client.wait_until_ready()
    while client.is_ready:
        if fail == False:
            artist = choice(
                [
                    "Tux Penguin",
                    "Qumu",
                    "Robotic Wisp",
                    "xGravity",
                    "Nick Nitro",
                    "ynk",
                    "KEDD",
                    "Jesse Cook",
                    "musical rock",
                    "SharaX"
                ]
            )
            game = choice(
                [
                    "Minecraft",
                    "OpenRA",
                    "3D Pinball: Space Cadet",
                    "SuperTux",
                    "Project Muse",
                    "Shattered Pixel Dungeon",
                    "Super Hexagon",
                    "osu!",
                    "AstroMenace",
                    "Space Pirates and Zombies"
                ]
            )
            youtuber = choice(
                [
                    "Ethoslab",
                    "MumboJumbo",
                    "Blue Television Games",
                    "The King of Random",
                    "Phoenix SC"
                ]
            )
            movie = choice(
                [
                    "Avengers: Endgame",
                    "Avengers: Infinity War",
                    "Star Wars Episode IV: A New Hope",
                    "Spiderman: Into the Spiderverse",
                    "Back to the Future"
                ]
            )
            activities = [
                discord.Activity(
                    type = discord.ActivityType.listening,
                    name = artist
                ),
                discord.Game(
                    name = game
                ),
                discord.Activity(
                    type = discord.ActivityType.watching,
                    name = movie
                ),
                discord.Activity(
                    type = discord.ActivityType.watching,
                    name = youtuber
                )
            ]
            activity = choice(
                activities
            )
            await client.change_presence(
                activity = activity
            )
            await sleep(
                randint(
                    2,
                    10
                ) * 60
            ) # task runs every few minutes (random 1-10)
        else:
            break
print(
    "Defined status switcher"
)
def remove_duplicates(inList: list):
    return list(dict.fromkeys(inList))

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
                with open(rf"data/servers/{client.guilds[guild].id}/config.json", "r") as optionsfile:
                    allOptions = load(
                        optionsfile
                    )
                    if connected == False:
                        print(
                            f"""Data loaded for {
                                client.guilds[guild].name
                            }"""
                        )
            # if something goes wrong...
            except:
                # ...try to make the servers folder (just in case)...
                try:
                    os.mkdir(
                        r"data/servers"
                    )
                    print(
                        'Created "servers" folder'
                    )
                except FileExistsError:
                    pass
                # ...try to make the guild ID folder...
                try:
                    os.mkdir(
                        rf"""data/servers/{
                            client.guilds[guild].id
                        }"""
                    )
                    print(
                        f"""Created server folder for {
                            client.guilds[guild].name
                        }"""
                    )
                except FileExistsError:
                    pass
                # ...make a blank file...
                try:
                    open(
                        rf"""data/servers/{client.guilds[guild].id}/config.json""",
                        "x"
                    ).close()
                except FileExistsError:
                    pass
                # ...and restore the default options file
                with open(r"data/default_options.json", "r") as defaultsfile:
                    allOptions = load(
                        defaultsfile
                    )
                with open(rf"data/servers/{client.guilds[guild].id}/config.json", "w") as optionsfile:
                    dump(
                        allOptions,
                        optionsfile,
                        sort_keys = True,
                        indent = 4
                    )
                print(
                    f"""Options file created for {client.guilds[guild].name}"""
                )
    if fail == True:
        exit()
    else:
        if connected == False:
            connectstatus = f"""{
                client.user
            } connected to Discord"""
        else:
            connectstatus = "Reconnected"
        print()
        print(
            connectstatus
        )
        connected = True
print(
    "Defined on_ready"
)

@client.event
async def on_guild_join(guild, ctx = None):
    print(
        f"""Joined {
            guild.name
        }"""
    )
    welcomeEmbed = discord.Embed(
        title = "Howdy fellas! I'm the Pengaelic Bot!",
        description = f"Type `{client.command_prefix}help` for a list of commands.",
        color = 32639
    ).set_thumbnail(
        url = client.user.avatar_url
    )
    channelkeys = [
        "welcome",
        "arrivals",
        "entrance",
        "entry",
        "log",
        "general"
    ]
    possiblechannels = [filter([channel.name for channel in guild.text_channels], f"*{channel}*") for channel in channelkeys]
    for channelset in possiblechannels:
        for channel in channelset:
            try:
                await get(
                    guild.text_channels,
                    name = channel
                ).send(
                    embed = welcomeEmbed
                )
                await ctx.send(
                    """Be sure to join the Support server for news and updates!
https://discord.gg/DHHpA7k"""
                )
                return
            except:
                continue

    # create fresh options file for new server
    try:
        os.mkdir(
            rf"""data/servers/{
                guild.id
            }"""
        )
        open(
            rf"""data/servers/{
                guild.id
            }/config.json""",
            "x"
        ).close()
        with open(r"data/default_options.json", "r") as defaultsfile:
            allOptions = load(
                defaultsfile
            )
        with open(rf"data/servers/{guild.id}/config.json", "w") as optionsfile:
            dump(
                allOptions,
                optionsfile,
                sort_keys = True,
                indent = 4
            )
        print(
            f"""Options file created for {
                guild.name
            }"""
        )
    except FileExistsError:
        print(
            f"""Found existing options file for {
                guild.name
            }"""
        )
    except:
        print(
            f"""Failed to create options file for {
                guild.name
            }"""
        )
print(
    "Defined on_guild_join"
)

@client.event
async def on_command_error(ctx, error):
    # this checks if the individual commands have their own error handling. if not...
    if hasattr(ctx.command, 'on_error'):
        return
    # ...send the global error
    await ctx.send(
        f"""Invalid command/usage. Type `{
            client.command_prefix
        }help` for a list of commands and their usages."""
    )
    if "is not found" in str(error):
        print(
            "Invalid command {}{} sent in {} in #{} by {}#{}".format(
                client.command_prefix,
                str(
                    error
                ).split(
                    '"'
                )[1],
                ctx.guild,
                ctx.channel,
                ctx.message.author.name,
                ctx.message.author.discriminator
            )
        )
    else:
        print(
            error
        )
print(
    "Defined on_command_error"
)

@client.command(name = "join", help = "Show the join message if it doesn't show up automatically")
async def redoWelcome(ctx):
    await on_guild_join(
        ctx.guild, ctx.channel
    )
    await ctx.message.delete()

@client.group(name = "help", help = "Show this message", aliases = ["commands", "h", "?"])
async def help(ctx):
    if ctx.invoked_subcommand is None:
        helpMenu = discord.Embed(
            title = client.description,
            description = f"""Type `{
                client.command_prefix
            }help <lowercase category name without spaces/dashes>` for more info on each category.""",
            color = 32639
        ).set_footer(
            text = f"""    Command prefix is {
                client.command_prefix
            }
    <arg> = required parameter
    [arg] = optional parameter
    [arg (value)] = default value for optional parameter
    (command/command/command) = all aliases you can run the command with"""
        )
        cogs = [
            client.get_cog(cog)
            for cog in [
                cog[:-3]
                for cog in os.listdir("./cogs")
                if cog.endswith(".py")
            ]
        ]
        for cog in cogs:
            if cog == None or cog.name == "options":
                pass
            elif load(open(rf"data/servers/{ctx.guild.id}/config.json", "r"))["cogs"][cog.name_typable] == True:
                helpMenu.add_field(
                    name = cog.name.capitalize(),
                    value = cog.description
                )
        helpMenu.add_field(
            name = "Options",
            value = client.get_cog(
                "options"
            ).description
        )
        await ctx.send(embed = helpMenu)
print(
    "Defined root help menu"
)

@help.command(name = "actions")
async def hActions(ctx):
    if load(open(rf"data/servers/{ctx.guild.id}/config.json", "r"))["cogs"]["actions"] == True:
        cog = client.get_cog("actions")
        helpMenu = discord.Embed(
            title = cog.name.capitalize(),
            description = cog.description_long,
            color = 32639
        ).set_footer(
            text = f"""    Command prefix is {
                client.command_prefix
            }
        <arg> = required parameter
        [arg] = optional parameter
        [arg (value)] = default value for optional parameter
        (command/command/command) = all aliases you can run the command with"""
        )
        for command in cog.get_commands():
            helpMenu.add_field(
                name = "(" + str(
                    [command.name] + command.aliases
                )[1:-1].replace(
                    "'",
                    ""
                ).replace(
                    ", ",
                    "/"
                ) + ")",
                value = command.name.capitalize()
            )
        await ctx.send(embed = helpMenu)
    else:
        await ctx.send(f"This module is disabled. Type `{client.command_prefix}cog load actions` to enable it.")
print(
    "Defined actions help menu"
)

@help.command(name = "actsofviolence")
async def hActsOfViolence(ctx):
    if load(open(rf"data/servers/{ctx.guild.id}/config.json", "r"))["cogs"]["actsofviolence"] == True:
        cog = client.get_cog("actsofviolence")
        helpMenu = discord.Embed(
            title = cog.name.capitalize(),
            description = cog.description_long,
            color = 32639
        ).set_footer(
            text = f"""    Command prefix is {
                client.command_prefix
            }
        <arg> = required parameter
        [arg] = optional parameter
        [arg (value)] = default value for optional parameter
        (command/command/command) = all aliases you can run the command with"""
        )
        for command in cog.get_commands():
            helpMenu.add_field(
                name = "(" + str(
                    [command.name] + command.aliases
                )[1:-1].replace(
                    "'",
                    ""
                ).replace(
                    ", ",
                    "/"
                ) + ")\n <username or nickname or @mention> ",
                value = command.help
            )
        await ctx.send(embed = helpMenu)
    else:
        await ctx.send(f"This module is disabled. Type `{client.command_prefix}cog load actsofviolence` to enable it.")
print(
    "Defined actsofviolence help menu"
)

@help.command(name = "converters")
async def hConverters(ctx):
    if load(open(rf"data/servers/{ctx.guild.id}/config.json", "r"))["cogs"]["converters"] == True:
        cog = client.get_cog("converters")
        helpMenu = discord.Embed(
            title = cog.name.capitalize(),
            description = cog.description_long,
            color = 32639
        ).set_footer(
            text = f"""    Command prefix is {
                client.command_prefix
            }
        <arg> = required parameter
        [arg] = optional parameter
        [arg (value)] = default value for optional parameter
        (command/command/command) = all aliases you can run the command with"""
        )
        for command in cog.get_commands():
            helpMenu.add_field(
                name = "(" + str(
                    [command.name] + command.aliases
                )[1:-1].replace(
                    "'",
                    ""
                ).replace(
                    ", ",
                    "/"
                ) + ")\n <text to convert> ",
                value = command.help
            )
        await ctx.send(embed = helpMenu)
    else:
        await ctx.send(f"This module is disabled. Type `{client.command_prefix}cog load converters` to enable it.")
print(
    "Defined converters help menu"
)

@help.command(name = "games")
async def hGames(ctx):
    if load(open(rf"data/servers/{ctx.guild.id}/config.json", "r"))["cogs"]["games"] == True:
        cog = client.get_cog("games")
        helpMenu = discord.Embed(
            title = cog.name.capitalize(),
            description = cog.description_long,
            color = 32639
        ).set_footer(
            text = f"""    Command prefix is {
                client.command_prefix
            }
        <arg> = required parameter
        [arg] = optional parameter
        [arg (value)] = default value for optional parameter
        (command/command/command) = all aliases you can run the command with"""
        )
        for command in cog.get_commands():
            if command.usage:
                helpMenu.add_field(
                    name = "({})\n{}".format(
                        str(
                            [command.name] + command.aliases
                        )[1:-1].replace(
                            "'",
                            ""
                        ).replace(
                            ", ",
                            "/"
                        ),
                        command.usage
                    ),
                    value = command.help
                )
            else:
                helpMenu.add_field(
                    name = "({})".format(
                        str(
                            [command.name] + command.aliases
                        )[1:-1].replace(
                            "'",
                            ""
                        ).replace(
                            ", ",
                            "/"
                        )
                    ),
                    value = command.help
                )
        await ctx.send(embed = helpMenu)
    else:
        await ctx.send(f"This module is disabled. Type `{client.command_prefix}cog load games` to enable it.")
print(
    "Defined games help menu"
)

@help.command(name = "interactions")
async def hinteractions(ctx):
    if load(open(rf"data/servers/{ctx.guild.id}/config.json", "r"))["cogs"]["interactions"] == True:
        cog = client.get_cog("interactions")
        helpMenu = discord.Embed(
            title = cog.name.capitalize(),
            description = cog.description_long,
            color = 32639
        ).set_footer(
            text = f"""    Command prefix is {
                client.command_prefix
            }
        <arg> = required parameter
        [arg] = optional parameter
        [arg (value)] = default value for optional parameter
        (command/command/command) = all aliases you can run the command with"""
        )
        for command in cog.get_commands():
            helpMenu.add_field(
                name = "(" + str(
                    [command.name] + command.aliases
                )[1:-1].replace(
                    "'",
                    ""
                ).replace(
                    ", ",
                    "/"
                ) + ")\n <username or nickname or @mention> ",
                value = command.help
            )
        await ctx.send(embed = helpMenu)
    else:
        await ctx.send(f"This module is disabled. Type `{client.command_prefix}cog load interactions` to enable it.")
print(
    "Defined interactions help menu"
)

@help.command(name = "messages")
async def hMessages(ctx):
    if load(open(rf"data/servers/{ctx.guild.id}/config.json", "r"))["cogs"]["messages"] == True:
        cog = client.get_cog("messages")
        helpMenu = discord.Embed(
            title = cog.name.capitalize(),
            description = cog.description_long,
            color = 32639
        ).set_footer(
            text = f"""    Command prefix is {
                client.command_prefix
            }
        <arg> = required parameter
        [arg] = optional parameter
        [arg (value)] = default value for optional parameter
        (command/command/command) = all aliases you can run the command with"""
        )
        for command in cog.get_commands():
            if command.usage:
                helpMenu.add_field(
                    name = "({})\n{}".format(
                        str(
                            [command.name] + command.aliases
                        )[1:-1].replace(
                            "'",
                            ""
                        ).replace(
                            ", ",
                            "/"
                        ),
                        command.usage
                    ),
                    value = command.help
                )
            else:
                helpMenu.add_field(
                    name = "({})".format(
                        str(
                            [command.name] + command.aliases
                        )[1:-1].replace(
                            "'",
                            ""
                        ).replace(
                            ", ",
                            "/"
                        )
                    ),
                    value = command.help
                )
        await ctx.send(embed = helpMenu)
    else:
        await ctx.send(f"This module is disabled. Type `{client.command_prefix}cog load messages` to enable it.")
print(
    "Defined messages help menu"
)

@help.command(name = "noncommands")
async def hNonCommands(ctx):
    if load(open(rf"data/servers/{ctx.guild.id}/config.json", "r"))["cogs"]["noncommands"] == True:
        cog = client.get_cog("noncommands")
        await ctx.send(
            embed = discord.Embed(
                title = cog.name.capitalize(),
                description = cog.description_long,
                color = 32639
            ).add_field(
                name = "I'm <message> ",
                value = "Like Dad Bot!"
            ).add_field(
                name = "Yo mama so <mama type> ",
                value = "Automatic Yo Mama jokes!"
            ).add_field(
                name = "Yo mama list",
                value = "Show the list of mama types to use in the auto-joker."
            ).add_field(
                name = "You know the rules",
                value = "A rickroll-themed Russian Roulette."
            )
        )
    else:
        await ctx.send(f"This module is disabled. Type `{client.command_prefix}cog load noncommands` to enable it.")
print(
    "Defined noncommands help menu"
)

@help.command(name = "tools")
async def hTools(ctx):
    if load(open(rf"data/servers/{ctx.guild.id}/config.json", "r"))["cogs"]["tools"] == True:
        cog = client.get_cog("tools")
        helpMenu = discord.Embed(
            title = cog.name.capitalize(),
            description = cog.description_long,
            color = 32639
        ).set_footer(
            text = f"""    Command prefix is {
                client.command_prefix
            }
        <arg> = required parameter
        [arg] = optional parameter
        [arg (value)] = default value for optional parameter
        (command/command/command) = all aliases you can run the command with"""
        )
        for command in cog.get_commands():
            if command.usage:
                helpMenu.add_field(
                    name = "({})\n{}".format(
                        str(
                            [command.name] + command.aliases
                        )[1:-1].replace(
                            "'",
                            ""
                        ).replace(
                            ", ",
                            "/"
                        ),
                        command.usage
                    ),
                    value = command.help
                )
            else:
                helpMenu.add_field(
                    name = "({})".format(
                        str(
                            [command.name] + command.aliases
                        )[1:-1].replace(
                            "'",
                            ""
                        ).replace(
                            ", ",
                            "/"
                        )
                    ),
                    value = command.help
                )
        await ctx.send(embed = helpMenu)
    else:
        await ctx.send(f"This module is disabled. Type `{client.command_prefix}cog load tools` to enable it.")
print(
    "Defined tools help menu"
)

@help.command(name = "oddcommands")
async def hOdds(ctx):
    if load(open(rf"data/servers/{ctx.guild.id}/config.json", "r"))["cogs"]["oddcommands"] == True:
        cog = client.get_cog("oddcommands")
        helpMenu = discord.Embed(
            title = cog.name.capitalize(),
            description = cog.description_long,
            color = 32639
        ).set_footer(
            text = f"""    Command prefix is {
                client.command_prefix
            }
        <arg> = required parameter
        [arg] = optional parameter
        [arg (value)] = default value for optional parameter
        (command/command/command) = all aliases you can run the command with"""
        )
        for command in cog.get_commands():
            if command.usage:
                helpMenu.add_field(
                    name = "({})\n{}".format(
                        str(
                            [command.name] + command.aliases
                        )[1:-1].replace(
                            "'",
                            ""
                        ).replace(
                            ", ",
                            "/"
                        ),
                        command.usage
                    ),
                    value = command.help
                )
            else:
                helpMenu.add_field(
                    name = "({})".format(
                        str(
                            [command.name] + command.aliases
                        )[1:-1].replace(
                            "'",
                            ""
                        ).replace(
                            ", ",
                            "/"
                        )
                    ),
                    value = command.help
                )
        await ctx.send(embed = helpMenu)
    else:
        await ctx.send(f"This module is disabled. Type `{client.command_prefix}cog load oddcommands` to enable it.")
print(
    "Defined oddcommands help menu"
)

@help.group(name = "options")
async def hOptions(ctx):
    if ctx.invoked_subcommand is None:
        cog = client.get_cog("options")
        helpMenu = discord.Embed(
            title = cog.name.capitalize(),
            description = cog.description_long,
            color = 32639
        ).set_footer(
            text = f"""    Command prefix is {
                client.command_prefix
            }
    <arg> = required parameter
    [arg] = optional parameter
    [arg (value)] = default value for optional parameter
    (command/command/command) = all aliases you can run the command with"""
        )
        for command in cog.get_commands():
            if command.usage:
                helpMenu.add_field(
                    name = "({})\n{}".format(
                        str(
                            [command.name] + command.aliases
                        )[1:-1].replace(
                            "'",
                            ""
                        ).replace(
                            ", ",
                            "/"
                        ),
                        command.usage
                    ),
                    value = command.help
                )
            else:
                helpMenu.add_field(
                    name = "({})".format(
                        str(
                            [command.name] + command.aliases
                        )[1:-1].replace(
                            "'",
                            ""
                        ).replace(
                            ", ",
                            "/"
                        )
                    ),
                    value = command.help
                )
        await ctx.send(embed = helpMenu)
print(
    "Defined root options menu"
)

@hOptions.command(name = "toggle")
async def hToggle(ctx):
    global remove_duplicates
    group = client.get_command("toggle")
    helpMenu = discord.Embed(
        title = group.name.capitalize(),
        description = group.help,
        color = 32639
    ).set_footer(
        text = f"""    Command prefix is {
            client.command_prefix
        }toggle
    <arg> = required parameter
    [arg] = optional parameter
    [arg (value)] = default value for optional parameter
    (command/command/command) = all aliases you can run the command with"""
    )
    for command in remove_duplicates(group.walk_commands()):
        if command.usage:
            helpMenu.add_field(
                name = "({})\n{}".format(
                    str(
                        [command.name] + command.aliases
                    )[1:-1].replace(
                        "'",
                        ""
                    ).replace(
                        ", ",
                        "/"
                    ),
                    command.usage
                ),
                value = command.help,
            )
        else:
            helpMenu.add_field(
                name = "({})".format(
                    str(
                        [command.name] + command.aliases
                    )[1:-1].replace(
                        "'",
                        ""
                    ).replace(
                        ", ",
                        "/"
                    )
                ),
                value = command.help
            )
    await ctx.send(embed = helpMenu)
print(
    "Defined toggle options menu"
)

@hOptions.command(name = "censor", aliases = ["filter"])
async def hCensor(ctx):
    group = client.get_command("censor")
    helpMenu = discord.Embed(
        title = group.name.capitalize(),
        description = group.help,
        color = 32639
    ).set_footer(
        text = f"""    Command prefix is {
            client.command_prefix
        }censor or {
            client.command_prefix
        }filter
    <arg> = required parameter
    [arg] = optional parameter
    [arg (value)] = default value for optional parameter
    (command/command/command) = all aliases you can run the command with"""
    )
    for command in remove_duplicates(group.walk_commands()):
        if command.usage:
            helpMenu.add_field(
                name = "({})\n{}".format(
                    str(
                        [command.name] + command.aliases
                    )[1:-1].replace(
                        "'",
                        ""
                    ).replace(
                        ", ",
                        "/"
                    ),
                    command.usage
                ),
                value = command.help,
            )
        else:
            helpMenu.add_field(
                name = "({})".format(
                    str(
                        [command.name] + command.aliases
                    )[1:-1].replace(
                        "'",
                        ""
                    ).replace(
                        ", ",
                        "/"
                    )
                ),
                value = command.help
            )
    await ctx.send(embed = helpMenu)
print(
    "Defined censor options menu"
)

@hOptions.command(name = "cog", aliases = ["module"])
async def hCog(ctx):
    group = client.get_command("cog")
    helpMenu = discord.Embed(
        title = group.name.capitalize(),
        description = group.help,
        color = 32639
    ).set_footer(
        text = f"""    Command prefix is {
            client.command_prefix
        }cog or {
            client.command_prefix
        }module
    <arg> = required parameter
    [arg] = optional parameter
    [arg (value)] = default value for optional parameter
    (command/command/command) = all aliases you can run the command with"""
    )
    for command in remove_duplicates(group.walk_commands()):
        if command.usage:
            helpMenu.add_field(
                name = "({})\n{}".format(
                    str(
                        [command.name] + command.aliases
                    )[1:-1].replace(
                        "'",
                        ""
                    ).replace(
                        ", ",
                        "/"
                    ),
                    command.usage
                ),
                value = command.help,
            )
        else:
            helpMenu.add_field(
                name = "({})".format(
                    str(
                        [command.name] + command.aliases
                    )[1:-1].replace(
                        "'",
                        ""
                    ).replace(
                        ", ",
                        "/"
                    )
                ),
                value = command.help
            )
    await ctx.send(embed = helpMenu)
print(
    "Defined cog options menu"
)

@client.command(name = "update", aliases = ["ud"])
async def update(ctx):
    if str(ctx.author) == "chickenmeister#7140" or str(ctx.author) == "Hyperfresh#8080":
        status = await ctx.send(
            "Updating..."
        )
        await client.change_presence(
            activity = discord.Game(
                "Updating..."
            ),
            status = discord.Status.idle
        )
        await status.edit(
            content = "Pulling the latest commits from GitHub..."
        )
        os.system(
            "bash update.bash > update.log"
        ) # fetch and pull boys. fetch and pull.
        await status.edit(
            content = f"""```{
                "".join([line for line in open("update.log", "r")][1:])
            }```
Commits pulled.
Restarting..."""
        )
        await client.change_presence(
            activity = discord.Game(
                "Restarting..."
            ),
            status = discord.Status.dnd
        )
        os.execl(
            sys.executable,
            sys.executable,
            * sys.argv
        )
    else:
        await ctx.send(
            "Hey, only my developers can do this!"
        )
print(
    "Defined update function"
)

@client.command(name = "restart", aliases = ["reload", "reboot", "rs", "rl", "rb"])
async def restart(ctx):
    if str(ctx.author) == "chickenmeister#7140" or str(ctx.author) == "Hyperfresh#8080":
        await ctx.send(
            "Restarting..."
        )
        print(
            "Restarting..."
        )
        await client.change_presence(
            activity = discord.Game(
                "Restarting..."
            ),
            status = discord.Status.dnd
        )
        os.execl(
            sys.executable,
            sys.executable,
            * sys.argv
        )
    else:
        await ctx.send(
            "Hey, only my developers can do this!"
        )
print(
    "Defined reload function"
)

# load all the cogs
for cog in os.listdir("./cogs"):
    if cog.endswith(".py"):
        client.load_extension(
            f"""cogs.{
                cog[:-3]
            }"""
        )
        print(
            f"""Loaded cog {
                cog[:-3]
            }"""
        )
print(
    "Loaded all cogs"
)

client.loop.create_task(
    statusSwitcher()
) # as defined above
print(
    "Started status switcher"
)

while True:
    try:
        client.run(
            os.getenv(
                "DISCORD_TOKEN"
            )
        )
    except KeyboardInterrupt:
        print(
            "Disconnected"
        )
        while True:
            exit(0)
    except:
        print(
            "Unable to connect to Discord"
        )
        while True:
            exit(1)