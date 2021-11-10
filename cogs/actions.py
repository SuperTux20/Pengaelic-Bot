#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from discord	import Embed
from discord.ext	import commands
from random	import randint
from os	import listdir


class Actions(commands.Cog):
	def __init__(self, client):	self.client	= client
	teal	= 0x007F7F
	name	= "actions"
	name_typable	= name
	description	= "Emote actions!"
	description_long	= description

	async def act(self, ctx, act, punct="..."):	await ctx.send(embed=Embed(title=f"{ctx.author.mention} is {act}ing{punct}", color=self.teal).set_image(url=f"https://supertux20.github.io/Pengaelic-Bot/images/actions/{act}/{randint(1,len(listdir(f'images/actions/{act}'))-1)}.gif"))

	@commands.command(name="cry")
	async def cry(self, ctx):	await self.act(ctx, "cry")

	@commands.command(name="glare")
	async def glare(self, ctx):	await self.act(ctx, "glar")

	@commands.command(name="laugh")
	async def laugh(self, ctx):	await self.act(ctx, "laugh", "!")

	@commands.command(name="shrug")
	async def shrug(self, ctx):	await self.act(ctx, "shrugg", ".")

	@commands.command(name="sleep")
	async def sleep(self, ctx):	await self.act(ctx, "sleep")


def setup(client):	client.add_cog(Actions(client))
