#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from sys import	version

# ANCHOR: version checker
major, minor = [int(num) for num in version.split(".")[:2]]
if major < 3 or minor < 9:
	print("Pengaelic Bot requires Python 3.9 or newer to function properly.")
	print("Please run Pengaelic Bot with Python >= 3.9")
	exit()

from json	import dumps
from subprocess	import CalledProcessError,	call,	STDOUT
from sys	import argv,	executable					as	python
from os	import getenv,	system,	execl,	devnull,	get_terminal_size,	listdir	as	ls
from pengaelicutils	import argv_parse,	newops,	list2str,	jsoncheck,	unhandling,	shell,	tux_in_guild,	Developers,	Stopwatch

if argv_parse(argv, ["uninstall", "delete"]):
	system("rm -rvf ~/Pengaelic-Bot")
	print("Uninstalled Pengaelic Bot.")
	exit()

system("clear")
launchtime = Stopwatch()
launchtime.start()
devs = Developers()

# ANCHOR: package test
print("Imported modules")
if shell("uname -o") != "Android":
	devnull = open(devnull, "w")
	requirements = [
		"figlet",
		"fortune-mod",
		"fortunes",
		"fortunes-min",
		"lolcat",
		"neofetch",
		"toilet",
		"toilet-fonts",
	]
	needed = []
	missing_dependencies = False
	for package in requirements:
		if call(["dpkg", "-s", package], stdout=devnull, stderr=STDOUT):
			needed.append(package)
			missing_dependencies = True
	devnull.close()
	if missing_dependencies:
		print(f"Packages {list2str(needed, 0, True)} are not installed.")
		print("Install them with APT.")
		exit()
	print("Passed package test")

else:	print("Ignored package test")

# ANCHOR: module test
requirements = ["py-cord", "discord-components", "num2words", "python-dotenv", "speedtest-cli", "tinydb"]
needed = []
modules = [r.split("==")[0] for r in shell(f"{python} -m pip freeze").split()]
missing_dependencies = False
for module in requirements:
	if module not in modules:
		needed.append(module)
		missing_dependencies = True
if missing_dependencies:
	print(f"Modules {list2str(needed, 0, True)} are not installed.")
	print("Installing them now...")
	shell(f"{python} -m pip install " + list2str(needed, 2))
	print("Done.")
print("Passed module test")

import discord
from discord.errors	import HTTPException
from discord.ext	import commands
from discord_components	import Button,	ButtonStyle,	ActionRow,	DiscordComponents,	InteractionEventType
from dotenv	import load_dotenv as	dotenv
from tinydb	import TinyDB,	Query

# ANCHOR: unstable flagger
unstable = True if argv_parse(argv, ["unstable", "beta", "dev"]) else False

# ANCHOR: client
client = commands.Bot(
	command_prefix	= "p",
	description	= "Pengaelic B",
	help_command	= None,
	case_insensitive	= True,
	strip_after_prefix	= True,
	intents	= discord.Intents.all()
)

client.command_prefix	+= "@"	if unstable else "!"
client.description	+= "eta"	if unstable else "ot"

system(f'toilet -w 1000 -f standard -F border -F gay "{client.description}"')
system('echo "{}" | lolcat'.format(list2str(open("boot.txt", "r").readlines(), 1)))
print("Defined client")
db = TinyDB("config.json")

if "--reset-options" in argv:
	print("Options reset")
	db.truncate()

# ANCHOR: status setter
async def set_status(): await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Tux's unending screaming") if unstable else discord.Activity(type=discord.ActivityType.watching, name=str(len(db.all())) + " servers! | p!help"))

