#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from asyncio	import get_event_loop
from discord	import PCMVolumeTransformer,	FFmpegPCMAudio
from discord.errors	import ClientException
from discord.ext	import commands
from os	import mkdir
from youtube_dl	import YoutubeDL, utils

utils.bug_reports_message = lambda: ""

ytdl_format_options = {
	"format":	"bestaudio/best",
	"restrictfilenames":	True,
	"noplaylist":	True,
	"nocheckcertificate":	True,
	"ignoreerrors":	False,
	"logtostderr":	False,
	"quiet":	True,
	"no_warnings":	True,
	"default_search":	"auto",
	"source_address":	"0.0.0.0", # bind to ipv4 since ipv6 addresses cause issues sometimes
	"outtmpl":	"youtube-dl/%(title)s.%(ext)s"
}

ffmpeg_options = {
	"options":	"-vn"
}

ytdl = YoutubeDL(ytdl_format_options)

class YTDLSource(PCMVolumeTransformer):
	def __init__(self, source, *, data, volume=0.5):
		super().__init__(source, volume)
		self.data = data
		self.title = data.get("title")
		self.url = ""

	@classmethod
	async def from_url(cls, url, *, loop=None, stream=False):
		loop = loop or get_event_loop()
		data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
		if "entries" in data:
			# take first item from a playlist
			data = data["entries"][0]
		filename = data["title"] if stream else ytdl.prepare_filename(data)
		return filename

class Music(commands.Cog):
	def __init__(self, client):	self.client	= client
	name	= "music"
	name_typable	= name
	description	= "Play music in a voice channel!"
	description_long	= description + " Here's hoping I don't get a cease-and-desist from Google."

	def fname_formatter(self, filename):
		removes =	["Official", "Music Video"]
		filename =	filename.split("/", 1)[1].rsplit(".", 1)[0].replace("_", " ")
		for key in removes:	filename = filename.replace(key,"")
		while filename != filename.replace("  ", " "):	filename = filename.replace("  ", " ")
		return filename

	@commands.command(name="play", help="Join VC and play music from a YouTube link.", usage="[url]")
	async def play(self, ctx, url = None):
		if not ctx.message.author.voice:
			await ctx.send("You aren't connected to a voice channel.")
		else:
			try:	await ctx.message.author.voice.channel.connect()
			except ClientException:	pass
			if url:
				vc =	ctx.message.guild.voice_client
				await ctx.send("Downloading audio from YouTube link...")
				async with ctx.typing():
					try:	mkdir("youtube-dl")
					except FileExistsError:	pass
					filename =	await YTDLSource.from_url(url if not (url.startswith("<") and url.endswith(">")) else url[1:-1], loop=self.client.loop)
					try:	vc.play(FFmpegPCMAudio(executable="ffmpeg", source=filename))
					except ClientException:
						vc.stop()
						vc.play(FFmpegPCMAudio(executable="ffmpeg", source=filename))
				await ctx.send("**Now playing:** {}".format(self.fname_formatter(filename)))
			else:
				await ctx.send("Joined the chat. If you want to play music, specify a URL to pull from.")

	@commands.command(name="stop", help="Stop the music.")
	async def stop(self, ctx):
		vc =	ctx.message.guild.voice_client
		try:	await vc.disconnect()
		except:	await ctx.send("I'm not connected to a voice channel.")

async def setup(client):	await client.add_cog(Music(client))
