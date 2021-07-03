#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from sys import executable as python, argv as args, version as pyversion

if "3.9" not in pyversion:
    print("Pengaelic Bot requires Python 3.9 to function properly.")
    print("Please run Pengaelic Bot with Python 3.9")
    exit()

from asyncio import sleep
from json import loads, dumps
from os import system as cmd, getenv as env, listdir as ls, execl, devnull, environ
from pengaelicutils import newops, getops, remove_duplicates, list2str, jsoncheck
from random import choice, randint
from subprocess import check_output as shell, call, STDOUT

print("Imported modules")
if shell("uname -o", shell=True).decode()[:-1] != "Android":
    devnull = open(devnull, "w")
    requirements = [
        "figlet",
        "fortune-mod",
        "fortunes",
        "fortunes-min",
        "neofetch",
        "toilet",
        "toilet-fonts",
    ]
    needed = []
    missing_dependencies = False
    for package in requirements:
        if call(["dpkg", "-s", package], stdout=devnull, stderr=STDOUT):
            needed.append(package)
            missing_dependencies = True
    devnull.close()
    if missing_dependencies:
        print(f"Packages {list2str(needed, 0, True)} are not installed.")
        print("Install them with APT.")
        exit()
    print("Passed package test")
else:
    print("Ignored package test")

requirements = ["discord.py", "num2words", "python-dotenv", "speedtest-cli", "tinydb"]
needed = []
modules = [
    r.decode().split("==")[0] for r in shell([python, "-m", "pip", "freeze"]).split()
]
missing_dependencies = False
for module in requirements:
    if module not in modules:
        needed.append(module)
        missing_dependencies = True
if missing_dependencies:
    print(f"Modules {list2str(needed, 0, True)} are not installed.")
    print("Installing them now...")
    shell([python, "-m", "pip", "install"] + requirements)
    print("Done.")
print("Passed module test")

import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv as dotenv
from tinydb import TinyDB, Query

if "--unstable" in args:
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
Copyright (C) 2020-2021 Tux Penguin | https://github.com/SuperTux20/Pengaelic-Bot/

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
    cmd(
        r"toilet -w 1000 -f standard -F border -F gay Pengaelic Bot \(Unstable Dev Version\)"
    )
else:
    cmd("toilet -w 1000 -f standard -F border -F gay Pengaelic Bot")
print(info)

if unstable:
    client = commands.Bot(
        command_prefix="p@",
        case_insensitive=True,
        description="Pengaelic Bot (Unstable Dev Version)",
        help_command=None,
        intents=discord.Intents.all(),
    )
else:
    client = commands.Bot(
        command_prefix="p!",
        case_insensitive=True,
        description="Pengaelic Bot",
        help_command=None,
        intents=discord.Intents.all(),
    )
print("Defined client")
db = TinyDB("config.json")

if "--reset-options" in args:
    print("Options reset")
    db.truncate()


async def status_switcher():
    global client
    await client.wait_until_ready()
    while client.is_ready:
        artist = choice(
            [
                "Tux Penguin",
                "Qumu",
                "Chipzel",
                "Gooseworx",
                "Nick Nitro",
                "Zakarra",
                "Kawai Sprite",
                "Jesse Cook",
                "Chai Tea Music",
                "SharaX",
            ]
        )
        game = choice(
            [
                "Minecraft",
                "OpenRA",
                "3D Pinball: Space Cadet",
                "SuperTux",
                "Project Arrhythmia",
                "Shattered Pixel Dungeon",
                "Super Hexagon",
                "Slime Rancher",
                "AstroMenace",
                "Space Pirates and Zombies",
            ]
        )
        moviesyt = choice(
            [
                "Ethoslab",
                "MumboJumbo",
                "Blue Television Games",
                "The King of Random",
                "Alan Becker",
                "Avengers: Endgame",
                "Avengers: Infinity War",
                "Star Wars Episode IV: A New Hope",
                "Spiderman: Into the Spiderverse",
                "Back to the Future",
            ]
        )
        activity = choice(
            [
                discord.Activity(type=discord.ActivityType.listening, name=artist),
                discord.Activity(type=discord.ActivityType.playing, name=game),
                discord.Activity(type=discord.ActivityType.watching, name=moviesyt),
            ]
        )
        await client.change_presence(activity=activity)
        # task runs every few minutes (random 2-10)
        await sleep(randint(2, 10) * 60)