# ANCHOR: help menu template
def help_menu(guild, cog, client):
	if len(cog.get_commands()) == 1:	cog.get_commands = cog.walk_commands
	if jsoncheck(guild):
		info = {"description": cog.description_long.lower()} | {"commands": {list2str([command.name] + command.aliases, 0).replace(", ", "/"): command.usage.split("\n") for command in cog.get_commands()}}
		for command in info["commands"]:
			if len(info["commands"][command]) == 1:	info["commands"][command] = info["commands"][command][0]
		menu = (f'```json\n"{cog.name}": ' + dumps(info, indent=4) + "\n```")
	else:
		menu = discord.Embed(
			title	= cog.name.capitalize(),
			description	= cog.description_long,
			color	= 0x007F7F,
		).set_footer(text=f"Command prefix is {client.command_prefix}\n<arg> = required parameter\n[arg] = optional parameter\n[arg (value)] = default value for optional parameter\n(command/command/command) = all aliases you can run the command with")
		for command in cog.get_commands():
			names = "({})".format(str([command.name] + command.aliases)[1:-1].replace("'", "").replace(", ", "/"))
			if	command.usage:	names += "\n" + command.usage
			else:		names += "\nno args"
			menu.add_field(
				name	= names,
				value	= command.help
			)
	return menu

# SECTION: EVENTS

# ANCHOR: ON CONNECT
@client.event
async def on_connect():	print("Connected to Discord")

# ANCHOR: ON DISCONNECT
@client.event
async def on_disconnect():	print("Disconnected")

# ANCHOR: ON RECONNECT
@client.event
async def on_resumed():	print("Reconnected")

# ANCHOR: ON READY
@client.event
async def on_ready():
	# create a server's configs
	if db.all() == []:	[db.insert({"guildName": guild.name, "guildID": guild.id} | newops()) for guild in client.guilds]
	newconfigs	= [{"guildID": guild.id} for guild in client.guilds]
	configgedservers	= [{"guildID": guild["guildID"]} for guild in db.all()]
	# try to make configs for a server that the bot was added to while it was offline
	for server in range(len(client.guilds)):
		if newconfigs[server] not in configgedservers:
			db.insert({"guildName": client.get_guild(newconfigs[server]["guildID"]).name} | {"guildID": newconfigs[server]["guildID"]} | newops())
			print(f"Configs created for {client.get_guild(newconfigs[server]['guildID']).name}")
	# add any options that may have been created since the option dicts' creation
	for guild in client.guilds:
		gid = guild.id
		if unstable:	ops = db.search(Query().guildName == "Pengaelic Bot Support")[0]	# Pengaelic Beta is only on Pengaelic Bot Support
		else:	ops = db.all()[client.guilds.index(guild)]
		ops.pop("guildName")
		ops.pop("guildID")
		nops = newops()
		for op in ["channels", "lists", "messages", "roles", "toggles"]:
			for opt in list(ops[op].keys()):
				if opt not in nops[op]:	ops[op].pop(opt)
		for op in ["channels", "lists", "messages", "roles", "toggles"]:
			ops[op] = dict(list(nops[op].items()) + list(ops[op].items()))
			db.update(dict(sorted({op: ops[op]}.items())), Query().guildID == gid)

		db.update({"guildName": guild.name}, Query().guildID == gid)	# did the server's name change?
		print(f"Loaded options for {guild.name}")
	await set_status()
	DiscordComponents(client)
	print(f"{client.description} launched in {launchtime.end()}")
	if not unstable:	print(f"Currently on {len(client.guilds)} servers")
	if not shell("hostname").startswith("TrueMintguin"): print("Connected to Discord\nCheck out the support server at https://discord.gg/DHHpA7k")


# ANCHOR: ON GUILD JOIN
@client.event
async def on_guild_join(guild, auto=True):
	if not unstable:
		print(f"Joined {guild.name}")
		for channel in guild.text_channels:
			if any(name in channel.name for name in ["bot", "command", "general"]):
				await channel.send(
					embed=discord.Embed(
						title	= f"Howdy fellas! I'm {client.description}!",
						description	= f"Type `{client.command_prefix}help` for a list of commands.",
						color	= 0x007F7F
					).set_thumbnail(url=client.user.avatar_url))
				break
		if auto:
			# create fresh options row for new server
			newconfigs = {"guildName": guild.name, "guildID": guild.id} | newops()
			if newconfigs not in db.all():	db.insert(newconfigs)
			print(f"Configs created for {guild.name}")


