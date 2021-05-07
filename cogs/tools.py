# -*- coding: utf-8 -*-

import discord
import speedtest
import time
from asyncio import sleep
from asyncio.events import get_event_loop
from discord.ext import commands
from discord.utils import get
from concurrent.futures import ThreadPoolExecutor
from json import dumps
from pengaelicutils import getops, updop
from re import search
from subprocess import check_output
from tinydb import TinyDB

class Tools(commands.Cog):
    def __init__(self, client):
        self.client = client
    teal = 0x007f7f
    nukeconfirm = False
    testing = False
    db = TinyDB("config.json")
    name = "tools"
    name_typable = name
    description = "Various tools and info."
    description_long = description

    def UpdateTime(self, speed=False):
        global CurrentTime
        global SpeedPerformTime
        CurrentTime = (time.strftime("%d %b %Y %H:%M:%S", time.localtime()))
        if speed: # record this as the time the speedtest was done
            SpeedPerformTime = CurrentTime

    def TestSpeed(self):
        global results
        self.UpdateTime(True)
        s = speedtest.Speedtest()
        s.get_best_server()
        s.download(threads=None)
        s.upload(threads=None)
        s.results.share()
        results = s.results.dict()
        return results

    @commands.command(name="os", help="Read what OS I'm running on!", aliases=["getos"])
    async def showOS(self, ctx):
        os = check_output(
            'neofetch | grep OS | sed "s/\x1B\[[0-9;]\{1,\}[A-Za-z]//g"',
            shell=True
        ).decode().split(':')[1][1:-2].split("x86")[0][:-1]
        kernel = check_output(
            'neofetch | grep Kernel | sed "s/\x1B\[[0-9;]\{1,\}[A-Za-z]//g"',
            shell=True
        ).decode().split(':')[1][1:-2]
        await ctx.send(f"I'm running on {os}, kernel version {kernel}.")

    @commands.command(name="ping", help="How slow am I to respond?", aliases=["ng"])
    async def ping(self, ctx):
        await ctx.send(
            embed=discord.Embed(
                title=":ping_pong: Pong!",
                description=f"{round(self.client.latency * 1000)} ms",
                color=self.teal
            ).set_image(url="https://supertux20.github.io/Pengaelic-Bot/images/gifs/pingpong.gif")
        )

    @commands.command(name="test", help="Am I online? I'm not sure.")
    async def test(self, ctx):
        await ctx.send("Yep, I'm alive :sunglasses:")

    @commands.command(name="avatar", help="Get someone's avatar.", usage="[username or nickname or @mention]", aliases=["pfp", "profilepic"])
    async def get_avatar(self, ctx, *, member: discord.Member = None):
        avatar2get = ctx.author
        embed = discord.Embed(
            title="Here's your avatar!",
            color=self.teal
        )
        if member:
            avatar2get = member
            if member.id == 736720500285505596:
                embed = discord.Embed(
                    title="Here's my avatar!",
                    color=self.teal
                )
            else:
                embed = discord.Embed(
                    title=f"Here's {member.display_name}'s avatar!",
                    color=self.teal
                )
        embed.set_image(url=avatar2get.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="icon", help="Get the icon for the server.", aliases=["servericon"])
    async def get_icon(self, ctx):
        try:
            await ctx.send(
                embed=discord.Embed(
                    title="Here's the server icon!",
                    color=self.teal
                ).set_image(
                    url=ctx.guild.icon_url
                )
            )
        except:
            await ctx.send(
                "This server doesn't have an icon... :pensive:"
            )

    @commands.command(name="emoji", help="Get the specified (server-specific) emoji.", usage="[:emoji:]", aliases=["emote"])
    async def get_emoji(self, ctx, emoji=None):
        emojis = [
            f"<:{em.name}:{em.id}>" for em in ctx.guild.emojis
        ]
        emojiurls = [
            f"https://cdn.discordapp.com/emojis/{em.id}.png" for em in ctx.guild.emojis
        ]
        if emoji == None:
            await ctx.send("Here's all the emojis on this server.\n" + str(emojis)[1:-1].replace("'", "").replace(", ", ""))
        else:
            if emoji in emojis:
                await ctx.send(
                    embed=discord.Embed(
                        title="Here's your emoji!",
                        color=self.teal
                    ).set_image(
                        url=emojiurls[emojis.index(emoji)]
                    )
                )
            else:
                await ctx.send("Invalid emoji specified!")

    @commands.command(name="poll", help="Send a poll!", aliases=["suggest"], usage='"<poll name>" <poll content>')
    async def poll(self, ctx, title=None, *, arg=None):
        if title == None:
            await ctx.send("You didn't specify a name for the poll!")
        if arg == None:
            await ctx.send("You didn't specify anything to make a poll for!")
        else:
            the_poll = await ctx.send(
                embed=discord.Embed(
                    color=self.teal,
                    title=title,
                    description=arg
                ).set_author(
                    name=ctx.author.name,
                    icon_url=ctx.author.avatar_url
                )
            )
            await the_poll.add_reaction("✅")
            await the_poll.add_reaction("❌")
            try:
                await ctx.message.delete()
            except:
                pass

    @commands.command(name="clear", help="Clear some messages away.", aliases=["delmsgs", "purge"], usage="[number of messages to delete (5)]")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, msgcount: int = 5):
        await ctx.channel.purge(limit=msgcount + 1)
        report = await ctx.send(f"{msgcount} (probably) messages deleted.")
        await sleep(3)
        try:
            await report.delete()
        except:
            pass

    @commands.command(name="nuke", help="Purge a channel of EVERYTHING.", aliases=["wipe", "wipechannel"])
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx):
        if not self.nukeconfirm:
            await ctx.send(f"Are you **really** sure you want to wipe this channel? Type the command again to confirm. This will expire in 10 seconds.")
            self.nukeconfirm = True
            await sleep(10)
            if self.nukeconfirm:
                self.nukeconfirm = False
                await ctx.send("Pending nuke expired.")
        elif self.nukeconfirm:
            newchannel = await ctx.channel.clone(reason=f"Nuking #{ctx.channel.name}")
            await newchannel.edit(position=ctx.channel.position, reason=f"Nuking #{ctx.channel.name}")
            await ctx.channel.delete(reason=f"Nuked #{ctx.channel.name}")
            self.nukeconfirm = False

    @commands.command(name="mute", help="Mute a member.")
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.add_roles(get(ctx.guild.roles, id=getops(ctx.guild.id, "roles", "muteRole")), reason=reason)
            await ctx.send(f"Muted {member} for reason `{reason}`.")
        except:
            await ctx.send(f"To set a mute role, type `{self.client.command_prefix}options set muteRole <mute role>`.")

    @commands.command(name="kick", help="Kick a member.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member} for reason `{reason}`.")

    @commands.command(name="ban", help="Ban a member.")
    @commands.has_permissions(kick_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member} for reason `{reason}`.")

    @commands.command(name="server", help="See a bunch of data about the server at a glance.", aliases=["info"])
    @commands.has_permissions(manage_messages=True)
    async def get_server_info(self, ctx):
        guild = ctx.guild
        owner = guild.owner
        if guild.owner.nick == None:
            owner.nick = owner.name
        creation = guild.created_at
        jsoninfo = str(
            dumps(
                {
                    "basic info": {
                        "server name": guild.name,
                        "server owner": f"{owner.nick} ({owner.name}#{owner.discriminator})",
                        "server id": guild.id,
                        "two-factor authentication": bool(guild.mfa_level),
                        "creation date": f"{creation.month}/{creation.day}/{creation.year} {creation.hour}:{creation.minute}:{creation.second} UTC/GMT"
                    },
                    "levels": {
                        "verification level": f"{guild.verification_level[0]} (level {guild.verification_level[1]+1})",
                        "notification level": f"{guild.default_notifications[0].replace('_',' ')} (level {guild.default_notifications[1]+1})",
                        "content filter": f"{guild.explicit_content_filter[0].replace('_',' ')} (level {guild.explicit_content_filter[1]+1})"
                    },
                    "counts": {
                        "members": guild.member_count,
                        "boosters": guild.premium_subscription_count,
                        "text channels": len(guild.text_channels),
                        "voice channels": len(guild.voice_channels),
                        "channel categories": len(guild.categories),
                        "emojis": len(guild.emojis)
                    }
                },
                indent=4
            )
        )
        embedinfo = discord.Embed(
            title="Server Details",
            color=self.teal
        ).add_field(
            name="Basic Info",
            value=f"""Server Name: {guild.name}
                Server Owner: "{owner.nick}" (`{owner.name}#{owner.discriminator}`)
                Server ID: `{guild.id}`
                Two-Factor Authentication: {bool(guild.mfa_level)}
                Creation Date: `{creation.month}/{creation.day}/{creation.year} {creation.hour}:{creation.minute}:{creation.second} UTC/GMT`""".replace("True", "Enabled").replace("False", "Disabled"),
            inline=False
        ).add_field(
            name="Levels",
            value=f"""Verification Level: {guild.verification_level[0]} (level {guild.verification_level[1]+1}),
                Notification Level: {guild.default_notifications[0].replace('_',' ')} (level {guild.default_notifications[1]+1}),
                Content Filter: {guild.explicit_content_filter[0].replace('_',' ')} (level {guild.explicit_content_filter[1]+1})""",
            inline=False
        ).add_field(
            name="Counts",
            value=f"""Members: {guild.member_count}
                Boosters: {guild.premium_subscription_count}
                Text Channels: {len(guild.text_channels)}
                Voice Channels: {len(guild.voice_channels)}
                Channel Categories: {len(guild.categories)}
                Emojis: {len(guild.emojis)}""",
            inline=False
        )
        if getops(guild.id, "jsonMenus"):
            await ctx.send(f'```json\n"server information": {jsoninfo}```')
        else:
            await ctx.send(embed=embedinfo)

