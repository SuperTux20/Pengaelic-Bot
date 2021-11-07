# !/usr/bin/python3.9
# -*- coding: utf-8 -*-

import	discord
from io import	BytesIO
from discord.ext import	commands
from pengaelicutils import	jsoncheck,	unhandling,	tux_in_guild
from PIL import	Image,	ImageFont,	ImageDraw
from requests import	get

class Memes(commands.Cog):
	def __init__(self, client):	self.client	= client
	teal	= 0x007F7F
	name	= "memes"
	name_typable	= name
	description	= "Image manipulation is fun, isn't it?"
	description_long	= description
	valid_image	= lambda self, filename: any(filename.endswith(ext) for ext in ["png", "jpg", "jpeg"])

	def Image2File(self, img: Image, name: str) -> discord.File:
		with BytesIO() as image_binary:
			img.save(image_binary, "PNG")
			image_binary.seek(0)
			return discord.File(image_binary, name)

	def getImage(self, ctx) -> Image:
		if ctx.message.attachments:
			if self.valid_image(ctx.message.attachments[0].filename):	return Image.open(BytesIO(get(ctx.message.attachments[0].url).content))
			else:	return Image.open("images/meme_templates/generic.jpg")

		else:	return Image.open("images/meme_templates/generic.jpg")

	@commands.command(name="2012meme", help="Make a classic top-text bottom-text meme. Supply your own PNG or JPG!", usage="<top text> | [bottom text]")
	async def topbottom(self, ctx, *, text):
		img	= self.getImage(ctx)
		width, height	= img.size
		try:	topString, bottomString = text.upper().split("|")
		except ValueError as error:
			if "not enough" in str(error):	topString, bottomString	= [text.upper(), ""]
			else:	raise

		fontSize	= int(height / 5)	# find biggest font size that works
		font	= ImageFont.truetype("fonts/impact.ttf", fontSize)
		topTextSize	= font.getsize(topString)
		bottomTextSize	= font.getsize(bottomString)
		while topTextSize[0] > width - 20 or bottomTextSize[0] > width - 20:
			fontSize	= fontSize - 1
			font	= ImageFont.truetype("fonts/impact.ttf", fontSize)
			topTextSize	= font.getsize(topString)
			bottomTextSize	= font.getsize(bottomString)

		topTextPosition	= ((width / 2) - (topTextSize[0]	/ 2), 0)
		bottomTextPosition	= ((width / 2) - (bottomTextSize[0]	/ 2), height - bottomTextSize[1])
		draw	= ImageDraw.Draw(img)
		outlineRange	= int(fontSize / 15)	# draw outlines
		for x in range(-outlineRange, outlineRange + 1):
			for y in range(-outlineRange, outlineRange + 1):
				draw.text((topTextPosition[0] + x,	topTextPosition[1] + y),	topString,	(0, 0, 0), font=font)
				draw.text((bottomTextPosition[0] + x,	bottomTextPosition[1] + y),	bottomString,	(0, 0, 0), font=font)

		draw.text(topTextPosition,	topString,	0xffffffff, font=font)
		draw.text(bottomTextPosition,	bottomString,	0xffffffff, font=font)
		await ctx.send(file=self.Image2File(img, "2012meme.png"))

	@commands.command(name="2016meme", help="Make a more modern top-text meme. Supply your own PNG or JPG!", usage="<text> | [text] | [text] | [etc]")
	async def toponly(self, ctx, *, text):
		img	= self.getImage(ctx)
		width, height	= img.size
		text	= text.split("|")
		fontSize	= int(height / 10)	# find biggest font size that works
		font	= ImageFont.truetype("fonts/liberation.ttf", fontSize)
		for line in text:
			textSize	= font.getsize(line)
			while textSize[0] > width - 20:
				fontSize	= fontSize - 1
				font	= ImageFont.truetype("fonts/liberation.ttf", fontSize)
				textSize	= font.getsize(line)

		pad = Image.new(img.mode, (width, height + (fontSize * len(text))), 0xffffffff)	# add white padding
		pad.paste(img, (0, (fontSize * len(text)) + 10))
		draw	= ImageDraw.Draw(pad)

		for line in text:	draw.text((0, (fontSize * text.index(line))),	line,	(0, 0, 0), font=font)
		await ctx.send(file=self.Image2File(pad, "2016meme.png"))

	# FIXME: holy fuck come back to this later, text issues
	# @commands.command(name="drakememe", help="Make a drake meme.", usage="<text> | <text>")
	# async def drake(self, ctx, *, text):
	#	img	= Image.open("images/meme_templates/drake.jpg")
	#	width, height	= [img.size[0]*2, img.size[1]]
	#	try:	topString, bottomString = text.split("|")
	#	except ValueError as error:
	#		if "not enough" in str(error):	topString, bottomString	= [text, ""]
	#		else:	raise

	#	fontSize	= int(height / 10)	# find biggest font size that works
	#	font	= ImageFont.truetype("fonts/liberation.ttf", fontSize)
	#	topTextSize	= font.getsize(topString)
	#	bottomTextSize	= font.getsize(bottomString)
	#	twrap = 0
	#	bwrap = 0
	#	while topTextSize[0] > width - 20 or bottomTextSize[0] > width - 20:
	#		tmp = topString.split()
	#		if len(topString.split("\n")) > 1:	tmp += [topString.split("\n")[1]]
	#		try:	topString = " ".join(tmp[:-twrap]) + "\n".join(tmp[-twrap:])
	#		except IndexError:	pass
	#		twrap += 1
	#		tmp = bottomString.split()
	#		if len(bottomString.split("\n")) > 1:	tmp += [bottomString.split("\n")[1]]
	#		try:	bottomString = " ".join(tmp[:-bwrap]) + "\n".join(tmp[-bwrap:])
	#		except IndexError:	pass
	#		bwrap += 1
	#		try:	topTextSize	= (font.getsize(topString)[0] - font.getsize("\n".join(topString.split()[-twrap:]))[0], font.getsize(topString)[1] - font.getsize("\n".join(topString.split()[-twrap:]))[1])
	#		except IndexError:	topTextSize	= font.getsize(topString)
	#		try:	bottomTextSize	= (font.getsize(bottomString)[0] - font.getsize("\n".join(bottomString.split()[-bwrap:]))[0], font.getsize(bottomString)[1] - font.getsize("\n".join(bottomString.split()[-bwrap:]))[1])
	#		except IndexError:	bottomTextSize	= font.getsize(bottomString)

	#	pad = Image.new(img.mode, (width, height), 0xffffffff)	# add white padding
	#	pad.paste(img, (0, 0))
	#	topTextPosition	= (((width / 2) - (topTextSize[0]	/ 2)), 10)
	#	bottomTextPosition	= (((width / 2) - (bottomTextSize[0]	/ 2)), bottomTextSize[1] + 500)
	#	if "\n" in topString:	topTextPosition = (topTextPosition[0] + width / 2, topTextPosition[1])
	#	if "\n" in bottomString:	bottomTextPosition = ((bottomTextPosition[0] + width / 2) - width / 24, bottomTextPosition[1] + width / 12)

	#	draw	= ImageDraw.Draw(pad)

	#	draw.text(topTextPosition,	topString,	(0, 0, 0), font=font)
	#	draw.text(bottomTextPosition,	bottomString,	(0, 0, 0), font=font)
	#	await ctx.send(file=self.Image2File(pad, "drakememe.png"))

	# TODO: actually make this meme
	# @commands.command(name="galaxybrainmeme", help="Smarter and smarter.", usage="<text> | [text] | [text] | [etc]")
	# async def galaxybrain(self, ctx, *, text):
	#	img	= Image.open("images/meme_templates/galaxy_brain.jpg")
	#	width, height	= img.size
	#	text	= text.split("|")
	#	fontSize	= int(height / 10)	# find biggest font size that works
	#	font	= ImageFont.truetype("fonts/liberation.ttf", fontSize)
	#	for line in text:
	#		textSize	= font.getsize(line)
	#		while textSize[0] > width - 20:
	#			fontSize	= fontSize - 1
	#			font	= ImageFont.truetype("fonts/liberation.ttf", fontSize)
	#			textSize	= font.getsize(line)

	#	pad = Image.new(img.mode, (width, height + (fontSize * len(text))), 0xffffffff)	# add white padding
	#	pad.paste(img, (0, (fontSize * len(text)) + 10))
	#	draw	= ImageDraw.Draw(pad)

	#	for line in text:	draw.text((0, (fontSize * text.index(line))),	line,	(0, 0, 0), font=font)
	#	await ctx.send(file=self.Image2File(pad, "galaxybrainmeme.png"))

	@topbottom.error
	@toponly.error
	# @drake.error
	# @galaxybrain.error
	async def messageError(self, ctx, error):
		error = str(error)
		if "text is a required argument that is missing." in error:	await ctx.send("<:winxp_warning:869760947114348604>No caption specified!")
		elif "too many values to unpack" in error:	await ctx.send("<:winxp_warning:869760947114348604>Too many lines specified!")
		else:	await ctx.send(unhandling(error, tux_in_guild(ctx, self.client)))


def setup(client):	client.add_cog(Memes(client))
