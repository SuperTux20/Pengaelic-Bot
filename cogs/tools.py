import discord
import platform
from discord.ext import commands
from discord.utils import get
from asyncio import sleep

class Tools(commands.Cog):
    purgeconfirm = False
    name="tools"
    description ="Various tools and info."
    def __init__(self, client):
        self.client = client

    @commands.command(name="os", help="Read what OS I'm running on!", aliases=["getos"])
    async def showos(self, ctx):
        defaultmsg = f"I'm running on {platform.system()} "
        if platform.release() == "10":
            await ctx.send(defaultmsg + platform.version())
        else:
            await ctx.send(defaultmsg + platform.release() + " " + platform.version())

    @commands.command(name="ping", help="How slow am I to respond?", aliases=["ng"])
    async def ping(self, ctx):
        embed = discord.Embed(title=f":ping_pong: Pong!", description=f"{round(self.client.latency * 1000)} ms", color=32639)
        embed.set_image(url="https://supertux20.github.io/Pengaelic-Bot/images/gifs/pingpong.gif")
        await ctx.send(embed=embed)

    @commands.command(name="avatar", help="Get someone's avatar.", usage="<@mention>", aliases=["pfp", "profilepic"])
    async def avatar(self, ctx, *,  member: discord.Member=None):
        await ctx.send(member.avatar_url)

    @commands.command(name="icon", help="Get the icon for the server.", aliases=["servericon","servicon"])
    async def servericon(self, ctx):
        try:
            await ctx.send(ctx.guild.icon_url)
        except:
            await ctx.send("This server doesn't have an icon for some reason... :neutral_face:")

    @commands.command(name="emoji", help="Get the specified (server-specific) emoji.", usage="[:emoji:]")
    async def getemoji(self, ctx, emoji: str=None):
        emojis = [f"<:{em.name}:{em.id}>" for em in ctx.guild.emojis]
        emojiurls = [f"https://cdn.discordapp.com/emojis/{em.id}.png" for em in ctx.guild.emojis]
        if emoji == None:
            await ctx.send(str(emojis)[1:-1].replace("'","").replace(", ",""))
        else:
            if emoji in emojis:
                await ctx.send(emojiurls[emojis.index(emoji)])
            else:
                await ctx.send("Invalid emoji specified!")

    @commands.command(name="clear", help="Clear some messages away.", aliases=["delmsgs"], usage="[number of messages to delete (5)]")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx, msgcount: int=5):
        await ctx.channel.purge(limit=msgcount + 1)
        report = await ctx.send(str(msgcount) + " (probably) messages deleted.")
        await sleep(3)
        await report.delete()

    @clear.error
    async def clearError(self, ctx, error):
        if error == discord.ext.commands.errors.MissingPermissions:
            await ctx.send(f"{ctx.author.mention}, you have insufficient permissions (Manage Messages)")
        elif error == discord.ext.commands.errors.BotMissingPermissions:
            await ctx.send(f"{ctx.author.mention}, ***I*** have insufficient permissions! (Manage Messages)")

    @commands.command(name="purge", help="Purge a channel of everything.\n:warning:WARNING:warning: This command clears an ENTIRE channel!", aliases=["wipe", "wipechannel"])
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def purge(self, ctx, msgcount: int=5):
        if self.purgeconfirm == False:
            await ctx.send("Are you **really** sure you want to wipe this channel? Type p!purge again to confirm.")
            self.purgeconfirm = True
        elif self.purgeconfirm == True:
            await ctx.channel.clone()
            await ctx.channel.delete()
            self.purgeconfirm = False

    @purge.error
    async def purgeError(self, ctx, error):
        if error == discord.ext.commands.errors.MissingPermissions:
            await ctx.send(f"{ctx.author.mention}, you have insufficient permissions (Manage Channels)")
        elif error == discord.ext.commands.errors.BotMissingPermissions:
            await ctx.send(f"{ctx.author.mention}, ***I*** have insufficient permissions! (Manage Channels)")
        else:
            await ctx.send(f"Unhandled error occurred: {error}. If my developer (chickenmeister#7140) is not here, please tell him what the error is so that he can add handling!")

    @avatar.error
    async def avatarError(self, ctx, error):
        await ctx.send("Invalid user specified!")

def setup(client):
    client.add_cog(Tools(client))