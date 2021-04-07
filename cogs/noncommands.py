import discord
from pengaelicutils import options as getops
from fnmatch import filter, fnmatch
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

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        options = getops(member.guild.id)
        if options["welcome"] == True:
            channelkeys = [
                "welcome",
                "arrivals",
                "entrance",
                "entry",
                "log",
                "lobby",
                "general"
            ]
            possiblechannels = [
                filter(
                    [
                        channel.name
                        for channel in member.guild.text_channels
                    ],
                    f"*{channel}*"
                ) for channel in channelkeys
            ]
            for channelset in possiblechannels:
                for channel in channelset:
                    try:
                        await get(
                            member.guild.text_channels,
                            name=channel
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

    @commands.Cog.listener()
    async def on_member_leave(self, member: discord.Member):
        options = getops(member.guild.id)
        if options["welcome"] == True:
            channelkeys = [
                "welcome",
                "arrivals",
                "entrance",
                "entry",
                "log",
                "lobby",
                "general"
            ]
            possiblechannels = [filter(
                [channel.name for channel in member.guild.text_channels], f"*{channel}*") for channel in channelkeys]
            for channelset in possiblechannels:
                for channel in channelset:
                    try:
                        await get(
                            member.guild.text_channels,
                            name=channel
                        ).send(
                            f"""See you later, {
                                member.name
                            }..."""
                        )
                        return
                    except:
                        continue

    @commands.Cog.listener()
    async def on_message(self, message):
        message.content = message.content.lower()

        # this section is for Dad Bot-like responses
        if getops(message.guild.id, "dadJokes"):
            dad_prefixes = [
                "i'm",
                "i`m",
                "i‘m",
                "i’m",
                "im",
                "i am"
            ]
            for dad in dad_prefixes:
                if dad + " " == message.content[0:len(dad)+1]:
                    if "pengaelic bot" in message.content:
                        if "not" in message.content:
                            await message.channel.send("Darn right, you're not!")
                        else:
                            await message.channel.send("You're not the Pengaelic Bot, I am!")
                    elif "chickenmeister" in message.content or "Tux" == message.content:
                        if message.author.id == 686984544930365440:
                            await message.channel.send("Yes you are! Hiya!")
                        else:
                            if "not" in message.content:
                                await message.channel.send("Darn right, you're not!")
                            else:
                                await message.channel.send("You dare to impersonate my creator?! **You shall be punished.**")
                    else:
                        if dad + "a " == message.content[0:len(dad)+2]:
                            await message.channel.send(f"Hi{message.content[len(dad)+2:]}, I'm the Pengaelic Bot!")
                        elif dad + "an " == message.content[0:len(dad)+3]:
                            await message.channel.send(f"Hi{message.content[len(dad)+3:]}, I'm the Pengaelic Bot!")
                        else:
                            await message.channel.send(f"Hi{message.content[len(dad):]}, I'm the Pengaelic Bot!")

        # this section is to auto-delete messages containing a keyphrase in the censor text file
        if getops(message.guild.id, "censor"):
            all_bads = getops(message.guild.id, "censorlist")
            for bad in all_bads:
                if bad in message.content.split():
                    await message.delete()

        # this section randomizes yo mama jokes
        if getops(message.guild.id, "yoMamaJokes"):
            with open(r"yo_mama_jokes.json", "r") as AllTheJokes:
                jokes = load(AllTheJokes)
            for mom in jokes:
                if message.content.lower().startswith("yo mama "):
                    if message.content.lower().startswith("yo mama so "):
                        if message.content[11:] == mom:
                            await message.channel.send(choice(jokes[mom]))
                            break
                        else:
                            await message.channel.send("Invalid Yo Mama type detected...")
                            await message.channel.send("Type `yo mama list` for a list of valid types!")
                            break
                    elif message.content == "yo mama list":
                        await message.channel.send(str(list(jokes.keys()))[1:-1].replace("'", ""))
                        break

        # bro, did someone seriously say the chat was dead?
        if ("dead" in message.content and ("chat" in message.content or "server" in message.content)) and getops(message.guild.id, "deadChat"):
            await message.channel.send(f"{choice(['N', 'n'])}o {choice(['U', 'u'])}")

        # this section makes automatic polls in any validly named channel
        if getops(message.guild.id, "polls"):
            possiblechannels = filter(
                [
                    channel.name
                    for channel in message.guild.text_channels
                ],
                f"*{'suggest'}*"
            )
            for channelset in possiblechannels:
                for channel in channelset:
                    if message.channel.name == channel and "discuss" not in message.channel.name:
                        try:
                            thepoll = await get(
                                message.guild.text_channels,
                                name=channel
                            ).send(
                                embed=discord.Embed(
                                    color=randint(
                                        0,
                                        16777215
                                    ),
                                    title="Suggestion",
                                    description=message.content
                                ).set_author(
                                    name=message.author.name,
                                    icon_url=message.author.avatar_url
                                )
                            )
                            await thepoll.add_reaction("✅")
                            await thepoll.add_reaction("❌")
                            try:
                                await message.delete()
                            except:
                                pass
                            return
                        except:
                            continue

        # a rickroll-themed game of russian roulette
        if "you know the rules" == message.content and getops(message.guild.id, "rickRoulette"):
            responses = [
                "And so do I :pensive:"
                for _ in range(5)
            ]
            responses.append(
                choice(
                    [
                        "It's time to die <:handgun:828696987728740352>",
                        "And so do I :pensive:\nSay goodbye <:handgun:828696987728740352>",
                        "It's time to die <:handgun:828696987728740352>\nSay goodbye <:handgun:828696987728740352>"
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