# ANCHOR: ON GUILD LEAVE
@client.event
async def on_guild_remove(guild):	print(f"Was removed from {guild.name}")


if not unstable:
	# ANCHOR: ERROR HANDLING
	@client.event
	async def on_command_error(ctx, error):
		if not hasattr(ctx.command, "on_error"):	# if the command doesn't have its own error handling...

			if str(error).startswith("Command") and str(error).endswith("is not found"):	await ctx.send(f"Invalid command/usage. Type `{client.command_prefix}help` for a list of commands and their usages.")
			else:	await ctx.send(unhandling(error, tux_in_guild(ctx, client)))	# ...send the global error
# END SECTION


# ANCHOR: load token
dotenv(".env")
print("Loaded bot token and developer IDs")

# ANCHOR: EXIT
@client.command(name="exit", aliases=["quit"])
async def quit_the_bot(ctx):
	if Developers.check(None, ctx.author):
		await ctx.send("<:winxp_information:869760946808180747>Shutting down.")
		exit(0)

	else:	await ctx.send("<:winxp_warning:869760947114348604>Hey, only my developers can do this!")


# ANCHOR: SH
@client.command()
async def sh(ctx, *, args):
	if client.is_owner(ctx.author):
		try:
			if args.startswith("cd"):	await ctx.send("<:winxp_critical_error:869760946816553020>Cannot change directory, that's too messy even for you.")
			else:	await ctx.send("```\n" + shell(args) + "\n```")
		except CalledProcessError as error:
			error = str(error)
			if "returned non-zero exit status" in error:
				error = int(float(error.split("returned non-zero exit status ")[1]))
				if	(args.startswith("rm") or args.startswith("cat")) and error == 1:	await ctx.send("<:winxp_critical_error:869760946816553020>That file doesn't exist.")
				elif	args.startswith("python") and error == 1:	await ctx.send("<:winxp_critical_error:869760946816553020>Invalid Python syntax.")
				else:
					if error == 127:	await ctx.send("<:winxp_critical_error:869760946816553020>Invalid command.")
					else:	await ctx.send(f"<:winxp_critical_error:869760946816553020>Returned non-zero exit status{error} (look it up to add error handling)")

			else:	await ctx.send(error)
		except HTTPException as error:
			error = str(error)
			if error.startswith("Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body"):	await ctx.send("<:winxp_critical_error:869760946816553020>Output too large.")

	else:	await ctx.send("<:winxp_warning:869760947114348604>Hey, only my creator can do this! >:(")


# ANCHOR: RESTART
@client.command(name="restart", aliases=["reload", "reboot", "rs", "rl", "rb"])
async def restart(ctx, *, restargs=""):
	if Developers.check(None, ctx.author):
		if unstable:	restargs = "--unstable"
		await ctx.send("<:winxp_information:869760946808180747>Restarting...")
		print("Restarting...")
		await client.change_presence(activity=discord.Game("Restarting..."), status=discord.Status.dnd)
		execl(python, python, *[argv[0]] + restargs.split())

	else:	await ctx.send("<:winxp_warning:869760947114348604>Hey, only my developers can do this!")


