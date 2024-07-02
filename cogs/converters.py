#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from num2words	import num2words
from fnmatch	import fnmatch
from discord.ext	import commands
from random	import choice,	shuffle
from pengaelicutils	import unhandling,	tux_in_guild,	Developers

devs = Developers()


class Converters(commands.Cog):
	def __init__(self, client):	self.client = client
	teal	= 0x007F7F
	name	= "converters"
	name_typable	= name
	description	= "Run some text through a converter to make it look funny!"
	description_long	= description

	async def test_for_content(self, ctx, arg) -> str:
		if arg:	return arg
		else:	return list([message async for message in ctx.channel.history(limit=2)])[1].content

	async def substitutor(self, ctx, arg, alphabet, upper=False):
		arg = await self.test_for_content(ctx, arg)
		if upper:	arg = arg.upper()
		for letter in alphabet:	arg = arg.replace(letter, alphabet[letter])
		await ctx.send(arg)

	@commands.command(name="owo",help="Convert whatever text into owo-speak... oh god why did i make this",aliases=["uwu", "furry"],usage="<text to convert>",)
	async def owoConverter(self, ctx, *, arg=None):
		arg = await self.test_for_content(ctx, arg)
		await ctx.send(arg.replace("l", "w").replace("r", "w").replace("t", "tw").replace("twh", "thw").replace("n", "ny") + " " + choice(["OwO", "UwU", "owo", "uwu", "^w^"]))

	@commands.command(name="blockify",help="Convert text into\n:regional_indicator_b: :regional_indicator_i: :regional_indicator_g: text.",aliases=["bigtext", "big"],usage="<text to convert>",)
	async def big_text(self, ctx, *, arg=None):
		arg = await self.test_for_content(ctx, arg)
		alphabet = "qwertyuiopasdfghjklzxcvbnm 1234567890"
		symbols = {
			"?": "question",
			"!": "exclamation",
			"#": "hash",
			"*": "asterisk",
			"+": "heavy_plus_sign",
			"-": "heavy_minus_sign",
			"×": "heavy_multiplication_x",
			"÷": "heavy_division_sign",
			"☼": "high_brightness",
			"♫": "musical_note",
			"†": "cross",
		}
		textlist = []
		for char in arg.lower():
			for letter in alphabet + "".join(list(symbols.keys())):
				if fnmatch(letter, char):
					try:
						_ = int(char)
						number = True

					except ValueError:	number = False
					if number:	textlist.append(f":{num2words(char)}:")
					elif char == " ":	textlist.append("\n")
					elif char in list(symbols.keys()):
						textlist.append(f":{symbols[char]}:")
						break

					else:	textlist.append(f":regional_indicator_{char}:")
		await ctx.send(" ".join(textlist).replace("\n ", "\n"))

	@commands.command(name="greekify",help="Make words *look* Greek, but the pronunciation is still roughly similar to English.",usage="<text to convert>",)
	async def greekify(self, ctx, *, arg=None):
		upper_alphabet = {
			"CH": "Χ",
			"PS": "Ψ",
			"AV": "ΑΥ",
			"AF": "ΑΥ",
			"EV": "ΕΥ",
			"EF": "ΕΥ",
			"OO": "ΟΥ",
			"EH": "ΑΙ",
			"TH": "Θ",
			"YE": "Γ",
			"YI": "Γ",
			"YU": "Γ",
			"A": "Α",
			"B": "Β",
			"C": "K",
			"D": "Δ",
			"E": "Ε",
			"F": "Φ",
			"G": "Γ",
			"H": "",
			"I": "Ι",
			"J": "Γ",
			"K": "Κ",
			"L": "Λ",
			"M": "Μ",
			"N": "Ν",
			"O": "Ο",
			"P": "Π",
			"Q": "Κ",
			"R": "Ρ",
			"S": "Σ",
			"T": "Τ",
			"U": "Ω",
			"V": "Φ",
			"W": "ΟΥ",
			"X": "Ξ",
			"Y": "Υ",
			"Z": "Ζ",
		}
		await self.substitutor(ctx, arg, {**upper_alphabet, **{letter.lower(): upper_alphabet[letter].lower() for letter in upper_alphabet}})

	@commands.command(name="japanize",help="Make text look and sound Japanese according to [this image](https://imgur.com/a/qEiCfhG). (Disclaimer: this is not Japanese at all)",usage="<text to convert>",)
	async def japanize(self, ctx, *, arg=None):
		arg	= await self.test_for_content(ctx, arg)
		output	= ""
		alphabet = {
			"a":	"ka",
			"b":	"tu",
			"c":	"mi",
			"d":	"te",
			"e":	"ku",
			"f":	"lu",
			"g":	"ji",
			"h":	"ri",
			"i":	"ki",
			"j":	"zu",
			"k":	"me",
			"l":	"ta",
			"m":	"rin",
			"n":	"to",
			"o":	"mo",
			"p":	"no",
			"q":	"ke",
			"r":	"shi",
			"s":	"ari",
			"t":	"chi",
			"u":	"do",
			"v":	"ru",
			"w":	"mei",
			"x":	"na",
			"y":	"fu",
			"z":	"zi",
		}
		for letter in range(len(arg)):
			try:	output += alphabet[arg[letter].lower()]
			except KeyError:	output += arg[letter]
		await ctx.send(output.capitalize())

	@commands.command(name="stroke",help="Shuffle a message",aliases=["shuffle", "mix"],usage="<text to convert>",)
	async def shuffle(self, ctx, *, arg=None):
		arg	= await self.test_for_content(ctx, arg)
		to_shuffle	= list(arg)
		shuffle(to_shuffle)
		await ctx.send("".join(to_shuffle))

	@commands.command(name="strokebyword",help="Shuffle the individual words instead of the entire message.",aliases=["shufflebyword", "mixbyword"],usage="<text to convert>",)
	async def shufflebyword(self, ctx, *, arg=None):
		arg	= await self.test_for_content(ctx, arg)
		words_to_shuffle	= arg.split()
		for to_shuffle in range(len(words_to_shuffle)):
			words_to_shuffle[to_shuffle] = list(words_to_shuffle[to_shuffle])
			shuffle(words_to_shuffle[to_shuffle])
			words_to_shuffle[to_shuffle] = "".join(words_to_shuffle[to_shuffle])
		await ctx.send(" ".join(words_to_shuffle))

	@commands.command(name="spacer",help="Insert spaces between every character",aliases=["space", "gaps"],usage="<text to convert>",)
	async def spacer(self, ctx, *, arg=None):
		arg = await self.test_for_content(ctx, arg)
		await ctx.send(" ".join(arg[i : i + 1] for i in range(0, len(arg), 1)))

	@commands.command(name="wingdings",help="You heard what the River Person said.",aliases=["dings", "gaster", "wd"],usage="<text to convert>",)
	async def dings(self, ctx, *, arg=None):
		await self.substitutor(ctx, arg, {
			"A":	":v:",
			"B":	":ok_hand:",
			"C":	":thumbsup:",
			"D":	":thumbsdown:",
			"E":	":point_left:",
			"F":	":point_right:",
			"G":	":point_up_2:",
			"H":	":point_down:",
			"I":	":raised_hand:",
			"J":	":slight_smile:",
			"K":	":neutral_face:",
			"L":	":frowning:",
			"M":	":bomb:",
			"N":	":skull_crossbones:",
			"O":	":flag_white:",
			"P":	":triangular_flag_on_post:",
			"Q":	":airplane:",
			"R":	":sunny:",
			"S":	":droplet:",
			"T":	":snowflake:",
			"U":	":cross:",
			"V":	":orthodox_cross:",
			"W":	":atom:",
			"X":	":diamond_shape_with_a_dot_inside:",
			"Y":	":star_of_david:",
			"Z":	":star_and_crescent:",
			" ":	"<:empty:903321647874994208>",
		}, True)

	@commands.command(name="sga",help="Ever wanted to speak Enchanting Table?",aliases=["enchant", "enchantingtable"],usage="<text to convert>",)
	async def sga(self, ctx, *, arg=None):
		await self.substitutor(ctx, arg, {
			"A":	"ᔑ",
			"B":	"ʖ",
			"C":	"ᓵ",
			"D":	"↸",
			"E":	"ᒷ",
			"F":	"⎓",
			"G":	"⊣",
			"H":	"⍑",
			"I":	"╎",
			"J":	"⋮",
			"K":	"ꖌ",
			"L":	"ꖎ",
			"M":	"ᒲ",
			"N":	"リ",
			"O":	"𝙹",
			"P":	"!¡",
			"Q":	"ᑑ",
			"R":	"∷",
			"S":	"ᓭ",
			"T":	"ℸ",
			"U":	"⚍",
			"V":	"⍊",
			"W":	"∴",
			"X":	" ̇/",
			"Y":	"\|\|",
			"Z":	"ᓭ",
		}, True)

	@owoConverter.error
	@big_text.error
	@greekify.error
	@shuffle.error
	@shufflebyword.error
	@spacer.error
	@dings.error
	@sga.error
	@japanize.error
	async def overcharlimit(self, ctx, error):
		errorstr = str(error)[29:]
		if	errorstr.startswith("HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body"):	await ctx.send("<:winxp_critical_error:869760946816553020>Sending all that would put me over the character limit!")
		elif	errorstr.startswith("HTTPException: 400 Bad Request (error code: 50006): Cannot send an empty message"):	await ctx.send("<:winxp_critical_error:869760946816553020>There's no text in the previous message for me to mess with!")
		elif	errorstr == "arg is a required argument that is missing.":	await ctx.send("<:winxp_warning:869760947114348604>You didn't specify any text to convert!")
		else:		await ctx.send(unhandling(tux_in_guild(ctx, self.client)))


async def setup(client):	await client.add_cog(Converters(client))
