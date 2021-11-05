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
			if self.valid_image(ctx.message.attachments[0].filename):
				return Image.open(BytesIO(get(ctx.message.attachments[0].url).content))
			else:
				return Image.open("images/meme_templates/generic.jpg")
		else:
			return Image.open("images/meme_templates/generic.jpg")

	@commands.group(name="2012meme", help="Make a classic top-text bottom-text meme. Supply your own PNG or JPG!", usage="<top text | bottom text>")
	async def topbottom(self, ctx, *, text):
		img	= self.getImage(ctx)
		width, height	= img.size
		try:
			topString, bottomString = text.upper().split("|")
		except ValueError:
			topString	= text.upper()
			bottomString	= ""
		# find biggest font size that works
		fontSize	= int(height / 5)
		font	= ImageFont.truetype("fonts/impact.ttf", fontSize)
		topTextSize	= font.getsize(topString)
		bottomTextSize	= font.getsize(bottomString)
		while topTextSize[0] > width - 20 or bottomTextSize[0] > width - 20:
			fontSize	= fontSize - 1
			font	= ImageFont.truetype("fonts/impact.ttf", fontSize)
			topTextSize	= font.getsize(topString)
			bottomTextSize	= font.getsize(bottomString)

		topTextPosition	= ((width / 2) - (topTextSize[0] / 2), 0)
		bottomTextPosition	= ((width / 2) - (bottomTextSize[0] / 2), height - bottomTextSize[1])
		draw	= ImageDraw.Draw(img)
		outlineRange	= int(fontSize / 15)	# draw outlines
		for x in range(-outlineRange, outlineRange + 1):
			for y in range(-outlineRange, outlineRange + 1):
				draw.text((topTextPosition[0] + x,	topTextPosition[1] + y),	topString,	(0, 0, 0), font=font)
				draw.text((bottomTextPosition[0] + x,	bottomTextPosition[1] + y),	bottomString,	(0, 0, 0), font=font)

		draw.text(topTextPosition,	topString,	0xffffffff, font=font)
		draw.text(bottomTextPosition,	bottomString,	0xffffffff, font=font)
		await ctx.send(file=self.Image2File(img, "2012meme.png"))

	@commands.group(name="2016meme", help="Make a more modern top-text meme. Supply your own PNG or JPG!", usage="<top text | bottom text>")
	async def toponly(self, ctx, *, text):
		img	= self.getImage(ctx)
		width, height	= img.size
		text	= text.split("|")
		# find biggest font size that works
		fontSize	= int(height / 10)
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

	@topbottom.error
	@toponly.error
	async def messageError(self, ctx, error):
		error = str(error)
		if error.endswith("text is a required argument that is missing."):	await ctx.send("<:winxp_warning:869760947114348604>No caption specified!")
		else:	await ctx.send(unhandling(error, tux_in_guild(ctx, self.client)))


def setup(client):	client.add_cog(Memes(client))