# Thanks to https://github.com/iwa for helping Hy out with the custom roles, and thanks to Hy for letting me reuse and adapt their code to Pengaelic Bot's systems
    @commands.command(name="speedtest")
    async def speedtest(self, ctx):
        if self.testing == False:
            self.testing = True
            async with ctx.typing():
                await get_event_loop().run_in_executor(ThreadPoolExecutor(), self.TestSpeed)
            await ctx.channel.send(
f"""{SpeedPerformTime} South Australia Time
Server: {results["server"]["sponsor"]} {results["server"]["name"]}
Ping: {results["ping"]} ms
Download: {round(float((results["download"])/1000000), 2)} Mbps
Upload: {round(float((results["upload"])/1000000), 2)} Mbps

*Conducted using Ookla\'s Speedtest CLI: https://speedtest.net*"""
)
            self.testing = False
        else:
            await ctx.send("A test is already in progress. Please wait...")

    @commands.command(name="role")
    async def role(self, ctx, color, *, role_name):
        member = ctx.author
        role_lock = get(ctx.guild.roles, id=getops(ctx.guild.id, "roles", "customRoleLock"))
        if role_lock in member.roles or role_lock == None:
            try:
                result = getops(ctx.guild.id, "customRoles", str(member.id))
            except KeyError:
                result = None
            hex_code_match = search(r"(?:[0-9a-fA-F]{3}){1,2}$", color)
            if result:
                if hex_code_match:
                    role = ctx.guild.get_role(int(result))
                    await role.edit(name=role_name, color=discord.Color(int(color, 16)))
                    await member.add_roles(role)
                    await ctx.send(f"Role {role.mention} edited.")
                else:
                    await ctx.send(f"Invalid hex code `{color}`.")
            else:
                if hex_code_match:
                    role_color = discord.Color(int(color, 16))
                    role = await ctx.guild.create_role(name=role_name, colour=role_color)
                    await member.add_roles(role)
                    updop(ctx.guild.id, "customRoles", str(member.id), str(role.id))
                    await ctx.send(f"Role {role.mention} created and given.")
                else:
                    await ctx.send("Invalid hex code.")
        else:
            await ctx.send(f"{member.mention}, this is only for users with the {role_lock} role.")

    @commands.command(name="delrole")
    async def delrole(self, ctx):
        member = ctx.author
        role_lock = get(ctx.guild.roles, id=getops(ctx.guild.id, "roles", "customRoleLock"))
        if role_lock in member.roles or role_lock == None:
            result = getops(ctx.guild.id, "customRoles", str(member.id))
            if result:
                await member.remove_roles(ctx.guild.get_role(int(result)))
                await ctx.channel.send(f"Removed custom role.")
            else:
                await ctx.channel.send(f"{member.mention}, you don't have a custom role to remove!")
        else:
            await ctx.channel.send(f"{member.mention}, this is only for users with the {role_lock} role.")


    @clear.error
    async def clearError(self, ctx, error):
        if str(error) == "You are missing Manage Messages permission(s) to run this command.":
            await ctx.send(
                f"{ctx.author.mention}, you have insufficient permissions (Manage Messages)"
            )
        else:
            await ctx.send(f"Unhandled error occurred:\n```{error}```If my developer (<@!686984544930365440>) is not here, please tell him what the error is so that he can add handling or fix the issue!")

    @nuke.error
    async def nukeError(self, ctx, error):
        if str(error) == "You are missing Manage Channels permission(s) to run this command.":
            await ctx.send(f"{ctx.author.mention}, you have insufficient permissions (Manage Channels)")
        else:
            await ctx.send(f"Unhandled error occurred:\n```{error}```\nIf my developer (<@!686984544930365440>) is not here, please tell him what the error is so that he can add handling or fix the issue!")

    @get_avatar.error
    async def avatarError(self, ctx, error):
        await ctx.send("Invalid user specified!")

def setup(client):
    client.add_cog(Tools(client))