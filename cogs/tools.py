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
        await ctx.send(embed=discord.Embed(title=f":ping_pong: Pong!", description=f"{round(self.client.latency * 1000)} ms", color=32639).set_image(url="https://supertux20.github.io/Pengaelic-Bot/images/gifs/pingpong.gif"))

    @commands.command(name="test", help="Am I online? I'm not sure.")
    async def test(self, ctx):
        await ctx.send("Yep, I'm alive :stuck_out_tongue:")

    @commands.command(name="avatar", help="Get someone's avatar.", usage="[username or nickname or @mention]", aliases=["pfp", "profilepic"])
    async def avatar(self, ctx, *,  member: discord.Member=None):
        if member:
            avatar = member.avatar_url
            if member.id == 721092139953684580:
                embed = discord.Embed(title=f"Here's my avatar!", color=32639)
            else:
                embed = discord.Embed(title=f"Here's {member.display_name}'s avatar!", color=32639)
        else:
            avatar = ctx.author.avatar_url
            embed = discord.Embed(title="Here's your avatar!", color=32639)
        embed.set_image(url=avatar)
        await ctx.send(embed=embed)

    @commands.command(name="icon", help="Get the icon for the server.", aliases=["servericon","servicon"])
    async def servericon(self, ctx):
        try:
            await ctx.send(embed=discord.Embed(title="Here's the server icon!", color=32639).set_image(url=ctx.guild.icon_url))
        except:
            await ctx.send("This server doesn't have an icon for some reason... :neutral_face:")

    @commands.command(name="emoji", help="Get the specified (server-specific) emoji.", usage="[:emoji:]", aliases=["emote"])
    async def getemoji(self, ctx, emoji=None):
        emojis = [f"<:{em.name}:{em.id}>" for em in ctx.guild.emojis]
        emojiurls = [f"https://cdn.discordapp.com/emojis/{em.id}.png" for em in ctx.guild.emojis]
        if emoji == None:
            await ctx.send("Here's all the emojis on this server.\n" + str(emojis)[1:-1].replace("'","").replace(", ",""))
        else:
            if emoji in emojis:
                await ctx.send(embed=discord.Embed(title="Here's your emoji!", color=32639).set_image(url=emojiurls[emojis.index(emoji)]))
            else:
                await ctx.send("Invalid emoji specified!")

    @commands.command(name="clear", help="Clear some messages away.", aliases=["delmsgs"], usage="[number of messages to delete (5)]")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, msgcount: int=5):
        await ctx.channel.purge(limit=msgcount + 1)
        report = await ctx.send(str(msgcount) + " (probably) messages deleted.")
        await sleep(3)
        await report.delete()

    @commands.command(name="purge", help="Purge a channel of everything.\n:warning:WARNING:warning: This command clears an ENTIRE channel!", aliases=["wipe", "wipechannel"])
    @commands.has_permissions(manage_channels=True)
    async def purge(self, ctx, msgcount: int=5):
        if self.purgeconfirm == False:
            await ctx.send("Are you **really** sure you want to wipe this channel? Type `p!purge` again to confirm.")
            self.purgeconfirm = True
        elif self.purgeconfirm == True:
            await ctx.channel.clone()
            await ctx.channel.delete()
            self.purgeconfirm = False
        else:
            self.purgeconfirm = False
            await ctx.send("wtf?? Something weird happened. Try running `p!purge` again.")

    @commands.command(name="server", help="Small list of servers to join, if you want.", aliases=["discord", "invite"], usage="[server name]")
    async def getserver(self, ctx, server=None):
        if server == "creativity":
            await ctx.send("Here is a place where you can share your creativity, regardless of what it may be.\nhttps://discord.gg/XNFjmdV")
        elif server == "sandbox":
            await ctx.send("Here is a place where you can test your bots! Please don't join if you don't make your own bot(s).\nhttps://discord.gg/My67QSZ")
        elif server == "minecraft":
            await ctx.send("Sorry, this server was taken down. It may return again in the future!")
        else:
            await ctx.send("Select a server: `creativity`, `sandbox`")


    @clear.error
    async def clearError(self, ctx, error):
        if str(error) == "You are missing Manage Messages permission(s) to run this command.":
            await ctx.send(f"{ctx.author.mention}, you have insufficient permissions (Manage Messages)")

    @purge.error
    async def purgeError(self, ctx, error):
        if str(error) == "You are missing Manage Channels permission(s) to run this command.":
            await ctx.send(f"{ctx.author.mention}, you have insufficient permissions (Manage Channels)")
        else:
            await ctx.send(f"Unhandled error occurred:\n{error}\nIf my developer (chickenmeister#7140) is not here, please tell him what the error is so that he can add handling or fix the issue!")

    @avatar.error
    async def avatarError(self, ctx, error):
        await ctx.send("Invalid user specified!")

def setup(client):
    client.add_cog(Tools(client))