async def statuses():
    if not unstable:
        if "--casual-status" in args:
            client.loop.create_task(status_switcher())  # as defined above
        else:
            await client.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name=str(len(db.all())) + " servers! | p!help",
                )
            )


def help_menu(guild, cog, client):
    if jsoncheck(guild):
        try:
            menu = (
                f'```json\n"{cog.name}": "{cog.description_long.lower()}",\n"commands": '
                + dumps(
                    {
                        list2str([command.name] + command.aliases, 0).replace(
                            ", ", "/"
                        ): command.usage.split("\n")
                        for command in cog.get_commands()
                    },
                    indent=4,
                )
                + "```"
            )
        except AttributeError:
            menu = (
                f'```json\n"{cog.name}": "{cog.description_long.lower()}",\n"commands": '
                + dumps(
                    {
                        list2str([command.name] + command.aliases, 0).replace(
                            ", ", "/"
                        ): command.usage
                        for command in cog.get_commands()
                    },
                    indent=4,
                )
                + "```"
            )
    else:
        menu = discord.Embed(
            title=cog.name.capitalize(),
            description=cog.description_long,
            color=0x007F7F,
        ).set_footer(
            text=f"Command prefix is {client.command_prefix}\n<arg> = required parameter\n[arg] = optional parameter\n[arg (value)] = default value for optional parameter\n(command/command/command) = all aliases you can run the command with"
        )
        for command in cog.get_commands():
            if command.usage:
                menu.add_field(
                    name="({})\n{}".format(
                        str([command.name] + command.aliases)[1:-1]
                        .replace("'", "")
                        .replace(", ", "/"),
                        command.usage,
                    ),
                    value=command.help,
                )
            else:
                menu.add_field(
                    name="({})".format(
                        str([command.name] + command.aliases)[1:-1]
                        .replace("'", "")
                        .replace(", ", "/")
                    ),
                    value=command.help,
                )
    return menu


@client.event
async def on_ready():
    # create a server's configs
    if db.all() == []:
        for server in [
            {"guildName": guild.name, "guildID": guild.id} | newops()
            for guild in client.guilds
        ]:
            db.insert(server)
    else:
        for guild in client.guilds:
            ops = db.all()[client.guilds.index(guild)]
            ops.pop("guildName")
            ops.pop("guildID")
            nops = newops()
            for opts in ops.keys():
                if opts != newops().keys():
                    for key in ops[opts]:
                        try:
                            nops[opts].pop(key)
                        except KeyError:
                            pass
                    ops[opts] |= nops[opts]
                    db.update({"guildName": guild.name}, Query().guildID == guild.id)
                    db.update(
                        {"channels": ops["channels"]}, Query().guildID == guild.id
                    )
                    db.update({"lists": ops["lists"]}, Query().guildID == guild.id)
                    db.update(
                        {"messages": ops["messages"]}, Query().guildID == guild.id
                    )
                    db.update({"roles": ops["roles"]}, Query().guildID == guild.id)
                    db.update({"toggles": ops["toggles"]}, Query().guildID == guild.id)
    await statuses()
    print(f"{client.description} connected to Discord")
    print(f"Currently on {len(db.all())} servers")


@client.event
async def on_guild_join(guild, auto=True):
    global unstable
    if not unstable:
        print(f"Joined {guild.name}")
        welcomeembed = discord.Embed(
            title="Howdy fellas! I'm the Pengaelic Bot!",
            description=f"Type `{client.command_prefix}help` for a list of commands.",
            color=0x007F7F,
        ).set_thumbnail(url=client.user.avatar_url)
        possiblechannels = ["general", "general-1", "general-2"]
        for channel in possiblechannels:
            succ = False
            if succ:
                break
            try:
                await get(guild.text_channels, name=channel).send(embed=welcomeembed)
                succ = True
                break
            except:
                continue
        if auto:
            # create fresh options row for new server
            db.update({guild.id: newops()})
            print(f"Options set created for {guild.name}")


