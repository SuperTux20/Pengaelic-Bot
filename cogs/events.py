#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from datetime	import datetime
from discord.utils	import get
from discord.ext	import commands,	tasks
from pengaelicutils	import getops,	get_channel
from tinydb	import TinyDB,	Query


class Events(commands.Cog):
	def __init__(self, client):	self.client = client
	name	= "events"
	name_typable	= name
	description	= "Scheduled events that aren't commands."
	description_long	= description
	db	= TinyDB("profiles.json")

	# ANCHOR: BIRTHDAY DETECTION
	@tasks.loop(hours=24)
	async def birthday_detector(self):
		guilds	= self.client.guilds
		users	= [member for member in [guild.members for guild in guilds]][0]
		users_with_profiles = [self.db.search(Query().userID == member.id) for member in users]
		while [] in users_with_profiles:
			users_with_profiles.remove([])
		for user in range(len(users_with_profiles)):
			users_with_profiles[user] = users_with_profiles[user][0]
		for user in [(users_with_profiles[user]) for user in range(len(users_with_profiles))]:
			try:
				if len(user["birthday"].rsplit(" ", 1)[1]) == 4: user["birthday"] = user["birthday"].rsplit(" ", 1)[0]
				if datetime.strftime(datetime.now(), "%B %-d") == user["birthday"]:
					birthday_wishes = f'Happy birthday, {self.client.get_user(user["userID"]).mention}! :birthday:'
					general_chat = [get(guild.text_channels, id=get_channel(guild.id, "general")) for guild in guilds][0]
					for usr in users:
						if usr.id in [get(guild.members, id=user["id"]) for guild in guilds]:
							await general_chat.send(birthday_wishes)
			except AttributeError:
				pass

def setup(client):	client.add_cog(Events(client))
