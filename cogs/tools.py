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
    purgeconfirm = False
    name="tools"
    name_typable = name
    description ="Various tools and info."
    description_long = description

    @commands.command(name="os", help="Read what OS I'm running on!", aliases=["getos"])
    async def showos(self, ctx):
        await ctx.send(f"I'm running on {platform.system()} {platform.release()} ver. {platform.version()}")

    @commands.command(name="ping", help="How slow am I to respond?", aliases=["ng"])
    async def ping(self, ctx):
        await ctx.send(
            embed=discord.Embed(
                title=":ping_pong: Pong!",
                description=f"""{
                    round(
                        self.client.latency * 1000
                    )
                } ms""",
                color=32639
            ).set_image(
                url="https://supertux20.github.io/Pengaelic-Bot/images/gifs/pingpong.gif"
            )
        )

    @commands.command(name="test", help="Am I online? I'm not sure.")
    async def test(self, ctx):
        await ctx.send("Yep, I'm alive :sunglasses:")

    @commands.command(name="avatar", help="Get someone's avatar.", usage="[username or nickname or @mention]", aliases=["pfp", "profilepic"])
    async def avatar(self, ctx, *,  member: discord.Member=None):
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
                    title=f"""Here's {
                        member.display_name
                    }'s avatar!""",
                    color=32639
                )
        embed.set_image(url=avatar2get.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="icon", help="Get the icon for the server.", aliases=["servericon","servicon"])
    async def servericon(self, ctx):
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
    async def getemoji(self, ctx, emoji=None):
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
    async def poll(self, ctx, *, arg):
        thepoll = await ctx.send(
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
        await ctx.message.delete()
        await thepoll.add_reaction("✅")
        await thepoll.add_reaction("❌")

    @commands.command(name="clear", help="Clear some messages away.", aliases=["delmsgs"], usage="[number of messages to delete (5)]")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, msgcount: int=5):
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
        await report.delete()

    @commands.command(name="purge", help="Purge a channel of everything.\n:warning:WARNING:warning: This command clears an ENTIRE channel!", aliases=["wipe", "wipechannel"])
    @commands.has_permissions(manage_channels=True)
    async def purge(self, ctx):
        if self.purgeconfirm == False:
            await ctx.send(
                "Are you **really** sure you want to wipe this channel? Type `p!purge` again to confirm. This will expire in 10 seconds."
            )
            self.purgeconfirm = True
            await sleep(10)
            self.purgeconfirm = False
            await ctx.send("Pending purge expired.")
        elif self.purgeconfirm == True:
            newchannel = await ctx.channel.clone(
                reason=f"""Purging #{
                    ctx.channel.name
                }"""
            )
            await newchannel.edit(
                position=ctx.channel.position,
                reason=f"""Purging #{
                    ctx.channel.name
                }"""
            )
            await ctx.channel.delete(
                reason=f"""Purged #{
                    ctx.channel.name
                }"""
            )
            self.purgeconfirm = False

    @commands.command(name="support", help="Get the invite link to the official support server.", aliases=["discord", "invite"])
    async def getserver(self, ctx):
        await ctx.send(
            """Here is the official support server for Pengaelic Bot!
            https://discord.gg/DHHpA7k"""
        )

    @commands.command(name="server", help="See a bunch of data about the server at a glance.", aliases=["info"])
    @commands.has_permissions(manage_messages=True)
    async def getops(self, ctx):
        await ctx.send(
            f"""```json
{
dumps(
    {
        "server name": ctx.guild.name,
        "server owner": ctx.guild.owner.name + "#" + ctx.guild.owner.discriminator,
        "amounts": {
            "members": ctx.guild.member_count,
            "boosters": len(
                ctx.guild.premium_subscribers
            ), "text channels": len(
                ctx.guild.text_channels
            ),
            "emojis": len(
                ctx.guild.emojis
            )
        }
    },
    sort_keys=False,
    indent=4
)
}
```"""
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
                If my developer (chickenmeister#7140) is not here, please tell him what the error is so that he can add handling or fix the issue!"""
            )

    @purge.error
    async def purgeError(self, ctx, error):
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
If my developer (chickenmeister#7140) is not here, please tell him what the error is so that he can add handling or fix the issue!"""
            )

    @avatar.error
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