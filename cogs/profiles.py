#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

import	discord
from discord.ext import	commands
from json import	dumps
from tinydb import	TinyDB,	Query
from pengaelicutils import	jsoncheck,	unhandling,	tux_in_guild,	Developers

class Profiles(commands.Cog):
	def __init__(self, client):	self.client	= client
	teal	= 0x007F7F
	db	= TinyDB("profiles.json")
	name	= "profiles"
	name_typable	= name
	description	= "Set your personal profile!"
	description_long	= description

	# SECTION FUNCTIONS
	# ANCHOR: GENERATE NEW PROFILE
	newprof = lambda self: {
		"bio":	None,
		"image":	None,
		"motd":	None,
		"nickname":	None,
		"pronouns":	[],
		"region":	None,
	}


	# ANCHOR: GET PROFILE
	def getprof(self, member: str) -> dict:
		user	= Query()
		profile	= dict(sorted(self.db.search(user.userID == member)[0].items()))
		profile.pop("userName")
		profile.pop("userID")
		return profile


	# ANCHOR: UPDATE PROFILE
	def uprof(self, member: str, category: str, option: str, value):
		user	= Query()
		options	= self.db.search(user.userID == member)[0][category]
		options[option]	= value
		self.db.update({category: options}, user.userID == member)
	# END SECTION

	@commands.group(name="profile", help="Take a look at your profile!")
	async def showprofile(self, ctx):
		if ctx.invoked_subcommand == None:
			try:
				# add any options that may have been created since the profile's creation
				user	= Query()
				uid	= ctx.author.id
				nof	= self.newprof()
				prof	= self.db.search(user.userID == uid)[0]
				prof.pop("userName")
				prof.pop("userID")
				for rof in ["image", "nickname", "bio", "motd", "region", "pronouns"]:
					if rof not in nof:	prof.pop(rof)
				for rof in ["image", "nickname", "bio", "motd", "region", "pronouns"]:
					prof = dict(list(nof.items()) + list(prof.items()))
					self.db.update(dict(sorted(prof.items())), user.userID == uid)

				self.db.update({"userName": ctx.author.name}, user.userID == uid)	# did the user's name change?
				await ctx.send(f"Profile for {ctx.author.name}")
				await ctx.send(f"```json\n{dumps(self.getprof(uid), indent=4)}\n```")
			except IndexError:
				newprofile	= {"userName": ctx.author.name, "userID": ctx.author.id} | self.newprof()
				self.db.insert(newprofile)
				await ctx.send(f"Created new profile for {ctx.author.name}")
				await ctx.send(f"```json\n{dumps(self.getprof(ctx.author.id), indent=4)}\n```")

	@showprofile.error
	async def error(self, ctx, error):
		error = str(error)
		await ctx.send(unhandling(error, tux_in_guild(ctx, self.client)))

def setup(client):	client.add_cog(Profiles(client))
