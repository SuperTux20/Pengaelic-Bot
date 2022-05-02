#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from cogs.profiles	import Profiles
from datetime	import datetime,	timedelta
from discord.utils	import get
from discord.ext	import commands
from discord	import Embed,	Member,	DMChannel
from pengaelicutils	import getops,	updop,	Developers
from random	import randint
from tinydb	import TinyDB


class XP(commands.Cog):
	def __init__(self, client):	self.client = client
	devs	= Developers()
	name	= "xp"
	name_typable	= name
	description	= "You know, experience points. You get 'em every message."
	description_long	= description
	db	= TinyDB("profiles.json")

	@commands.Cog.listener()
	async def on_message(self, message):
		profiles = Profiles(self.client)
		delay = 1
		increment = randint(2, 5)
		try:	current = getops(message.guild.id, "xp", str(message.author.id))
		except KeyError:	updop(message.guild.id, "xp", str(message.author.id), 0) if not message.author.bot else None
		# check if...
		# 1.) message is not in a DM (avoid errors)
		# 2.) message is not from a bot (don't give bots XP)
		# 3.) message is not within `delay` minutes of the previous message by the same user (avoid spam farming)
		if not isinstance(message.channel, DMChannel) and not message.author.bot and ([msg for msg in await message.channel.history(limit=1000).flatten() if msg.author == message.author][0].created_at < datetime.now() - timedelta(minutes=delay)):
			updop(message.guild.id, "xp", str(message.author.id), current + increment)
			await profiles.uprof(message, None, "xp", profiles.getdata(str(message.author.id))["xp"] + increment, False)

	@commands.command(name="xp", help="See your XP.", aliases=["rank"])
	async def xp(self, ctx):
		try:	serverXP = getops(ctx.guild.id, 'xp', str(ctx.author.id))
		except KeyError:	serverXP = 0
		await ctx.send(f"You have {serverXP} server XP and {Profiles(self.client).getdata(str(ctx.author.id))['xp']} global XP!")

	@commands.command(name="leaderboard", help="See the rankings on the server.", aliases=["top", "lb"])
	async def lb(self, ctx):
		await ctx.send(str([(get(ctx.guild.members,id=int(user)).name,xp) for user,xp in sorted(getops(ctx.guild.id,"xp").items(),key=lambda x:x[1],reverse=True)])[2:-2].replace("), (","\n").replace("'","").replace(",",":"))

	@commands.command(name="debug")
	async def debug(self, ctx):
		await ctx.send()


def setup(client):	client.add_cog(XP(client))