if not unstable:
	# ANCHOR: UPDATE LOG
	@client.command(name="updatelog", aliases=["ul", "ulog"])
	async def updatelog(ctx, formatted=True, status: discord.Message = None):
		if Developers.check(None, ctx.author):
			if jsoncheck(ctx.guild.id):
				if status:	await status.edit(content="Looking in the logs...")
				else:	status = await ctx.send("<:winxp_information:869760946808180747>Looking in the logs...")
				update_log = [line.replace("\n", "") for line in open("update.log", "r")][1:]
				if formatted:
					if "A" == update_log[0][0]:
						await status.edit(content=f'```json\n"{list2str(update_log[0][:-1].split()[1:], 2)}": true```')
						return False
					update_summary = update_log[-1]
					update_log = update_log[2:-1]
					update_summary = update_summary.split(", ")
					update_summary = [
						{"files changed":	int(update_summary[0][1:].split()[0])},
						{
							"insertions":	int(update_summary[1][:-3].split()[0]),
							"deletions":	int(update_summary[2][:-3].split()[0]),
						}
					]
					for item in range(len(update_log)):
						while "  " in update_log[item]:	update_log[item] = update_log[item].replace("  ", " ")
					update_log = {update_log[item].split("|")[0].replace(" ", ""): update_log[item].split("|")[1][1:]for item in range(len(update_log))}
					await status.edit(content=f'```json\n"summary": {dumps(update_summary, indent=4)},\n"changes": {dumps(update_log, indent=4)}```')

				else:	await ctx.send(f'Raw log contents```{open("update.log", "r").read()}```')
			else:
				if status:	await status.edit(embed=discord.Embed(title="Looking in the logs...", color=0x007F7F))
				else:	status = await ctx.send(embed=discord.Embed(title="Looking in the logs...", color=0x007F7F))
				update_log = [line.replace("\n", "") for line in open("update.log", "r")][1:]
				await status.edit(embed=discord.Embed(title=update_log[0], color=0x007F7F))
				if formatted:
					if "A" == update_log[0][0]:	return False
					else:
						await status.edit(
							embed = discord.Embed(
								title	= update_log[0],
								description	= list2str(update_log[2:-1], 3),
								color	= 0x007F7F
							).set_footer(text=update_log[-1])
						)
				else:
					await status.delete()
					await ctx.send(
						embed = discord.Embed(
							title	= "Raw log contents",
							description	= open("update.log", "r").read(),
							color	= 0xFF0000
						)
					)
			return True
		else:
			await ctx.send("<:winxp_warning:869760947114348604>Hey, only my developers can do this!")
			return False

	# ANCHOR: UPDATE COMMAND
	@client.command(name="update", aliases=["ud"])
	async def update(ctx, force=False):
		if Developers.check(None, ctx.author):
			if jsoncheck(ctx.guild.id):	status = await ctx.send("<:winxp_information:869760946808180747>Pulling the latest commits from GitHub...")
			else:	status = await ctx.send(embed=discord.Embed(title="Pulling the latest commits from GitHub...", color=0x007F7F))
			await client.change_presence(activity=discord.Game("Updating..."), status=discord.Status.idle)
			system("bash update.sh > update.log")
			if force:	await restart(ctx)
			else:
				if await updatelog(ctx, True, status):	await restart(ctx)

		else:	await ctx.send("<:winxp_warning:869760947114348604>Hey, only my developers can do this!")

	@update.error
	async def update_error(ctx, error):
		await ctx.send(f"<:winxp_critical_error:869760946816553020>An error occurred while updating...```\n{error}\n```Attempting force-update.")
		await update(ctx, True)


