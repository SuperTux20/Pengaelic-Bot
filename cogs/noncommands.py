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
        options = getops(member.guild.id, "welcome")
        if options:
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
                        ).send(f"Welcome to {member.guild.name}, {member.name}!")
                        return
                    except:
                        continue

    @commands.Cog.listener()
    async def on_member_leave(self, member: discord.Member):
        options = getops(member.guild.id, "welcome")
        if options:
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
                        ).send(f"See you later, {member.name}...")
                        return
                    except:
                        continue

    @commands.Cog.listener()
    async def on_message(self, message):
        # lowercase everything to make my life easier
        message.content = message.content.lower()
        # check if it's a DM, in which case, don't test options (because there are none)
        if not isinstance(message.channel, discord.channel.DMChannel):
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

            # bro, did someone seriously say the chat was dead?
            if ("dead" in message.content and ("chat" in message.content or "server" in message.content)) and getops(message.guild.id, "deadChat"):
                await message.channel.send(f"{choice(['N', 'n'])}o {choice(['U', 'u'])}")

            # this section makes automatic suggestion polls
            if getops(message.guild.id, "suggestions") and ("suggest" in message.channel.name) and "discuss" not in message.channel.name:
                thepoll = await message.channel.send(
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

            # a rickroll-themed game of russian roulette, except the barrel is reset every time
            if "you know the rules" == message.content and getops(message.guild.id, "rickRoulette"):
                responses = [
                    "And so do I :pensive:"
                    for _ in range(5)
                ]
                threats = [
                    "It's time to die <:handgun:829404528054501467>",
                    "Say goodbye <:handgun:829404528054501467>"
                ]
                responses.append(
                    choice(
                        [
                            threats[0],
                            responses[0] + "\n" + threats[1],
                            threats[0] + "\n" + threats[1]
                        ]
                    )
                )
                await message.channel.send(choice(responses))


def setup(client):
    client.add_cog(NonCommands(client))