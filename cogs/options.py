#!/usr/bin/python
# -*- coding: utf-8 -*-

import discord
from asyncio import sleep
from discord.ext import commands
from json import dumps
from pengaelicutils import (
	newops,
	getops,
	updop,
	jsoncheck,
	unhandling,
	tux_in_guild,
	Developers,
)
from random import choice
from re import sub
from tinydb import TinyDB, Query

devs = Developers()


class Options(commands.Cog):
	def __init__(self, client):	self.client = client
	db	= TinyDB("config.json")
	teal	= 0x007F7F
	wipe_censor_confirm	= False
	reset_options_confirm	= False
	name	= "options"
	name_typable	= name
	description	= "My settings."
	description_long	= "You need permissions to use these settings."

	# SECTION: FUNCTIONS
	# ANCHOR: TOGGLE
	async def toggle_option(self, ctx, option, disable_message, enable_message):
		status = getops(ctx.guild.id, "toggles", option)
		updop(ctx.guild.id, "toggles", option, not status)
		if status:	await ctx.send("<:winxp_information:869760946808180747>" + disable_message)
		else:	await ctx.send("<:winxp_information:869760946808180747>" + enable_message)

	# SECTION: SET
	# ANCHOR: GENERAL
	async def setop(self, ctx, option, value, optype, message):
		if ctx.author.guild_permissions.manage_roles or getops(ctx.guild.id, "roles", "botCommanderRole"):
			updop(ctx.guild.id, optype + "s", option + optype.capitalize(), value.id)
			await ctx.send(
				"<:winxp_information:869760946808180747>{} {} {} {} {}.".format(
					optype.capitalize(),
					value.mention,
					message,
					sub(r"([A-Z])", r" \1", option).lower(),
					optype,
				)  # i would use an fstring here but they don't allow backslashes
			)

		else:	await ctx.send("<:winxp_critical_error:869760946816553020>You do not have permission to use that command.")

	# ANCHOR: CHANNEL
	async def set_channel(self, ctx, option, value, message="is now set as the"):
		await self.setop(ctx, option, value, "channel", message)

	# ANCHOR: ROLE
	async def set_role(self, ctx, option, value, message="is now set as the"):
		await self.setop(ctx, option, value, "role", message)

	# END SECTION
	# END SECTION

	# SECTION: OPTIONS
	# SECTION: BASE COMMANDS
	# ANCHOR: MENU
	@commands.group(name="options", help="Show the current values of all options")
	@commands.has_permissions(manage_messages=True)
	async def read_options(self, ctx):
		if ctx.invoked_subcommand == None:
			p = self.client.command_prefix
			options = getops(ctx.guild.id)
			options.pop("lists")
			options.pop("customRoles")
			for option, value in options["channels"].items():
				try:
					if jsoncheck(ctx.guild.id):	options["channels"][option] = "#" + ctx.guild.get_channel(int(value)).name
					else:	options["channels"][option] = f"<#{ctx.guild.get_channel(int(value)).id}>"

				except AttributeError:	options["channels"][option] = "#invalid-channel"
				except TypeError:	pass
			for option, value in options["roles"].items():
				try:
					if jsoncheck(ctx.guild.id):	options["roles"][option] = "@" + ctx.guild.get_role(int(value)).name
					else:	options["roles"][option] = f"<@&{ctx.guild.get_role(int(value)).id}>"

				except AttributeError:	options["roles"][option] = "@deleted-role"
				except TypeError:	pass
			if jsoncheck(ctx.guild.id):
				jsoninfo = dumps({"options": options}, sort_keys=True, indent=4)[6:-2].replace("\n    ", "\n")
				await ctx.send(f"```json\n{jsoninfo}\n```")
			else:
				embedinfo = discord.Embed(
					title="Options",
					description="All of the options.\n"
					+ f"To set an option, type `{p}options set <option> <value>`\n"
					+ f"To toggle a toggle option, type `{p}options toggle <option>`\n"
					+ f'To add to the censor list, type `{p}options censor add "<word or phrase>"\n`'
					+ "\n",
					color=self.teal,
				)
				for category in options.items():
					embedinfo.description += f"\n**{category[0].capitalize()}**\n"
					if category[0] == "channels":
						for option in category[1].items():	embedinfo.description += f"{option[0]}: {option[1]}\n".replace("None", "No Channel Set")
					elif category[0] == "messages":
						for option in category[1].items():	embedinfo.description += f"{option[0]}: {option[1]}\n"
					elif category[0] == "roles":
						for option in category[1].items():	embedinfo.description += f"{option[0]}: {option[1]}\n".replace("None", "No Role Set")
					elif category[0] == "toggles":
						for option in category[1].items():	embedinfo.description += f"{option[0]}: {option[1]}\n".replace("False", "Disabled").replace("True", "Enabled")
				await ctx.send(embed=embedinfo)

	# ANCHOR: RESET
	@read_options.command(name="reset", help="Reset to the default options.", aliases=["defaults"])
	@commands.has_permissions(manage_messages=True)
	async def reset_options(self, ctx):
		gid = ctx.guild.id
		if not self.reset_options_confirm:
			await ctx.send("<:winxp_question:869760946904645643>Are you *really* sure you want to reset the options? Type the command again to confirm. This will expire in 10 seconds.")
			self.reset_options_confirm = True
			await sleep(10)
			if self.reset_options_confirm:	self.reset_options_confirm = False
		elif self.reset_options_confirm:
			for op in ["channels", "lists", "messages", "roles", "toggles"]:	self.db.update({op: newops()[op]}, Query().guildID == gid)
			await ctx.send("<:winxp_information:869760946808180747>Options reset to defaults.")
			await self.read_options(ctx)
			self.reset_options_confirm = False

	# ANCHOR: TOGGLE
	@read_options.group(name="toggle", help="Toggle an option.")
	async def optoggle(self, ctx):
		if ctx.invoked_subcommand is None:	await ctx.send("<:winxp_warning:869760947114348604>You didn't specify an option to toggle!")

	# ANCHOR: SET
	@read_options.group(name="set", help="Set an option.")
	async def opset(self, ctx):
		if ctx.invoked_subcommand is None:	await ctx.send("<:winxp_warning:869760947114348604>You didn't specify an option to set!")

	# END SECTION

	# SECTION: TOGGLES
	# ANCHOR[id=@toggle]: @SOMEONE
	@optoggle.command(name="atSomeone", help="Change whether custom roles should be locked to members with only a specific role.")
	@commands.has_permissions(manage_roles=True)
	async def toggle_at_someone(self, ctx):
		await self.toggle_option(ctx, "atSomeone", "Server members can no longer ping @someone.", "Server members can now ping @someone.")

	# ANCHOR[id=censortoggle]: CENSOR
	@optoggle.command(name="censor", help="Toggle the automatic deletion of messages containing specific keywords.", aliases=["filter"])
	@commands.has_permissions(manage_messages=True)
	async def toggle_censor(self, ctx):
		await self.toggle_option(ctx, "censor", "Censorship turned off.", "Censorship turned on.")

	# ANCHOR[id=dadtoggle]: DAD JOKES
	@optoggle.command(name="dadJokes", help='Toggle the automatic Dad Bot-like responses to messages starting with "I\'m".')
	@commands.has_permissions(manage_messages=True)
	async def toggle_dad_jokes(self, ctx):
		await self.toggle_option(ctx, "dadJokes", "Bye Dad, I'm the Pengaelic Bot! (dad jokes turned off)", "Hi Dad, I'm the Pengaelic Bot! (dad jokes turned on)")

	# ANCHOR[id=dedtoggle]: DEAD CHAT
	@optoggle.command(name="deadChat", help='Toggle the automatic "no u" response to someone saying "dead chat".')
	@commands.has_permissions(manage_messages=True)
	async def toggle_dead_chat(self, ctx):
		await self.toggle_option(ctx, "deadChat", "The server lives! (dead chat jokes turned off)", f"{choice(['N', 'n'])}o {choice(['U', 'u'])} (dead chat jokes turned on)")

	# ANCHOR[id=jsontoggle]: JSON MENUS
	@optoggle.command(name="jsonMenus", help="Change whether menus should be shown in embed or JSON format.")
	@commands.has_permissions(manage_messages=True)
	async def toggle_json(self, ctx):
		await self.toggle_option(ctx, "jsonMenus", "Menus will be shown in embed format.", "Menus will be shown in JSON format.")

	# ANCHOR[id=locktoggle]: LOCK CUSTOM ROLES
	@optoggle.command(name="lockCustomRoles", help="Change whether custom roles should be locked to members with only a specific role.")
	@commands.has_permissions(manage_roles=True)
	async def toggle_role_lock(self, ctx):
		message = ""
		if getops(ctx.guild.id, "roles", "customLockRole") == None:	message = f" Use `{self.client.command_prefix}options set customLockRole <role name>` to set what role they should be locked behind."
		await self.toggle_option(ctx, "lockCustomRoles", "Custom roles are now available to everyone.", "Custom roles are now locked." + message)

	# ANCHOR[id=ricktoggle]: RICK ROULETTE
	@optoggle.command(name="rickRoulette", help="Turn Rickroll-themed Russian Roulette on or off.")
	@commands.has_permissions(manage_messages=True)
	async def toggle_rick_roulette(self, ctx):
		await self.toggle_option(ctx, "rickRoulette", "You know the rules, and so do I. (Rick Roulette turned off)", "You know the rules, it's time to die. (Rick Roulette turned on)")

	# ANCHOR[id=suggtoggle]: AUTO SUGGESTIONS
	@optoggle.command(name="suggestions", help="Turn automatic poll-making on or off. This does not effect the p!suggest command.")
	@commands.has_permissions(manage_messages=True)
	async def toggle_suggestions(self, ctx):
		await self.toggle_option(ctx, "suggestions", "Auto-suggestions turned off.", "Auto-suggestions turned on.")

	# ANCHOR[id=welcometoggle]: WELCOME MESSAGES
	@optoggle.command(name="welcome", help="Toggle the automatic welcome messages.")
	@commands.has_permissions(manage_messages=True)
	async def toggle_welcome(self, ctx):
		await self.toggle_option(ctx, "welcome", "Welcome messages turned off.", "Welcome messages turned on.")

	# END SECTION

	# SECTION: ROLES
	# ANCHOR[id=cmdr]: BOT COMMANDER
	@opset.command(name="botCommanderRole", help="Set the bot commander role (required for a lot of commands).")
	@commands.has_permissions(manage_roles=True)
	async def change_cmdr_role(self, ctx, *, role: discord.Role):
		await self.set_role(ctx, "botCommander", role)

	# ANCHOR[id=customlock]: CUSTOM ROLE LOCK
	@opset.command(name="customRoleLockRole", help="Set what role is required to use custom roles.")
	@commands.has_permissions(manage_roles=True)
	async def change_required_role(self, ctx, *, role: discord.Role):
		await self.set_role(ctx, "customRoleLock", role)

	# ANCHOR[id=dramarole]: DRAMA ROLE
	@opset.command(name="dramaRole", help="Set the drama role.")
	@commands.has_permissions(manage_roles=True)
	async def change_drama_role(self, ctx, *, role: discord.Role):
		await self.set_role(ctx, "drama", role)

	# ANCHOR[id=muterole]: MUTE ROLE
	@opset.command(name="muteRole", help="Set the muted role.")
	@commands.has_permissions(manage_roles=True)
	async def change_mute_role(self, ctx, *, role: discord.Role):
		await self.set_role(ctx, "mute", role)

	# END SECTION

	# SECTION: CHANNELS
	# ANCHOR[id=dramachan]: DRAMA CHANNEL
	@opset.command(name="dramaChannel", help="Set what channel auto-suggestions should be converted in.")
	@commands.has_permissions(manage_roles=True)
	async def change_drama_channel(self, ctx, *, channel: discord.TextChannel):
		await self.set_channel(ctx, "drama", channel)

	# ANCHOR[id=suggchan]: SUGGESTIONS
	@opset.command(name="suggestionsChannel", help="Set what channel auto-suggestions should be converted in.")
	@commands.has_permissions(manage_roles=True)
	async def change_suggestions_channel(self, ctx, *, channel: discord.TextChannel):
		await self.set_channel(ctx, "suggestions", channel)

	# ANCHOR[id=welcomechan]: WELCOME CHANNEL
	@opset.command(name="welcomeChannel", help="Set what channel welcome messages should be sent in.")
	@commands.has_permissions(manage_roles=True)
	async def change_welcome_channel(self, ctx, *, channel: discord.TextChannel):
		await self.set_channel(ctx, "welcome", channel)

	# END SECTION

	# SECTION: MESSAGES
	# ANCHOR[id=welcome]: WELCOME
	@opset.command(name="welcomeMessage", help="Set what message should be sent in the welcome channel when someone joins.")
	@commands.has_permissions(manage_roles=True)
	async def change_welcome_message(self, ctx, *, message: str):
		updop(ctx.guild.id, "messages", "welcomeMessage", message)
		await ctx.send(f'<:winxp_information:869760946808180747>Welcome message set to "{message}".')

	# ANCHOR[id=goodbye]: GOODBYE
	@opset.command(name="goodbyeMessage", help="Set what message should be sent in the welcome channel when someone leaves.")
	@commands.has_permissions(manage_roles=True)
	async def change_goodbye_message(self, ctx, *, message: str):
		updop(ctx.guild.id, "messages", "goodbyeMessage", message)
		await ctx.send(f'<:winxp_information:869760946808180747>Goodbye message set to "{message}".')

	# END SECTION

	# SECTION: CENSOR
	# ANCHOR: CENSOR INFO
	@read_options.group(name="censor", help="Edit the censor.", aliases=["filter"])
	async def censor(self, ctx):
		if ctx.invoked_subcommand is None:	await ctx.send("<:winxp_information:869760946808180747>Available options: `(show/list/get), add, (delete/remove), (wipe/clear)`")

	# ANCHOR: SHOW CENSOR
	@censor.command(name="show", help="Display the contents of the censorship filter.", aliases=["list", "get"])
	@commands.has_permissions(manage_messages=True)
	async def show_censor(self, ctx):
		all_bads = list(getops(ctx.guild.id, "lists", "censorList"))
		if all_bads == [""] or all_bads == []:	await ctx.send("Filter is empty.")
		else:	await ctx.send(f'```json\n"censor list": {dumps(all_bads, indent=4, sort_keys=True)}\n```')

	# ANCHOR: ADD TO CENSOR
	@censor.command(name="add", help="Add a word to the censorship filter.", usage="<one phrase ONLY>")
	@commands.has_permissions(manage_messages=True)
	async def add_censor(self, ctx, word):
		all_bads = getops(ctx.guild.id, "lists", "censorList")
		word = word.lower()
		if word in all_bads:	await ctx.send("<:winxp_information:869760946808180747>That word is already in the filter.")
		else:
			all_bads.append(word)
			all_bads.sort()
			updop(ctx.guild.id, "lists", "censorList", all_bads)
			await ctx.send("<:winxp_information:869760946808180747>Word added to the filter.")

	# ANCHOR: REMOVE FROM CENSOR
	@censor.command(name="delete", help="Remove a word from the censorship filter.", usage="<one phrase ONLY>", aliases=["remove"])
	@commands.has_permissions(manage_messages=True)
	async def del_censor(self, ctx, word):
		all_bads = getops(ctx.guild.id, "lists", "censorList")
		word = word.lower()
		if word not in all_bads:	await ctx.send("<:winxp_information:869760946808180747>That word is not in the filter.")
		else:
			all_bads.remove(word)
			all_bads.sort()
			updop(ctx.guild.id, "lists", "censorList", all_bads)
			await ctx.send("<:winxp_information:869760946808180747>Word removed from the filter.")

	# ANCHOR: WIPE CENSOR
	@censor.command(name="wipe", help="Clear the censor file.", aliases=["clear"])
	@commands.has_permissions(manage_messages=True)
	async def wipe_censor(self, ctx):
		if not self.wipe_censor_confirm:
			await ctx.send("<:winxp_question:869760946904645643>Are you *really* sure you want to wipe the filter? Type the command again to confirm. This will expire in 10 seconds.")
			self.wipe_censor_confirm = True
			await sleep(10)
			if self.wipe_censor_confirm:	self.wipe_censor_confirm = False
		elif self.wipe_censor_confirm:
			updop(ctx.guild.id, "lists", "censorList", [])
			await ctx.send("<:winxp_information:869760946808180747>Filter wiped.")
			self.wipe_censor_confirm = False

	# END SECTION
	# END SECTION

	@read_options.error
	@reset_options.error
	@optoggle.error
	@opset.error
	@toggle_censor.error
	@toggle_dad_jokes.error
	@toggle_dead_chat.error
	@toggle_role_lock.error
	@toggle_json.error
	@toggle_rick_roulette.error
	@toggle_suggestions.error
	@toggle_welcome.error
	@change_cmdr_role.error
	@change_drama_role.error
	@change_mute_role.error
	@change_required_role.error
	@change_drama_channel.error
	@change_suggestions_channel.error
	@change_welcome_channel.error
	@change_welcome_message.error
	@change_goodbye_message.error
	@censor.error
	@show_censor.error
	@add_censor.error
	@del_censor.error
	@wipe_censor.error
	async def messageError(self, ctx, error):
		error = str(error)
		if error.startswith("You are missing") and error.endswith(
			"permission(s) to run this command."
		):
			await ctx.send(
				"<:winxp_critical_error:869760946816553020>You do not have permission to use that command."
			)
		if error.endswith('" not found.'):
			if error.startswith('Channel "'):
				await ctx.send(
					f"<:winxp_warning:869760947114348604>{ctx.author.mention}, that isn't a valid channel."
				)
			if error.startswith('Role "'):
				await ctx.send(
					f"<:winxp_warning:869760947114348604>{ctx.author.mention}, that isn't a valid role."
				)
		else:
			await ctx.send(
				unhandling(
					error,
					tux_in_guild(ctx, self.client),
				)
			)


def setup(client):	client.add_cog(Options(client))