# ANCHOR: HELP MENU
@client.group(name="help", help="Show this message", aliases=["commands", "h", "?"])
async def help(ctx, *, cogname: str = None):
	if cogname == None:
		cogs = dict(client.cogs)
		cogs.pop("Options")
		cogs.pop("NonCommands")
		if jsoncheck(ctx.guild.id):
			info = {cogs[cog].name: cogs[cog].description.lower()[:-1] for cog in cogs}
			links = {
				"support server":	"<https://discord.gg/DHHpA7k>",
				"invite me":	"<https://discord.com/api/oauth2/authorize?client_id=721092139953684580&permissions=805661782&scope=bot>",
				"github":	"<https://github.com/SuperTux20/Pengaelic-Bot>"
			}
			if not isinstance(ctx.channel, discord.channel.DMChannel):	info |= {"options": client.get_cog("Options").description.lower()[:-1]}
			if Developers.check(None, ctx.author):	info |= {"control": "update, restart, that sort of thing"}
			menu = dumps(
				{
					"help":	f"type {client.command_prefix}help <category name without spaces or dashes> for more info on each category",
					"categories":	info,
					"links":	links
				},
				indent=4
			)
			await ctx.send(f'```json\n"{client.description}": {menu}```')
		else:
			menu = discord.Embed(
				title	= client.description,
				description	= f"Type `{client.command_prefix}help `**`<lowercase category name without spaces or dashes>`** for more info on each category.",
				color	= 0x007F7F
			)
			for cog in sorted(cogs):	menu.add_field(name=cogs[cog].name.capitalize(), value=cogs[cog].description)
			if not isinstance(ctx.channel, discord.channel.DMChannel):	menu.add_field(name="Options", value=client.get_cog("Options").description)
			if Developers.check(None, ctx.author):	menu.add_field(name="Control", value="Update, restart, that sort of thing.")
			await ctx.send(
				embed=menu,
				components=[
					Button(
						style=ButtonStyle.URL,
						label="Support Server",
						url="https://discord.gg/DHHpA7k"
					),
					Button(
						style=ButtonStyle.URL,
						label="Invite Me",
						url="https://discord.com/api/oauth2/authorize?client_id=721092139953684580&permissions=805661782&scope=bot"
					),
					Button(
						style=ButtonStyle.URL,
						label="GitHub",
						url="https://github.com/SuperTux20/Pengaelic-Bot"
					),
				]
			)
	elif cogname == "options":
		if jsoncheck(ctx.guild.id):	await ctx.send(f'```json\n"options": "{client.get_cog("Options").description_long.lower()}",\n"commands": ' + dumps({list2str([command.name] + command.aliases, 1).replace(", ", "/"): command.usage for command in client.get_cog("Options").get_commands()} | {list2str([command.name] + command.aliases, 1).replace(", ", "/"): command.usage for command in list(client.get_cog("Options").get_commands()[0].walk_commands()) if command.parents[0] == client.get_cog("Options").get_commands()[0]}, indent=4) + "```")
		else:
			menu = discord.Embed(title="Options", description=client.get_cog("Options").description_long, color=0x007F7F).set_footer(text=f"Command prefix is {client.command_prefix}\n<arg> = required parameter\n[arg] = optional parameter\n[arg (value)] = default value for optional parameter\n(command/command/command) = all aliases you can run the command with")
			for command in client.get_cog("Options").get_commands():	menu.add_field(name="options", value="Show the current values of all options.")
			for subcommand in list(command.walk_commands()):
				if subcommand.parents[0] == command:	menu.add_field(name=subcommand.name, value=subcommand.help)
			await ctx.send(embed=menu)
	elif cogname == "control" and Developers.check(None, ctx.author):
		if jsoncheck(ctx.guild.id):	await ctx.send(f'```json\n"control": "update, restart, that sort of thing",\n"commands": ' + dumps(["exit", "restart", "update", "forceupdate", "updatelog", "sh"], indent=4) + "```")
		else:	await ctx.send(embed=discord.Embed(title="Control", description="Commands for developers to control the bot itself.", color=0x007F7F).add_field(name="exit", value="Shut off the bot.").add_field(name="restart", value="Reload the bot.").add_field(name="update", value="Check if there's new commits on GitHub, and if there are, pull them and restart.").add_field(name="forceupdate", value="Same as update, but it always restarts regardless of what the update log says, because I'm sure I fucked up the regular update command somehow.").add_field(name="updatelog", value="Show the log of the last update.").add_field(name="sh", value="Direct Bash access. Don't fuck this up."))
	else:
		if jsoncheck(ctx.guild.id):	await ctx.send(help_menu(ctx.guild.id, client.get_cog(cogname.capitalize()), client))
		else:	await ctx.send(embed=help_menu(ctx.guild.id, client.get_cog(cogname.capitalize()), client))


