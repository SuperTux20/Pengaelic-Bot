import discord
import platform
from discord.ext import commands
from discord.utils import get
from asyncio import sleep
from random import randint
from json import dumps


class tools(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cyan = 32639
    nukeconfirm = False
    name = "tools"
    name_typable = name
    description = "Various tools and info."
    description_long = description

    @commands.command(name="os", help="Read what OS I'm running on!", aliases=["getos"])
    async def showOS(self, ctx):
        await ctx.send(f"I'm running on {platform.system()} {platform.release()} ver. {platform.version()}")

    @commands.command(name="ping", help="How slow am I to respond?", aliases=["ng"])
    async def ping(self, ctx):
        await ctx.send(
            embed=discord.Embed(
                title=":ping_pong: Pong!",
                description=f"{round(self.client.latency * 1000)} ms",
                color=32639
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
            color=32639
        )
        if member:
            avatar2get = member
            if member.id == 736720500285505596:
                embed = discord.Embed(
                    title="Here's my avatar!",
                    color=32639
                )
            else:
                embed = discord.Embed(
                    title=f"Here's {member.display_name}'s avatar!",
                    color=32639
                )
        embed.set_image(url=avatar2get.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="icon", help="Get the icon for the server.", aliases=["servericon"])
    async def get_icon(self, ctx):
        try:
            await ctx.send(
                embed=discord.Embed(
                    title="Here's the server icon!",
                    color=32639
                ).set_image(
                    url=ctx.guild.icon_url
                )
            )
        except:
            await ctx.send(
                "This server doesn't have an icon... :neutral_face:"
            )

    @commands.command(name="emoji", help="Get the specified (server-specific) emoji.", usage="[:emoji:]", aliases=["emote"])
    async def get_emoji(self, ctx, emoji=None):
        emojis = [
            f"""<:{
                em.name
            }:{
                em.id
            }>"""
            for em in ctx.guild.emojis
        ]
        emojiurls = [
            f"""https://cdn.discordapp.com/emojis/{
                em.id
            }.png"""
            for em in ctx.guild.emojis
        ]
        if emoji == None:
            await ctx.send(
                "Here's all the emojis on this server.\n" + str(
                    emojis
                )[1:-1].replace(
                    "'",
                    ""
                ).replace(
                    ", ",
                    ""
                )
            )
        else:
            if emoji in emojis:
                await ctx.send(
                    embed=discord.Embed(
                        title="Here's your emoji!",
                        color=32639
                    ).set_image(
                        url=emojiurls[
                            emojis.index(
                                emoji
                            )
                        ]
                    )
                )
            else:
                await ctx.send("Invalid emoji specified!")

    @commands.command(name="suggest", help="Send a suggestion poll!", aliases=["poll", "suggestion"])
    async def poll(self, ctx, *, arg=None):
        if arg == None:
            await ctx.send("You didn't specify anything to make a poll for!")
        else:
            the_poll = await ctx.send(
                embed=discord.Embed(
                    color=randint(
                        0,
                        16777215
                    ),
                    title="Suggestion",
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
        await ctx.channel.purge(
            limit=msgcount + 1
        )
        report = await ctx.send(
            f"""{
                msgcount
            } (probably) messages deleted."""
        )
        await sleep(
            3
        )
        try:
            await report.delete()
        except:
            pass

    @commands.command(name="nuke", help="Purge a channel of EVERYTHING.", aliases=["wipe", "wipechannel"])
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx):
        if self.nukeconfirm == False:
            await ctx.send(
                f"Are you **really** sure you want to wipe this channel? Type `{self.client.command_prefix}nuke` again to confirm. This will expire in 10 seconds."
            )
            self.nukeconfirm = True
            await sleep(
                10
            )
            self.nukeconfirm = False
            await ctx.send(
                "Pending nuke expired."
            )
        elif self.nukeconfirm == True:
            newchannel = await ctx.channel.clone(
                reason=f"""Nuking #{
                    ctx.channel.name
                }"""
            )
            await newchannel.edit(
                position=ctx.channel.position,
                reason=f"""Nuking #{
                    ctx.channel.name
                }"""
            )
            await ctx.channel.delete(
                reason=f"""Nuked #{
                    ctx.channel.name
                }"""
            )
            self.nukeconfirm = False

    @commands.command(name="support", help="Get the invite link to the official support server.", aliases=["discord"])
    async def support(self, ctx):
        await ctx.send(
            """Here is my official support server!
https://discord.gg/DHHpA7k"""
        )

    @commands.command(name="invite", help="Invite me to your server!", aliases=["inviteme"])
    async def invite(self, ctx):
        await ctx.send(
            embed=discord.Embed(
                color=self.cyan,
                title="Can I come on to your server?",
                description="[Click here to invite me!](https://discord.com/oauth2/authorize?client_id=721092139953684580&permissions=388176&scope=bot)"
            )
        )

    @commands.command(name="server", help="See a bunch of data about the server at a glance.", aliases=["info"])
    @commands.has_permissions(manage_messages=True)
    async def get_server_info(self, ctx):
        creation = ctx.guild.created_at
        jsoninfo = str(
            dumps(
                {
                    "basic info": {
                        "server name": ctx.guild.name,
                        "server owner": f"{ctx.guild.owner.nick} ({ctx.guild.owner.name}#{ctx.guild.owner.discriminator})",
                        "server id": ctx.guild.id,
                        "two-factor authentication": bool(ctx.guild.mfa_level),
                        "creation date": f"{creation.month}/{creation.day}/{creation.year} {creation.hour}:{creation.minute}:{creation.second} UTC/GMT"
                    },
                    "levels": {
                        "verification level": f"{ctx.guild.verification_level[0]} (level {ctx.guild.verification_level[1]+1})",
                        "notification level": f"{ctx.guild.default_notifications[0].replace('_',' ')} (level {ctx.guild.default_notifications[1]+1})",
                        "content filter": f"{ctx.guild.explicit_content_filter[0].replace('_',' ')} (level {ctx.guild.explicit_content_filter[1]+1})"
                    },
                    "counts": {
                        "members": ctx.guild.member_count,
                        "boosters": ctx.guild.premium_subscription_count,
                        "text channels": len(ctx.guild.text_channels),
                        "voice channels": len(ctx.guild.voice_channels),
                        "channel categories": len(ctx.guild.categories),
                        "emojis": len(ctx.guild.emojis)
                    }
                },
                sort_keys=False,
                indent=4
            )[6:-2].replace("\n    ", "\n")
        )
        await ctx.send(
            f"""server information
```json
{jsoninfo}
```""",
            # embed=discord.Embed(
            #     title="Server Details",
            #     color=self.cyan
            # ).add_field(
            #     name="Basic Info",
            #     value=f"""Server Name: {ctx.guild.name}
            #     Server Owner: "{ctx.guild.owner.nick}" (`{ctx.guild.owner.name}#{ctx.guild.owner.discriminator}`)
            #     Server Id: `{ctx.guild.id}`
            #     Two-factor Authentication: {bool(ctx.guild.mfa_level)}
            #     Creation Date: `{creation.month}/{creation.day}/{creation.year} {creation.hour}:{creation.minute}:{creation.second} UTC/GMT`""",
            #     inline=False
            # ).add_field(
            #     name="Levels",
            #     value=f"""Verification Level: {ctx.guild.verification_level[0]} (level {ctx.guild.verification_level[1]+1}),
            #     Notification Level: {ctx.guild.default_notifications[0].replace('_',' ')} (level {ctx.guild.default_notifications[1]+1}),
            #     Content Filter: {ctx.guild.explicit_content_filter[0].replace('_',' ')} (level {ctx.guild.explicit_content_filter[1]+1})""",
            #     inline=False
            # ).add_field(
            #     name="Counts",
            #     value=f"""Members: {ctx.guild.member_count}
            #     Boosters: {ctx.guild.premium_subscription_count}
            #     Text Channels: {len(ctx.guild.text_channels)}
            #     Voice Channels: {len(ctx.guild.voice_channels)}
            #     Channel Categories: {len(ctx.guild.categories)}
            #     Emojis: {len(ctx.guild.emojis)}""",
            #     inline=False
            # )
        )

    @clear.error
    async def clearError(self, ctx, error):
        if str(error) == "You are missing Manage Messages permission(s) to run this command.":
            await ctx.send(
                f"""{
                    ctx.author.mention
                }, you have insufficient permissions (Manage Messages)"""
            )
        else:
            await ctx.send(
                f"""Unhandled error occurred:
                {
                    error
                }
                If my developer (<@!686984544930365440>) is not here, please tell him what the error is so that he can add handling or fix the issue!"""
            )

    @nuke.error
    async def nukeError(self, ctx, error):
        if str(error) == "You are missing Manage Channels permission(s) to run this command.":
            await ctx.send(
                f"""{
                    ctx.author.mention
                }, you have insufficient permissions (Manage Channels)"""
            )
        else:
            await ctx.send(
                f"""Unhandled error occurred:
        {
            error
        }
If my developer (<@!686984544930365440>) is not here, please tell him what the error is so that he can add handling or fix the issue!"""
            )

    @get_avatar.error
    async def avatarError(self, ctx, error):
        await ctx.send(
            "Invalid user specified!"
        )


def setup(client):
    client.add_cog(
        tools(
            client
        )
    )
