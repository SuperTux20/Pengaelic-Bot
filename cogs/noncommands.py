# -*- coding: utf-8 -*-

import discord
from pengaelicutils import getops
from fnmatch import filter
from discord.utils import get
from discord.ext import commands
from random import choice

class NonCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
    name = "non-commands"
    name_typable = "noncommands"
    description = "Automatic message responses that aren't commands."
    description_long = description

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if getops(member.guild.id, "toggles", "welcome"):
            welcome_channel = getops(member.guild.id, "channels", "welcomeChannel")
            if welcome_channel:
                await get(
                    member.guild.text_channels,
                    id=welcome_channel
                ).send(
                    getops(
                        member.guild.id,
                        "messages",
                        "welcomeMessage"
                    ).replace("SERVER", member.guild.name).replace("USER", member.name)
                )

    @commands.Cog.listener()
    async def on_member_leave(self, member: discord.Member):
        if getops(member.guild.id, "toggles", "welcome"):
            welcome_channel = getops(member.guild.id, "channels", "welcomeChannel")
            if welcome_channel:
                await get(
                    member.guild.text_channels,
                    id=welcome_channel
                ).send(
                    getops(
                        member.guild.id,
                        "messages",
                        "goodbyeMessage"
                    ).replace("SERVER", member.guild.name).replace("USER", member.name)
                )

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.client.user.mention in message.content:
            await message.channel.send(f"My prefix is `{self.client.command_prefix}` :smiley:")
        # lowercase everything to make my life easier
        messagetext = message.content.lower()
        # check if it's a DM, in which case, don't test options (because there are none)
        # then make sure the message it's reading doesn't belong to the bot itself
        if not isinstance(message.channel, discord.channel.DMChannel) and message.author != self.client.user:
            # this section is for Dad Bot-like responses
            if getops(message.guild.id, "toggles", "dadJokes"):
                dad_prefixes = [
                    "i'm",
                    "i`m",
                    "i‘m",
                    "i’m",
                    "im",
                    "i am"
                ]
                for dad in dad_prefixes:
                    if dad + " " == messagetext[0:len(dad)+1]:
                        if "pengaelic bot" in messagetext:
                            if "not" in messagetext:
                                await message.channel.send("Darn right, you're not!")
                            else:
                                await message.channel.send("You're not the Pengaelic Bot, I am!")
                        elif "chickenmeister" in messagetext or "tux" in messagetext:
                            if message.author.id == 686984544930365440:
                                await message.channel.send("Yes you are! Hiya!")
                            else:
                                if "not" in messagetext:
                                    await message.channel.send("Darn right, you're not!")
                                else:
                                    await message.channel.send("You dare to impersonate my creator?! **You shall be punished.**")
                        else:
                            if dad + "a " == messagetext[0:len(dad)+2]:
                                await message.channel.send(f"Hi{messagetext[len(dad)+2:]}, I'm the Pengaelic Bot!")
                            elif dad + "an " == messagetext[0:len(dad)+3]:
                                await message.channel.send(f"Hi{messagetext[len(dad)+3:]}, I'm the Pengaelic Bot!")
                            else:
                                await message.channel.send(f"Hi{messagetext[len(dad):]}, I'm the Pengaelic Bot!")

            # this section is to auto-delete messages containing a keyphrase in the censor text file
            if getops(message.guild.id, "toggles", "censor"):
                all_bads = getops(message.guild.id, "lists", "censorList")
                for bad in all_bads:
                    if bad in messagetext.split():
                        await message.delete()
                        await message.author.send(f"Hey, that word `{bad}` isn't allowed here!")

            # bro, did someone seriously say the chat was dead?
            if ("dead" in messagetext and ("chat" in messagetext or "server" in messagetext)) and getops(message.guild.id, "toggles", "deadChat"):
                await message.channel.send(f"{choice(['N', 'n'])}o {choice(['U', 'u'])}")

            # this section makes automatic suggestion polls
            if getops(message.guild.id, "toggles", "suggestions") and (message.channel.id == getops(message.guild.id, "channels", "suggestionsChannel")):
                thepoll = await message.channel.send(
                    embed=discord.Embed(
                        title="Suggestion",
                        description=message.content,
                        color=0x007f7f
                    ).set_author(
                        name=message.author.name,
                        icon_url=message.author.avatar_url
                    )
                )
                try:
                    await message.delete()
                    await thepoll.add_reaction("✅")
                    await thepoll.add_reaction("❌")
                except:
                    pass
                return

            # a rickroll-themed game of russian roulette, except the barrel is reset every time
            if "you know the rules" == messagetext and getops(message.guild.id, "toggles", "rickRoulette"):
                responses = [
                    "And so do I :pensive:"
                    for _ in range(5)
                ]
                threats = [
                    "It's time to die",
                    "Say goodbye <:delet_this:828693389712949269>"
                ]
                responses.append(
                    choice(
                        [
                            threats[0] + "<:delet_this:828693389712949269>",
                            responses[0] + "\n" + threats[1],
                            threats[0] + "\n" + threats[1]
                        ]
                    )
                )
                await message.channel.send(choice(responses))

def setup(client):
    client.add_cog(NonCommands(client))