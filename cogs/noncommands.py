#!/usr/bin/python
# -*- coding: utf-8 -*-

import discord
from discord.utils import get
from discord.ext import commands
from pengaelicutils import getops, Developers
from os import system as cmd
from random import choice


class NonCommands(commands.Cog):
	def __init__(self, client):	self.client = client
	devs	= Developers()
	name	= "non-commands"
	name_typable	= "noncommands"
	description	= "Automatic message responses that aren't commands."
	description_long	= description

	# ANCHOR: ON MEMBER JOIN
	@commands.Cog.listener()
	async def on_member_join(self, member: discord.Member):
		if getops(member.guild.id, "toggles", "welcome"):
			welcome_channel = getops(member.guild.id, "channels", "welcomeChannel")
			if welcome_channel:	await get(member.guild.text_channels, id=welcome_channel).send(getops(member.guild.id, "messages", "welcomeMessage").replace("SERVER", member.guild.name).replace("USER", member.name))

	# ANCHOR: ON MEMBER LEAVE
	@commands.Cog.listener()
	async def on_member_remove(self, member: discord.Member):
		if getops(member.guild.id, "toggles", "welcome"):
			welcome_channel = getops(member.guild.id, "channels", "welcomeChannel")
			if welcome_channel:	await get(member.guild.text_channels, id=welcome_channel).send(getops(member.guild.id, "messages", "goodbyeMessage").replace("SERVER", member.guild.name).replace("USER", member.name))

	@commands.Cog.listener()
	async def on_message(self, message):
		# ANCHOR: RETURN HELP NOTE
		if "<@!" + str(self.client.user.id) + ">" == message.content:	await message.channel.send(f"My prefix is `{self.client.command_prefix}`")
		# check if the message it's reading belongs to a bot
		# then make sure it's not a DM, in which case, don't test options (because there are none)
		if not message.author.bot:
			if not isinstance(message.channel, discord.channel.DMChannel):
				# send everything to variables to make my life easier
				messagetext = message.content.lower()
				server = message.guild.id

				# ANCHOR: DAD JOKES
				if getops(server, "toggles", "dadJokes"):
					# four types of apostrophes/ticks plus allowance for "im"
					dad_prefixes = ["'", "`", "‘", "’", ""]
					for dad in dad_prefixes:
						if messagetext.startswith(f"i{dad}m "):
							if "pengaelic bot" in messagetext:
								if	"not" in messagetext:	await message.channel.send("Darn right, you're not!")
								else:		await message.channel.send("You're not the Pengaelic Bot, I am!")
							elif "chickenmeister" in messagetext or "tux" in messagetext:
								if Developers.check(self, message.author, "tux"):
									if	"not" in messagetext:	await message.channel.send("What? Of course you are!")
									else:		await message.channel.send("Yes you are! Hiya!")
								else:
									if	"not" in messagetext:	await message.channel.send("Darn right, you're not!")
									else:		await message.channel.send("You dare to impersonate my creator?! **You shall be punished.** /j")
							else:
								if	messagetext.startswith(f"i{dad}m an"):	slicer = 5
								elif	messagetext.startswith(f"i{dad}m a"):	slicer = 4
								else:		slicer = 2
								await message.channel.send(f"Hi{messagetext[len(dad)+slicer:]}, I'm the Pengaelic Bot!")

				# ANCHOR: CENSOR
				if getops(server, "toggles", "censor"):
					all_bads = getops(server, "lists", "censorList")
					for bad in all_bads:
						if bad in messagetext.split():
							await message.delete()
							await message.author.send(f"Hey, that word `{bad}` isn't allowed here!")

				# ANCHOR: DEAD CHAT
				if "dead" in messagetext and ("chat" in messagetext or "server" in messagetext) and getops(server, "toggles", "deadChat") and list(await message.channel.history(limit=2).flatten())[0].author != self.client.user:	await message.channel.send(f"{choice(['N', 'n'])}o {choice(['U', 'u'])}")

				# ANCHOR: AUTO POLLS
				if getops(server, "toggles", "suggestions") and message.channel.id == getops(server, "channels", "suggestionsChannel"):
					thepoll = await message.channel.send(
						embed=discord.Embed(
							title	= "Suggestion",
							description	= message.content,
							color	= 0x007F7F
						).set_author(
							name	= message.author.name,
							icon_url	= message.author.avatar_url
						)
					)
					try:	await message.delete()
					except:	pass
					await thepoll.add_reaction("✅")
					await thepoll.add_reaction("🤷")
					await thepoll.add_reaction("❌")

				# ANCHOR: RICK ROULETTE
				if "you know the rules" == messagetext and getops(server, "toggles", "rickRoulette"):	await message.channel.send(choice(["And so do I :pensive:" for _ in range(5)] + ["Say goodbye <:delet_this:828693389712949269>"]))

				# ANCHOR: @SOMEONE
				if "@someone" == messagetext and getops(server, "toggles", "atSomeone"):	await message.channel.send(choice(message.guild.members).mention + ", you have been randomly selected by a @someone ping!")

				# ANCHOR: REACTIONS
				if any(message in messagetext for message in ["pengaelic", self.client.user.mention, "<@!" + str(self.client.user.id) + ">"]):
					if	any(message in messagetext.split() for message in ["thank", "thanks"]):	await message.add_reaction("<:teal_heart:904458637139922994>")
					elif	any(message in messagetext.split() for message in ["fuck", "bad", "die"]):	await message.add_reaction("<:broken_teal_heart:904460939984781363>")
					elif	any(message in messagetext.split() for message in ["hi", "hey", "hello"]):	await message.add_reaction("👋")

			# ANCHOR: BOT OWNER DM INTERACTION
			elif isinstance(message.channel, discord.channel.DMChannel):
				if message.attachments and await self.client.is_owner(message.author):
					if message.attachments[0].filename == "config.json":
						await message.attachments[0].save("config.json")
						await message.channel.send("Downloaded new config file.")
					if message.attachments[0].filename == "env":
						await message.attachments[0].save(".env")
						await message.channel.send("Downloaded new dotenv file.")


def setup(client):	client.add_cog(NonCommands(client))
