import os
info = """
 ____________
| ___| | | | |
|| | |\|_| | |
||_|_|    \| |
| ________  \|
| \_______|  |
|__\______|__|

Pengaelic Bot - the custom-built Discord bot, coded in Python
Copyright (C) 2020 Tux Penguin | https://github.com/SuperTux20/Pengaelic-Bot/

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

"""
os.system("toilet -f standard -F border -F gay Pengaelic Bot")
print(info)
import discord
import sys
import sqlite3
from json import load
from fnmatch import filter
from discord.utils import get
from discord.ext import commands
from random import choice, randint
from dotenv import load_dotenv as dotenv
from asyncio import sleep
from time import sleep as realsleep
print(
    "Imported modules"
)

dotenv(
    "data/.env"
)
print(
    "Loaded bot token"
)
connected = False
client = commands.Bot(
    command_prefix = "p!",
    case_insensitive = True,
    description = "Pengaelic Bot",
    help_command = None,
    intents = discord.Intents.all()
)
print(
    "Defined client"
)
database = "data/config.db"
def create_connection(database):
    """ create a database connection to a SQLite database """
    conn = sqlite3.connect(database)
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    cur = conn.cursor()
    cur.execute(create_table_sql)

def create_database():
    global database

    sql_create_options_table = """CREATE TABLE IF NOT EXISTS options (
                                    id INTEGER PRIMARY KEY
                                    );"""

    sql_create_cogs_table = """CREATE TABLE IF NOT EXISTS cogs (
                                id INTEGER PRIMARY KEY
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create options table
        create_table(conn, sql_create_options_table)

        # create cogs table
        create_table(conn, sql_create_cogs_table)
    else:
        raise sqlite3.DatabaseError("Cannot create the database connection.")

def create_options(conn, guild_id):
    all_options = {
        "censor": True,
        "dadJokes": False,
        "polls": False,
        "welcome": True,
        "yoMamaJokes": False
    }
    options = guild_id + tuple(all_options.values())
    marks = tuple("?" for _ in range(len(all_options) - 1))
    """
    Create a new server config set into the options table
    :param conn:
    :param server:
    :return: server id
    """
    make_columns = [
        f"""ALTER TABLE options
            ADD COLUMN {option} BIT NOT NULL DEFAULT {int(all_options[option])};"""
            for option in all_options
    ]
    values = ["id"] + list(all_options.keys())
    add_values = f"""INSERT INTO options {str(tuple(values)).replace("'", "")}
                VALUES{str(marks + ("?", "?")).replace("'", "")}"""
    cur = conn.cursor()
    for make in make_columns:
        try:
            cur.execute(make)
            conn.commit()
        except sqlite3.OperationalError:
            pass
    try:
        cur.execute(add_values, options)
    except sqlite3.IntegrityError:
        pass
    conn.commit()

def create_cogs(conn, guild_id):
    all_cogs = {
        cog[1:-3]: cog[0]
        for cog in os.listdir("cogs") if cog[-3:] == ".py"
    }
    cog_defaults = [
        True,
        False,
        True,
        True,
        True,
        True,
        True,
        True,
        False,
        True,
        True,
        True
    ]
    cogs = guild_id + tuple(cog_defaults)
    all_cogs.pop("options")
    marks = tuple(
        "?"
        for _ in range(len(all_cogs) - 1)
    )
    """
    Create a new cogs config set into the cogs table
    :param conn:
    :param cogs:
    :return: server id
    """
    make_columns = [
        f"""ALTER TABLE cogs
            ADD COLUMN {cog} BIT NOT NULL DEFAULT {all_cogs[cog]};"""
            for cog in all_cogs
    ]
    values = ["id"] + list(all_cogs.keys())
    add_values = f"""INSERT INTO cogs{str(tuple(values)).replace("'", "")}
                VALUES{str(marks + ("?", "?")).replace("'", "")}"""
    cur = conn.cursor()
    for make in make_columns:
        try:
            cur.execute(make)
        except sqlite3.OperationalError:
            pass
    try:
        cur.execute(add_values, cogs)
    except sqlite3.IntegrityError:
        pass
    conn.commit()

def create_channels(conn, guild_id):
    channel_possibilities = {
        "welcome": [
            "welcome",
            "arrivals",
            "entrance",
            "entry",
            "join",
            "log",
            "lobby",
            "general"
        ],
        "leave": [
            "leave",
            "goodbye",
            "exit",
            "log",
            "lobby",
            "general"
        ],
        "suggestions": [
            "poll",
            "petition",
            "suggest",
            "suggestion",
            "suggestions",
            "server-suggestions",
            "vote",
            "voting"
        ],
        "commands": [
            "bot-commands",
            "commands",
            "bots"
        ]
    }
    possiblechannels = [
        filter(
            [
                channel.name
                for channel in message.guild.text_channels
            ],
            f"*{channel}*"
        )
        for channel in list(channel_possibilities.values())
    ]
    sadf = [
        channel
        for channel in possiblechannels
    ]
    options = guild_id + tuple(channel_possibilities.values())
    marks = tuple("?" for _ in range(len(channel_possibilities) - 1))
    """
    Create a new server config set into the options table
    :param conn:
    :param server:
    :return: server id
    """
    make_columns = [
        f"""ALTER TABLE channels
            ADD COLUMN {channel} NVARCHAR NOT NULL DEFAULT {int(channel_possibilities[option])};"""
            for channel in channel_possibilities
    ]
    values = ["id"] + list(channel_possibilities.keys())
    add_values = f"""INSERT INTO options {str(tuple(values)).replace("'", "")}
                VALUES{str(marks + ("?", "?")).replace("'", "")}"""
    cur = conn.cursor()
    for make in make_columns:
        try:
            cur.execute(make)
            conn.commit()
        except sqlite3.OperationalError:
            pass
    try:
        cur.execute(add_values, options)
    except sqlite3.IntegrityError:
        pass
    conn.commit()

def get_options(database, table, guild):
    conn = sqlite3.connect(
        database
    )
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    rows = cur.execute(
        f"SELECT * from {table}"
    ).fetchall()

    conn.commit()
    conn.close()

    currentserver = [
        server
        for server in [
            dict(index)
            for index in rows
        ]
        if server["id"] == guild
    ][0]

    currentserver.pop(
        "id"
    )

    return currentserver

async def status_switcher():
    global client
    await client.wait_until_ready()
    while client.is_ready:
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

def remove_duplicates(inlist: list):
    return list(dict.fromkeys(inlist))

@client.event
async def on_ready():
    global connected
    global database
    create_database() # just to be sure
    for guild in client.guilds:
        conn = create_connection(database)
        with conn:
            # create a server's configs
            create_options(conn, tuple([guild.id]))
            create_cogs(conn, tuple([guild.id]))
    print("Loaded all configs")
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

@client.event
async def on_guild_join(guild, ctx = None):
    global database
    print(
        f"""Joined {
            guild.name
        }"""
    )
    welcomeembed = discord.Embed(
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
        "living-room",
        "lobby",
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
                    embed = welcomeembed
                )
                break
            except:
                continue

    # create fresh options row for new server
    conn = create_connection(database)
    with conn:
        # create a server's configs
        options = (guild.id)
        create_options(conn, options)
        # cogs
        cogs = (guild.id)
        create_cogs(conn, cogs)
    print(
        f"""Options row created for {
            guild.name
        }"""
    )

@client.event
async def on_command_error(ctx, error):
    # this checks if the individual commands have their own error handling. if not...
    if not hasattr(ctx.command, 'on_error'):
        # ...send the global error
        if "is not found" in str(error):
            await ctx.send(
                f"""Invalid command/usage. Type `{
                    client.command_prefix
                }help` for a list of commands and their usages."""
            )
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
            await ctx.send(
                f"""Oops! An error occurred! `{
                    error
                }`"""
            )
            print(
                error
            )

@client.command(name = "join", help = "Show the join message if it doesn't show up automatically")
async def redo_welcome(ctx):
    await on_guild_join(
        ctx.guild, ctx.channel
    )
    await ctx.message.delete()

@client.group(name = "help", help = "Show this message", aliases = ["commands", "h", "?"])
async def help(ctx):
    global database
    if ctx.invoked_subcommand is None:
        help_menu = discord.Embed(
            title = client.description,
            description = f"""Type `{
                client.command_prefix
            }help **<lowercase category name without spaces or dashes>** for more info on each category.""",
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
        cogs = dict(client.cogs)
        cogs.pop("Options")
        for cog in cogs:
            if get_options(database, "cogs", ctx.guild.id)[cogs[cog].name_typable] == True:
                help_menu.add_field(
                    name = cogs[cog].name.capitalize(),
                    value = cogs[cog].description
                )
        help_menu.add_field(
            name = "Options",
            value = client.get_cog(
                "Options"
            ).description
        )
        await ctx.send(embed = help_menu)

@help.command(name = "actions")
async def h_actions(ctx):
    if get_options(database, "cogs", ctx.guild.id)["actions"] == True:
        cog = client.get_cog("Actions")
        help_menu = discord.Embed(
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
            help_menu.add_field(
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
        await ctx.send(embed = help_menu)
    else:
        await ctx.send(f"This module is disabled. Type `{client.command_prefix}cog load actions` to enable it.")

@help.command(name = "actsofviolence")
async def h_actsofviolence(ctx):
    if get_options(database, "cogs", ctx.guild.id)["actsofviolence"] == True:
        cog = client.get_cog("ActsOfViolence")
        help_menu = discord.Embed(
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
            help_menu.add_field(
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
        await ctx.send(embed = help_menu)
    else:
        await ctx.send(f"This module is disabled. Type `{client.command_prefix}cog load actsofviolence` to enable it.")

@help.command(name = "converters")
async def h_converters(ctx):
    if get_options(database, "cogs", ctx.guild.id)["converters"] == True:
        cog = client.get_cog("Converters")
        help_menu = discord.Embed(
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
            help_menu.add_field(
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
        await ctx.send(embed = help_menu)
    else:
        await ctx.send(f"This module is disabled. Type `{client.command_prefix}cog load converters` to enable it.")

@help.command(name = "games")
async def h_games(ctx):
    if get_options(database, "cogs", ctx.guild.id)["games"] == True:
        cog = client.get_cog("Games")
        help_menu = discord.Embed(
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
                help_menu.add_field(
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
                help_menu.add_field(
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
        await ctx.send(embed = help_menu)
    else:
        await ctx.send(f"This module is disabled. Type `{client.command_prefix}cog load games` to enable it.")

@help.command(name = "interactions")
async def h_interactions(ctx):
    if get_options(database, "cogs", ctx.guild.id)["interactions"] == True:
        cog = client.get_cog("Interactions")
        help_menu = discord.Embed(
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
            help_menu.add_field(
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
        await ctx.send(embed = help_menu)
    else:
        await ctx.send(f"This module is disabled. Type `{client.command_prefix}cog load interactions` to enable it.")

@help.command(name = "messages")
async def h_messages(ctx):
    if get_options(database, "cogs", ctx.guild.id)["messages"] == True:
        cog = client.get_cog("Messages")
        help_menu = discord.Embed(
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
                help_menu.add_field(
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
                help_menu.add_field(
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
        await ctx.send(embed = help_menu)
    else:
        await ctx.send(f"This module is disabled. Type `{client.command_prefix}cog load messages` to enable it.")

@help.command(name = "noncommands")
async def h_noncommands(ctx):
    if get_options(database, "cogs", ctx.guild.id)["noncommands"] == True:
        cog = client.get_cog("NonCommands")
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

@help.command(name = "tools")
async def h_tools(ctx):
    if get_options(database, "cogs", ctx.guild.id)["tools"] == True:
        cog = client.get_cog("Tools")
        help_menu = discord.Embed(
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
                help_menu.add_field(
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
                help_menu.add_field(
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
        await ctx.send(embed = help_menu)
    else:
        await ctx.send(f"This module is disabled. Type `{client.command_prefix}cog load tools` to enable it.")

@help.command(name = "oddcommands")
async def h_oddcommands(ctx):
    if get_options(database, "cogs", ctx.guild.id)["oddcommands"] == True:
        cog = client.get_cog("OddCommands")
        help_menu = discord.Embed(
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
                help_menu.add_field(
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
                help_menu.add_field(
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
        await ctx.send(embed = help_menu)
    else:
        await ctx.send(f"This module is disabled. Type `{client.command_prefix}cog load oddcommands` to enable it.")

@help.group(name = "options")
async def h_options(ctx):
    if ctx.invoked_subcommand is None:
        cog = client.get_cog("Options")
        help_menu = discord.Embed(
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
                help_menu.add_field(
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
                help_menu.add_field(
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
        await ctx.send(embed = help_menu)

@h_options.command(name = "toggle")
async def h_toggle(ctx):
    global remove_duplicates
    group = client.get_command("toggle")
    help_menu = discord.Embed(
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
            help_menu.add_field(
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
            help_menu.add_field(
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
    await ctx.send(embed = help_menu)

@h_options.command(name = "censor", aliases = ["filter"])
async def h_censor(ctx):
    group = client.get_command("censor")
    help_menu = discord.Embed(
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
            help_menu.add_field(
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
            help_menu.add_field(
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
    await ctx.send(embed = help_menu)

@h_options.command(name = "cog", aliases = ["module"])
async def h_cog(ctx):
    group = client.get_command("cog")
    help_menu = discord.Embed(
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
            help_menu.add_field(
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
            help_menu.add_field(
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
    await ctx.send(embed = help_menu)

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
        ) # fetch and pull, boys. fetch and pull.
        update_log = [line for line in open("update.log", "r")][1:]
        if update_log == ["Already up to date.\n"]:
            await status.edit(
                content = "Already up to date, no restart required."
            )
            await client.change_presence(
                activity = discord.Game(
                    "Factory Idle" # special status for when there's no update :o
                ),
                status = discord.Status.online
            )
        else:
            update_log = update_log[2:]
            await status.edit(
                content = f"""
```fix
 {"".join(update_log[:-1])[1:-1]}
```
```ini
[{update_log[-1][:-1]} ]
```
Commits pulled.
Restarting...
"""
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

# load all the cogs
for cog in os.listdir("cogs"):
    if cog.endswith(".py"):
        client.load_extension(
            f"""cogs.{
                cog[:-3]
            }"""
        )
        print(
            f"""Loaded cog {
                cog[1:-3]
            }"""
        )

client.loop.create_task(
    status_switcher()
) # as defined above

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
