#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from discord	import Embed,	User
from datetime	import datetime
from discord.ext	import commands
from json	import dumps
from re	import search
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
	description_long	= description + " Specifying no arg will reset the value."

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
	} | {"color": 0, "region": "united_nations"}

	# ANCHOR: GET PROFILE
	def getprof(self, member: str):
		user	= Query()
		profile	= dict(sorted(self.db.search(user.userID == member)[0].items()))
		uname = profile.pop("userName")
		try:
			if len(profile["region"]) == 2:	profile["region"] = f"flag_{profile['region']}"
		except TypeError:
			pass
		profile["region"] = f":{profile['region']}:"
		embed = Embed(title=profile["nickname"] + f" ({uname})" if profile["nickname"] else uname, description=profile["bio"] if profile["bio"] else "No bio set", color=profile["color"])
		if profile["image"]: embed.set_image(url=profile["image"])
		embed.add_field(name="Message of the Day", value=profile["motd"] if profile["motd"] else "No MOTD set")
		[profile.pop(key) for key in ["userID", "bio", "color", "image", "motd", "nickname"]]
		for bit in profile:
			embed.add_field(name=bit.capitalize(), value=str(profile[bit]).replace("None", f"No {bit} set"), inline=False)
		return embed

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
		else:
			await ctx.send("Invalid date format! Please use MM/DD/YYYY (year is optional)")
	# END SECTION

	@commands.group(name="profile", help="Take a look at your profile!", aliases=["me"], usage="[user]")
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
				await ctx.send(f"Profile for {ctx.author.name}", embed=self.getprof(ctx.author.id))
			except IndexError:
				newprofile	= {"userName": ctx.author.name, "userID": ctx.author.id} | self.newprof()
				self.db.insert(newprofile)
				await ctx.send(f"Created new profile for {ctx.author.name}", embed=self.getprof(ctx.author.id))

	@profile.command(name="get", help="Get someone else's profile.", usage="<user>")
	async def pget(self, ctx, *, user: User = None):
		if ctx.invoked_subcommand == None:
			if user:
				try:	await ctx.send(f"<:winxp_information:869760946808180747>Profile for {user.name}", embed=self.getprof(user.id))
				except IndexError:	await ctx.send(f"<:winxp_warning:869760947114348604>{user.name} has no registered profile.")
			else:
				await ctx.send("<:winxp_critical_error:869760946816553020>You didn't specify a username or ID to get their profile.")

	@profile.command(name="bio", help="Set a bio for your profile.", aliases=["about", "aboutme"], usage="[text]")
	async def set_bio(self, ctx, *, text=None): await self.uprof(ctx, text, "bio", text)

	@profile.command(name="birthday", help="Set a birthday for your profile. An invalid date will unset it.", aliases=["bday", "bd"], usage="<MM>/<DD>/[YYYY]")
	async def set_bday(self, ctx, *, text=None): await self.uprof(ctx, text, "birthday", await self.parsedate(ctx, text))

	@profile.command(name="color", help="Set your favorite color for your profile.", usage="<hex code with no #>")
	async def set_color(self, ctx, *, text=None): await self.uprof(ctx, text, "color", int(text, 16) if text else 0)

	@profile.command(name="image", help="Set an image for your profile with attachment or URL.", aliases=["img", "background", "bg"], usage="[text]")
	async def set_img(self, ctx, *, text=None): await self.uprof(ctx, text or ctx.message.attachments, "image", (ctx.message.attachments[0].url if ctx.message.attachments else text).replace("media.discordapp.net", "cdn.discordapp.com"))

	@profile.command(name="motd", help='Set a "Message of the Day" for your profile.', aliases=["motto", "slogan", "tagline"], usage="[text]")
	async def set_motd(self, ctx, *, text=None): await self.uprof(ctx, text, "motd", text)

	@profile.command(name="nickname", help="Set a nickname for your profile.", aliases=["nick", "name"], usage="[text]")
	async def set_nick(self, ctx, *, text=None): await self.uprof(ctx, text, "nickname", text)

	@profile.command(name="pronouns", help="Set your preferred pronouns for your profile.", usage="[text]")
	async def set_pronouns(self, ctx, *, text=None): await self.uprof(ctx, text, "pronouns", text.lower())

	@profile.command(name="region", help="Set a region for your profile.", aliases=["country"], usage="[two-letter country code (see flag emoji names)]")
	async def set_region(self, ctx, text=None): await self.uprof(ctx, text, "region", text.lower() if text else "united_nations")

	@profile.command(name="sexuality", help="Set your sexuality for your profile.", usage="[text]")
	async def set_sexuality(self, ctx, *, text=None): await self.uprof(ctx, text, "sexuality", text)

	@profile.error
	@pget.error
	@set_bio.error
	@set_bday.error
	@set_color.error
	@set_img.error
	@set_motd.error
	@set_nick.error
	@set_pronouns.error
	@set_region.error
	@set_sexuality.error
	async def error(self, ctx, error):
		error = str(error)
		if error.startswith("User") and error.endswith("not found."):	await ctx.send("<:winxp_warning:869760947114348604>That user isn't on this server!")
		elif error.endswith("'%m/%d/%Y'") or error.endswith("'%m/%d'"):	await ctx.send("<:winxp_critical_error:869760946816553020>Invalid date format! Please use MM/DD/YYYY (year is optional)")
		else:	await ctx.send(unhandling(error, tux_in_guild(ctx, self.client)))

def setup(client):	client.add_cog(Profiles(client))
