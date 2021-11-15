#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from discord	import Embed
from datetime	import datetime
from discord.ext	import commands
from json	import dumps
from tinydb	import TinyDB,	Query
from pengaelicutils	import unhandling,	tux_in_guild, img2file, url2img
from PIL	import Image,	ImageFont,	ImageDraw

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
	newprof = lambda self: {key: None for key in [
			"bio",
			"birthday",
			"image",
			"motd",
			"nickname",
			"pronouns",
			"sexuality"
		]
	} | {"region": "united_nations"}

	# ANCHOR: GET PROFILE
	def getprof(self, member: str) -> dict:
		user	= Query()
		profile	= dict(sorted(self.db.search(user.userID == member)[0].items()))
		[profile.pop(key) for key in ["userName", "userID", "image"]]
		try:
			if len(profile["region"]) == 2:	profile["region"] = f"flag_{profile['region']}"
		except TypeError:
			pass
		profile["region"] = f":{profile['region']}:"
		return dumps(profile, indent=0)[1:-2].replace('"',"").replace(",","").replace("null", "No value set.")

	# ANCHOR: UPDATE PROFILE
	async def uprof(self, ctx, cond, option: str, value):
		user	= Query()
		profile	= self.db.search(user.userID == ctx.author.id)[0]
		profile[option]	= value
		self.db.update(profile, user.userID == ctx.author.id)
		await ctx.send(f"<:winxp_information:869760946808180747>{'Updated' if cond else 'Removed'} {option}.")

	async def parsedate(self, ctx, text):
		if "/" in text:
			if len(text.split("/")) == 3:	return datetime.strftime(datetime.strptime(text, "%m/%d/%Y"), "%B %-d %Y")
			if len(text.split("/")) == 2:	return datetime.strftime(datetime.strptime(text, "%m/%d"), "%B %-d")
			else:	await ctx.send("Invalid date format! Please use M/D/YYYY (year is optional)")

		else:	await ctx.send("Invalid date format! Please use M/D/YYYY (year is optional)")
	# END SECTION

	@commands.group(name="profile", help="Take a look at your profile!", aliases=["me"])
	async def profile(self, ctx):
		if ctx.invoked_subcommand == None:
			try:
				# add any parameters that may have been created since the profile's creation
				user	= Query()
				uid	= ctx.author.id
				nof	= self.newprof()
				prof	= self.db.search(user.userID == uid)[0]
				[prof.pop(key) for key in ["userName", "userID"]]
				for rof in list(nof.keys()):
					if rof not in nof:	prof.pop(rof)
				for rof in list(nof.keys()):
					prof = dict(list(nof.items()) + list(prof.items()))
					self.db.update(dict(sorted(prof.items())), user.userID == uid)

				self.db.update({"userName": ctx.author.name}, user.userID == uid)	# did the user's name change?
				await ctx.send(f"Profile for {ctx.author.name}")
				await ctx.send(self.getprof(ctx.author.id))
			except IndexError:
				newprofile	= {"userName": ctx.author.name, "userID": ctx.author.id} | self.newprof()
				self.db.insert(newprofile)
				await ctx.send(f"Created new profile for {ctx.author.name}")
				await ctx.send(self.getprof(ctx.author.id))

	@profile.command(name="help", help="Get help on how to configure your profile.", aliases=["commands", "?"])
	async def set_bio(self, ctx, *, text=None): await ctx.send(embed=Embed(title="Profiles"))

	@profile.command(name="bio", help="Set a bio for your profile.", aliases=["about", "aboutme"])
	async def set_bio(self, ctx, *, text=None): await self.uprof(ctx, text, "bio", text)

	@profile.command(name="birthday", help="Set a birthday for your profile.", aliases=["bday", "bd"], usage="<M>/<D>/[YYYY]")
	async def set_bday(self, ctx, *, text=None): await self.uprof(ctx, text, "birthday", await self.parsedate(ctx, text))

	@profile.command(name="image", help="Set an image for your profile with attachment or URL.", aliases=["img", "background", "bg"])
	async def set_img(self, ctx, text=None): await self.uprof(ctx, text or ctx.message.attachments, "image", ctx.message.attachments[0].url if ctx.message.attachments else text)

	@profile.command(name="motd", help='Set a "Message of the Day"/motto/slogan for your profile.', aliases=["motto", "slogan", "tagline"])
	async def set_motd(self, ctx, *, text=None): await self.uprof(ctx, text, "motd", text)

	@profile.command(name="nickname", help="Set a nickname for your profile.", aliases=["nick", "name"])
	async def set_nick(self, ctx, *, text=None): await self.uprof(ctx, text, "nickname", text)

	@profile.command(name="pronouns", help="Set pronouns for your profile.")
	async def set_pronouns(self, ctx, text=None): await self.uprof(ctx, text, "pronouns", text)

	@profile.command(name="region", help="Set a region for your profile.", aliases=["country"])
	async def set_region(self, ctx, text=None): await self.uprof(ctx, text, "region", text)

	@profile.command(name="sexuality", help="Set a sexuality for your profile.")
	async def set_sexuality(self, ctx, text=None): await self.uprof(ctx, text, "sexuality", text)

	@profile.error
	@set_bio.error
	@set_img.error
	@set_motd.error
	@set_nick.error
	@set_pronouns.error
	@set_region.error
	@set_sexuality.error
	async def error(self, ctx, error):
		error = str(error)
		await ctx.send(unhandling(error, tux_in_guild(ctx, self.client)))

def setup(client):	client.add_cog(Profiles(client))
