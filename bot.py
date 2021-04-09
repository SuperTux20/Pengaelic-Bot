import os
import sqlite3
import subprocess
import sys
from asyncio import sleep
from json import loads, dumps
from pengaelicutils import options, remove_duplicates
from platform import node as hostname
from random import choice, randint
print("Imported modules")

devnull = open(os.devnull, "w")
requirements = ["fortune-mod", "fortunes", "fortunes-min", "neofetch", "toilet", "toilet-fonts"]
need2install = False
for package in requirements:
    if subprocess.call(["dpkg", "-s", package], stdout=devnull, stderr=subprocess.STDOUT):
        print(f"Package {package} not installed.")
        need2install = True
devnull.close()
if need2install:
    print("Install these with APT.")
    exit()
print("Passed package test")

requirements = ["discord.py", "python-dotenv", "num2words"]
modules = [
    r.decode().split('==')[0]
    for r in subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).split()
]
need2install = False
for module in requirements:
    if module not in modules:
        print(f"Module {module} not installed.")
        need2install = True
if need2install:
    print("Install these with Pip.")
    exit()
print("Passed module test")
import discord
from dotenv import load_dotenv as dotenv
from discord.utils import get
from discord.ext import commands

if any(tuxPC in hostname() for tuxPC in ["Mintguin", "Winguin", "Pengwindows"]):
    unstable = True
else:
    unstable = False
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
database = "config.db"


def create_database():
    global database
    conn = sqlite3.connect(database)
    conn.cursor().execute(
        "CREATE TABLE IF NOT EXISTS options (id INTEGER PRIMARY KEY);"
    )


