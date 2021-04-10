import sqlite3
import discord
from pengaelicutils import getops
from discord.ext import commands
from json import dumps
from asyncio import sleep
from random import choice

class Options(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.wipe_censor_confirm = False
        self.reset_options_confirm = False
        self.db = "config.db"
        self.teal = 0x007f7f
    name = "options"
    name_typable = name
    description = "My settings."
    description_long = description + \
        ' You need the "Manage Messages" permission to use these settings.\nType `p!help options [option]` for more info on each subcategory.'

    def update_option(self, database, guild: int, option: str, value):
        conn = sqlite3.connect(database)
        with conn:
            sql = f"""UPDATE options
                    SET {option} = ?
                    WHERE id = ?"""
            cur = conn.cursor()
            cur.execute(
                sql,
                (value, guild)
            )
            conn.commit()

    async def toggle_option(self, ctx, option, disable_message, enable_message):
        if getops(ctx.guild.id, option):
            self.update_option(
                self.db,
                ctx.guild.id,
                option,
                False
            )
            await ctx.send(disable_message)
        else:
            self.update_option(
                self.db,
                ctx.guild.id,
                option,
                True
            )
            await ctx.send(enable_message)

    @commands.group(name="options", help="Show the current values of all options")
    @commands.has_permissions(manage_messages=True)
    async def read_options(self, ctx):
        if ctx.invoked_subcommand == None:
            options = getops(ctx.guild.id, "*")
            jsoninfo = str(
                dumps(
                    {"options": options},
                    sort_keys=True,
                    indent=4
                )[6:-2].replace("\n    ", "\n")
            )
            embedinfo = discord.Embed(
                title="Options",
                color=self.teal)
            for option in options:
                embedinfo.add_field(
                    name=option,
                    value=str(
                        options[option]
                    ).replace(
                        "False",
                        "Disabled"
                    ).replace(
                        "True",
                        "Enabled"
                    )
                )
            if getops(ctx.guild.id, "jsonMenus"):
                await ctx.send(f"```json\n{jsoninfo}\n```")
            else:
                await ctx.send(embed=embedinfo)

    @read_options.command(name="reset", help="Reset to the default options.", aliases=["defaults"])
    @commands.has_permissions(manage_messages=True)
    async def reset_options(self, ctx):
        if not self.reset_options_confirm:
            await ctx.send("Are you *really* sure you want to reset the options? Type the command again to confirm. This will expire in 10 seconds.")
            self.reset_options_confirm = True
            await sleep(10)
            if self.reset_options_confirm:
                self.reset_options_confirm = False
                await ctx.send("Pending reset expired.")
        elif self.reset_options_confirm:
            with sqlite3.connect(self.db) as conn:
                options = f""" UPDATE options
                        SET censor = ?,
                            dadJokes = ?,
                            deadChat = ?,
                            jsonMenus = ?,
                            suggestions = ?,
                            welcome = ?,
                            yoMamaJokes = ?
                        WHERE id = {ctx.guild.id}"""
                cur = conn.cursor()
                cur.execute(
                    options,
                    ([0 for _ in range(7)])
                )
                conn.commit()
            await ctx.send("Options reset to defaults.")
            await self.read_options(ctx)
            self.reset_options_confirm = False

    @commands.group(name="toggle", help="Toggle an option.")
    async def toggle(self, ctx):
        if ctx.invoked_subcommand is None:
            if getops(ctx.guild.id, "jsonMenus"):
                await ctx.send(f'```json\n"Type {self.client.command_prefix}options to see all options and their current statuses",\n"Type {self.client.command_prefix}toggle <option> to turn <option> on or off"```')
            else:
                await ctx.send(f"Type `{self.client.command_prefix}options` to see all options and their current statuses\nType `{self.client.command_prefix}toggle <option>` to turn <option> on or off")

    @toggle.command(name="censor", help="Toggle the automatic deletion of messages containing specific keywords.", aliases=["filter"])
    @commands.has_permissions(manage_messages=True)
    async def toggle_censor(self, ctx):
        await self.toggle_option(ctx, "censor", "Censorship turned off.", "Censorship turned on.")

    @toggle.command(name="dadJokes", help="Toggle the automatic Dad Bot-like responses to messages starting with \"I'm\".")
    @commands.has_permissions(manage_messages=True)
    async def toggle_dad_jokes(self, ctx):
        await self.toggle_option(ctx, "dadJokes", "Bye Dad, I'm the Pengaelic Bot! (dad jokes turned off)", "Hi Dad, I'm the Pengaelic Bot! (dad jokes turned on)")

    @toggle.command(name="deadChat", help="Toggle the automatic \"no u\" response to someone saying \"dead chat\".")
    @commands.has_permissions(manage_messages=True)
    async def toggle_dead_chat(self, ctx):
        await self.toggle_option(ctx, "deadChat", "The server lives! (dead chat jokes turned off)", f"{choice(['N', 'n'])}o {choice(['U', 'u'])} (dead chat jokes turned on)")

    @toggle.command(name="jsonMenus", help="Change whether menus should be shown in embed or JSON format.")
    @commands.has_permissions(manage_messages=True)
    async def toggle_json(self, ctx):
        await self.toggle_option(ctx, "jsonMenus", "Menus will be shown in embed format.", "Menus will be shown in JSON format.")

    @toggle.command(name="suggestions", help="Turn automatic poll-making on or off. This does not effect the p!suggest command.")
    @commands.has_permissions(manage_messages=True)
    async def toggle_suggestions(self, ctx):
        await self.toggle_option(ctx, "suggestions", "Auto-suggestions turned off.", "Auto-suggestions turned on.")

    @toggle.command(name="rickRoulette", help="Turn Rickroll-themed Russian Roulette on or off.")
    @commands.has_permissions(manage_messages=True)
    async def toggle_rick_roulette(self, ctx):
        await self.toggle_option(ctx, "rickRoulette", "You know the rules, and so do I. (Rick Roulette turned off)", "You know the rules, it's time to die. (Rick Roulette turned on)")

    @toggle.command(name="welcome", help="Toggle the automatic welcome messages.")
    @commands.has_permissions(manage_messages=True)
    async def toggle_welcome(self, ctx):
        await self.toggle_option(ctx, "welcome", "Welcome messages turned off.", "Welcome messages turned on.")

    @commands.group(name="censor", help="Edit the censor.", aliases=["filter"])
    async def censor(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Available options: `(show/list/get), add, (delete/remove), (wipe/clear)`")

    @censor.command(name="show", help="Display the contents of the censorship filter.", aliases=["list", "get"])
    @commands.has_permissions(manage_messages=True)
    async def show_censor(self, ctx):
        all_bads = list(getops(ctx.guild.id, "censorlist"))
        if all_bads == ['']:
            await ctx.send("Filter is empty.")
        else:
            await ctx.send(f'```json\n"censor list": {dumps(all_bads, indent=4, sort_keys=True)}\n```')

    @censor.command(name="add", help="Add a word to the censorship filter.", usage="<one phrase ONLY>")
    @commands.has_permissions(manage_messages=True)
    async def add_censor(self, ctx, word):
        all_bads = list(getops(ctx.guild.id, "censorlist"))
        word = word.lower()
        if all_bads == [""]:
            all_bads = []
        if word in all_bads:
            await ctx.send("That word is already in the filter.")
        else:
            all_bads.append(word)
            all_bads.sort()
            finalbads = str(all_bads)[1:-1].replace("'", "")
            self.update_option(
                self.db,
                ctx.guild.id,
                "censorlist",
                finalbads
            )
            await ctx.send("Word added to the filter.")

    @censor.command(name="delete", help="Remove a word from the censorship filter.", usage="<one phrase ONLY>", aliases=["remove"])
    @commands.has_permissions(manage_messages=True)
    async def del_censor(self, ctx, word):
        all_bads = list(getops(ctx.guild.id, "censorlist"))
        word = word.lower()
        if all_bads == [""]:
            all_bads = []
        if word not in all_bads:
            await ctx.send("That word is not in the filter.")
        else:
            all_bads.remove(word)
            all_bads.sort()
            finalbads = str(all_bads)[1:-1].replace("'", "")
            self.update_option(
                self.db,
                ctx.guild.id,
                "censorlist",
                finalbads
            )
            await ctx.send("Word removed from the filter.")

    @censor.command(name="wipe", help="Clear the censor file.", aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    async def wipe_censor(self, ctx):
        if self.wipe_censor_confirm == False:
            await ctx.send("Are you *really* sure you want to wipe the filter? Type the command again to confirm. This will expire in 10 seconds.")
            self.wipe_censor_confirm = True
            await sleep(10)
            self.wipe_censor_confirm = False
            await ctx.send("Pending wipe expired.")
        elif self.wipe_censor_confirm == True:
            self.update_option(
                self.db,
                ctx.guild.id,
                "censorlist",
                ""
            )
            self.wipe_censor_confirm = False

    @reset_options.error
    @toggle_censor.error
    @toggle_dad_jokes.error
    @toggle_welcome.error
    @toggle_suggestions.error
    @censor.error
    @show_censor.error
    @add_censor.error
    @del_censor.error
    @wipe_censor.error
    @read_options.error
    async def messageError(self, ctx, error):
        if str(error) == "You are missing Manage Messages permission(s) to run this command.":
            await ctx.send(f"{ctx.author.mention}, you have insufficient permissions (Manage Messages)")
        else:
            await ctx.send(f"Unhandled error occurred:\n```{error}```\nIf my developer (<@!686984544930365440>) is not here, please tell him what the error is so that he can add handling or fix the issue!")

def setup(client):
    client.add_cog(Options(client))