#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from datetime	import datetime,	timedelta
from discord.utils	import get
from discord.ext	import commands
from pengaelicutils	import getops,	Developers
from tinydb	import TinyDB, Query


class Events(commands.Cog):
	def __init__(self, client):	self.client = client
	devs	= Developers()
	name	= "events"
	name_typable	= name
	description	= "Scheduled events that aren't commands."
	description_long	= description
	db	= TinyDB("profiles.json")

	# ANCHOR: BIRTHDAY DETECTION
	async def birthday_detector(self):
		users_with_profiles = [self.db.search(Query().userID == member.id) for member in message.guild.members]
		while [] in users_with_profiles:
			users_with_profiles.remove([])
		for user in range(len(users_with_profiles)):
			users_with_profiles[user] = users_with_profiles[user][0]
		for user in [(users_with_profiles[user]) for user in range(len(users_with_profiles))]:
			try:
				if len(user["birthday"].rsplit(" ", 1)[1]) == 4: user["birthday"] = user["birthday"].rsplit(" ", 1)[0]
				if datetime.strftime(datetime.now(), "%B %-d") == user["birthday"]:
					birthday_wishes = f'Happy birthday, {self.client.get_user(user["userID"]).mention}! :birthday:'
					general_chat = get(message.guild.text_channels, id=getops(message.guild.id, "channels", "generalChannel"))
					async for message in general_chat.history(limit=None, after=datetime.now()-timedelta(days=1)): already_sent = True if message.content == birthday_wishes else False
					if not already_sent: await general_chat.send(birthday_wishes)
			except AttributeError:
				pass

def setup(client):	client.add_cog(Events(client))