if not unstable:

    @client.event
    async def on_command_error(ctx, error):
        # this checks if the individual commands have their own error handling. if not...
        if not hasattr(ctx.command, "on_error"):
            # ...send the global error
            if "is not found" in str(error):
                await ctx.send(
                    f"Invalid command/usage. Type `{client.command_prefix}help` for a list of commands and their usages."
                )
                # print(
                #     "Invalid command {}{} sent in {} in #{} by {}#{}".format(
                #         client.command_prefix,
                #         str(error).split('"')[1],
                #         ctx.guild,
                #         ctx.channel,
                #         ctx.message.author.name,
                #         ctx.message.author.discriminator,
                #     )
                # )
            else:
                await ctx.send(
                    f"Unhandled error occurred:```{error}```If my developer (<@!686984544930365440>) is not here, please tell him what the error is so that he can add handling or fix the issue!"
                )


@client.command(
    name="join", help="Show the join message if it doesn't show up automatically"
)
async def redo_welcome(ctx):
    await on_guild_join(ctx.guild, False)
    await ctx.message.delete()


# load token
dotenv(".env")
DISCORD_TOKEN = env("DISCORD_TOKEN")

# load all developer user IDs
class developers:
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
async def quit_the_bot(ctx):
    if developer(ctx.author):
        await ctx.send("Goodbye...")
        exit(0)
    else:
        await ctx.send("Hey, only my developers can do this!")


