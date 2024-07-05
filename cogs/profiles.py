#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from discord	import Embed, User
from discord.ext	import commands
from discord.utils	import get
from flag	import flag
from json	import dumps
from pengaelicutils	import unhandling, tux_in_guild, parsedate, url2img, pil2wand, wand2pil
from wand.color	import Color
from wand.drawing	import Drawing
from wand.image	import Image as Wand
from tinydb	import TinyDB, Query

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
	newprof = lambda self: {
		key: None for key in [
			"bio",
			"birthday",
			"image",
			"motd",
			"nickname",
			"pronouns",
			"sexuality"
		]
	} | {
		key: 0 for key in [
			"color",
			"xp"
		]
	} | {"region": "UN"}

	# ANCHOR: GET PROFILE DATA
	async def getdata(self, member):
		return dict(sorted(self.db.search(Query().userID == int(member))[0].items())) if not (await self.client.fetch_user(member)).bot else None

	# ANCHOR: GET PROFILE
	async def getprof(self, member: str):
		profile	= await self.getdata(member)
		uname	= profile.pop("userName")
		profile["region"]	= flag(profile["region"])
		embed	= Embed(title=profile["nickname"] + f" ({uname})" if profile["nickname"] else uname, description=profile["bio"] if profile["bio"] else "No bio set", color=profile["color"])
		if profile["image"]:	embed.set_image(url=profile["image"])
		embed.add_field(name="Message of the Day", value=profile["motd"] if profile["motd"] else "No MOTD set")
		[profile.pop(key) for key in ["userID", "bio", "color", "image", "motd", "nickname"]]
		for bit in profile:	embed.add_field(name=bit.capitalize(), value=str(profile[bit]).replace("None", f"No {bit} set"), inline=False)
		return embed

	# ANCHOR: GET IMAGE PROFILE
	# FIXME
	# def getiprof(self, member: str):
	# 	user	= Query()
	# 	profile	= dict(sorted(self.db.search(user.userID == member)[0].items()))
	# 	color	= profile.pop("color")
	# 	image	= pil2wand(url2img(profile["image"] if profile["image"] else "images/meme_templates/generic.jpg"))
	# 	width, height	= image.width, image.height
	# 	fontcolor	= Color("#ffffff" if color < 0x7f7f7f else "#000000")
	# 	color	= hex(color)[2:]
	# 	color	= "#" + "".join(["0" for _ in range(6-len(color))]) + color
	# 	profile["region"]	= flag(profile["region"])
	# 	fg	= Wand(width=int(width*(7/8)), height=int(height*(7/8)), background=Color(color))
	# 	with Drawing() as draw:
	# 		draw.font	= "static/fonts/liberation.ttf"
	# 		draw.font_size	= int(height / 20)
	# 		draw.fill_color	= fontcolor
	# 		draw.text(0, 50, f"{profile['nickname']} ({profile['userName']})")
	# 		draw.text(0, 100, str(profile["bio"]))
	# 		draw.text(0, 200, str(profile["motd"]))
	# 		draw.text(0, 250, str(profile["birthday"]))
	# 		draw.text(0, 300, str(profile["pronouns"]))
	# 		draw.text(0, 350, str(profile["region"]))
	# 		draw.text(0, 400, str(profile["sexuality"]))
	# 		draw(fg)
	# 		image.composite(fg, int(width*(1/16)), int(height*(1/16)))
	# 	return wand2pil(image)

	# ANCHOR: UPDATE PROFILE
	async def uprof(self, ctx, cond, option: str, value, show: bool = True):
		if value == "_ _": cond	= False
		user	= Query()
		profile	= self.db.search(user.userID == ctx.author.id)
		if profile:
			if option == "region" and len(value) != 2:
				await ctx.send("<:winxp_critical_error:869760946816553020>You have to use a proper country code (look at the flag emojis for reference).")
				return
			profile = profile[0]
			profile[option] = value
			self.db.update(profile, user.userID == ctx.author.id)
			if show: await ctx.send(f"<:winxp_information:869760946808180747>{'Updated' if cond else 'Removed'} {option}.")
		else:
			await ctx.send(f"<:winxp_warning:869760947114348604>You don't have a profile yet. Run `{self.client.command_prefix}profile` to create one!")
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
				self.db.update({"userName": ctx.author.name}, user.userID == uid) # did the user's name change?
				await ctx.send(f"Profile for {ctx.author.name}", embed=(await self.getprof(ctx.author.id)))#file=await get_event_loop().run_in_executor(ThreadPoolExecutor(), img2file, self.getiprof(ctx.author.id), f"profile_{ctx.author.name.replace(' ', '_')}_Pengaelic_Bot.png"))
			except IndexError:
				newprofile	= {"userName": ctx.author.name, "userID": ctx.author.id} | self.newprof()
				self.db.insert(newprofile)
				await ctx.send(f"Created new profile for {ctx.author.name}", embed=(await self.getprof(ctx.author.id)))

	@profile.command(name="get", help="Get someone else's profile.", usage="<user>")
	async def pget(self, ctx, *, user: User = None):
		if ctx.invoked_subcommand == None:
			if user:
				try:	await ctx.send(f"<:winxp_information:869760946808180747>Profile for {user.name}", embed=(await self.getprof(user.id)))
				except IndexError:	await ctx.send(f"<:winxp_warning:869760947114348604>{user.name} has no registered profile.")
			else:
				await ctx.send("<:winxp_critical_error:869760946816553020>You didn't specify a username or ID to get their profile.")

	@profile.command(name="bio", help="Set a bio for your profile.", aliases=["about", "aboutme", "Bio"], usage="[text]")
	async def set_bio(self, ctx, *, text=None):	await self.uprof(ctx, text, "bio", text)

	@profile.command(name="birthday", help="Set a birthday for your profile. An invalid date will unset it.", aliases=["bday", "bd", "Birthday"], usage="<MM>/<DD>/[YYYY]")
	async def set_bday(self, ctx, *, text=None):	await self.uprof(ctx, text, "birthday", await parsedate(ctx, text))

	@profile.command(name="color", help="Set your favorite color for your profile.", usage="<hex code with no #>")
	async def set_color(self, ctx, *, text=None):	await self.uprof(ctx, text, "color", int(text, 16) if text else 0)

	@profile.command(name="image", help="Set an image for your profile with attachment or URL.", aliases=["img", "background", "bg"], usage="[URL or image attachment]")
	async def set_img(self, ctx, *, text=None):	await self.uprof(ctx, text or ctx.message.attachments, "image", (ctx.message.attachments[0].url if ctx.message.attachments else text).replace("media.discordapp.net", "cdn.discordapp.com"))

	@profile.command(name="motd", help='Set a "Message of the Day" for your profile.', aliases=["motto", "slogan", "tagline", "MOTD"], usage="[text]")
	async def set_motd(self, ctx, *, text=None):	await self.uprof(ctx, text, "motd", text)

	@profile.command(name="nickname", help="Set a nickname for your profile.", aliases=["nick", "name"], usage="[text]")
	async def set_nick(self, ctx, *, text=None):	await self.uprof(ctx, text, "nickname", text)

	@profile.command(name="pronouns", help="Set your preferred pronouns for your profile.", aliases=["Pronouns"], usage="[text]")
	async def set_pronouns(self, ctx, *, text=None):	await self.uprof(ctx, text, "pronouns", text.lower())

	@profile.command(name="region", help="Set a region for your profile.", aliases=["country", "Region"], usage="[two-letter country code (see flag emoji names)]")
	async def set_region(self, ctx, text=None):	await self.uprof(ctx, text, "region", text.upper() if text else "UN")

	@profile.command(name="sexuality", help="Set your sexuality for your profile.", aliases=["Sexuality"], usage="[text]")
	async def set_sexuality(self, ctx, *, text=None):	await self.uprof(ctx, text, "sexuality", text)

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
		errorstr = str(error)[29:]
		if errorstr.startswith("User") and errorstr.endswith("not found."):	await ctx.send("<:winxp_warning:869760947114348604>That user doesn't exist on any servers I'm in.")
		elif errorstr.endswith("'%m/%d/%Y'") or errorstr.endswith("'%m/%d'"):	await ctx.send("<:winxp_critical_error:869760946816553020>Invalid date format! Please use MM/DD/YYYY (year is optional)")
		elif "base 16" in errorstr:	await ctx.send("<:winxp_critical_error:869760946816553020>Invalid color format! Please use any hexadecimal code from 000000 to FFFFFF.")
		else:	await ctx.send(unhandling(tux_in_guild(ctx, self.client)))

async def setup(client):	await client.add_cog(Profiles(client))
