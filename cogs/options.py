import discord
import sqlite3
from discord.ext import commands
from discord.utils import get
from json import load, dump, dumps
from asyncio import sleep

class Options(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.wipe_censor_confirm = False
        self.reset_options_confirm = False
        self.db = "data/config.db"
    name = "options"
    name_typable = name
    description = "My settings."
    description_long = description + ' You need the "Manage Messages" permission to use these settings.\nType `pn!help options [option]` for more info on each subcategory.'

    def updateOption(self, database, table, guild: int, option: str, value: bool):
        conn = sqlite3.connect(
            database
        )
        with conn:
            sql = f"""UPDATE {table}
                    SET {option} = ?
                    WHERE id = ?"""
            cur = conn.cursor()
            cur.execute(
                sql,
                (value, guild)
            )
            conn.commit()

    def get_options(self, database, table, guild):
        conn = sqlite3.connect(
            database
        )
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        rows = cur.execute(
            f"SELECT * from {table}"
        ).fetchall()

        conn.commit()
        conn.close()

        currentserver = [
            server
            for server in [
                dict(ix)
                for ix in rows
            ]
            if server["id"] == guild
            ][0]

        currentserver.pop(
            "id"
        )

        return currentserver

    @commands.command(name = "options", help = "Show the current values of all options")
    @commands.has_permissions(manage_messages = True)
    async def read_options(self, ctx):
        await ctx.send(
            f"""```json
{
    dumps(
        [
            "Options",
            self.get_options(
                self.db,
                "options",
                ctx.guild.id
            ),
            "Cogs",
            self.get_options(
                self.db,
                "cogs",
                ctx.guild.id
            )
        ],
        indent = 4
    )
}
```"""
        )

    @commands.command(name = "reset", help = "Reset to the default options.", aliases = ["defaults"])
    @commands.has_permissions(manage_messages = True)
    async def reset_options(self, ctx):
        if self.reset_options_confirm == False:
            await ctx.send(
                "Are you *really* sure you want to reset the options? Type the command again to confirm. This will expire in 10 seconds."
            )
            self.reset_options_confirm = True
            await sleep(
                10
            )
            self.reset_options_confirm = False
            await ctx.send(
                "Pending reset expired."
            )
        elif self.reset_options_confirm == True:
            conn = sqlite3.connect(
                self.db
            )
            with conn:
                options = f""" UPDATE options
                        SET censor = ?,
                            dadJokes = ?,
                            polls = ?,
                            welcome = ?,
                            yoMamaJokes = ?
                        WHERE id = {ctx.guild.id}"""
                cogs = f""" UPDATE cogs
                        SET actions = ?,
                            actsofviolence = ?,
                            converters = ?,
                            foods = ?,
                            games = ?,
                            generators = ?,
                            interactions = ?,
                            messages = ?,
                            oddcommands = ?,
                            noncommands = ?,
                            tools = ?
                        WHERE id = {ctx.guild.id}"""
                cur = conn.cursor()
                cur.execute(
                    options,
                    (
                        1,
                        0,
                        0,
                        1,
                        0
                    )
                )
                cur.execute(
                    cogs,
                    (
                        1,
                        0,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1
                    )
                )
                conn.commit()
            await ctx.send(
                "Options reset to defaults."
            )
            await self.read_options(
                ctx
            )
            self.reset_options_confirm = False

    @commands.group(name = "toggle", help = "Toggle an option.")
    async def toggle(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                """```fix
Available options are as follows...
```"""
f"""```ini
[ {
    str(
        list(
            self.get_options(
                'data/config.db',
                'options',
                ctx.guild.id
            ).keys()
        )
    ).replace(
        "'",
        ""
    )[1:-1]
} ]
```"""
f"""```fix
Type {self.client.command_prefix}toggle <option> to turn it on or off.
Type {self.client.command_prefix}options to see their values.
```"""
            )

    @toggle.command(name = "censor", help = "Toggle the automatic deletion of messages containing specific keywords.", aliases = ["filter"])
    @commands.has_permissions(manage_messages = True)
    async def toggle_censor(self, ctx):
        if self.get_options(self.db, "options", ctx.guild.id)["censor"] == 1:
            self.updateOption(
                self.db,
                "options",
                ctx.guild.id,
                "censor",
                False
            )
            await ctx.send(
                "Censorship turned off."
            )
        else:
            self.updateOption(
                self.db,
                "options",
                ctx.guild.id,
                "censor",
                True
            )
            await ctx.send(
                "Censorship turned on."
            )

    @toggle.command(name = "dadJokes", help = "Toggle the automatic Dad Bot-like responses to messages starting with \"I'm\".")
    @commands.has_permissions(manage_messages = True)
    async def toggle_dad_jokes(self, ctx):
        if self.get_options(self.db, "options", ctx.guild.id)["dadJokes"] == 1:
            self.updateOption(
                self.db,
                "options",
                ctx.guild.id,
                "dadJokes",
                False
            )
            await ctx.send(
                "Bye Dad, I'm Pengaelic Bot Nightly!"
            )
        else:
            self.updateOption(
                self.db,
                "options",
                ctx.guild.id,
                "dadJokes",
                True
            )
            await ctx.send(
                "Hi Dad, I'm Pengaelic Bot Nightly!"
            )

    @toggle.command(name = "yoMamaJokes", help = "Toggle the automatic Yo Mama jokes.")
    @commands.has_permissions(manage_messages = True)
    async def toggle_yo_mama_jokes(self, ctx):
        if self.get_options(self.db, "options", ctx.guild.id)["yoMamaJokes"] == 1:
            self.updateOption(
                self.db,
                "options",
                ctx.guild.id,
                "yoMamaJokes",
                False
            )
            await ctx.send(
                "Yo Mama jokes turned off."
            )
        else:
            self.updateOption(
                self.db,
                "options",
                ctx.guild.id,
                "yoMamaJokes",
                True
            )
            await ctx.send(
                "Yo Mama jokes turned on."
            )

    @toggle.command(name = "welcome", help = "Toggle the automatic welcome messages.")
    @commands.has_permissions(manage_messages = True)
    async def toggle_welcome(self, ctx):
        if self.get_options(self.db, "options", ctx.guild.id)["welcome"] == 1:
            self.updateOption(
                self.db,
                "options",
                ctx.guild.id,
                "welcome",
                False
            )
            await ctx.send(
                "Welcome messages turned off."
            )
        else:
            self.updateOption(
                self.db,
                "options",
                ctx.guild.id,
                "welcome",
                True
            )
            await ctx.send(
                "Welcome messages turned on."
            )

    @toggle.command(name = "polls", help = "Turn automatic poll-making on or off. This does not effect the p!suggest command.")
    @commands.has_permissions(manage_messages = True)
    async def toggle_polls(self, ctx):
        if self.get_options(self.db, "options", ctx.guild.id)["polls"] == 1:
            self.updateOption(
                self.db,
                "options",
                ctx.guild.id,
                "polls",
                False
            )
            await ctx.send(
                "Polls turned off."
            )
        else:
            self.updateOption(
                self.db,
                "options",
                ctx.guild.id,
                "polls",
                True
            )
            await ctx.send(
                "Polls turned on."
            )

    @commands.group(name = "censor", help = "Edit the censor.", aliases = ["filter"])
    async def censor(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                "Available options: `(show/list/get), add, delete, (wipe/clear)`"
            )

    @censor.command(name = "show", help = "Display the contents of the censorship filter.", aliases = ["list", "get"])
    @commands.has_permissions(manage_messages = True)
    async def show_censor(self, ctx):
        with open(rf"data/{ctx.guild.id}censor.txt", "r") as bads_file:
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

    @censor.command(name = "add", help = "Add a word to the censorship filter.", usage = "<one phrase ONLY>")
    @commands.has_permissions(manage_messages = True)
    async def add_censor(self, ctx, word2add):
        with open(rf"data/{ctx.guild.id}censor.txt", "r") as bads_file:
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
                with open(rf"data/{ctx.guild.id}censor.txt", "w") as bads_file_to:
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

    @censor.command(name = "delete", help = "Remove a word from the censorship filter.", usage = "<one phrase ONLY>", aliases = ["remove"])
    @commands.has_permissions(manage_messages = True)
    async def del_censor(self, ctx, word2del):
        with open(rf"data/{ctx.guild.id}censor.txt", "r") as bads_file:
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
                with open(rf"data/{ctx.guild.id}censor.txt", "w") as bads_file_to:
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

    @censor.command(name = "wipe", help = "Clear the censor file.", aliases = ["clear"])
    @commands.has_permissions(manage_messages = True)
    async def wipe_censor(self, ctx):
        if self.wipe_censor_confirm == False:
            await ctx.send(
                "Are you *really* sure you want to wipe the filter? Type the command again to confirm. This will expire in 10 seconds."
            )
            self.wipe_censor_confirm = True
            await sleep(
                10
            )
            self.wipe_censor_confirm = False
            await ctx.send(
                "Pending wipe expired."
            )
        elif self.wipe_censor_confirm == True:
            open(
                rf"data/{ctx.guild.id}censor.txt",
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
            self.wipe_censor_confirm = False

    @commands.group(name = "cog", help = "Edit the modules.", aliases = ["module"])
    async def modules(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                "Available options: `list`, `(load/enable)`, `(unload/disable)`"
            )

    @modules.command(name = "list", help = "See a list of all cogs and their statuses.")
    @commands.has_permissions(manage_messages = True)
    async def list_cogs(self, ctx, cog2load = None):
        await ctx.send(
            """```fix
Available cogs are as follows...
```"""
f"""```ini
[ {
    str(
        list(
            self.get_options(
                'data/config.db',
                'cogs',
                ctx.guild.id
            ).keys()
        )
    ).replace(
        "'",
        ""
    )[1:-1]
} ]
```"""
f"""```fix
Type {self.client.command_prefix}cog load <cog> to enable it.
Type {self.client.command_prefix}cog unload <cog> to disable it.
```"""
        )

    @modules.command(name = "load", help = "Load a cog.", usage = "[cog to load]", aliases = ["enable"])
    @commands.has_permissions(manage_messages = True)
    async def enable_cog(self, ctx, cog2load = None):
        cogs = self.get_options(
            self.db,
            "cogs",
            ctx.guild.id
        )
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
                    self.updateOption(
                        self.db,
                        "cogs",
                        ctx.guild.id,
                        cog2load,
                        True
                    )
                    await ctx.send(
                        f"""Cog `{
                            cog2load
                        }` loaded. Type `{self.client.command_prefix}!help {
                            cog2load
                        }` to see how it works.""")
                    print(
                        f"""Cog '{
                            cog2load
                        }' loaded for {
                            ctx.guild.name
                        }""")
                except sqlite3.OperationalError:
                    await ctx.send(
                        f"""Invalid cog `{
                            cog2load
                        }`"""
                    )
            else:
                await ctx.send(
                    """Please specify a cog to load. Avaliable options are
```ini
[ {} ]
```""".format(
                        str(
                            inactivecogs
                        )[1:-1].replace(
                        "'",
                        ""
                        )
                    )
                )

    @modules.command(name = "unload", help = "Unload a cog.", usage = "[cog to unload]", aliases = ["disable"])
    @commands.has_permissions(manage_messages = True)
    async def disable_cog(self, ctx, cog2unload = None):
        cogs = self.get_options(
            self.db,
            "cogs",
            ctx.guild.id
        )
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
                    _ = self.get_options(self.db, "cogs", ctx.guild.id)[cog2unload]
                    self.updateOption(
                        self.db,
                        "cogs",
                        ctx.guild.id,
                        cog2unload,
                        False
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
                except sqlite3.OperationalError:
                    await ctx.send(
                        f"""Invalid cog `{
                            cog2unload
                        }`"""
                    )
            else:
                await ctx.send(
                    """Please specify a cog to load. Avaliable options are
```ini
[ {} ]
```""".format(
                        str(
                            activecogs
                        )[1:-1].replace(
                        "'",
                        ""
                        )
                    )
                )

    @reset_options.error
    @toggle_censor.error
    @toggle_dad_jokes.error
    @toggle_yo_mama_jokes.error
    @toggle_welcome.error
    @toggle_polls.error
    @list_cogs.error
    @enable_cog.error
    @disable_cog.error
    @censor.error
    @show_censor.error
    @add_censor.error
    @del_censor.error
    @wipe_censor.error
    @read_options.error
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
        Options(
            client
        )
    )