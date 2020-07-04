import discord
from discord.ext import commands
from json import load, dump, dumps

class Options(commands.Cog):
    name = "options"
    description = "My settings."
    def __init__(self, client):
        self.client = client
        self.wipecensorcinfirm = False

    async def updateoptions(self, guild, options2dump):
        with open(rf"../pengaelicbot.data/configs/{guild.id}.json", "w+") as optionsfile:
            dump(options2dump, optionsfile, sort_keys=True, indent=4)
            print("Options file updated for " + guild.name)

    @commands.command(name="reset", help="Reset to the default options.", aliases=["defaults"])
    @commands.has_permissions(kick_members=True)
    async def resetoptions(self, ctx):
        with open(r"default_options.json", "r") as defaultoptions:
            await self.updateoptions(ctx.guild, load(defaultoptions))
            await ctx.send("Options reset to defaults.")
            await ctx.send(defaultoptions.read())

    @commands.command(name="togglecensor", help="Toggle the automatic deletion of messages containing specific keywords.", aliases=["togglefilter"])
    @commands.has_permissions(kick_members=True)
    async def togglecensor(self, ctx):
        with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
            allOptions = load(optionsfile)
        if allOptions["toggles"]["censor"] == True:
            allOptions["toggles"]["censor"] = False
            await ctx.send("Censorship turned off.")
        elif allOptions["toggles"]["censor"] == False:
            allOptions["toggles"]["censor"] = True
            await ctx.send("Censorship turned on.")
        await self.updateoptions(ctx.guild, allOptions)

    @commands.command(name="toggledad", help="Toggle the automatic Dad Bot-like responses to messages starting with \"I'm\".")
    @commands.has_permissions(kick_members=True)
    async def toggledad(self, ctx):
        with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
            allOptions = load(optionsfile)
        if allOptions["toggles"]["dad"] == True:
            allOptions["toggles"]["dad"] = False
            await ctx.send("Bye p!toggledad, I'm the Pengaelic Bot!")
        elif allOptions["toggles"]["dad"] == False:
            allOptions["toggles"]["dad"] = True
            await ctx.send("Hi p!toggledad, I'm the Pengaelic Bot!")
        await self.updateoptions(ctx.guild, allOptions)

    @commands.command(name="togglemama", help="Toggle the automatic Yo Mama jokes.")
    @commands.has_permissions(kick_members=True)
    async def togglemama(self, ctx):
        with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
            allOptions = load(optionsfile)
        if allOptions["toggles"]["yoMama"] == True:
            allOptions["toggles"]["yoMama"] = False
            await ctx.send("Yo Mama jokes turned off.")
        elif allOptions["toggles"]["yoMama"] == False:
            allOptions["toggles"]["yoMama"] = True
            await ctx.send("Yo Mama jokes turned on.")
        await self.updateoptions(ctx.guild, allOptions)

    @commands.command(name="rudenesslevel", help="Change how rude the bot can be.", aliases=["rudeness"], usage="<level>")
    @commands.has_permissions(manage_messages=True)
    async def rudenesslevel(self, ctx, level: int=-1):
        with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
            allOptions = load(optionsfile)
        if level == -1:
            await ctx.send("Current rudeness level is " + str(allOptions["numbers"]["rudeness"]))
        else:
            if level < 0:
                await ctx.send("Wait- What would negative rudeness even mean?")
            else:
                if level > 3:
                    await ctx.send("Sorry pal, 3 is the highest it can go.")
                    allOptions["numbers"]["rudeness"] = 3
                    await ctx.send("Rudeness level set to 3")
                    await self.updateoptions(ctx.guild, allOptions)
                else:
                    allOptions["numbers"]["rudeness"] = level
                    await ctx.send("Rudeness level set to " + str(level))
                    await self.updateoptions(ctx.guild, allOptions)

    @commands.command(name="showcensor", help="Display the contents of the censorship filter.", aliases=["showfilter", "getcensor", "getfilter", "censorlist", "filterlist"])
    @commands.has_permissions(manage_messages=True)
    async def showfilter(self, ctx):
        with open(rf"../pengaelicbot.data/censorfilters/{ctx.guild.id}.txt", "r") as bads_file:
            all_bads = bads_file.read()
            if all_bads.split(', ') == ['']:
                await ctx.send("Filter is empty.")
            else:
                await ctx.send(f"```{str(all_bads)}```")

    @commands.command(name="addcensor", help="Add a word to the censorship filter.", aliases=["addfilter"], usage="<one word ONLY>")
    @commands.has_permissions(manage_messages=True)
    async def addfilter(self, ctx, word2add):
        with open(rf"../pengaelicbot.data/censorfilters/{ctx.guild.id}.txt", "r") as bads_file:
            all_bads = bads_file.read()
            oneword = []
            if ", " in all_bads:
                all_bads = all_bads.split(", ")
            else:
                oneword.append(all_bads)
                all_bads = oneword
            if all_bads == [""]:
                all_bads = []
            if word2add in all_bads:
                await ctx.send("That word is already in the filter.")
            else:
                all_bads.append(word2add)
                all_bads.sort()
                finalbads = str(all_bads)[1:-1].replace("'","")
                with open(rf"../pengaelicbot.data/censorfilters/{ctx.guild.id}.txt", "w") as bads_file_to:
                    bads_file_to.write(finalbads)
                    await ctx.send("Word added to the filter.")
                    print("Censor file updated for " + ctx.guild.name)

    @commands.command(name="delcensor", help="Remove a word from the censorship filter.", aliases=["delfilter"], usage="<one word ONLY>")
    @commands.has_permissions(manage_messages=True)
    async def delfilter(self, ctx, word2del):
        with open(rf"../pengaelicbot.data/censorfilters/{ctx.guild.id}.txt", "r") as bads_file:
            all_bads = bads_file.read()
            oneword = []
            if ", " in all_bads:
                all_bads = all_bads.split(", ")
            else:
                oneword.append(all_bads)
                all_bads = oneword
            if all_bads == [""]:
                all_bads = []
            if word2del not in all_bads:
                await ctx.send("That word is not in the filter.")
            else:
                all_bads.remove(word2del)
                all_bads.sort()
                finalbads = str(all_bads)[1:-1].replace("'","")
                with open(rf"../pengaelicbot.data/censorfilters/{ctx.guild.id}.txt", "w") as bads_file_to:
                    bads_file_to.write(finalbads)
                    await ctx.send("Word removed from the filter.")
                    print("Censor file updated for " + ctx.guild.name)

    @commands.command(name="wipecensor", help="Clear the censor file.", aliases=["wipefilter", "clearcensor", "clearfilter"])
    @commands.has_permissions(manage_messages=True)
    async def wipefilter(self, ctx):
        if self.wipecensorcinfirm == False:
            await ctx.send("Are you **really** sure you want to clear the censor filter? Type p!wipecensor again to confirm.")
            self.wipecensorcinfirm = True
        else:
            open(rf"../pengaelicbot.data/censorfilters/{ctx.guild.id}.txt", "w").close()
            await ctx.send("Filter cleared.")
            print("Censor file wiped for " + ctx.guild.name)
            self.wipecensorcinfirm = False

    @commands.command(name="cogs", help="See a list of all cogs and their statuses.")
    async def cogs(self, ctx, cog2load=None):
        with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
            allOptions = load(optionsfile)
            cogs = dumps(allOptions["toggles"]["cogs"], indent=4)
            await ctx.send(f"```{cogs}```")

    @commands.command(name="load", help="Load a cog.", usage="[cog to load]")
    @commands.has_permissions(kick_members=True)
    async def loadcog(self, ctx, cog2load=None):
        activecogs = []
        inactivecogs = []
        with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
            allOptions = load(optionsfile)
            cogs = list(allOptions["toggles"]["cogs"].keys())
            enabled = list(allOptions["toggles"]["cogs"].values())
            for cog in range(len(cogs)):
                if enabled[cog] == True:
                    activecogs.append(cogs[cog])
                else:
                    inactivecogs.append(cogs[cog])

        if len(inactivecogs) == 0:
            await ctx.send("All cogs are already loaded, you can't load any more.")
        else:
            if cog2load:
                try:
                    with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
                        allOptions = load(optionsfile)
                        _ = allOptions["toggles"]["cogs"][cog2load]
                        allOptions["toggles"]["cogs"][cog2load] = True
                        await self.updateoptions(ctx.guild, allOptions)
                    await ctx.send(f"Cog '{cog2load}' loaded. Type `p!help {cog2load}` to see how it works.")
                    print(f"Cog '{cog2load}' loaded for {ctx.guild.name}")
                except:
                    await ctx.send(f"Invalid cog '{cog2load}'")
            else:
                await ctx.send("Please specify a cog to load. Avaliable options are " + str(inactivecogs)[1:-1].replace("\'",""))

    @commands.command(name="unload", help="Unload a cog.", usage="[cog to unload]")
    @commands.has_permissions(kick_members=True)
    async def unloadcog(self, ctx, cog2unload=None):
        activecogs = []
        with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
            allOptions = load(optionsfile)
            cogs = list(allOptions["toggles"]["cogs"].keys())
            enabled = list(allOptions["toggles"]["cogs"].values())
            for cog in range(len(cogs)):
                if enabled[cog] == True:
                    activecogs.append(cogs[cog])

        if len(activecogs) == 0:
            await ctx.send("No cogs are loaded, you can't unload any more.")
        else:
            if cog2unload:
                try:
                    with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
                        allOptions = load(optionsfile)
                        _ = allOptions["toggles"]["cogs"][cog2unload]
                        allOptions["toggles"]["cogs"][cog2unload] = False
                        await self.updateoptions(ctx.guild, allOptions)
                    await ctx.send(f"Cog '{cog2unload}' unloaded.")
                    print(f"Cog '{cog2unload}' unloaded for {ctx.guild.name}")
                except:
                    await ctx.send(f"Invalid cog '{cog2unload}'")
            else:
                await ctx.send("Please specify a cog to unload. Avaliable options are " + str(activecogs).lower()[1:-1].replace("\'",""))

    @resetoptions.error
    @togglecensor.error
    @toggledad.error
    @togglemama.error
    @loadcog.error
    @unloadcog.error
    async def kickError(self, ctx, error):
        global errorAlreadyHandled
        await ctx.send(f"{ctx.author.mention}, you have insufficient permissions (Kick Members)")
        errorAlreadyHandled = True

    @showfilter.error
    @addfilter.error
    @delfilter.error
    @wipefilter.error
    @rudenesslevel.error
    async def messageError(self, ctx, error):
        global errorAlreadyHandled
        await ctx.send(f"{ctx.author.mention}, you have insufficient permissions (Manage Messages)")
        errorAlreadyHandled = True

def setup(client):
    client.add_cog(Options(client))