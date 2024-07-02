#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from asyncio	import sleep
from datetime	import timedelta
from discord	import Member,	Embed
from discord.ext	import commands
from discord.utils	import get
from tinydb	import TinyDB,	Query
from pengaelicutils	import getops,	updop,	unhandling,	tux_in_guild,	Developers,	get_channel,	get_role

devs = Developers()


class Moderation(commands.Cog):
	def __init__(self, client):	self.client = client
	db	= TinyDB("config.json")
	nukeconfirm	= False
	name	= "moderation"
	name_typable	= name
	description	= "Staff tools!"
	description_long	= description + " Obviously, you need adequate permissions to use these commands."
	teal = 0x007f7f

	async def editsuggestion(self, ctx, suggestion_id, reason, type) -> list:
		if not suggestion_id.startswith("#"):	suggestion_id = "#" + suggestion_id
		suggestion	= getops(ctx.guild.id, "suggestions", suggestion_id)
		message	= await get(ctx.guild.text_channels, id=suggestion[0]).fetch_message(suggestion[1])
		embed	= message.embeds[0]
		embed.color	= {":white_check_mark: Approved": 0x00ff00, ":x: Denied": 0xff0000, ":thinking: Considered": 0xffff00, ":ballot_box_with_check: Implemented": 0x0000ff}[type]
		await message.clear_reactions()
		await message.edit(embed=embed.add_field(name=f"{type} by {ctx.author.name}", value=reason if reason else "_ _", inline=False))
		await ctx.message.add_reaction("✅")

	@commands.command(name="clear", help="Clear some messages away.", aliases=["delmsgs", "purge"], usage="[number of messages to delete (5)]")
	@commands.has_permissions(manage_messages=True)
	async def clear(self, ctx, msgcount: int = 5):
		await ctx.channel.purge(limit=msgcount + 1)
		report = await ctx.send(f"<:winxp_information:869760946808180747>{msgcount} messages deleted.")
		await sleep(3)
		try:	await report.delete()
		except:	pass

	@commands.command(name="nuke",help="Purge a channel of EVERYTHING.", aliases=["wipe", "wipechannel"])
	@commands.has_permissions(manage_channels=True)
	async def nuke(self, ctx):
		if not self.nukeconfirm:
			await ctx.send("<:winxp_question:869760946904645643>Are you **really** sure you want to wipe this channel? Type the command again to confirm. This will expire in 10 seconds.")
			self.nukeconfirm = True
			await sleep(10)
			if self.nukeconfirm:	self.nukeconfirm = False
		elif self.nukeconfirm:
			newchannel = await ctx.channel.clone(reason=f"Nuking #{ctx.channel.name}")
			await newchannel.edit(position=ctx.channel.position, reason=f"Nuking #{ctx.channel.name}")
			await ctx.channel.delete(reason=f"Nuked #{ctx.channel.name}")
			self.nukeconfirm = False

	@commands.command(name="warn", help="Warn a member.", usage="<member> [reason]")
	@commands.has_permissions(kick_members=True)
	async def warn(self, ctx, member: Member, *, reason=None):
		try:	warns = getops(ctx.guild.id, "warnings", str(member.id))
		except KeyError:	warns = {}
		number = str(len(warns)+1)
		await member.send(f"You have been warned in {ctx.guild.name} for reason `{reason}`")
		updop(ctx.guild.id, "warnings", str(member.id), warns | {number: reason})
		await ctx.message.add_reaction("✅")

	@commands.command(name="unwarn", help="Remove a warning.", usage="<member> <warning number>")
	@commands.has_permissions(kick_members=True)
	async def unwarn(self, ctx, member: Member, id):
		warns	= getops(ctx.guild.id, "warnings")
		userwarns	= getops(ctx.guild.id, "warnings", str(member.id))
		userwarns.pop(id)
		userwarns = {number+1: list(userwarns.values())[number] for number in range(len(userwarns))}
		warns[str(member.id)] = userwarns
		if userwarns == {}: warns.pop(str(member.id))
		self.db.update({"warnings": warns}, Query().guildID == ctx.guild.id)
		await ctx.message.add_reaction("✅")

	@commands.command(name="warns", help="See all warnings.", usage="[member]")
	@commands.has_permissions(kick_members=True)
	async def warns(self, ctx, member: Member=None):
		if member:
			try:
				warns	= getops(ctx.guild.id, "warnings", str(member.id))
				embed	= Embed(title=f"Warnings for {member.name}", color=self.teal)
				[embed.add_field(name=warn, value=warns[warn], inline=False) for warn in warns]
				await ctx.send(embed=embed)
			except KeyError:
				await ctx.send(f"There are no logged warnings for {member.name}")
		else:
			warns	= getops(ctx.guild.id, "warnings")
			embed	= Embed(title=f"Warnings in {ctx.guild.name}", color=self.teal)
			[embed.add_field(name=get(ctx.guild.members, id=int(mem)).name, value=len(warns[mem]), inline=False) for mem in warns]
			if warns == {}:	await ctx.send("There are no logged warnings in this server.")
			else:	await ctx.send(embed=embed)

	@commands.command(name="mute", help="Mute a member.", usage="<member> [duration in hours, decimals accepted] [reason]", aliases=["timeout"])
	@commands.has_permissions(moderate_members=True)
	async def mute(self, ctx, member: Member, time: float=1, reason: str=None):
		await member.timeout(timedelta(hours=time), reason=reason)
		await ctx.message.add_reaction("✅")

	@commands.command(name="unmute", help="Unmute a muted member.", usage="<member>", aliases=["untimeout"])
	@commands.has_permissions(moderate_members=True)
	async def unmute(self, ctx, member: Member):
		await member.timeout(None)
		await ctx.message.add_reaction("✅")

	# LINK cogs/options.py#dramarole
	# LINK cogs/options.py#dramachan
	@commands.command(name="drama", help="Assign a member the drama role.", usage="<member> [reason]")
	@commands.has_permissions(kick_members=True)
	async def drama(self, ctx, member: Member, *, reason=None):
		if get_role(ctx.guild.id, "drama"):
			if get_channel(ctx.guild.id, "drama"):
				await member.add_roles(get(ctx.guild.roles, id=get_role(ctx.guild.id, "drama")), reason=reason)
				await ctx.message.add_reaction("✅")

			else:	await ctx.send(f"<:winxp_warning:869760947114348604>There is no set drama channel. To set a drama channel, type `{self.client.command_prefix}options set dramaChannel <drama channel>`.")

		else:	await ctx.send(f"<:winxp_warning:869760947114348604>There is no set drama role. To set a drama role, type `{self.client.command_prefix}options set dramaRole <drama role>`.")

	# LINK cogs/options.py#dramarole
	# LINK cogs/options.py#dramachan
	@commands.command(name="undrama", help="Remove the drama role from a member.", usage="<member>")
	@commands.has_permissions(kick_members=True)
	async def undrama(self, ctx, member: Member):
		if get_role(ctx.guild.id, "drama"):
			if get_channel(ctx.guild.id, "drama"):
				if get(ctx.guild.roles, id=get_role(ctx.guild.id, "drama")) in member.roles:
					await member.remove_roles(get(ctx.guild.roles, id=get_role(ctx.guild.id, "drama")), reason="Release from drama channel")
					await ctx.message.add_reaction("✅")
				else:
					await ctx.send(f"{member} doesn't have the drama role.")

			else:	await ctx.send(f"<:winxp_warning:869760947114348604>There is no set drama channel. To set a drama channel, type `{self.client.command_prefix}options set dramaChannel <drama channel>`.")

		else:	await ctx.send(f"<:winxp_warning:869760947114348604>There is no set drama role. To set a drama role, type `{self.client.command_prefix}options set dramaRole <drama role>`.")

	@commands.command(name="kick", help="Kick a member.", usage="<member> [reason]")
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, member: Member, *, reason=None):
		await member.kick(reason=reason)
		await ctx.send(f"<:winxp_information:869760946808180747>Kicked {member} for reason `{reason}`.")

	@commands.command(name="ban", help="Ban a member.", usage="<member> [reason]")
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, member: Member, *, reason=None):
		await member.ban(reason=reason)
		await ctx.send(f"<:winxp_information:869760946808180747>Banned {member} for reason `{reason}`.")

	@commands.group(name="suggestion", help="Modify someone's suggestion.")
	@commands.has_permissions(manage_messages=True)
	async def suggestion(self, ctx):
		if ctx.invoked_subcommand == None:
			await ctx.send(embed=Embed(title="Suggestion", description="Modify someone's suggestion. Arg for all commands need the suggestion ID, found on the embed's footer.", color=0x007f7f).add_field(name="approve", value="Mark the suggestion as approved.").add_field(name="deny", value="Mark the suggestion as denied.").add_field(name="consider", value="Mark the suggestion as considered.").add_field(name="implement", value="Mark the suggestion as implemented."))

	@suggestion.command(name="approve", help="Approve someone's suggestion.")
	@commands.has_permissions(manage_messages=True)
	async def approve(self, ctx, suggestion_id, *, reason: str = None):	await self.editsuggestion(ctx, suggestion_id, reason, ":white_check_mark: Approved")

	@suggestion.command(name="deny", help="Deny someone's suggestion.")
	@commands.has_permissions(manage_messages=True)
	async def deny(self, ctx, suggestion_id, *, reason: str = None):	await self.editsuggestion(ctx, suggestion_id, reason, ":x: Denied")

	@suggestion.command(name="consider", help="Consider someone's suggestion.")
	@commands.has_permissions(manage_messages=True)
	async def consider(self, ctx, suggestion_id, *, reason: str = None):	await self.editsuggestion(ctx, suggestion_id, reason, ":thinking: Considered")

	@suggestion.command(name="implement", help="Implement someone's suggestion.")
	@commands.has_permissions(manage_messages=True)
	async def implement(self, ctx, suggestion_id, *, reason: str = None):	await self.editsuggestion(ctx, suggestion_id, reason, ":ballot_box_with_check: Implemented")

	@clear.error
	@nuke.error
	@approve.error
	@deny.error
	@consider.error
	@implement.error
	async def managementError(self, ctx, error):
		errorstr = str(error)[29:]
		if errorstr.startswith("You are missing Manage") and errorstr.endswith("permission(s) to run this command."):
			permmsg = f"<:winxp_information:869760946808180747>{ctx.author.mention}, you have insufficient permissions (Manage "
			if "Members" in errorstr:	await ctx.send(permmsg + "Members)")
			if "Messages" in errorstr:	await ctx.send(permmsg + "Messages)")
			if "Channels" in errorstr:	await ctx.send(permmsg + "Channels)")

		elif "KeyError: '#" in errorstr:	await ctx.send("<:winxp_critical_error:869760946816553020>Invalid suggestion ID (look in the footers of the embeds!)")
		elif errorstr == "NotFound: 404 Not Found (error code: 10008): Unknown Message":	await ctx.send("<:winxp_critical_error:869760946816553020>Suggestions could not be searched properly. Did one get deleted?)")
		else:	await ctx.send(unhandling(tux_in_guild(ctx, self.client)))


async def setup(client):	await client.add_cog(Moderation(client))
