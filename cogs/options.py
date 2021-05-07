# -*- coding: utf-8 -*-

import discord
from asyncio import sleep
from discord.ext import commands
from json import dumps
from pengaelicutils import newops, getops
from random import choice
from tinydb import TinyDB, Query

class Options(commands.Cog):
    def __init__(self, client):
        self.client = client
    db = TinyDB("config.json")
    teal = 0x007f7f
    wipe_censor_confirm = False
    reset_options_confirm = False
    name = "options"
    name_typable = name
    description = "My settings."
    description_long = "You need permissions to use these settings."

    def update_option(self, guild: str, category: str, option: str, value):
        options = self.db.all()[0][str(guild)]
        options[category][option] = value
        self.db.update({guild: options})

    async def toggle_option(self, ctx, option, disable_message, enable_message):
        status = getops(ctx.guild.id, "toggles", option)
        self.update_option(ctx.guild.id, "toggles", option, not status)
        if status:
            await ctx.send(disable_message)
        else:
            await ctx.send(enable_message)

    @commands.group(name="options", help="Show the current values of all options")
    @commands.has_permissions(manage_messages=True)
    async def read_options(self, ctx):
        if ctx.invoked_subcommand == None:
            p = self.client.command_prefix
            options = getops(ctx.guild.id)
            jsoninfo = str(
                dumps(
                    {"options": options},
                    sort_keys=True,
                    indent=4
                )[6:-2].replace("\n    ", "\n")
            )
            header = discord.Embed(
                title="Options",
                description=f'All of the options.\nTo set an option, type `{p}options set <option> <value>`\nTo toggle a toggle option, type `{p}options toggle <option>`\nTo add to the censor list, type `{p}options censor add "<word or phrase>"',
                color=self.teal
            )
            channels = discord.Embed(
                title="Channels",
                description="Channels for specific functions.",
                color=self.teal
            )
            lists = discord.Embed(
                title="Lists",
                description="The censor list. Maybe more lists will be necessary in the future, I don't know.",
                color=self.teal
            )
            roles = discord.Embed(
                title="Roles",
                description="Roles for specific functions.",
                color=self.teal
            )
            toggles = discord.Embed(
                title="Toggles",
                description="Toggleable options.",
                color=self.teal
            )
            for category in options.items():
                if category[0] == "channels":
                    for option in category[1].items():
                        channels.add_field(
                            name=option[0],
                            value=str(option[1]).replace("None", "No Channel Set")
                        )
                elif category[0] == "lists":
                    for option in category[1].items():
                        lists.add_field(
                            name=option[0],
                            value=str(option[1]).replace("None", "Empty")
                        )
                elif category[0] == "roles":
                    for option in category[1].items():
                        roles.add_field(
                            name=option[0],
                            value=str(option[1]).replace("None", "No Role Set")
                        )
                elif category[0] == "toggles":
                    for option in category[1].items():
                        toggles.add_field(
                            name=option[0],
                            value=str(option[1]).replace("False", "Disabled").replace("True", "Enabled")
                        )
            if getops(ctx.guild.id, "toggles", "jsonMenus"):
                await ctx.send(f"```json\n{jsoninfo}\n```")
            else:
                for embed in [header, channels, lists, roles, toggles]:
                    await ctx.send(embed=embed)

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
            self.db.update({str(ctx.guild.id): newops()})
            await ctx.send("Options reset to defaults.")
            await self.read_options(ctx)
            self.reset_options_confirm = False

    @read_options.group(name="toggle", help="Toggle an option.")
    async def optoggle(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("You didn't specify an option to toggle!")

    @read_options.group(name="set", help="Set an option.")
    async def opset(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("You didn't specify an option to set!")

    @optoggle.command(name="censor", help="Toggle the automatic deletion of messages containing specific keywords.", aliases=["filter"])
    @commands.has_permissions(manage_messages=True)
    async def toggle_censor(self, ctx):
        await self.toggle_option(ctx, "censor", "Censorship turned off.", "Censorship turned on.")

    @optoggle.command(name="dadJokes", help="Toggle the automatic Dad Bot-like responses to messages starting with \"I'm\".")
    @commands.has_permissions(manage_messages=True)
    async def toggle_dad_jokes(self, ctx):
        await self.toggle_option(ctx, "dadJokes", "Bye Dad, I'm the Pengaelic Bot! (dad jokes turned off)", "Hi Dad, I'm the Pengaelic Bot! (dad jokes turned on)")

    @optoggle.command(name="deadChat", help="Toggle the automatic \"no u\" response to someone saying \"dead chat\".")
    @commands.has_permissions(manage_messages=True)
    async def toggle_dead_chat(self, ctx):
        await self.toggle_option(ctx, "deadChat", "The server lives! (dead chat jokes turned off)", f"{choice(['N', 'n'])}o {choice(['U', 'u'])} (dead chat jokes turned on)")

    @optoggle.command(name="jsonMenus", help="Change whether menus should be shown in embed or JSON format.")
    @commands.has_permissions(manage_messages=True)
    async def toggle_json(self, ctx):
        await self.toggle_option(ctx, "jsonMenus", "Menus will be shown in embed format.", "Menus will be shown in JSON format.")

    @optoggle.command(name="lockCustomRoles", help="Change whether custom roles should be locked to members with only a specific role.")
    @commands.has_permissions(manage_roles=True)
    async def toggle_role_lock(self, ctx):
        await self.toggle_option(ctx, "lockCustomRoles", "Custom roles are now available to everyone.", f"Custom roles are now locked. Use `{self.client.command_prefix}options roleRequiredForCustomRoles @role_name` to set what role they should be locked behind.")

    @optoggle.command(name="suggestions", help="Turn automatic poll-making on or off. This does not effect the p!suggest command.")
    @commands.has_permissions(manage_messages=True)
    async def toggle_suggestions(self, ctx):
        await self.toggle_option(ctx, "suggestions", "Auto-suggestions turned off.", "Auto-suggestions turned on.")

    @optoggle.command(name="rickRoulette", help="Turn Rickroll-themed Russian Roulette on or off.")
    @commands.has_permissions(manage_messages=True)
    async def toggle_rick_roulette(self, ctx):
        await self.toggle_option(ctx, "rickRoulette", "You know the rules, and so do I. (Rick Roulette turned off)", "You know the rules, it's time to die. (Rick Roulette turned on)")

    @optoggle.command(name="welcome", help="Toggle the automatic welcome messages.")
    @commands.has_permissions(manage_messages=True)
    async def toggle_welcome(self, ctx):
        await self.toggle_option(ctx, "welcome", "Welcome messages turned off.", "Welcome messages turned on.")

    @opset.command(name="customRoleLock", help="Set what role is required to use custom roles (if they're locked in the first place)")
    @commands.has_permissions(manage_roles=True)
    async def change_required_role(self, ctx, *, role: discord.Role):
        self.update_option(ctx.guild.id, "roles", "customRoleLock", role)
        await ctx.send(f"Role {role} is now required for custom roles.")

    @opset.command(name="modRole", help="Set what role the moderators are.")
    @commands.has_permissions(manage_roles=True)
    async def change_mod_role(self, ctx, *, role: discord.Role):
        self.update_option(ctx.guild.id, "roles", "moderator", role)
        await ctx.send(f"Role {role} is now set as the mod role.")

    @opset.command(name="muteRole", help="Set the muted role.")
    @commands.has_permissions(manage_roles=True)
    async def change_mute_role(self, ctx, *, role: discord.Role):
        self.update_option(ctx.guild.id, "roles", "muted", role)
        await ctx.send(f"Role {role} is now set as the muted role.")

    @opset.command(name="commandsChannel", help="Set what channel bot commands are ususally sent to.")
    @commands.has_permissions(manage_roles=True)
    async def change_bot_channel(self, ctx, *, channel: discord.TextChannel):
        self.update_option(ctx.guild.id, "channels", "commands", channel)
        await ctx.send(f"Channel {channel} is set as the default command channel.")

    @opset.command(name="suggestionsChannel", help="Set what channel auto-suggestions should be converted in.")
    @commands.has_permissions(manage_roles=True)
    async def change_suggestions_channel(self, ctx, *, channel: discord.TextChannel):
        self.update_option(ctx.guild.id, "channels", "suggestions", channel)
        await ctx.send(f"Channel {channel} is now the suggestions channel.")

    @read_options.group(name="censor", help="Edit the censor.", aliases=["filter"])
    async def censor(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Available options: `(show/list/get), add, (delete/remove), (wipe/clear)`")

    @censor.command(name="show", help="Display the contents of the censorship filter.", aliases=["list", "get"])
    @commands.has_permissions(manage_messages=True)
    async def show_censor(self, ctx):
        all_bads = list(getops(ctx.guild.id, "censorList"))
        if all_bads == ['']:
            await ctx.send("Filter is empty.")
        else:
            await ctx.send(f'```json\n"censor list": {dumps(all_bads, indent=4, sort_keys=True)}\n```')

    @censor.command(name="add", help="Add a word to the censorship filter.", usage="<one phrase ONLY>")
    @commands.has_permissions(manage_messages=True)
    async def add_censor(self, ctx, word):
        all_bads = getops(ctx.guild.id, "censorList")
        word = word.lower()
        if word in all_bads:
            await ctx.send("That word is already in the filter.")
        else:
            all_bads.append(word)
            all_bads.sort()
            self.update_option(
                ctx.guild.id,
                "lists",
                "censorList",
                all_bads
            )
            await ctx.send("Word added to the filter.")

    @censor.command(name="delete", help="Remove a word from the censorship filter.", usage="<one phrase ONLY>", aliases=["remove"])
    @commands.has_permissions(manage_messages=True)
    async def del_censor(self, ctx, word):
        all_bads = getops(ctx.guild.id, "censorList")
        word = word.lower()
        if word not in all_bads:
            await ctx.send("That word is not in the filter.")
        else:
            all_bads.remove(word)
            all_bads.sort()
            self.update_option(
                ctx.guild.id,
                "lists",
                "censorList",
                all_bads
            )
            await ctx.send("Word removed from the filter.")

    @censor.command(name="wipe", help="Clear the censor file.", aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    async def wipe_censor(self, ctx):
        if not self.wipe_censor_confirm:
            await ctx.send("Are you *really* sure you want to wipe the filter? Type the command again to confirm. This will expire in 10 seconds.")
            self.wipe_censor_confirm = True
            await sleep(10)
            if self.wipe_censor_confirm:
                self.wipe_censor_confirm = False
                await ctx.send("Pending wipe expired.")
        elif self.wipe_censor_confirm:
            self.update_option(
                ctx.guild.id,
                "lists",
                "censorList",
                []
            )
            await ctx.send("Filter wiped.")
            self.wipe_censor_confirm = False

    # @reset_options.error
    # @toggle_censor.error
    # @toggle_dad_jokes.error
    # @toggle_welcome.error
    # @toggle_suggestions.error
    # @censor.error
    # @show_censor.error
    # @add_censor.error
    # @del_censor.error
    # @wipe_censor.error
    # @read_options.error
    # async def messageError(self, ctx, error):
    #     if str(error) == "You are missing Manage Messages permission(s) to run this command.":
    #         await ctx.send(f"{ctx.author.mention}, you have insufficient permissions (Manage Messages)")
    #     else:
    #         await ctx.send(f"Unhandled error occurred:\n```{error}```\nIf my developer (<@!686984544930365440>) is not here, please tell him what the error is so that he can add handling or fix the issue!")

def setup(client):
    client.add_cog(Options(client))