# -*- coding: utf-8 -*-

import subprocess
import sys
from asyncio import sleep
from json import loads, dumps
from os import system as cmd, getenv as env, listdir as ls, execl, devnull
from pengaelicutils import newops, getops, remove_duplicates, list2str
from platform import node as hostname
from random import choice, randint
print("Imported modules")

devnull = open(devnull, "w")
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

requirements = ["discord.py", "num2words", "python-dotenv", "speedtest-cli", "tinydb"]
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
    print("Installing...")
    subprocess.check_output([sys.executable, '-m', 'pip', 'install'] + requirements)
    print("Done.")
print("Passed module test")
import discord
from dotenv import load_dotenv as dotenv
from discord.utils import get
from discord.ext import commands
from tinydb import TinyDB

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
    cmd(r"toilet -w 1000 -f standard -F border -F gay Pengaelic Bot \(Unstable Dev Version\)")
else:
    cmd("toilet -w 1000 -f standard -F border -F gay Pengaelic Bot")
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
db = TinyDB("config.json")

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
        activity = choice([
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
        ])
        await client.change_presence(activity=activity)
        # task runs every few minutes (random 2-10)
        await sleep(randint(2, 10) * 60)


def help_menu(cog, client):
    menu = discord.Embed(
        title=cog.name.capitalize(),
        description=cog.description_long,
        color=0x007f7f
    ).set_footer(
        text=f"Command prefix is {client.command_prefix}\n<arg> = required parameter\n[arg] = optional parameter\n[arg (value)] = default value for optional parameter\n(command/command/command) = all aliases you can run the command with"
    )
    for command in cog.get_commands():
        if command.usage:
            menu.add_field(
                name="({})\n{}".format(
                    str([command.name] + command.aliases)[1:-1].replace("'", "").replace(", ", "/"),
                    command.usage
                ),
                value=command.help
            )
        else:
            menu.add_field(
                name="({})".format(
                    str([command.name] + command.aliases)[1:-1].replace("'", "").replace(", ", "/")
                ),
                value=command.help
            )
    return menu


@client.event
async def on_ready():
    global db
    # create a server's configs
    if db.all() == []:
        db.insert({guild.id: newops() for guild in client.guilds})
    print(f"{client.description} connected to Discord")