def create_options(conn, guild_id):
    all_options = [
        "censor",
        "dadJokes",
        "deadChat",
        "jsonMenus",
        "rickRoulette",
        "suggestions",
        "welcome"
    ]
    options = guild_id + tuple([False for _ in all_options])
    marks = tuple("?" for _ in range(len(all_options) - 1))
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
        cur.execute(
            add_values,
            options
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    try:
        cur.execute(
            f"""ALTER TABLE options
                ADD COLUMN censorlist TEXT;"""
        )
        conn.commit()
    except sqlite3.OperationalError:
        pass


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
        moviesyt = choice([
            "Ethoslab",
            "MumboJumbo",
            "Blue Television Games",
            "The King of Random",
            "Phoenix SC",
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
            discord.Activity(
                type=discord.ActivityType.playing,
                name=game
            ),
            discord.Activity(
                type=discord.ActivityType.watching,
                name=moviesyt
            )
        ]
        activity = choice(activities)
        await client.change_presence(activity=activity)
        # task runs every few minutes (random 2-10)
        await sleep(randint(2, 10) * 60)


def help_menu(cog, client, ctx):
    menu = discord.Embed(
        title=cog.name.capitalize(),
        description=cog.description_long,
        color=32639
    ).set_footer(
        text=f"Command prefix is {client.command_prefix}\n<arg> = required parameter\n[arg] = optional parameter\n[arg (value)] = default value for optional parameter\n(command/command/command) = all aliases you can run the command with"
    )
    for command in cog.get_commands():
        if command.usage:
            menu.add_field(
                name="({})\n{}".format(
                    str([command.name] + command.aliases)[1:-
                                                          1].replace("'", "").replace(", ", "/"),
                    command.usage
                ),
                value=command.help
            )
        else:
            menu.add_field(
                name="({})".format(
                    str([command.name] + command.aliases)[1:-
                                                          1].replace("'", "").replace(", ", "/")
                ),
                value=command.help
            )
    return menu


@client.event
async def on_ready():
    global database
    create_database()  # just to be sure
    # create a server's configs
    for guild in client.guilds:
        with sqlite3.connect(database) as conn:
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
            create_options(sqlite3.connect(database), (guild.id))
            print(f"Options row created for {guild.name}")

if not unstable:
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
                await ctx.send(f"Unhandled error occurred:```{error}```If my developer (<@!686984544930365440>) is not here, please tell him what the error is so that he can add handling or fix the issue!")


@client.command(name="join", help="Show the join message if it doesn't show up automatically")
async def redo_welcome(ctx):
    await on_guild_join(ctx.guild, False)
    await ctx.message.delete()


# load token
dotenv(".env")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# load all developer user IDs
class developers():
    everyone = loads(os.getenv("DEVELOPER_IDS"))

# function to make testing if someone's a dev easier
def developer(user, dev=None):
    if dev == None:
        if user.id in list(developers.everyone.values()):
            return True
        else:
            return False
    else:
        if user.id == developers.everyone[dev]:
            return True
        else:
            return False


print("Loaded bot token and developer IDs")


@client.command(name="exit", aliases=["quit"])
async def restart(ctx):
    if ctx.author.id in developers.everyone:
        await ctx.send("Goodbye...")
        exit(0)
    else:
        await ctx.send("Hey, only my developers can do this!")

if not unstable:
    @client.command(name="restart", aliases=["reload", "reboot", "rs", "rl", "rb"])
    async def restart(ctx):
        if developer(ctx.author):
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

    @client.command(name="update", aliases=["ud"])
    async def update(ctx):
        if developer(ctx.author):
            status = await ctx.send("Updating...")
            await client.change_presence(
                activity=discord.Game("Updating..."),
                status=discord.Status.idle
            )
            await status.edit(content="Pulling the latest commits from GitHub...")
            os.system("bash update.sh > update.log")
            update_log = [line for line in open("update.log", "r")][1:]
            if "Already up to date.\n" in update_log:
                await status.edit(content="Already up to date, no restart required.")
                await status_switcher()
            else:
                update_log = update_log[2:]
                if options(ctx.guild.id, "jsonMenus"):
                    update_summary = update_log[-1][1:-1]
                    update_log = {
                        str(update_log[:-1]).split("|")[0][3:]: str(update_log[:-1]).split("|")[1][:-4]
                        for _ in str(update_log[:-1]).split("\n")
                    }
                    await status.edit(content=f'```json\n"{update_summary}": {dumps(update_log, indent=4)}```')
                else:
                    update_summary = update_log[-1][:-1]
                    update_log = update_log[2:-1]
                    await status.edit(embed=discord.Embed(title="Updating...", description=update_log, color=32639).set_footer(text=update_summary))
                await restart(ctx)
        else:
            await ctx.send("Hey, only my developers can do this!")
# so close nwo
    @update.error
    async def update_error(ctx, error):
        await ctx.send(f"An error occured while updating: ```{error}```")

    @client.command(name="forceupdate", aliases=["fud"])
    async def forceupdate(ctx):
        if developer(ctx.author):
            await ctx.send("Updating...")
            await client.change_presence(
                activity=discord.Game("Updating..."),
                status=discord.Status.idle
            )
            os.system("bash update.sh > update.log")
            await restart(ctx)
        else:
            await ctx.send("Hey, only my developers can do this!")


@client.group(name="help", help="Show this message", aliases=["commands", "h", "?"])
async def help(ctx, *, cogname: str = None):
    if cogname == None:
        menu = discord.Embed(
            title=client.description,
            description=f"Type `{client.command_prefix}help **<lowercase category name without spaces or dashes>** for more info on each category.",
            color=32639
        )
        cogs = dict(client.cogs)
        cogs.pop("Options")
        cogs.pop("NonCommands")
        for cog in cogs:
            menu.add_field(
                name=cogs[cog].name.capitalize(),
                value=cogs[cog].description
            )
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            menu.add_field(
                name="Options",
                value=client.get_cog("Options").description,
                inline=False
            )
        if developer(ctx.author):
            menu.add_field(
                name="Control",
                value="Update, restart, that sort of thing.",
                inline=False
            )
        menu.add_field(
            name="Links",
            value=f"My official [support server](https://discord.gg/DHHpA7k)\n[Invite me](https://discord.com/oauth2/authorize?client_id=721092139953684580&permissions=388176&scope=bot) to your own server\nMy [GitHub repo](https://github.com/SuperTux20/Pengaelic-Bot)",
            inline=False
        )
        await ctx.send(embed=menu)
    elif cogname == "all":
        menu = discord.Embed(
            title=client.description,
            description="ALL COMMANDS across ALL MODULES for the ENTIRE BOT",
            color=32639
        )
        cogs = dict(client.cogs)
        cogs.pop("NonCommands")
        for cog in cogs:
            menu.add_field(
                name=dict(client.cogs)[cog].name.capitalize(),
                value=str(
                    [
                        command.qualified_name
                        for command in dict(client.cogs)[cog].walk_commands()
                    ]
                )[1:-1].replace("'", "").replace(", ", "\n")
            )
        await ctx.send(embed=menu)
    elif cogname == "control" and developer(ctx.author):
        menu = discord.Embed(
            title="Control",
            description="Commands for developers to control the bot itself.",
            color=32639
        ).add_field(
            name="exit",
            value="Shut off the bot."
        ).add_field(
            name="restart",
            value="Reload the bot."
        ).add_field(
            name="update",
            value="Check if there's new commits on GitHub, and if there are, pull them and restart."
        ).add_field(
            name="forceupdate",
            value="Same as update, but it always restarts regardless of what the update log says, because I'm sure I fucked up the regular update command somehow."
        )
        await ctx.send(embed=menu)
    else:
        await ctx.send(embed=help_menu(client.get_cog(cogname.capitalize()), client, ctx))


@help.error
async def not_a_cog(ctx, error):
    if str(error) == "AttributeError: 'NoneType' object has no attribute 'name'":
        await ctx.send("There isn't a help menu for that.")


@help.command(name="toggle")
async def h_toggle(ctx):
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


@help.command(name="censor", aliases=["filter"])
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


client.loop.create_task(status_switcher())  # as defined above

# load all the cogs
for cog in os.listdir("cogs"):
    if cog.endswith(".py"):
        client.load_extension(f"cogs.{cog[:-3]}")
        print(f"Loaded cog {cog[:-3]}")

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