if not unstable:

    @client.command(name="restart", aliases=["reload", "reboot", "rs", "rl", "rb"])
    async def restart(ctx, *, restargs=""):
        if developer(ctx.author):
            await ctx.send("Restarting...")
            print("Restarting...")
            await client.change_presence(
                activity=discord.Game("Restarting..."), status=discord.Status.dnd
            )
            execl(python, python, *[args[0]] + restargs.split())
        else:
            await ctx.send("Hey, only my developers can do this!")

    @client.command(name="updatelog", aliases=["ul", "ulog"])
    async def updatelog(ctx, formatted=True, status: discord.Message = None):
        if developer(ctx.author):
            if jsoncheck(ctx.guild.id):
                if status:
                    await status.edit(content="Looking in the logs...")
                else:
                    status = await ctx.send("Looking in the logs...")
                update_log = [
                    line.replace("\n", "") for line in open("update.log", "r")
                ][1:]
                if formatted:
                    if "A" == update_log[0][0]:
                        await status.edit(
                            content=f'```json\n"{list2str(update_log[0][:-1].split()[1:], 2)}": true```'
                        )
                        return False
                    update_summary = update_log[-1]
                    update_log = update_log[2:-1]
                    update_summary = update_summary.split(", ")
                    update_summary = [
                        {"files changed": int(update_summary[0][1:].split()[0])},
                        {
                            "insertions": int(update_summary[1][:-3].split()[0]),
                            "deletions": int(update_summary[2][:-3].split()[0]),
                        },
                    ]
                    for item in range(len(update_log)):
                        while "  " in update_log[item]:
                            update_log[item] = update_log[item].replace("  ", " ")
                    update_log = {
                        update_log[item]
                        .split("|")[0]
                        .replace(" ", ""): update_log[item]
                        .split("|")[1][1:]
                        for item in range(len(update_log))
                    }
                    await status.edit(
                        content=f'```json\n"summary": {dumps(update_summary, indent=4)},\n"changes": {dumps(update_log, indent=4)}```'
                    )
                else:
                    await ctx.send(
                        f'Raw log contents```{open("update.log", "r").read()}```'
                    )
            else:
                if status:
                    await status.edit(
                        embed=discord.Embed(
                            title="Looking in the logs...", color=0x007F7F
                        )
                    )
                else:
                    status = await ctx.send(
                        embed=discord.Embed(
                            title="Looking in the logs...", color=0x007F7F
                        )
                    )
                update_log = [
                    line.replace("\n", "") for line in open("update.log", "r")
                ][1:]
                await status.edit(
                    embed=discord.Embed(title=update_log[0], color=0x007F7F)
                )
                if formatted:
                    if "A" == update_log[0][0]:
                        return False
                    else:
                        await status.edit(
                            embed=discord.Embed(
                                title=update_log[0],
                                description=list2str(update_log[2:-1], 3),
                                color=0x007F7F,
                            ).set_footer(text=update_log[-1])
                        )
                else:
                    await status.delete()
                    await ctx.send(
                        embed=discord.Embed(
                            title="Raw log contents",
                            description=open("update.log", "r").read(),
                            color=0xFF0000,
                        )
                    )
            return True
        else:
            await ctx.send("Hey, only my developers can do this!")
            return False

    @client.command(name="update", aliases=["ud"])
    async def update(ctx, force=False):
        if developer(ctx.author):
            if jsoncheck(ctx.guild.id):
                status = await ctx.send("Pulling the latest commits from GitHub...")
            else:
                status = await ctx.send(
                    embed=discord.Embed(
                        title="Pulling the latest commits from GitHub...",
                        color=0x007F7F,
                    )
                )
            await client.change_presence(
                activity=discord.Game("Updating..."), status=discord.Status.idle
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
        await ctx.send(
            f"An error occured while updating...```{error}```Attempting force-update."
        )
        await update(ctx, True)


@client.group(name="help", help="Show this message", aliases=["commands", "h", "?"])
async def help(ctx, *, cogname: str = None):
    if cogname == None:
        cogs = dict(client.cogs)
        cogs.pop("Options")
        cogs.pop("NonCommands")
        if jsoncheck(ctx.guild.id):
            info = {cogs[cog].name: cogs[cog].description.lower()[:-1] for cog in cogs}
            if not isinstance(ctx.channel, discord.channel.DMChannel):
                info |= {"options": client.get_cog("Options").description.lower()[:-1]}
            if developer(ctx.author):
                info |= {"control": "update, restart, that sort of thing"}
            menu = dumps(info, indent=4)
            await ctx.send(
                f'```json\n"help": "type {client.command_prefix}help <category name without spaces or dashes> for more info on each category",\n"pengaelic bot": {menu}```'
            )
        else:
            menu = discord.Embed(
                title=client.description,
                description=f"Type `{client.command_prefix}help `**`<lowercase category name without spaces or dashes>`** for more info on each category.",
                color=0x007F7F,
            )
            for cog in cogs:
                menu.add_field(
                    name=cogs[cog].name.capitalize(), value=cogs[cog].description
                )
            if not isinstance(ctx.channel, discord.channel.DMChannel):
                menu.add_field(
                    name="Options",
                    value=client.get_cog("Options").description,
                    inline=False,
                )
            if developer(ctx.author):
                menu.add_field(
                    name="Control",
                    value="Update, restart, that sort of thing.",
                    inline=False,
                )
            menu.add_field(
                name="Links",
                value=f"My official [support server](https://discord.gg/DHHpA7k)\n[Invite me](https://discord.com/api/oauth2/authorize?client_id=721092139953684580&permissions=805661782&scope=bot) to your own server\nMy [GitHub repo](https://github.com/SuperTux20/Pengaelic-Bot)",
                inline=False,
            )
            await ctx.send(embed=menu)
    elif cogname == "options":
        if jsoncheck(ctx.guild.id):
            await ctx.send(
                f'```json\n"options": "{client.get_cog("Options").description_long.lower()}",\n"commands": '
                + dumps(
                    {
                        list2str([command.name] + command.aliases, 1).replace(
                            ", ", "/"
                        ): command.usage
                        for command in client.get_cog("Options").get_commands()
                    }
                    | {
                        list2str([command.name] + command.aliases, 1).replace(
                            ", ", "/"
                        ): command.usage
                        for command in list(
                            client.get_cog("Options").get_commands()[0].walk_commands()
                        )
                        if command.parents[0]
                        == client.get_cog("Options").get_commands()[0]
                    },
                    indent=4,
                )
                + "```"
            )
        else:
            menu = discord.Embed(
                title="Options",
                description=client.get_cog("Options").description_long,
                color=0x007F7F,
            ).set_footer(
                text=f"Command prefix is {client.command_prefix}\n<arg> = required parameter\n[arg] = optional parameter\n[arg (value)] = default value for optional parameter\n(command/command/command) = all aliases you can run the command with"
            )
            for command in client.get_cog("Options").get_commands():
                menu.add_field(
                    name="options", value="Show the current values of all options."
                )
            for subcommand in list(command.walk_commands()):
                if subcommand.parents[0] == command:
                    menu.add_field(name=subcommand.name, value=subcommand.help)
            await ctx.send(embed=menu)
    elif cogname == "control" and developer(ctx.author):
        if jsoncheck(ctx.guild.id):
            await ctx.send(
                f'```json\n"control": "update, restart, that sort of thing",\n"commands": '
                + dumps(
                    [
                        "exit",
                        "restart",
                        "udpate",
                        "forceupdate",
                        "udpatelog",
                        "dogofwisdom",
                    ],
                    indent=4,
                )
                + "```"
            )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Control",
                    description="Commands for developers to control the bot itself.",
                    color=0x007F7F,
                )
                .add_field(name="exit", value="Shut off the bot.")
                .add_field(name="restart", value="Reload the bot.")
                .add_field(
                    name="update",
                    value="Check if there's new commits on GitHub, and if there are, pull them and restart.",
                )
                .add_field(
                    name="forceupdate",
                    value="Same as update, but it always restarts regardless of what the update log says, because I'm sure I fucked up the regular update command somehow.",
                )
                .add_field(name="updatelog", value="Show the log of the last update.")
                .add_field(
                    name="dogofwisdom",
                    value="Create a webhook for the Dog of Wisdom in the specified channel, or a new one if unspecified.",
                )
            )
    else:
        if jsoncheck(ctx.guild.id):
            await ctx.send(
                help_menu(ctx.guild.id, client.get_cog(cogname.capitalize()), client)
            )
        else:
            await ctx.send(
                embed=help_menu(
                    ctx.guild.id, client.get_cog(cogname.capitalize()), client
                )
            )


