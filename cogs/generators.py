#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from asyncio.events	import get_event_loop
from concurrent.futures	import ThreadPoolExecutor
from discord.ext	import commands
from time	import time
from random	import choice,	randint
from pengaelicutils	import list2str,	unhandling,	tux_in_guild,	Developers,	Stopwatch,	syllables,	eldritch_syllables, syllatest
from subprocess	import check_output as	bash

devs = Developers()


class Generators(commands.Cog):
	def __init__(self, client):	self.client = client
	name	= "generators"
	name_typable	= name
	description	= "Do ya like randomization?"
	description_long	= description + " So do I!"

	# SECTION: FUNCTIONS
	def MonkeyBusiness(
		self,
		word:	str,
		alphabet:	str,
		starttime:	float,
		success:	bool	= True,
		timer:	Stopwatch	= Stopwatch(),
		text:	str	= "",
	) -> tuple:
		while text.find(word) == -1:
			letter	= choice(alphabet)
			text	= text + letter
			if timer.monkeywatch(starttime) == "10:00":
				success = False
				break
		text = (
			text.replace("\\", "\\\\")
			.replace("*", "\*")
			.replace("_", "\_")
			.replace("`", "\`")
			.replace("~", "\~")
			.replace("|", "\|")
		)
		return text, True if len(text) > 1000 else False, len(text), success, timer.monkeywatch(starttime)

	def gen(self, amount: int = 1, upper_limit: int = 3, lower_limit: int = 2, eldritch: bool = False, test: bool = False) -> str:
		if	eldritch:
			syls = eldritch_syllables()
			if test:
				syls= syllatest
		else:		syls = syllables
		if amount > 0 and upper_limit > 0 and lower_limit > 0:
			if	lower_limit <= upper_limit:	return list2str(["".join([choice(choice(syls)) for _ in range(randint(lower_limit, upper_limit))]).capitalize() for _ in range(amount)], 3)
			else:		return "The lower limit cannot be higher than the upper limit."

		else:	return "Values can't be zero."

	# END SECTION

	@commands.command(name="name", help="Generate a random name! They tend to be mystic-sounding :eyes:", aliases=["namegen"], usage="[names to generate (1)]\n[max syllables (3)]\n[min syllables (2)]")
	async def name_generator(self, ctx, amount: int = 1, upper_limit: int = 3, lower_limit: int = 2):	await ctx.send(self.gen(amount, upper_limit, lower_limit))

	@commands.command(name="ename", help="Generate an eldritch name that sounds straight out of an H. P. Lovecraft novel.", aliases=["eldritchname"], usage="[names to generate (1)]\n[max syllables (3)]\n[min syllables (2)]")
	async def eldritch_name_generator(self, ctx, amount: int = 1, upper_limit: int = 3, lower_limit: int = 2):	await ctx.send(self.gen(amount, upper_limit, lower_limit, True))

	@commands.command(name="tname", help="A prototype name generator.", usage="[names to generate (1)]\n[max syllables (3)]\n[min syllables (2)]")
	async def testing_name_generator(self, ctx, amount: int = 1, upper_limit: int = 3, lower_limit: int = 2):	await ctx.send(self.gen(amount, upper_limit, lower_limit, True, True))

	@commands.command(name="floridaman", help="Generate random Florida Man headlines!", aliases=["florida"], usage="[other state/country]")
	async def florida_man(self, ctx, *, state="florida"):
		headline	= [" ".join([name.capitalize() for name in state.split()])]
		objects	= ["van", "dog", "cat", "car", "house", "alligator", "chicken nugget", "hospital bed", "penguin", "burger", "car salesman"]
		people	= ["man", "woman", "boy", "girl"]
		events	= ["pushed", "thrown", "dropped", "burned", "stabbed", "run over", "slapped", "arrested"]
		poss2	= ["", "by"]
		timing	= ["after", "when"]
		actions	= ["pushes", "throws", "drops", "burns", "stabs", "runs over", "slaps"]
		selected_object	= choice(objects)
		part2	= choice(poss2)
		headline.append(choice(people)).append(choice(events))

		if part2 != "":
			headline.append(part2).append(selected_object)
			objects.remove(selected_object)
			selected_object = choice(objects)

		headline.append(choice(timing)).append(selected_object)
		objects.remove(selected_object)
		headline.append(choice(actions)).append(choice(objects))
		await ctx.send(" ".join(headline))

	@commands.command(name="img", help="[Infinite Monkey Generator](https://codepen.io/justinchan/full/enBFA)", aliases=["monkeys", "infinitemonkey", "monkeygen"], usage="<word> [alphabet (abcdefghijklmnopqrstuvwxyz)]")
	async def img(self, ctx, word=None, alphabet="abcdefghijklmnopqrstuvwxyz"):
		if word == None:	await ctx.send("You didn't specify a keyword to search for!")
		else:
			invalid = False
			for character in word:
				if character not in alphabet:	invalid = True

			if invalid:	await ctx.send(f"<:winxp_warning:869760947114348604>Your keyword contained characters that weren't in the specified alphabet ({list2str(alphabet, 1)})")
			else:
				status = await ctx.send("<:winxp_information:869760946808180747>Generating...")
				async with ctx.typing():	text, cutoff, textlen, success, elapsed = await get_event_loop().run_in_executor(ThreadPoolExecutor(), self.MonkeyBusiness, word, alphabet, time())
				if success:
					await status.edit(content=f'<:winxp_information:869760946808180747>Keyword "{word}" found after {textlen} characters{" (last 1000 shown)" if cutoff else ""} in {elapsed}')
					await ctx.send("..." + text[-1000:] if cutoff else text)

				else:	await ctx.send(f'<:winxp_critical_error:869760946816553020>Could not find keyword "{word}" within ten minutes. :frowning:')

	@commands.command(name="fortune", help="Pipe output from [`fortune`](https://en.wikipedia.org/wiki/Fortune_(Unix))\nNote: My developer and I are **not** responsible for any offensive output it may generate.")
	async def fortune(self, ctx):	await ctx.send(f"```{bash('fortune').decode()[:-1]}```")

	@name_generator.error
	@eldritch_name_generator.error
	@testing_name_generator.error
	@florida_man.error
	@img.error
	@fortune.error
	async def error(self, ctx, error):
		errorstr = str(error)[29:]
		if	errorstr.startswith("HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body"):	await ctx.send("<:winxp_critical_error:869760946816553020>Sending all that would put me over the character limit!")
		elif	errorstr.startswith("Unexpected quote mark") and errorstr.endswith("in non-quoted string"):	await ctx.send('<:winxp_warning:869760947114348604>You need to escape your "quotation marks" with doubled backslashes (\\\\\ these things \\\\\\\).')
		elif	errorstr == ('Expected closing ".'):	await ctx.send("<:winxp_warning:869760947114348604>A single unescaped quotation mark isn't going to work, sorry.")
		else:		await ctx.send(unhandling(tux_in_guild(ctx, self.client)))


async def setup(client):	await client.add_cog(Generators(client))
