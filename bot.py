from sys import argv
import os
from asyncio import sleep
from dotenv import load_dotenv as dotenv
from random import choice, randint
from discord.ext import commands
from discord.utils import get
import sqlite3
import sys
import discord
print("Imported modules")
if len(argv) == 2:
    unstable = bool(argv[1])
elif len(argv) == 1:
    unstable = False
else:
    print("bot.py: too many arguments")
    exit()
info = r"""
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
if unstable:
    os.system(
        "toilet -w 1000 -f standard -F border -F gay Pengaelic Bot \(Unstable Dev Version\)")
else:
    os.system("toilet -w 1000 -f standard -F border -F gay Pengaelic Bot")
print(info)

dotenv("data/.env")
print("Loaded bot token")
if unstable:
    client = commands.Bot(
        command_prefix="p@",
        case_insensitive=True,
        description="Pengaelic Bot (Unstable Dev Version)",
        help_command=None,
        intents=discord.Intents.all()
    )
else:
    client = commands.Bot(
        command_prefix="p!",
        case_insensitive=True,
        description="Pengaelic Bot",
        help_command=None,
        intents=discord.Intents.all()
    )
print("Defined client")
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

    sql_create_options_table = """CREATE TABLE IF NOT EXISTS options (    id INTEGER PRIMARY KEY
                                    );"""

    sql_create_cogs_table = """CREATE TABLE IF NOT EXISTS cogs (id INTEGER PRIMARY KEY
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
    all_options = [
        "censor",
        "dadJokes",
        "JSONmenus",
        "polls",
        "welcome",
        "yoMamaJokes"
    ]
    options = guild_id + tuple([False for _ in all_options])
    marks = tuple("?" for _ in range(len(all_options) - 1))
    """
    Create a new server config set into the options table
    :param conn:
    :param server:
    :return: server id
    """
    make_columns = [
        f"""ALTER TABLE options
            ADD COLUMN {option} BIT NOT NULL DEFAULT 0;"""
        for option in all_options
    ]
    values = ["id"] + list(all_options)
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


async def status_switcher():
    global client
    await client.wait_until_ready()
    while client.is_ready:
        artist = choice([
            "Tux Penguin",
            "Qumu",
            "Robotic Wisp",
            "xGravity",
            "Nick Nitro",
            "ynk",
            "KidoKat",
            "Jesse Cook",
            "musical rock",
            "SharaX"
        ])
        game = choice([
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
        ])
        youtuber = choice([
            "Ethoslab",
            "MumboJumbo",
            "Blue Television Games",
            "The King of Random",
            "Phoenix SC"
        ])
        movie = choice([
            "Avengers: Endgame",
            "Avengers: Infinity War",
            "Star Wars Episode IV: A New Hope",
            "Spiderman: Into the Spiderverse",
            "Back to the Future"
        ])
        activities = [
            discord.Activity(
                type=discord.ActivityType.listening,
                name=artist
            ),
            discord.Game(
                name=game
            ),
            discord.Activity(
                type=discord.ActivityType.watching,
                name=movie
            ),
            discord.Activity(
                type=discord.ActivityType.watching,
                name=youtuber
            )
        ]
        activity = choice(activities)
        await client.change_presence(activity=activity)
        # task runs every few minutes (random 2-10)
        await sleep(randint(2, 10) * 60)


def remove_duplicates(inlist: list):
    return list(dict.fromkeys(inlist))


def help_menu(cog, client, ctx):
    help_menu = discord.Embed(
        title=cog.name.capitalize(),
        description=cog.description_long,
        color=32639
    ).set_footer(
        text=f"Command prefix is {client.command_prefix}\n<arg> = required parameter\n[arg] = optional parameter\n[arg (value)] = default value for optional parameter\n(command/command/command) = all aliases you can run the command with"
    )
    for command in cog.get_commands():
        if command.usage:
            help_menu.add_field(
                name="({})\n{}".format(
                    str([command.name] + command.aliases)[1:-
                                                          1].replace("'", "").replace(", ", "/"),
                    command.usage
                ),
                value=command.help
            )
        else:
            help_menu.add_field(
                name="({})".format(
                    str([command.name] + command.aliases)[1:-
                                                          1].replace("'", "").replace(", ", "/")
                ),
                value=command.help
            )
    return help_menu


@client.event
async def on_ready():
    global database
    create_database()  # just to be sure
    # create a server's configs
    for guild in client.guilds:
        with create_connection(database) as conn:
            create_options(conn, tuple([guild.id]))
    print(f"{client.description} connected to Discord")


@client.event
async def on_guild_join(guild, auto=True):
    global unstable
    if not unstable:
        global database
        print(f"Joined {guild.name}")
        welcomeembed = discord.Embed(
            title="Howdy fellas! I'm the Pengaelic Bot!",
            description=f"Type `{client.command_prefix}help` for a list of commands.",
            color=32639
        ).set_thumbnail(url=client.user.avatar_url)
        possiblechannels = [
            "general",
            "general-1",
            "general-2"
        ]
        for channel in possiblechannels:
            succ = False
            if succ:
                break
            try:
                await get(
                    guild.text_channels,
                    name=channel
                ).send(embed=welcomeembed)
                succ = True
                break
            except:
                continue
        if auto:
            # create fresh options row for new server
            create_options(create_connection(database), (guild.id))
            print(f"Options row created for {guild.name}")

if unstable == False:
    @client.event
    async def on_command_error(ctx, error):
        # this checks if the individual commands have their own error handling. if not...
        if not hasattr(ctx.command, 'on_error'):
            # ...send the global error
            if "is not found" in str(error):
                await ctx.send(f"Invalid command/usage. Type `{client.command_prefix}help` for a list of commands and their usages.")
                print(
                    "Invalid command {}{} sent in {} in #{} by {}#{}".format(
                        client.command_prefix,
                        str(error).split('"')[1],
                        ctx.guild,
                        ctx.channel,
                        ctx.message.author.name,
                        ctx.message.author.discriminator
                    )
                )
            else:
                await ctx.send(f"""Oops! An error occurred! `{error}`""")
                print(error)


@client.command(name="join", help="Show the join message if it doesn't show up automatically")
async def redo_welcome(ctx):
    await on_guild_join(ctx.guild, False)
    await ctx.message.delete()


@client.group(name="help", help="Show this message", aliases=["commands", "h", "?"])
async def help(ctx):
    global database
    if ctx.invoked_subcommand is None:
        help_menu = discord.Embed(
            title=client.description,
            description=f"""Type `{client.command_prefix}help **<lowercase category name without spaces or dashes>** for more info on each category.""",
            color=32639
        )
        cogs = dict(client.cogs)
        cogs.pop("Options")
        for cog in cogs:
            help_menu.add_field(
                name=cogs[cog].name.capitalize(),
                value=cogs[cog].description
            )
        help_menu.add_field(
            name="Options",
            value=client.get_cog("Options").description,
            inline=False
        ).add_field(
            name="Links",
            value=f"My official [support server](https://discord.gg/DHHpA7k)\n[Invite me](https://discord.com/oauth2/authorize?client_id=721092139953684580&permissions=388176&scope=bot) to your own server\nMy [GitHub repo](https://github.com/SuperTux20/Pengaelic-Bot)",
            inline=False
        )
        await ctx.send(embed=help_menu)


@help.command(name="actions")
async def h_actions(ctx):
    await ctx.send(embed=help_menu(client.get_cog("Actions"), client, ctx))


@help.command(name="actsofviolence")
async def h_actsofviolence(ctx):
    await ctx.send(embed=help_menu(client.get_cog("ActsOfViolence"), client, ctx))


@help.command(name="converters")
async def h_converters(ctx):
    await ctx.send(embed=help_menu(client.get_cog("Converters"), client, ctx))


@help.command(name="games")
async def h_games(ctx):
    await ctx.send(embed=help_menu(client.get_cog("Games"), client, ctx))


@help.command(name="generators")
async def h_games(ctx):
    await ctx.send(embed=help_menu(client.get_cog("Generators"), client, ctx))


@help.command(name="interactions")
async def h_interactions(ctx):
    await ctx.send(embed=help_menu(client.get_cog("Interactions"), client, ctx))


@help.command(name="messages")
async def h_messages(ctx):
    await ctx.send(embed=help_menu(client.get_cog("Messages"), client, ctx))


@help.command(name="tools")
async def h_tools(ctx):
    await ctx.send(embed=help_menu(client.get_cog("Tools"), client, ctx))


@help.command(name="oddcommands")
async def h_oddcommands(ctx):
    await ctx.send(embed=help_menu(client.get_cog("OddCommands"), client, ctx))


@help.group(name="options")
async def h_options(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(embed=help_menu(client.get_cog("Options"), client, ctx))


@help.command(name="noncommands")
async def h_noncommands(ctx):
    cog = client.get_cog("NonCommands")
    await ctx.send(
        embed=discord.Embed(
            title=cog.name.capitalize(),
            description=cog.description_long,
            color=32639
        ).add_field(
            name="I'm <message>",
            value="Like Dad Bot!"
        ).add_field(
            name="Yo mama so <mama type>",
            value="Automatic Yo Mama jokes!"
        ).add_field(
            name="Yo mama list",
            value="Show the list of mama types to use in the auto-joker."
        ).add_field(
            name="You know the rules",
            value="A rickroll-themed Russian Roulette."
        )
    )


@h_options.command(name="toggle")
async def h_toggle(ctx):
    global remove_duplicates
    group = client.get_command("toggle")
    help_menu = discord.Embed(
        title=group.name.capitalize(),
        description=group.help,
        color=32639
    ).set_footer(
        text=f"Command prefix is {client.command_prefix}toggle\n<arg> = required parameter\n[arg] = optional parameter\n[arg (value)] = default value for optional parameter\n(command/command/command) = all aliases you can run the command with"
    )
    for command in remove_duplicates(group.walk_commands()):
        if command.usage:
            help_menu.add_field(
                name="({})\n{}".format(
                    str([command.name] + command.aliases)[1:-
                                                          1].replace("'", "").replace(", ", "/"),
                    command.usage
                ),
                value=command.help
            )
        else:
            help_menu.add_field(
                name="({})".format(
                    str([command.name] + command.aliases)[1:-1].replace("'", "").replace(", ", "/")),
                value=command.help
            )
    await ctx.send(embed=help_menu)


@h_options.command(name="censor", aliases=["filter"])
async def h_censor(ctx):
    group = client.get_command("censor")
    help_menu = discord.Embed(
        title=group.name.capitalize(),
        description=group.help,
        color=32639
    ).set_footer(
        text=f"Command prefix is {client.command_prefix}censor or {client.command_prefix}filter\n<arg> = required parameter\n[arg] = optional parameter\n[arg (value)] = default value for optional parameter\n(command/command/command) = all aliases you can run the command with"
    )
    for command in remove_duplicates(group.walk_commands()):
        if command.usage:
            help_menu.add_field(
                name="({})\n{}".format(
                    str([command.name] + command.aliases)[1:-
                                                          1].replace("'", "").replace(", ", "/"),
                    command.usage
                ),
                value=command.help
            )
        else:
            help_menu.add_field(
                name="({})".format(
                    str([command.name] + command.aliases)[1:-
                                                          1].replace("'", "").replace(", ", "/")
                ),
                value=command.help)
    await ctx.send(embed=help_menu)


@client.command(name="update", aliases=["ud"])
async def update(ctx):
    if str(ctx.author) == "chickenmeister#7140" or str(ctx.author) == "Hyperfresh#8080":
        status = await ctx.send("Updating...")
        await client.change_presence(
            activity=discord.Game("Updating..."),
            status=discord.Status.idle
        )
        await status.edit(content="Pulling the latest commits from GitHub...")
        # fetch and pull, boys. fetch and pull.
        os.system("bash update.sh > update.log")
        update_log = [line for line in open("update.log", "r")][1:]
        # special status for when there's no update :o (aka me being lazy lmao)
        if update_log == ["Already up to date.\n"]:
            await status.edit(content="Already up to date, no restart required.")
            await client.change_presence(
                activity=discord.Game("Factory Idle"),
                status=discord.Status.online
            )
        else:
            update_log = update_log[2:]
            await status.edit(content=f"""
```fix
 {"".join(update_log[:-1])[1:-1]}
```
```ini
[ {update_log[-1][:-1]} ]
```
Commits pulled.
Restarting...
""")
            await client.change_presence(
                activity=discord.Game("Restarting..."),
                status=discord.Status.dnd
            )
            os.execl(
                sys.executable,
                sys.executable,
                * sys.argv
            )
    else:
        await ctx.send("Hey, only my developers can do this!")


@client.command(name="restart", aliases=["reload", "reboot", "rs", "rl", "rb"])
async def restart(ctx):
    if str(ctx.author) == "chickenmeister#7140" or str(ctx.author) == "Hyperfresh#8080":
        await ctx.send("Restarting...")
        print("Restarting...")
        await client.change_presence(
            activity=discord.Game("Restarting..."),
            status=discord.Status.dnd
        )
        os.execl(
            sys.executable,
            sys.executable,
            * sys.argv
        )
    else:
        await ctx.send("Hey, only my developers can do this!")


@client.command(name="exit", aliases=["quit"])
async def restart(ctx):
    if str(ctx.author) == "chickenmeister#7140" or str(ctx.author) == "Hyperfresh#8080":
        await ctx.send("Goodbye...")
        exit(0)
    else:
        await ctx.send("Hey, only my developers can do this!")

# load all the cogs
for cog in os.listdir("cogs"):
    if cog.endswith(".py"):
        client.load_extension(f"cogs.{cog[:-3]}")
        print(f"Loaded cog {cog[:-3]}")

client.loop.create_task(status_switcher())  # as defined above

while True:
    try:
        client.run(os.getenv("DISCORD_TOKEN"))
    except KeyboardInterrupt:
        print("Disconnected")
        while True:
            exit(0)
    except:
        print("Unable to connect to Discord")
        while True:
            exit(1)
