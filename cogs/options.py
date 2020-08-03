import discord
from discord.ext import commands
from discord.utils import get
from json import load, dump, dumps

class options(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.wipecensorcinfirm = False
    name = "options"
    name_typable = name
    description = "My settings."
    description_long = description + ' You need the "Manage Messages" permission to use these settings.\nType `pn!help options [option]` for more info on each subcategory.'

    async def updateOptions(self, guild, options2dump):
        with open(rf"data/servers/{guild.id}/config.json", "w") as optionsfile:
            dump(
                options2dump,
                optionsfile,
                sort_keys=True,
                indent=4
            )
            print(
                f"""Options file updated for {
                    guild.name
                }"""
            )

    @commands.command(name="options", help="Show the current values of all options")
    @commands.has_permissions(manage_messages=True)
    async def getOptions(self, ctx):
        with open(rf"data/servers/{ctx.guild.id}/config.json", "r") as optionsfile:
            await ctx.send(
                f"""```json
{
    optionsfile.read()
}
```"""
            )

    @commands.command(name="reset", help="Reset to the default options.", aliases=["defaults"])
    @commands.has_permissions(manage_messages=True)
    async def resetOptions(self, ctx):
        with open(r"data/default_options.json", "r") as defaultoptions:
            await self.updateOptions(
                ctx.guild,
                load(
                    defaultoptions
                )
            )
            await ctx.send(
                "Options reset to defaults."
            )
            await ctx.send(
                defaultoptions.read()
            )

    @commands.command(name="rudeness", help="Change how rude the bot can be.", usage="<level>")
    @commands.has_permissions(manage_messages=True)
    async def rudeLevel(self, ctx, level: int=-9999):
        with open(rf"data/servers/{ctx.guild.id}/config.json", "r") as optionsfile:
            allOptions = load(optionsfile)
        if level == -9999:
            await ctx.send(
                f"""Current rudeness level is {
                    allOptions['numbers']['rudeness']
                }"""
            )
        else:
            if level < 0:
                await ctx.send(
                    "Sorry pal, can't go below 0."
                )
            else:
                if level > 3:
                    await ctx.send(
                        "Sorry pal, 3 is the highest it can go (for now)."
                    )
                    allOptions["numbers"]["rudeness"] = 3
                    await ctx.send(
                        "Rudeness level set to 3"
                    )
                    await self.updateOptions(
                        ctx.guild,
                        allOptions
                    )
                else:
                    allOptions["numbers"]["rudeness"] = level
                    await ctx.send(
                        f"""Rudeness level set to {
                            level
                        }"""
                    )
                    await self.updateOptions(
                        ctx.guild,
                        allOptions
                    )

    @commands.group(name="toggle", help="Toggle an option.")
    async def toggle(self, ctx):
        if ctx.invoked_subcommand is None:
            with open(rf"data/servers/{ctx.guild.id}/config.json", "r") as optionsfile:
                allToggles = load(
                    optionsfile
                )["toggles"]
                await ctx.send(
                    "Available toggles: `{}`".format(
                        str(
                            allToggles.remove(
                                "cogs"
                            )
                        )[
                            1:-1
                        ].replace(
                            "'",
                            ""
                        )
                    )
                )

    @toggle.command(name="censor", help="Toggle the automatic deletion of messages containing specific keywords.", aliases=["filter"])
    @commands.has_permissions(manage_messages=True)
    async def toggleCensor(self, ctx):
        with open(rf"data/servers/{ctx.guild.id}/config.json", "r") as optionsfile:
            allOptions = load(
                optionsfile
            )
        if allOptions["toggles"]["censor"] == True:
            allOptions["toggles"]["censor"] = False
            await ctx.send(
                "Censorship turned off."
            )
        else:
            allOptions["toggles"]["censor"] = True
            await ctx.send(
                "Censorship turned on."
            )
        await self.updateOptions(
            ctx.guild,
            allOptions
        )

    @toggle.command(name="dad", help="Toggle the automatic Dad Bot-like responses to messages starting with \"I'm\".")
    @commands.has_permissions(manage_messages=True)
    async def toggleDad(self, ctx):
        with open(rf"data/servers/{ctx.guild.id}/config.json", "r") as optionsfile:
            allOptions = load(optionsfile)
        if allOptions["toggles"]["jokes"]["dad"] == True:
            allOptions["toggles"]["jokes"]["dad"] = False
            await ctx.send("Bye Dad, I'm Pengaelic Bot Nightly!")
        else:
            allOptions["toggles"]["jokes"]["dad"] = True
            await ctx.send("Hi Dad, I'm Pengaelic Bot Nightly!")
        await self.updateOptions(
            ctx.guild,
            allOptions
        )

    @toggle.command(name="mama", help="Toggle the automatic Yo Mama jokes.")
    @commands.has_permissions(manage_messages=True)
    async def toggleMama(self, ctx):
        with open(rf"data/servers/{ctx.guild.id}/config.json", "r") as optionsfile:
            allOptions = load(optionsfile)
        if allOptions["toggles"]["jokes"]["yoMama"] == True:
            allOptions["toggles"]["jokes"]["yoMama"] = False
            await ctx.send(
                "Yo Mama jokes turned off."
            )
            await self.updateOptions(
                ctx.guild,
                allOptions
            )
        else:
            if allOptions["numbers"]["rudeness"] > 1:
                allOptions["toggles"]["jokes"]["yoMama"] = True
                await ctx.send(
                    "Yo Mama jokes turned on."
                )
                await self.updateOptions(
                ctx.guild,
                allOptions
            )
            else:
                await ctx.send(
                    "Unable to turn on Yo Mama jokes: Rudeness level is below 2"
                )

    @toggle.command(name="welcome", help="Toggle the automatic welcome messages.")
    @commands.has_permissions(manage_messages=True)
    async def toggleWelcome(self, ctx):
        with open(rf"data/servers/{ctx.guild.id}/config.json", "r") as optionsfile:
            allOptions = load(optionsfile)
        if allOptions["toggles"]["welcome"] == True:
            allOptions["toggles"]["welcome"] = False
            await ctx.send(
                "Welcome message turned off."
            )
        else:
            allOptions["toggles"]["welcome"] = True
            await ctx.send(
                "Welcome message turned on."
            )
        await self.updateOptions(
            ctx.guild,
            allOptions
        )

    @toggle.command(name="polls", help="Turn automatic poll-making on or off. This does not effect the p!suggest command.")
    @commands.has_permissions(manage_messages=True)
    async def togglePolls(self, ctx):
        with open(rf"data/servers/{ctx.guild.id}/config.json", "r") as optionsfile:
            allOptions = load(optionsfile)
        if allOptions["toggles"]["polls"] == True:
            allOptions["toggles"]["polls"] = False
            await ctx.send(
                "Polls turned off."
            )
        else:
            allOptions["toggles"]["polls"] = True
            await ctx.send(
                "Polls turned on."
            )
            fails = 0
            pollchannels = [
                "polls",
                "petition",
                "suggestions"
            ]
            for channel in pollchannels:
                try:
                    get(
                        ctx.guild.text_channels,
                        name=channel
                    )
                    break
                except:
                    fails+=1
            if fails == len(pollchannels):
                await ctx.send(
                    "Warning: There are no channels for the polls to work in. Please create a channel #polls, #petition, or #suggestions."
                )
        await self.updateOptions(
            ctx.guild,
            allOptions
        )

    @commands.group(name="censor", help="Edit the censor.", aliases=["filter"])
    async def filter(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                "Available options: `(show/list/get), add, delete, (wipe/clear)`"
            )

    @filter.command(name="show", help="Display the contents of the censorship filter.", aliases=["list", "get"])
    @commands.has_permissions(manage_messages=True)
    async def showFilter(self, ctx):
        with open(rf"data/servers/{ctx.guild.id}/censor.txt", "r") as bads_file:
            all_bads = bads_file.read()
            if all_bads.split(', ') == ['']:
                await ctx.send(
                    "Filter is empty."
                )
            else:
                await ctx.send(
                    f"""Censor list is as follows...
                    ```{
                        all_bads
                    }```"""
                )

    @filter.command(name="add", help="Add a word to the censorship filter.", usage="<one phrase ONLY>")
    @commands.has_permissions(manage_messages=True)
    async def addFilter(self, ctx, word2add):
        with open(rf"data/servers/{ctx.guild.id}/censor.txt", "r") as bads_file:
            all_bads = bads_file.read()
            oneword = []
            if ", " in all_bads:
                all_bads = all_bads.split(
                    ", "
                )
            else:
                oneword.append(
                    all_bads
                )
                all_bads = oneword
            if all_bads == [""]:
                all_bads = []
            if word2add in all_bads:
                await ctx.send(
                    "That word is already in the filter."
                )
            else:
                all_bads.append(
                    word2add
                )
                all_bads.sort()
                finalbads = str(
                    all_bads
                )[1:-1].replace(
                    "'",
                    ""
                )
                with open(rf"data/servers/{ctx.guild.id}/censor.txt", "w") as bads_file_to:
                    bads_file_to.write(
                        finalbads
                    )
                    await ctx.send(
                        "Word added to the filter."
                    )
                    print(
                        f"""Censor file updated for {
                            ctx.guild.name
                        }"""
                    )

    @filter.command(name="delete", help="Remove a word from the censorship filter.", usage="<one phrase ONLY>")
    @commands.has_permissions(manage_messages=True)
    async def delFilter(self, ctx, word2del):
        with open(rf"data/servers/{ctx.guild.id}/censor.txt", "r") as bads_file:
            all_bads = bads_file.read()
            oneword = []
            if ", " in all_bads:
                all_bads = all_bads.split(
                    ", "
                )
            else:
                oneword.append(
                    all_bads
                )
                all_bads = oneword
            if all_bads == [""]:
                all_bads = []
            if word2del not in all_bads:
                await ctx.send(
                    "That word is not in the filter."
                )
            else:
                all_bads.remove(
                    word2del
                )
                all_bads.sort()
                finalbads = str(
                    all_bads
                )[1:-1].replace(
                    "'",
                    ""
                )
                with open(rf"data/servers/{ctx.guild.id}/censor.txt", "w") as bads_file_to:
                    bads_file_to.write(
                        finalbads
                    )
                    await ctx.send(
                        "Word removed from the filter."
                    )
                    print(
                        f"""Censor file updated for {
                            ctx.guild.name
                        }"""
                    )

    @filter.command(name="wipe", help="Clear the censor file.", aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    async def wipeFilter(self, ctx):
        if self.wipecensorcinfirm == False:
            await ctx.send(
                "Are you **really** sure you want to clear the censor filter? Type p!wipecensor again to confirm."
            )
            self.wipecensorcinfirm = True
        else:
            open(
                rf"""data/servers/{
                    ctx.guild.id
                }/censor.txt""",
                "w"
            ).close()
            await ctx.send(
                "Filter cleared."
            )
            print(
                f"""Censor file wiped for {
                    ctx.guild.name
                }"""
            )
            self.wipecensorcinfirm = False

    @commands.group(name="cog", help="Edit the modules.", aliases=["module"])
    async def modules(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                "Available options: `list`, `(load/enable)`, `(unload/disable)`"
            )

    @modules.command(name="list", help="See a list of all cogs and their statuses.")
    @commands.has_permissions(manage_messages=True)
    async def cogList(self, ctx, cog2load=None):
        with open(rf"data/servers/{ctx.guild.id}/config.json", "r") as optionsfile:
            await ctx.send(
                f"""```json{
                    dumps(
                        load(
                            optionsfile
                        )["toggles"]["cogs"],
                        indent=4
                    )
                }```"""
            )

    @modules.command(name="load", help="Load a cog.", usage="[cog to load]", aliases=["enable"])
    @commands.has_permissions(manage_messages=True)
    async def loadCog(self, ctx, cog2load=None):
        with open(rf"data/servers/{ctx.guild.id}/config.json", "r") as optionsfile:
            cogs = load(
                optionsfile
            )["toggles"]["cogs"]
            inactivecogs = [
                cog
                for cog in cogs
                if cogs[cog] == False
            ]

        if len(inactivecogs) == 0:
            await ctx.send(
                "All cogs are already loaded, you can't load any more."
            )
        else:
            if cog2load:
                try:
                    with open(rf"data/servers/{ctx.guild.id}/config.json", "r") as optionsfile:
                        allOptions = load(
                            optionsfile
                        )
                        _ = allOptions["toggles"]["cogs"][cog2load]
                        allOptions["toggles"]["cogs"][cog2load] = True
                        await self.updateOptions(
                            ctx.guild,
                            allOptions
                        )
                    await ctx.send(
                        f"""Cog `{
                            cog2load
                        }` loaded. Type `p!help {
                            cog2load
                        }` to see how it works.""")
                    print(
                        f"""Cog '{
                            cog2load
                        }' loaded for {
                            ctx.guild.name
                        }""")
                except:
                    await ctx.send(
                        f"""Invalid cog `{
                            cog2load
                        }`"""
                    )
            else:
                await ctx.send(
                    "Please specify a cog to load. Avaliable options are {}".format(
                        str(
                            inactivecogs
                        )[1:-1].replace(
                        "'",
                        ""
                        )
                    )
                )

    @modules.command(name="unload", help="Unload a cog.", usage="[cog to unload]", aliases=["disable"])
    @commands.has_permissions(manage_messages=True)
    async def unloadCog(self, ctx, cog2unload=None):
        with open(rf"data/servers/{ctx.guild.id}/config.json", "r") as optionsfile:
            cogs = load(
                optionsfile
            )["toggles"]["cogs"]
            activecogs = [
                cog
                for cog in cogs
                if cogs[cog] == True
            ]

        if len(activecogs) == 0:
            await ctx.send(
                "No cogs are loaded, you can't unload any more."
            )
        else:
            if cog2unload:
                try:
                    with open(rf"data/servers/{ctx.guild.id}/config.json", "r") as optionsfile:
                        allOptions = load(optionsfile)
                        _ = allOptions["toggles"]["cogs"][cog2unload]
                        allOptions["toggles"]["cogs"][cog2unload] = False
                        await self.updateOptions(
                            ctx.guild,
                            allOptions
                        )
                    await ctx.send(
                        f"""Cog `{
                            cog2unload
                        }` unloaded."""
                    )
                    print(
                        f"""Cog '{
                            cog2unload
                        }' unloaded for {
                            ctx.guild.name
                        }"""
                    )
                except:
                    await ctx.send(
                        f"""Invalid cog `{
                            cog2unload
                        }`"""
                    )
            else:
                await ctx.send(
                    "Please specify a cog to unload. Avaliable options are {}".format(
                        str(
                            activecogs
                        ).lower()[1:-1].replace(
                            "\'",
                            ""
                        )
                    )
                )

    @resetOptions.error
    @toggleCensor.error
    @toggleDad.error
    @toggleMama.error
    @toggleWelcome.error
    @togglePolls.error
    @cogList.error
    @loadCog.error
    @unloadCog.error
    @filter.error
    @showFilter.error
    @addFilter.error
    @delFilter.error
    @wipeFilter.error
    @rudeLevel.error
    @getOptions.error
    async def messageError(self, ctx, error):
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

def setup(client):
    client.add_cog(
        options(
            client
        )
    )