@client.event
async def on_guild_join(guild, auto=True):
    global unstable
    if not unstable:
        print(f"Joined {guild.name}")
        welcomeembed = discord.Embed(
            title="Howdy fellas! I'm the Pengaelic Bot!",
            description=f"Type `{client.command_prefix}help` for a list of commands.",
            color=0x007f7f
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
            db.update({guild.id: newops()})
            print(f"Options row created for {guild.name}")

# if not unstable:
#     @client.event
#     async def on_command_error(ctx, error):
#         # this checks if the individual commands have their own error handling. if not...
#         if not hasattr(ctx.command, 'on_error'):
#             # ...send the global error
#             if "is not found" in str(error):
#                 await ctx.send(f"Invalid command/usage. Type `{client.command_prefix}help` for a list of commands and their usages.")
#                 print(
#                     "Invalid command {}{} sent in {} in #{} by {}#{}".format(
#                         client.command_prefix,
#                         str(error).split('"')[1],
#                         ctx.guild,
#                         ctx.channel,
#                         ctx.message.author.name,
#                         ctx.message.author.discriminator
#                     )
#                 )
#             else:
#                 await ctx.send(f"Unhandled error occurred:```{error}```If my developer (<@!686984544930365440>) is not here, please tell him what the error is so that he can add handling or fix the issue!")

@client.command(name="join", help="Show the join message if it doesn't show up automatically")
async def redo_welcome(ctx):
    await on_guild_join(ctx.guild, False)
    await ctx.message.delete()

# load token
dotenv(".env")
DISCORD_TOKEN = env("DISCORD_TOKEN")

# load all developer user IDs
class developers():
    everyone = loads(env("DEVELOPER_IDS"))

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
            execl(
                sys.executable,
                sys.executable,
                * sys.argv
            )
        else:
            await ctx.send("Hey, only my developers can do this!")

    @client.command(name="updatelog", aliases=["ul"])
    async def updatelog(ctx, formatted=True, status: discord.Message=None):
        if developer(ctx.author):
            if getops(ctx.guild.id, "toggles", "jsonMenus"):
                if status:
                    await status.edit(content="Looking in the logs...")
                else:
                    status = await ctx.send("Looking in the logs...")
                update_log = [line.replace("\n","") for line in open("update.log", "r")][1:]
                if formatted:
                    if "A" == update_log[0][0]:
                        await status.edit(content=f'```json\n"{list2str(update_log[0][:-1].split()[1:], 2)}": true```')
                        return False
                    update_summary = update_log[-1]
                    update_log = update_log[2:-1]
                    update_summary = update_summary.split(", ")
                    update_summary = [{"files changed": int(update_summary[0][1:].split()[0])}, {"insertions": int(update_summary[1][:-3].split()[0]), "deletions": int(update_summary[2][:-3].split()[0])}]
                    for item in range(len(update_log)):
                        while "  " in update_log[item]:
                            update_log[item] = update_log[item].replace("  ", " ")
                    update_log = {
                        update_log[item].split("|")[0].replace(" ", ""): update_log[item].split("|")[1][1:]
                        for item in range(len(update_log))
                    }
                    await status.edit(content=f'```json\n"summary": {dumps(update_summary, indent=4)},\n"changes": {dumps(update_log, indent=4)}```')
                else:
                    await ctx.send(f'Raw log contents```{open("update.log", "r").read()}```')
            else:
                if status:
                    await status.edit(embed=discord.Embed(title="Looking in the logs...", color=0x007f7f))
                else:
                    status = await ctx.send(embed=discord.Embed(title="Looking in the logs...", color=0x007f7f))
                update_log = [line.replace("\n","") for line in open("update.log", "r")][1:]
                await status.edit(embed=discord.Embed(title=update_log[0], color=0x007f7f))
                if formatted:
                    if "A" == update_log[0][0]:
                        return False
                    else:
                        update_summary = update_log[-1]
                        update_log = update_log[1:-1]
                        await status.edit(embed=discord.Embed(title=update_log[0], description=list2str(update_log, 3), color=0x007f7f).set_footer(text=update_summary))
                else:
                    await status.delete()
                    await ctx.send(embed=discord.Embed(title="Raw log contents", description=open("update.log", "r").read(), color=0xff0000))
            return True
        else:
            await ctx.send("Hey, only my developers can do this!")
            return False

    @client.command(name="update", aliases=["ud"])
    async def update(ctx, force=False):
        if developer(ctx.author):
            if getops(ctx.guild.id, "toggles", "jsonMenus"):
                status = await ctx.send("Pulling the latest commits from GitHub...")
            else:
                status = await ctx.send(embed=discord.Embed(title="Pulling the latest commits from GitHub...", color=0x007f7f))
            await client.change_presence(
                activity=discord.Game("Updating..."),
                status=discord.Status.idle
            )
            cmd("bash update.sh > update.log")
            if force:
                await restart(ctx)
            else:
                if await updatelog(ctx, True, status):
                    await restart(ctx)
        else:
            await ctx.send("Hey, only my developers can do this!")

    @update.error
    async def update_error(ctx, error):
        await ctx.send(f"An error occured while updating...```{error}```Attempting force-update.")
        await update(ctx, True)

@client.group(name="help", help="Show this message", aliases=["commands", "h", "?"])
async def help(ctx, *, cogname: str = None):
    if cogname == None:
        menu = discord.Embed(
            title=client.description,
            description=f"Type `{client.command_prefix}help `**`<lowercase category name without spaces or dashes>`** for more info on each category.",
            color=0x007f7f
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
            color=0x007f7f
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
    elif cogname == "options":
        menu = discord.Embed(
            title="Options",
            description=client.get_cog("Options").description_long,
            color=0x007f7f
        ).set_footer(text=f"Command prefix is {client.command_prefix}\n<arg> = required parameter\n[arg] = optional parameter\n[arg (value)] = default value for optional parameter\n(command/command/command) = all aliases you can run the command with")
        for command in client.get_cog("Options").get_commands():
            menu.add_field(
                name="options",
                value="Show the current values of all options."
            )
        for subcommand in list(command.walk_commands()):
            if subcommand.parents[0] == command:
                menu.add_field(name=subcommand.name, value=subcommand.help)
        await ctx.send(embed=menu)
    elif cogname == "control" and developer(ctx.author):
        menu = discord.Embed(
            title="Control",
            description="Commands for developers to control the bot itself.",
            color=0x007f7f
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
        ).add_field(
            name="updatelog",
            value="Show the log of the last update."
        )
        await ctx.send(embed=menu)
    else:
        await ctx.send(embed=help_menu(client.get_cog(cogname.capitalize()), client))


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
        color=0x007f7f
    ).set_footer(
        text=f"Command prefix is {client.command_prefix}toggle\n<arg> = required parameter\n[arg] = optional parameter\n[arg (value)] = default value for optional parameter\n(command/command/command) = all aliases you can run the command with"
    )
    for command in remove_duplicates(group.walk_commands()):
        if command.usage:
            help_menu.add_field(
                name="({})\n{}".format(
                    str([command.name] + command.aliases)[1:-1].replace("'", "").replace(", ", "/"),
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
        color=0x007f7f
    ).set_footer(
        text=f"Command prefix is {client.command_prefix}censor or {client.command_prefix}filter\n<arg> = required parameter\n[arg] = optional parameter\n[arg (value)] = default value for optional parameter\n(command/command/command) = all aliases you can run the command with"
    )
    for command in remove_duplicates(group.walk_commands()):
        if command.usage:
            help_menu.add_field(
                name="({})\n{}".format(
                    str([command.name] + command.aliases)[1:-1].replace("'", "").replace(", ", "/"),
                    command.usage
                ),
                value=command.help
            )
        else:
            help_menu.add_field(
                name="({})".format(
                    str([command.name] + command.aliases)[1:-1].replace("'", "").replace(", ", "/")
                ),
                value=command.help)
    await ctx.send(embed=help_menu)

if not unstable:
    client.loop.create_task(status_switcher())  # as defined above

# load all the cogs
for cog in ls("cogs"):
    if cog.endswith(".py"):
        client.load_extension(f"cogs.{cog[:-3]}")
        print(f"Loaded cog {cog[:-3]}")

while True:
    try:
        client.run(env("DISCORD_TOKEN"))
    except KeyboardInterrupt:
        print("Disconnected")
        while True:
            exit(0)
    except:
        print("Unable to connect to Discord")
        while True:
            exit(1)
