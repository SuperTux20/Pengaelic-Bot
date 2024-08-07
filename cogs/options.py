#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from asyncio	import sleep
from discord.ext	import commands
from json	import dumps
from random	import choice
from re	import sub
from tinydb	import TinyDB,	Query
from discord	import Embed,	Role,	TextChannel
from pengaelicutils	import newops_static,	newops_dynamic,	getops,	updop,	jsoncheck,	unhandling,	tux_in_guild,	Developers,	get_role

devs = Developers()


class Options(commands.Cog):
	def __init__(self, client):	self.client = client
	teal	= 0x007F7F
	db	= TinyDB("config.json")
	wipe_censor_confirm	= False
	reset_options_confirm	= False
	name	= "options"
	name_typable	= name
	description	= "My settings."
	description_long	= "You need permissions to use these settings."

	# SECTION: FUNCTIONS
	# ANCHOR: TOGGLE
	async def toggle_option(self, ctx, option):
		status = getops(ctx.guild.id, "toggles", option)
		updop(ctx.guild.id, "toggles", option, not status)
		await ctx.message.add_reaction("✅")

	# SECTION: SET
	# ANCHOR: GENERAL
	async def setop(self, ctx, option, value, optype):
		if ctx.author.guild_permissions.manage_roles or get_role(ctx.guild.id, "botCommander"):
			updop(ctx.guild.id, optype + "s", option + optype.capitalize(), value.id)
			await ctx.message.add_reaction("✅")

		else:	await ctx.send("<:winxp_critical_error:869760946816553020>You do not have permission to use that command.")

	# ANCHOR: CHANNEL
	async def set_channel(self, ctx, option, value):	await self.setop(ctx, option, value, "channel")

	# ANCHOR: ROLE
	async def set_role(self, ctx, option, value):	await self.setop(ctx, option, value, "role")
	# END SECTION
	# END SECTION

	# SECTION: OPTIONS
	# SECTION: BASE COMMANDS
	# ANCHOR: MENU
	@commands.group(name="options", help="Show the current values of all options")
	async def read_options(self, ctx):
		if ctx.author.guild_permissions.manage_messages or ctx.author.id == Developers.get("tux")["tux"]:
			if ctx.invoked_subcommand == None:
				p = self.client.command_prefix
				options = getops(ctx.guild.id)
				[options.pop(op) for op in list(newops_dynamic().keys()) + ["lists"]]
				for option, value in options["channels"].items():
					try:	options["channels"][option] = "#" + ctx.guild.get_channel(int(value)).name if jsoncheck(ctx.guild.id) else f"<#{ctx.guild.get_channel(int(value)).id}>"
					except AttributeError:	options["channels"][option] = "#invalid-channel"
					except TypeError:	pass
				for option, value in options["roles"].items():
					try:	options["roles"][option] = "@" + ctx.guild.get_role(int(value)).name if jsoncheck(ctx.guild.id) else f"<@&{ctx.guild.get_role(int(value)).id}>"
					except AttributeError:	options["roles"][option] = "@deleted-role"
					except TypeError:	pass

				if jsoncheck(ctx.guild.id):	await ctx.send("```json\n{}\n```".format(dumps({"options": options}, sort_keys=True, indent=4)[6:-2].replace("\n    ", "\n")))
				else:	await ctx.send(embed=Embed(title = "Options", description = f'All of the options.\nTo set an option, type `{p}options set <option> <value>`\nTo toggle a toggle option, type `{p}options toggle <option>`\nTo add to the censor list, type `{p}options censor add "<word or phrase>"`\n' +
						"".join(["".join([chunk for chunk in [
							f"\n\n**{category[0].capitalize()}**\n", "\n".join([
								f"{option[0]}: {option[1]}".replace("None", f"No {category[0].capitalize()[:-1]} Set")
								for option in category[1].items() if any(cat == category[0] for cat in ["channels", "roles"])]),
							"\n".join([f"{option[0]}: {option[1]}".replace("False", "Disabled").replace("True", "Enabled")
							for option in category[1].items()
							if category[0] == "toggles"]),
							"\n".join([f"{option[0]}: {option[1]}"
							for option in category[1].items()
							if category[0] == "messages"]),
							"\n".join([f"{option[0]}: {option[1]}"
							for option in category[1].items()
							if category[0] == "numbers"])
						]]) for category in options.items()]), color = self.teal))

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
			for op in ["channels", "lists", "messages", "roles", "toggles"]:	self.db.update({op: newops_static()[op]}, Query().guildID == gid)
			await ctx.send("<:winxp_information:869760946808180747>Options reset to defaults.")
			await self.read_options(ctx)
			self.reset_options_confirm = False

	# ANCHOR: TOGGLE
	@read_options.group(name="toggle", help="Toggle an option.")
	async def optoggle(self, ctx):	await ctx.send("<:winxp_warning:869760947114348604>You didn't specify a valid option to toggle!") if ctx.invoked_subcommand is None else None

	# ANCHOR: SET
	@read_options.group(name="set", help="Set an option.")
	async def opset(self, ctx):	await ctx.send("<:winxp_warning:869760947114348604>You didn't specify a valid option to set!") if ctx.invoked_subcommand is None else None
	# END SECTION

	# SECTION: TOGGLES
	# ANCHOR[id=@toggle]: @SOMEONE
	@optoggle.command(name="atSomeone", help="Change whether custom roles should be locked to members with only a specific role.")
	@commands.has_permissions(manage_roles=True)
	async def toggle_at_someone(self, ctx):	await self.toggle_option(ctx, "atSomeone")

	# ANCHOR[id=censortoggle]: CENSOR
	@optoggle.command(name="censor", help="Toggle the automatic deletion of messages containing specific keywords.", aliases=["filter"])
	@commands.has_permissions(manage_messages=True)
	async def toggle_censor(self, ctx):	await self.toggle_option(ctx, "censor")

	# ANCHOR[id=dadtoggle]: DAD JOKES
	@optoggle.command(name="dadJokes", help='Toggle the automatic Dad Bot-like responses to messages starting with "I\'m".')
	@commands.has_permissions(manage_messages=True)
	async def toggle_dad_jokes(self, ctx):	await self.toggle_option(ctx, "dadJokes")

	# ANCHOR[id=dedtoggle]: DEAD CHAT
	@optoggle.command(name="deadChat", help='Toggle the automatic "no u" response to someone saying "dead chat".')
	@commands.has_permissions(manage_messages=True)
	async def toggle_dead_chat(self, ctx):	await self.toggle_option(ctx, "deadChat")

	# ANCHOR[id=jsontoggle]: JSON MENUS
	@optoggle.command(name="jsonMenus", help="Change whether menus should be shown in embed or JSON format.")
	@commands.has_permissions(manage_messages=True)
	async def toggle_json(self, ctx):	await self.toggle_option(ctx, "jsonMenus")

	# ANCHOR[id=locktoggle]: LOCK CUSTOM ROLES
	@optoggle.command(name="lockCustomRoles", help="Change whether custom roles should be locked to members with only a specific role.")
	@commands.has_permissions(manage_roles=True)
	async def toggle_role_lock(self, ctx):	await self.toggle_option(ctx, "lockCustomRoles")

	# ANCHOR[id=ricktoggle]: RICK ROULETTE
	@optoggle.command(name="rickRoulette", help="Turn Rickroll-themed Russian Roulette on or off.")
	@commands.has_permissions(manage_messages=True)
	async def toggle_rick_roulette(self, ctx):	await self.toggle_option(ctx, "rickRoulette")

	# ANCHOR[id=suggtoggle]: AUTO SUGGESTIONS
	@optoggle.command(name="suggestions", help="Turn automatic poll-making on or off. This does not effect the p!suggest command.")
	@commands.has_permissions(manage_messages=True)
	async def toggle_suggestions(self, ctx):	await self.toggle_option(ctx, "suggestions")

	# ANCHOR[id=welcometoggle]: WELCOME MESSAGES
	@optoggle.command(name="welcome", help="Toggle the automatic welcome messages.")
	@commands.has_permissions(manage_messages=True)
	async def toggle_welcome(self, ctx):	await self.toggle_option(ctx, "welcome")
	# END SECTION

	# SECTION: ROLES
	# ANCHOR[id=cmdr]: BOT COMMANDER
	@opset.command(name="botCommanderRole", help="Set the bot commander role (required for a lot of commands).")
	@commands.has_permissions(manage_roles=True)
	async def change_cmdr_role(self, ctx, *, role: Role):	await self.set_role(ctx, "botCommander", role)

	# ANCHOR[id=customlock]: CUSTOM ROLE LOCK
	@opset.command(name="customRoleLockRole", help="Set what role is required to use custom roles.")
	@commands.has_permissions(manage_roles=True)
	async def change_required_role(self, ctx, *, role: Role):	await self.set_role(ctx, "customRoleLock", role)

	# ANCHOR[id=dramarole]: DRAMA ROLE
	@opset.command(name="dramaRole", help="Set the drama role.")
	@commands.has_permissions(manage_roles=True)
	async def change_drama_role(self, ctx, *, role: Role):	await self.set_role(ctx, "drama", role)
	# END SECTION

	# SECTION: CHANNELS
	# ANCHOR[id=dramachan]: DRAMA CHANNEL
	@opset.command(name="dramaChannel", help="Set the channel for the drama role.")
	@commands.has_permissions(manage_channels=True)
	async def change_drama_channel(self, ctx, *, channel: TextChannel):	await self.set_channel(ctx, "drama", channel)

	# ANCHOR[id=welcomechan]: GENERAL CHANNEL
	@opset.command(name="generalChannel", help="Set the general chat channel.")
	@commands.has_permissions(manage_channels=True)
	async def change_general_channel(self, ctx, *, channel: TextChannel):	await self.set_channel(ctx, "general", channel)

	# ANCHOR[id=suggchan]: SUGGESTIONS CHANNEL
	@opset.command(name="suggestionsChannel", help="Set what channel auto-suggestions should be converted in.")
	@commands.has_permissions(manage_channels=True)
	async def change_suggestions_channel(self, ctx, *, channel: TextChannel):	await self.set_channel(ctx, "suggestions", channel)

	# ANCHOR[id=welcomechan]: WELCOME CHANNEL
	@opset.command(name="welcomeChannel", help="Set what channel welcome messages should be sent in.")
	@commands.has_permissions(manage_channels=True)
	async def change_welcome_channel(self, ctx, *, channel: TextChannel):	await self.set_channel(ctx, "welcome", channel)
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

	# SECTION: NUMBERS
	# ANCHOR[id=xpd]: XP DELAY
	@opset.command(name="xpDelay", help="Set how many minutes it'll take for a user to gain XP.")
	@commands.has_permissions(manage_roles=True)
	async def change_xp_delay(self, ctx, delay: int):
		updop(ctx.guild.id, "numbers", "xpDelay", delay)
		await ctx.send(f"<:winxp_information:869760946808180747>Users will now gain XP every {delay} minutes.")

	# ANCHOR[id=xpl]: LOWER XP RANGE
	@opset.command(name="lowerXP", help="Set the lower range for random XP.")
	@commands.has_permissions(manage_roles=True)
	async def change_xp_lower_bound(self, ctx, xp: int):
		updop(ctx.guild.id, "numbers", "xpLower", xp)
		await ctx.send(f"<:winxp_information:869760946808180747>Users will now gain at least {xp} XP.")

	# ANCHOR[id=xpu]: UPPER XP RANGE
	@opset.command(name="upperXP", help="Set the upper range for random XP.")
	@commands.has_permissions(manage_roles=True)
	async def change_xp_upper_bound(self, ctx, xp: int):
		updop(ctx.guild.id, "numbers", "xpUpper", xp)
		await ctx.send(f"<:winxp_information:869760946808180747>Users will now gain at most {xp} XP.")
	# END SECTION

	# SECTION: CENSOR
	# ANCHOR: CENSOR INFO
	@read_options.group(name="censor", help="Edit the censor.", aliases=["filter"])
	async def censor(self, ctx):	await ctx.send("<:winxp_information:869760946808180747>Available options: `(show/list/get), add, (delete/remove), (wipe/clear)`") if ctx.invoked_subcommand is None else None

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
		all_bads	= getops(ctx.guild.id, "lists", "censorList")
		word	= word.lower()

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
		all_bads	= getops(ctx.guild.id, "lists", "censorList")
		word	= word.lower()

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
	@change_required_role.error
	@change_drama_channel.error
	@change_general_channel.error
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
		errorstr = str(error)[29:]
		if errorstr.endswith("permission(s) to run this command."):	await ctx.send("<:winxp_critical_error:869760946816553020>You do not have permission to use that command.")
		elif errorstr.endswith('" not found.'):
			if errorstr.startswith('Channel "'):	await ctx.send(f"<:winxp_warning:869760947114348604>{ctx.author.mention}, that isn't a valid channel.")
			if errorstr.startswith('Role "'):	await ctx.send(f"<:winxp_warning:869760947114348604>{ctx.author.mention}, that isn't a valid role.")

		else:	await ctx.send(unhandling(tux_in_guild(ctx, self.client)))


async def setup(client):	await client.add_cog(Options(client))
