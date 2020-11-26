import discord
import sqlite3
from fnmatch import filter
from fnmatch import fnmatch
from discord.utils import get
from discord.ext import commands
from json import load
from random import choice, randint

class NonCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
    name = "non-commands"
    name_typable = "noncommands"
    description = "Automatic message responses that aren't commands."
    description_long = description

    def get_options(self, guild):
        conn = sqlite3.connect(
            "data/config.db"
        )
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        rows = cur.execute(
            f"SELECT * from options"
        ).fetchall()

        conn.commit()
        conn.close()

        currentserver = [
            server
            for server in [
                dict(ix)
                for ix in rows
            ]
            if server["id"] == guild
            ][0]

        currentserver.pop(
            "id"
        )

        return currentserver

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        all_options = self.get_options(member.guild.id)
        if all_options["welcome"] == 1:
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
            possiblechannels = [filter([channel.name for channel in member.guild.text_channels], f"*{channel}*") for channel in channelkeys]
            for channelset in possiblechannels:
                for channel in channelset:
                    try:
                        await get(
                            member.guild.text_channels,
                            name = channel
                        ).send(
                            f"""Welcome to {
                                member.guild.name
                            }, {
                                member.name
                            }!"""
                        )
                        return
                    except:
                        continue
            print(
                f"""{
                    member
                } has joined {
                    member.guild.name
                }."""
            )

    @commands.Cog.listener()
    async def on_member_leave(self, member: discord.Member):
        all_options = self.get_options(member.guild.id)
        if all_options["welcome"] == 1:
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
            possiblechannels = [filter([channel.name for channel in member.guild.text_channels], f"*{channel}*") for channel in channelkeys]
            for channelset in possiblechannels:
                for channel in channelset:
                    try:
                        await get(
                            member.guild.text_channels,
                            name = channel
                        ).send(
                            f"""See you later, {
                                member.name
                            }..."""
                        )
                        return
                    except:
                        continue
            print(
                f"""{
                    member
                } has left {
                    member.guild.name
                }."""
            )

    @commands.Cog.listener()
    async def on_message(self, message):
        all_options = self.get_options(message.guild.id)

        if message.author.id == self.client.user.id or message.author.id == 503720029456695306: # that's the ID for Dad Bot, this is to prevent conflict.
            return

        # this section is for Dad Bot-like responses
        if all_options["dadJokes"] == 1:
            dad_prefixes = [
                "i'm",
                "i`m",
                "i‘m",
                "i’m",
                "im",
                "i am"
            ]
            for dad in dad_prefixes:
                if dad + " " == message.content[0:len(dad)+1].lower():
                    if "pengaelic bot" in message.content.lower():
                        if "not" in message.content:
                            await message.channel.send(
                                "Darn right, you're not!"
                            )
                        else:
                            await message.channel.send(
                                "You're not the Pengaelic Bot, I am!"
                            )
                    elif "chickenmeister" in message.content or "Tux" == message.content:
                        if message.author.id == 686984544930365440:
                            await message.channel.send(
                                "Yes you are! Hiya!"
                            )
                        else:
                            if "not" in message.content:
                                await message.channel.send(
                                    "Darn right, you're not!"
                                )
                            else:
                                await message.channel.send(
                                    "You dare to impersonate my creator?! **You shall be punished.**"
                                )
                    else:
                        if dad + "a " == message.content[0:len(dad)+2]:
                            await message.channel.send(
                                f"""Hi{
                                    message.content[len(dad)+2:]
                                }, I'm the Pengaelic Bot!"""
                            )
                        else:
                            await message.channel.send(
                                f"""Hi{
                                    message.content[len(dad):]
                                }, I'm the Pengaelic Bot!"""
                            )

        # this section is to auto-delete messages containing a keyphrase in the censor text file
        if all_options["censor"] == 1:
            try:
                try:
                    open(
                        rf"""data/{
                            message.guild.id
                        }censor.txt""",
                        "x"
                    ).close()
                    print(
                        f"""Censor file created for {
                            message.guild.name
                        }"""
                    )
                except FileExistsError:
                    pass
                with open(rf"data/{message.guild.id}censor.txt", "r") as bads_file:
                    all_bads = bads_file.read().split(
                        ", "
                    )
                    for bad in all_bads:
                        for word in message.content.split():
                            if fnmatch(bad.lower(), word.lower()):
                                await message.delete()
            except:
                pass

        # this section randomizes yo mama jokes
        if all_options["yoMamaJokes"] == 1:
            with open(r"data/Yo Mama Jokes.json", "r") as AllTheJokes:
                jokes = load(
                    AllTheJokes
                )
            for mom in jokes:
                if "yo mama " == message.content[0:7].lower():
                    if "so " == message.content[8:11]:
                        if message.content[12:] in list(jokes.keys()):
                            if message.content[12:] == mom:
                                await message.channel.send(
                                    choice(
                                        jokes[mom]
                                    )
                                )
                        else:
                            await message.channel.send(
                                "Invalid Yo Mama type detected..."
                            )
                            await message.channel.send(
                                "Type `yo mama list` for a list of valid types!"
                            )
                    elif "list" == message.content[8:12]:
                        await message.channel.send(
                            str(
                                list(
                                    jokes.keys()
                                )
                            )[1:-1].replace(
                                "'",
                                ""
                            )
                        )


        # bro, did someone seriously say the chat was dead?
        if "dead" in message.content.lower() and ("chat" in message.content.lower() or "server" in message.content.lower()):
            await message.channel.send(
                f"""{
                    choice(
                        [
                            'N',
                            'n'
                        ]
                    )
                }o {
                    choice(
                        [
                            'U',
                            'u'
                        ]
                    )
                }"""
            )

        # this section makes automatic polls in any validly named channel
        if all_options["polls"] == 1:
            channelkeys = [
                "poll",
                "petition",
                "suggestion",
                "vote",
                "voting"
            ]
            possiblechannels = [filter([channel.name for channel in message.guild.text_channels], f"*{channel}*") for channel in channelkeys]
            for channelset in possiblechannels:
                for channel in channelset:
                    if message.channel.name == channel:
                        try:
                            thepoll = await get(
                                message.guild.text_channels,
                                name = channel
                            ).send(
                                embed = discord.Embed(
                                    color = randint(
                                        0,
                                        16777215
                                    ),
                                    title = "Suggestion",
                                    description = message.content
                                ).set_author(
                                    name = message.author.name,
                                    icon_url = message.author.avatar_url
                                )
                            )
                            await thepoll.add_reaction(
                                "✅"
                            )
                            await thepoll.add_reaction(
                                "❌"
                            )
                            try:
                                await message.delete()
                            except:
                                pass
                            return
                        except:
                            continue

        # a rickroll-themed game of russian roulette
        if "You know the rules" == message.content.lower():
            responses = [
                "And so do I :pensive:"
                for _ in range(5)
            ]
            responses.append(
                choice(
                    [
                        "It's time to die <:handgun:706698375592149013>",
                        """And so do I :pensive:
Say goodbye <:handgun:706698375592149013>""",
                        """It's time to die <:handgun:706698375592149013>s
Say goodbye <:handgun:706698375592149013>"""
                    ]
                )
            )
            await message.channel.send(
                choice(responses)
            )

def setup(client):
    client.add_cog(
        NonCommands(
            client
        )
    )