# so that people can set up the Dog in their own servers without having to ask me about it first :>


@client.command(name="dogofwisdom")
async def dog(ctx, *, channel: discord.TextChannel = None):
    if getops(ctx.guild.id, "modRole") in ctx.author.roles:
        if not channel:
            channel = await ctx.guild.create_text_channel("dog-of-wisdom")
            await channel.edit(category=ctx.guild.categories[0])
        hook = await channel.create_webhook(name="The Dog of Wisdom")
        await client.get_user(developers.everyone["tux"]).send(
            f"@{ctx.author.name}#{ctx.author.discriminator} is requesting the Dog of Wisdom.\n"
            + hook.url.replace(
                "https://discord.com/api/webhooks/", f'["{ctx.guild.name}"]='
            )
        )


@help.error
async def not_a_cog(ctx, error):
    if str(error) == "AttributeError: 'NoneType' object has no attribute 'name'":
        await ctx.send("There isn't a help menu for that.")
    else:
        await ctx.send(
            f"Unhandled error occurred:\n```{error}```\nIf my developer (<@!686984544930365440>) is not here, please tell him what the error is so that he can add handling or fix the issue!"
        )


@help.command(name="toggle")
async def h_toggle(ctx):
    group = client.get_command("toggle")
    help_menu = discord.Embed(
        title=group.name.capitalize(), description=group.help, color=0x007F7F
    ).set_footer(
        text=f"Command prefix is {client.command_prefix}toggle\n<arg> = required parameter\n[arg] = optional parameter\n[arg (value)] = default value for optional parameter\n(command/command/command) = all aliases you can run the command with"
    )
    for command in remove_duplicates(group.walk_commands()):
        if command.usage:
            help_menu.add_field(
                name="({})\n{}".format(
                    str([command.name] + command.aliases)[1:-1]
                    .replace("'", "")
                    .replace(", ", "/"),
                    command.usage,
                ),
                value=command.help,
            )
        else:
            help_menu.add_field(
                name="({})".format(
                    str([command.name] + command.aliases)[1:-1]
                    .replace("'", "")
                    .replace(", ", "/")
                ),
                value=command.help,
            )
    await ctx.send(embed=help_menu)


@help.command(name="censor", aliases=["filter"])
async def h_censor(ctx):
    group = client.get_command("censor")
    help_menu = discord.Embed(
        title=group.name.capitalize(), description=group.help, color=0x007F7F
    ).set_footer(
        text=f"Command prefix is {client.command_prefix}censor or {client.command_prefix}filter\n<arg> = required parameter\n[arg] = optional parameter\n[arg (value)] = default value for optional parameter\n(command/command/command) = all aliases you can run the command with"
    )
    for command in remove_duplicates(group.walk_commands()):
        if command.usage:
            help_menu.add_field(
                name="({})\n{}".format(
                    str([command.name] + command.aliases)[1:-1]
                    .replace("'", "")
                    .replace(", ", "/"),
                    command.usage,
                ),
                value=command.help,
            )
        else:
            help_menu.add_field(
                name="({})".format(
                    str([command.name] + command.aliases)[1:-1]
                    .replace("'", "")
                    .replace(", ", "/")
                ),
                value=command.help,
            )
    await ctx.send(embed=help_menu)


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
