#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from asyncio	import sleep
from discord	import Member,	Embed
from discord.ext	import commands
from discord.utils	import get
from tinydb	import TinyDB
from pengaelicutils	import getops,	unhandling,	tux_in_guild,	Developers

devs = Developers()


class Moderation(commands.Cog):
	def __init__(self, client):	self.client = client
	db	= TinyDB("config.json")
	nukeconfirm	= False
	name	= "moderation"
	name_typable	= name
	description	= "Staff tools!"
	description_long	= description + " Obviously, you need adequate permissions to use these commands."

	async def editsuggestion(self, ctx, suggestionID, reason, type) -> list:
		if not suggestionID.startswith("#"):	suggestionID = "#" + suggestionID
		suggestion	= getops(ctx.guild.id, "suggestions", suggestionID)
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
			await ctx.send(f"<:winxp_question:869760946904645643>Are you **really** sure you want to wipe this channel? Type the command again to confirm. This will expire in 10 seconds.")
			self.nukeconfirm = True
			await sleep(10)
			if self.nukeconfirm:	self.nukeconfirm = False
		elif self.nukeconfirm:
			newchannel = await ctx.channel.clone(reason=f"Nuking #{ctx.channel.name}")
			await newchannel.edit(position=ctx.channel.position, reason=f"Nuking #{ctx.channel.name}")
			await ctx.channel.delete(reason=f"Nuked #{ctx.channel.name}")
			self.nukeconfirm = False

	# LINK cogs/options.py#dramarole
	# LINK cogs/options.py#dramachan
	@commands.command(name="drama", help="Assign a member the drama role.", usage="<member>")
	@commands.has_permissions(kick_members=True)
	async def drama(self, ctx, member: Member, *, reason=None):
		try:
			if getops(ctx.guild.id, "channels", "dramaChannel"):
				await member.add_roles(get(ctx.guild.roles, id=getops(ctx.guild.id, "roles", "dramaRole")),reason=reason)
				await ctx.send(f"Sent {member} to the drama channel for reason `{reason}`.")

			else:	await ctx.send(f"<:winxp_warning:869760947114348604>There is no set drama channel. To set a drama channel, type `{self.client.command_prefix}options set dramaChannel <drama channel>`.")

		except:	await ctx.send(f"<:winxp_warning:869760947114348604>There is no set drama role. To set a drama role, type `{self.client.command_prefix}options set dramaRole <drama role>`.")

	# LINK cogs/options.py#muterole
	@commands.command(name="mute", help="Mute a member.", usage="<member>")
	@commands.has_permissions(kick_members=True)
	async def mute(self, ctx, member: Member, *, reason=None):
		try:
			await member.add_roles(get(ctx.guild.roles, id=getops(ctx.guild.id, "roles", "muteRole")),reason=reason)
			await ctx.send(f"Muted {member} for reason `{reason}`.")

		except:	await ctx.send(f"<:winxp_warning:869760947114348604>There is no set mute role. To set a mute role, type `{self.client.command_prefix}options set muteRole <mute role>`.")

	@commands.command(name="kick", help="Kick a member.", usage="<member>")
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, member: Member, *, reason=None):
		await member.kick(reason=reason)
		await ctx.send(f"<:winxp_information:869760946808180747>Kicked {member} for reason `{reason}`.")

	@commands.command(name="ban", help="Ban a member.", usage="<member>")
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
	async def approve(self, ctx, suggestionID, *, reason: str = None):	await self.editsuggestion(ctx, suggestionID, reason, ":white_check_mark: Approved")

	@suggestion.command(name="deny", help="Deny someone's suggestion.")
	@commands.has_permissions(manage_messages=True)
	async def deny(self, ctx, suggestionID, *, reason: str = None):	await self.editsuggestion(ctx, suggestionID, reason, ":x: Denied")

	@suggestion.command(name="consider", help="Consider someone's suggestion.")
	@commands.has_permissions(manage_messages=True)
	async def consider(self, ctx, suggestionID, *, reason: str = None):	await self.editsuggestion(ctx, suggestionID, reason, ":thinking: Considered")

	@suggestion.command(name="implement", help="Implement someone's suggestion.")
	@commands.has_permissions(manage_messages=True)
	async def implement(self, ctx, suggestionID, *, reason: str = None):	await self.editsuggestion(ctx, suggestionID, reason, ":ballot_box_with_check: Implemented")

	@clear.error
	@nuke.error
	@approve.error
	@deny.error
	@consider.error
	@implement.error
	async def managementError(self, ctx, error):
		error = str(error)
		if error.startswith("You are missing Manage") and error.endswith("permission(s) to run this command."):
			permmsg = f"<:winxp_information:869760946808180747>{ctx.author.mention}, you have insufficient permissions (Manage "
			if "Members" in error:	await ctx.send(permmsg + "Members)")
			if "Messages" in error:	await ctx.send(permmsg + "Messages)")
			if "Channels" in error:	await ctx.send(permmsg + "Channels)")

		elif "KeyError: '#" in error:	await ctx.send("<:winxp_critical_error:869760946816553020>Invalid suggestion ID (look in the footers of the embeds!)")
		elif error == "NotFound: 404 Not Found (error code: 10008): Unknown Message":	await ctx.send("<:winxp_critical_error:869760946816553020>Suggestions could not be searched properly. Did one get deleted?)")
		else:	await ctx.send(unhandling(error, tux_in_guild(ctx, self.client)))


def setup(client):	client.add_cog(Moderation(client))