# ANCHOR: DOG OF WISDOM
@client.command(name="dogofwisdom")
async def dog(ctx, *, channel: discord.TextChannel = None):
	if not channel:
		channel = await ctx.guild.create_text_channel("dog-of-wisdom")
		await channel.edit(category=ctx.guild.categories[0])
	hook = await channel.create_webhook(name="The Dog of Wisdom")
	await ctx.send(f"<:winxp_information:869760946808180747>Webhook created in {channel}.")
	await client.get_user(devs.get("tux")).send(f"@{ctx.author.name}#{ctx.author.discriminator} is requesting the Dog of Wisdom.\n" + str({ctx.guild.name: hook.url.replace("https://discord.com/api/webhooks/", "")}))
	await ctx.send("<:winxp_information:869760946808180747>My developer has received the webhook URL and will be adding it to the Dog's code shortly.")


# ANCHOR: NOT A COG ERROR
@help.error
async def not_a_cog(ctx, error):
	error = str(error)
	if error.endswith("'NoneType' object has no attribute 'get_commands'"):	await ctx.send("<:winxp_warning:869760947114348604>There isn't a help menu for that.")
	else:	await ctx.send(unhandling(error, tux_in_guild(ctx, client)))


# ANCHOR: TOGGLE MENU
@help.command(name="toggle")
async def h_toggle(ctx):
	group = client.get_command("toggle")
	help_menu = discord.Embed(title=group.name.capitalize(), description=group.help, color=0x007F7F).set_footer(text=f"Command prefix is {client.command_prefix}toggle\n<arg> = required parameter\n[arg] = optional parameter\n[arg (value)] = default value for optional parameter\n(command/command/command) = all aliases you can run the command with")
	for command in list(set(group.walk_commands())):
		if command.usage:	help_menu.add_field(name="({})\n{}".format(str([command.name] + command.aliases)[1:-1].replace("'", "").replace(", ", "/"), command.usage), value=command.help)
		else:	help_menu.add_field(name="({})".format(str([command.name] + command.aliases)[1:-1].replace("'", "").replace(", ", "/")), value=command.help)
	await ctx.send(embed=help_menu)


# ANCHOR: CENSOR MENU
@help.command(name="censor", aliases=["filter"])
async def h_censor(ctx):
	group = client.get_command("censor")
	help_menu = discord.Embed(title=group.name.capitalize(), description=group.help, color=0x007F7F).set_footer(text=f"Command prefix is {client.command_prefix}censor or {client.command_prefix}filter\n<arg> = required parameter\n[arg] = optional parameter\n[arg (value)] = default value for optional parameter\n(command/command/command) = all aliases you can run the command with")
	for command in list(set(group.walk_commands())):
		if command.usage:	help_menu.add_field(name="({})\n{}".format(str([command.name] + command.aliases)[1:-1].replace("'", "").replace(", ", "/"), command.usage), value=command.help)
		else:	help_menu.add_field(name="({})".format(str([command.name] + command.aliases)[1:-1].replace("'", "").replace(", ", "/")), value=command.help)
	await ctx.send(embed=help_menu)


# ANCHOR: cog loader
for cog in ls("cogs"):
	if cog.endswith(".py"):
		client.load_extension(f"cogs.{cog[:-3]}")
		print(f"Loaded cog {cog[:-3]}")

# ANCHOR: login
while True:
	try:
		if unstable:	client.run(getenv("UNSTABLE_TOKEN"))
		else:	client.run(getenv("DISCORD_TOKEN"))
	except (KeyboardInterrupt, RuntimeError):
		print("\b".join(["\b" for _ in range(get_terminal_size().columns)]) + "Connection closed" + "".join([" " for _ in range(get_terminal_size().columns-17)]))
		while True:	exit(0)
	except Exception:
		print("Unable to connect to Discord")
		while True:	exit(1)
