# !/usr/bin/python3.9
# -*- coding: utf-8 -*-

import	discord
from asyncio.events import	get_event_loop
from concurrent.futures import	ThreadPoolExecutor
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

	def twelve(self, img: Image, text: str) -> Image:
		width, height	= img.size
		try:	top_string, bottom_string = text.upper().split("|")
		except ValueError as error:
			if "not enough" in str(error):	top_string, bottom_string	= [text.upper(), ""]
			else:	raise

		font_size	= int(height / 5)	# find biggest font size that works
		font	= ImageFont.truetype("fonts/impact.ttf", font_size)
		top_text_size	= font.getsize(top_string)
		bottom_text_size	= font.getsize(bottom_string)
		while top_text_size[0] > width - 20 or bottom_text_size[0] > width - 20:
			font_size	= font_size - 1
			font	= ImageFont.truetype("fonts/impact.ttf", font_size)
			top_text_size	= font.getsize(top_string)
			bottom_text_size	= font.getsize(bottom_string)

		top_text_pos	= ((width / 2) - (top_text_size[0]	/ 2), 0)
		bottom_text_pos	= ((width / 2) - (bottom_text_size[0]	/ 2), height - bottom_text_size[1])
		draw	= ImageDraw.Draw(img)
		outline_range	= int(font_size / 15)	# draw outlines
		for x in range(-outline_range, outline_range + 1):
			for y in range(-outline_range, outline_range + 1):
				draw.text((top_text_pos[0] + x,	top_text_pos[1] + y),	top_string,	(0, 0, 0), font=font)
				draw.text((bottom_text_pos[0] + x,	bottom_text_pos[1] + y),	bottom_string,	(0, 0, 0), font=font)

		draw.text(top_text_pos,	top_string,	0xffffffff, font=font)
		draw.text(bottom_text_pos,	bottom_string,	0xffffffff, font=font)

		return img

	def sixteen(self, img: Image, text: str) -> Image:
		width, height	= img.size
		text	= text.split("|")
		font_size	= int(height / 10)	# find biggest font size that works
		font	= ImageFont.truetype("fonts/liberation.ttf", font_size)
		for line in text:
			text_size	= font.getsize(line)
			while text_size[0] > width - 20:
				font_size	= font_size - 1
				font	= ImageFont.truetype("fonts/liberation.ttf", font_size)
				text_size	= font.getsize(line)

		pad = Image.new(img.mode, (width, height + (font_size * len(text))), 0xffffffff)	# add white padding
		pad.paste(img, (0, (font_size * len(text)) + 10))
		draw	= ImageDraw.Draw(pad)

		for line in text:	draw.text((0, (font_size * text.index(line))),	line,	(0, 0, 0), font=font)
		return pad

	@commands.command(name="2012meme", help="Make a classic top-text bottom-text meme. Supply your own PNG or JPG!", usage="<top text> | [bottom text]")
	async def topbottom(self, ctx, *, text):
		async with ctx.typing():	img = await get_event_loop().run_in_executor(ThreadPoolExecutor(), self.Image2File, self.twelve(self.getImage(ctx), text), "2012meme.png")
		await ctx.send(file=img)

	@commands.command(name="2016meme", help="Make a more modern top-text meme. Supply your own PNG or JPG!", usage="<text> | [text] | [text] | [etc]")
	async def toponly(self, ctx, *, text):
		async with ctx.typing():	img = await get_event_loop().run_in_executor(ThreadPoolExecutor(), self.Image2File, self.sixteen(self.getImage(ctx), text), "2016meme.png")
		await ctx.send(file=img)

	# FIXME: holy fuck come back to this later, text issues
	# @commands.command(name="drakememe", help="Make a drake meme.", usage="<text> | <text>")
	# async def drake(self, ctx, *, text):
	#	img	= Image.open("images/meme_templates/drake.jpg")
	#	width, height	= [img.size[0]*2, img.size[1]]
	#	try:	top_string, bottom_string = text.split("|")
	#	except ValueError as error:
	#		if "not enough" in str(error):	top_string, bottom_string	= [text, ""]
	#		else:	raise

	#	font_size	= int(height / 10)	# find biggest font size that works
	#	font	= ImageFont.truetype("fonts/liberation.ttf", font_size)
	#	top_text_size	= font.getsize(top_string)
	#	bottom_text_size	= font.getsize(bottom_string)
	#	top_wrap = 0
	#	bottom_wrap = 0
	#	while top_text_size[0] > width - 20 or bottom_text_size[0] > width - 20:
	#		tmp = top_string.split()
	#		if len(top_string.split("\n")) > 1:	tmp += [top_string.split("\n")[1]]
	#		try:	top_string = " ".join(tmp[:-top_wrap]) + "\n".join(tmp[-top_wrap:])
	#		except IndexError:	pass
	#		top_wrap += 1
	#		tmp = bottom_string.split()
	#		if len(bottom_string.split("\n")) > 1:	tmp += [bottom_string.split("\n")[1]]
	#		try:	bottom_string = " ".join(tmp[:-bottom_wrap]) + "\n".join(tmp[-bottom_wrap:])
	#		except IndexError:	pass
	#		bottom_wrap += 1
	#		try:	top_text_size	= (font.getsize(top_string)[0] - font.getsize("\n".join(top_string.split()[-top_wrap:]))[0], font.getsize(top_string)[1] - font.getsize("\n".join(top_string.split()[-top_wrap:]))[1])
	#		except IndexError:	top_text_size	= font.getsize(top_string)
	#		try:	bottom_text_size	= (font.getsize(bottom_string)[0] - font.getsize("\n".join(bottom_string.split()[-bottom_wrap:]))[0], font.getsize(bottom_string)[1] - font.getsize("\n".join(bottom_string.split()[-bottom_wrap:]))[1])
	#		except IndexError:	bottom_text_size	= font.getsize(bottom_string)

	#	pad = Image.new(img.mode, (width, height), 0xffffffff)	# add white padding
	#	pad.paste(img, (0, 0))
	#	top_text_pos	= (((width / 2) - (top_text_size[0]	/ 2)), 10)
	#	bottom_text_pos	= (((width / 2) - (bottom_text_size[0]	/ 2)), bottom_text_size[1] + 500)
	#	if "\n" in top_string:	top_text_pos = (top_text_pos[0] + width / 2, top_text_pos[1])
	#	if "\n" in bottom_string:	bottom_text_pos = ((bottom_text_pos[0] + width / 2) - width / 24, bottom_text_pos[1] + width / 12)

	#	draw	= ImageDraw.Draw(pad)

	#	draw.text(top_text_pos,	top_string,	(0, 0, 0), font=font)
	#	draw.text(bottom_text_pos,	bottom_string,	(0, 0, 0), font=font)
	#	await ctx.send(file=self.Image2File(pad, "drakememe.png"))

	# TODO: actually make this meme
	# @commands.command(name="galaxybrainmeme", help="Smarter and smarter.", usage="<text> | [text] | [text] | [etc]")
	# async def galaxybrain(self, ctx, *, text):
	#	img	= Image.open("images/meme_templates/galaxy_brain.jpg")
	#	width, height	= img.size
	#	text	= text.split("|")
	#	font_size	= int(height / 10)	# find biggest font size that works
	#	font	= ImageFont.truetype("fonts/liberation.ttf", font_size)
	#	for line in text:
	#		text_size	= font.getsize(line)
	#		while text_size[0] > width - 20:
	#			font_size	= font_size - 1
	#			font	= ImageFont.truetype("fonts/liberation.ttf", font_size)
	#			text_size	= font.getsize(line)

	#	pad = Image.new(img.mode, (width, height + (font_size * len(text))), 0xffffffff)	# add white padding
	#	pad.paste(img, (0, (font_size * len(text)) + 10))
	#	draw	= ImageDraw.Draw(pad)

	#	for line in text:	draw.text((0, (font_size * text.index(line))),	line,	(0, 0, 0), font=font)
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
