#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

import	speedtest
from asyncio.events	import get_event_loop
from discord.ext	import commands
from discord.utils	import get
from concurrent.futures	import ThreadPoolExecutor
from json	import dumps
from os	import environ
from re	import search
from tinydb	import TinyDB
from time	import strftime,	localtime
from discord	import Embed,	Member,	TextChannel,	Color
from pengaelicutils	import getops,	updop,	list2str,	unhandling,	tux_in_guild,	jsoncheck,	shell,	Stopwatch,	Developers,	get_role

devs = Developers()


class Tools(commands.Cog):
	def __init__(self, client):	self.client = client
	teal	= 0x007F7F
	db	= TinyDB("config.json")
	testing	= False
	name	= "tools"
	name_typable	= name
	description	= "Various tools and info."
	description_long	= description

	def UpdateTime(self, speed=False):
		global CurrentTime
		global SpeedPerformTime
		CurrentTime = strftime("%a/%b %d/%Y %l:%M:%S %p %Z", localtime())
		if speed:	SpeedPerformTime = CurrentTime	# record this as the time the speedtest was done

	def TestSpeed(self) -> dict:
		global results
		self.UpdateTime(True)
		s = speedtest.Speedtest()
		s.get_best_server()
		s.download(threads=None)
		s.upload(threads=None)
		s.results.share()
		results = s.results.dict()
		return results

	@commands.command(name="say",help="I'll repeat whatever you tell me.",pass_context=True,aliases=["repeat", "parrot"],usage="<message>")
	async def say_back(self, ctx, *, arg):	await ctx.send(arg)

	@commands.command(name="credits", help="See who helped me come to exist!")
	async def credits(self, ctx):
		bot_credits = {
			"Lead Developer and Creator":	"Tux Penguin",
			"Minor Contributor":	"Cherry Rain",
			"Former Contributor":	"Hyla Asencion",
		}
		if jsoncheck(ctx.guild.id):
			bot_credits = {cred.lower(): bot_credits[cred] for cred in bot_credits}
			await ctx.send(f'```json\n"credits": {str(dumps(bot_credits, indent=4))}\n```')
		else:
			embed = Embed(color=self.teal, title="Credits", description="All the people on Discord who helped me become what I am today.")
			for cred in bot_credits:	embed.add_field(name=cred, value=bot_credits[cred])
			await ctx.send(embed=embed)

	@commands.command(name="os", help="Read what OS I'm running on!", aliases=["getos"])
	async def showOS(self, ctx):
		def uname(item) -> str:	return shell(f"uname -{item}")
		async with ctx.typing():
			system	= (shell('neofetch | grep OS | sed "s/\x1B\[[0-9;]\{1,\}[A-Za-z]//g"').split(":")[1][1:-2].split("x86")[0][:-1])
			kernel	= uname("r")
			os	= uname("o")
		if	os == "Android":	emoji	= "<:os_android:901137017860136961>"
		elif	os == "GNU/Linux":
			if	kernel.endswith("microsoft-standard-WSL2"):	emoji	= "<:os_windows:901137018405400576>"
			else:	emoji	= "<:os_linux:901137018153754684>"
		await ctx.send(f"<:winxp_information:869760946808180747>I'm running on {system}, kernel version {kernel} {emoji}")

	@commands.command(name="test", help="Am I online? I'm not sure.")
	async def test(self, ctx):	await ctx.send("Yep, I'm alive :sunglasses:")

	# ANCHOR: INFO COMMANDS

	@commands.group(name="info", help="See a bunch of data!")
	async def info(self, ctx):
		if ctx.invoked_subcommand == None:	await ctx.send(embed=Embed(title="Information", description="See a bunch of data!", color=self.teal).add_field(name="channel", value="See details about the specified channel.").add_field(name="emoji", value="Fetch the specified (server-specific) emoji.").add_field(name="server", value="See information about the server at a glance.").add_field(name="user", value="Get info for the specified user."))

	@info.command(name="emoji", help="Fetch the specified (server-specific) emoji.", aliases=["emote"], usage="[:emoji:]")
	async def emoji(self, ctx, emoji=None):
		emojis	= [f"<:{em.name}:{em.id}>"	for em in ctx.guild.emojis	if not em.animated]
		animojis	= [f"<a:{em.name}:{em.id}>"	for em in ctx.guild.emojis	if em.animated]
		emojiurls	= (
			[f"https://cdn.discordapp.com/emojis/{em.id}.png"	for em in ctx.guild.emojis	if not em.animated] +
			[f"https://cdn.discordapp.com/emojis/{em.id}.gif"	for em in ctx.guild.emojis	if em.animated]
		)

		if emoji == None:
			statics	= Embed(title=f"Static emojis in {ctx.guild.name}",	description=str(emojis)[1:-1].replace("'", "").replace(", ", ""),	color=self.teal)
			anims	= Embed(title=f"Animated emojis in {ctx.guild.name}",	description=str(animojis)[1:-1].replace("'", "").replace(", ", ""),	color=self.teal)

			if len(emojis) == 0 and len(animojis) == 0:	await ctx.send("<:winxp_critical_error:869760946816553020>This server has no emojis!")
			else:
				embeds = []
				if len(emojis) > 0:	embeds.append(statics)
				if len(animojis) > 0:	embeds.append(anims)
				await ctx.send(embeds=embeds)
		else:
			emojis += animojis
			if emoji in emojis:
				emname = emoji.split(":")[:-1]
				emname = emname[1] + (".gif" if emname[0] == "<a" else ".png")
				await ctx.send(embed=Embed(title=emname, color=self.teal).set_image(url=emojiurls[emojis.index(emoji)]))

			else:	await ctx.send("<:winxp_warning:869760947114348604>Invalid emoji specified!")

	@info.command(name="server", help="See information about the server at a glance.")
	async def server_info(self, ctx):
		guild	= ctx.guild
		owner	= guild.owner

		if owner.nick == None:	owner.nick = owner.name
		creation = guild.created_at
		infofields = {
			"Server Name":	guild.name,
			"Server Owner":	f"{owner.display_name} ({owner.mention})",
			"Server ID":	guild.id
		}
		if guild.description:
			infofields |= {"Server Description": guild.description}
		infofields |= {
			"Two-Factor Authentication":	bool(guild.mfa_level),
			"Verification Level":	f"{guild.verification_level[0].title()} (Level {guild.verification_level[1]+1})",
			"Notification Level":	f"{guild.default_notifications[0].replace('_',' ').title()} (Level {guild.default_notifications[1]+1})",
			"Content Filter":	f"{guild.explicit_content_filter[0].replace('_',' ').title()} (Level {guild.explicit_content_filter[1]+1})",
			"Members":	guild.member_count,
			"Text Channels":	len(guild.text_channels),
			"Voice Channels":	len(guild.voice_channels),
			"Channel Categories":	len(guild.categories),
			"Emojis":	len(guild.emojis),
			"Roles":	len(guild.roles) - 1,
		}
		if guild.description: infofields |= {"Server Description": guild.description}
		bans = [entry async for entry in guild.bans()]
		if len(bans) > 0:	infofields |= {"Bans": len(bans)}
		if guild.premium_subscription_count > 0:	infofields |= {"Boosts": guild.premium_subscription_count, "Boosters": len(guild.premium_subscribers)}
		if getops(guild.id, "toggles", "jsonMenus"):
			infofields["Server Owner"] = f"{owner.display_name} (@{owner.name})"
			infofields |= {
				"Server Icon":	str(guild.icon.url).split("?")[0],
				"Creation Date":	f"{creation.month}/{creation.day}/{creation.year} {creation.hour}:{creation.minute}:{creation.second} GMT"
			}
			await ctx.send(f'```json\n"server information": {dumps(dict(zip([k.lower() for k in infofields.keys()], [(v.lower() if isinstance(v, str) else v) for v in infofields.values()])),indent=4)}```')
		else:
			embedinfo = Embed(title=guild.name, color=self.teal).set_thumbnail(url=guild.icon.url).set_author(name="Server Info", icon_url=owner.avatar.url).set_footer(text=f"Created {creation.month}/{creation.day}/{creation.year} {creation.hour}:{creation.minute}:{creation.second} GMT")
			for info in infofields: embedinfo.add_field(name=info, value=str(infofields[info]).replace("True", "Enabled").replace("False", "Disabled"), inline=True if isinstance(infofields[info], int) else False)
			await ctx.send(embed=embedinfo)

	@info.command(name="user",help="Get info for the specified user.",aliases=["member"],usage="[@member]")
	async def user_info(self, ctx, *, user: Member = None):
		if user == None:	user = ctx.author
		roles = user.roles[1:]
		roles.reverse()
		creation = user.created_at
		infofields = {
			"Name": f"{user.display_name} (@{user.name})",
			"ID": user.id,
			"Animated Avatar": user.avatar.is_animated(),
			"Bot": user.bot,
		}
		if getops(ctx.guild.id, "toggles", "jsonMenus"):
			infofields |= {
				"Avatar": str(user.avatar.url).split("?")[0],
				"Roles": [role.name.lower() for role in roles] if len(roles) > 0 else None,
				"Creation Date": f"{creation.month}/{creation.day}/{creation.year} {creation.hour}:{creation.minute}:{creation.second} GMT"
			}
			await ctx.send(f'```json\n"user information": {dumps(dict(zip([k.lower() for k in infofields.keys()], [(v.lower() if isinstance(v, str) else v) for v in infofields.values()])),indent=4)}```')
		else:
			embedinfo = Embed(title=user.display_name, color=self.teal).set_author(name="User Info").set_thumbnail(url=user.avatar.url).set_footer(text=f"Created {creation.month}/{creation.day}/{creation.year} {creation.hour}:{creation.minute}:{creation.second} GMT")
			if user.nick == user.display_name: embedinfo.add_field(name="Real Name", value=user.name)
			infofields.pop("Name")
			infofields = {"Ping": user.mention} | infofields
			for info in infofields: embedinfo.add_field(name=info, value=str(infofields[info]).replace("True", "Yes").replace("False", "No"), inline=True)
			embedinfo.add_field(name="Roles", value=list2str([f"<@&{role.id}>" for role in roles], 2) if len(roles) > 0 else None, inline=False)
			await ctx.send(embed=embedinfo)

	@info.command(name="channel",help="Get info for the specified channel.",usage="[#channel]")
	async def channel_info(self, ctx, *, channel: TextChannel = None):
		if channel == None:	channel = ctx.channel
		creation = channel.created_at
		infofields = {
			"Name": channel.name,
			"ID": channel.id
		}
		if channel.topic:	infofields |= {"Description": channel.topic}
		if channel.slowmode_delay:	infofields |= {"Slowmode": channel.slowmode_delay}
		infofields |= {"Category": channel.category.name, "NSFW": channel.is_nsfw()}
		if getops(ctx.guild.id, "toggles", "jsonMenus"):
			infofields |= {"creation date": f"{creation.month}/{creation.day}/{creation.year} {creation.hour}:{creation.minute}:{creation.second} GMT"}
			await ctx.send(f'```json\n"channel information": {dumps(dict(zip([k.lower() for k in infofields.keys()], [(v.lower() if isinstance(v, str) else v) for v in infofields.values()])),indent=4)}```')
		else:
			infofields.pop("Name")
			infofields = {"Ping": channel.mention} | infofields
			embedinfo = Embed(title=channel.name.replace("-", " ").title(), color=self.teal).set_footer(text=f"Created {creation.month}/{creation.day}/{creation.year} {creation.hour}:{creation.minute}:{creation.second} GMT")
			for info in infofields: embedinfo.add_field(name=info, value=str(infofields[info]).replace("True", "Yes").replace("False", "No"), inline=False)
			await ctx.send(embed=embedinfo)

	# ANCHOR: SPEEDTEST

	@commands.command(name="speedtest",aliases=["st", "ping", "ng"],help="See how good my internet is.")
	async def speedtest(self, ctx):
		if self.testing == False:
			self.testing = True
			stresults = await ctx.send(embed=Embed(title="Running Speedtest...", color=0x007F7F))
			async with ctx.typing():	await get_event_loop().run_in_executor(ThreadPoolExecutor(), self.TestSpeed)
			finished = await ctx.send("Complete!")
			await stresults.edit(embed=Embed(title="Speedtest Results", description="*Conducted using [Ookla's Speedtest CLI](https://speedtest.net)*", color=0x007F7F).add_field(name="Server", value=f'{results["server"]["sponsor"]} {results["server"]["name"]}', inline=False).add_field(name="Ping", value=f'{results["ping"]} ms', inline=False).add_field(name="Download Speed", value=f'{round(float((results["download"])/1000000), 2)} Mbps', inline=False).add_field(name="Upload Speed", value=f'{round(float((results["upload"])/1000000), 2)} Mbps', inline=False).set_footer(text=SpeedPerformTime))
			await finished.delete()
			self.testing = False

		else:	await ctx.send("<:winxp_information:869760946808180747>A test is already in progress. Please wait...")

	# ANCHOR: CUSTOM ROLES

	@commands.command(name="role",help="Create a custom color role for yourself!",usage="<hex code>\n<role name>")
	async def role(self, ctx, color, *, role_name):
		member = ctx.author
		role_lock = get(ctx.guild.roles, id=get_role(ctx.guild.id, "customRoleLock"))
		if role_lock in member.roles or role_lock == None:
			try:	result	= getops(ctx.guild.id, "customRoles", str(member.id))
			except KeyError:	result	= None
			hex_code_match = search(r"(?:[0-9a-fA-F]{3}){1,2}$", color)
			if result and ctx.guild.get_role(int(result)):
				if hex_code_match:
					role	= ctx.guild.get_role(int(result))
					await role.edit(name=role_name, color=Color(int(color, 16)))
					await member.add_roles(role)
					await ctx.message.add_reaction("✅")

				else:	await ctx.send(f"<:winxp_critical_error:869760946816553020>Invalid hex code `{color}`.")
			else:
				if hex_code_match:
					role_color	= Color(int(color, 16))
					role	= await ctx.guild.create_role(name=role_name, color=role_color)
					await member.add_roles(role)
					updop(ctx.guild.id, "customRoles", str(member.id), role.id)
					await ctx.message.add_reaction("✅")

				else:	await ctx.send(f"<:winxp_critical_error:869760946816553020>Invalid hex code `{color}`.")

		else:	await ctx.send(f"{member.mention}, this is only for users with the {role_lock} role.")

	@commands.command(name="delrole", help="Delete your custom role.")
	async def delrole(self, ctx):
		member	= ctx.author
		role_lock	= get(ctx.guild.roles, id=get_role(ctx.guild.id, "customRoleLock"))
		if role_lock in member.roles or role_lock == None:
			result = getops(ctx.guild.id, "customRoles", str(member.id))
			if result:
				await member.remove_roles(ctx.guild.get_role(result))
				await ctx.message.add_reaction("✅")

			else:	await ctx.channel.send(f"{member.mention}, you don't have a custom role to remove!")

		else:	await ctx.channel.send(f"{member.mention}, this is only for users with the {role_lock} role.")

	# FIXME: There's only one stopwatch across the entire bot
	# @commands.group(name="stopwatch", help="Track how long something goes.", usage="<start, stop>")
	# async def stopwatch(self, ctx):
	# 	if ctx.invoked_subcommand == None:
	# 		await ctx.send(
	# 			embed=Embed(
	# 				title	= "Stopwatch",
	# 				description	= "Track how long something goes.",
	# 				color	= self.teal,
	# 			)
	# 			.add_field(name="(start/begin)", value="Start the stopwatch.")
	# 			.add_field(name="(stop/end)", value="Stop the stopwatch.")
	# 		)

	# @stopwatch.command(name="start", help="Start the stopwatch.", aliases=["begin"])
	# async def stopwatch_start(self, ctx):
	# 	Stopwatch.start(self)
	# 	await ctx.send("Started the stopwatch.")

	# @stopwatch.command(name="stop", help="Stop the stopwatch.", aliases=["end"])
	# async def stopwatch_end(self, ctx):
	# 	await ctx.send(Stopwatch.end(self))

	@commands.command(name="bugreport", help="Send a bug report to my developer.")
	async def bugreport(self, ctx, *, bug):
		await self.client.get_user(devs.get("tux")).send(f"@{ctx.author} has sent a bug report from {ctx.guild}.\n```\n{bug}\n```")
		await ctx.message.add_reaction("✅")

	@commands.command(name="dummy", help="See a dummy error message.")
	async def dummy(self, ctx):	await ctx.send(unhandling(tux_in_guild(ctx, self.client)))

	@commands.command(name="invite", help="Invite me to your server!")
	async def invite(self, ctx):	await ctx.send("https://discord.com/api/oauth2/authorize?client_id=721092139953684580&permissions=805661782&scope=bot")

	@commands.command(name="support", help="Come to the support server!")
	async def support(self, ctx):	await ctx.send("https://discord.gg/DHHpA7k")

	@commands.command(name="github", help="See my source code!")
	async def github(self, ctx):	await ctx.send("https://github.com/SuperTux20/Pengaelic-Bot")

	@user_info.error
	@channel_info.error
	async def getError(self, ctx, error):
		error = str(error)
		if error.endswith("not found"):
			if	error.startswith("Member"):	await ctx.send("<:winxp_warning:869760947114348604>Invalid user specified!")
			elif	error.startswith("Channel"):	await ctx.send("<:winxp_warning:869760947114348604>Invalid channel specified!")

		else:	await ctx.send(unhandling(tux_in_guild(ctx, self.client)))

	@server_info.error
	# @stopwatch_start.error
	# @stopwatch_end.error
	# @stopwatch.error
	@bugreport.error
	@speedtest.error
	@role.error
	@delrole.error
	@emoji.error
	@info.error
	async def generalError(self, ctx, error):
		if str(error).endswith("color is a required argument that is missing."):	await ctx.send("<:winxp_warning:869760947114348604>You didn't specify a role color!")
		if str(error).endswith("role_name is a required argument that is missing."):	await ctx.send("<:winxp_warning:869760947114348604>You didn't specify a role name!")
		else:	await ctx.send(unhandling(tux_in_guild(ctx, self.client)))


async def setup(client):	await client.add_cog(Tools(client))
