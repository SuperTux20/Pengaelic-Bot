import discord
import platform
from discord.ext import commands
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

    @commands.command(name="clear", help="Clear some messages away.", aliases=["delmsgs"], usage="[number of messages (5)] [#channel-to-delete-from (current channel)]")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx, msgcount: int=5, channel: discord.TextChannel=None):
        channel = channel or ctx.channel
        allmsgcount = 0
        async for _ in channel.history(limit=None):
            allmsgcount += 1
        await channel.purge(limit=msgcount + 1)
        if allmsgcount > msgcount:
            report = await ctx.send(str(msgcount) + " messages deleted.")
        else:
            report = await ctx.send(str(allmsgcount - 1) + " messages deleted.")
        await sleep(3)
        await report.delete()

    @clear.error
    async def clearError(self, ctx, error):
        global errorAlreadyHandled
        await ctx.send(f"{ctx.author.mention}, you have insufficient permissions (Manage Messages)")
        errorAlreadyHandled = True

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
        global errorAlreadyHandled
        await ctx.send(f"{ctx.author.mention}, you have insufficient permissions (Manage Channels)")
        errorAlreadyHandled = True

def setup(client):
    client.add_cog(Tools(client))