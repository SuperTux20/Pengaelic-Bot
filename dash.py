#!/usr/bin/python3.9

from dotenv	import load_dotenv as	dotenv
from quart	import Quart,	redirect,	url_for,	render_template,	request
from quart_discord	import DiscordOAuth2Session
from os	import getenv,	environ

dotenv(".env")
# SECTION: web routes
app	= Quart(__name__)
app.secret_key = getenv("session")
environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
app.config["DISCORD_CLIENT_ID"] = getenv("CLIENT_ID")
app.config["DISCORD_CLIENT_SECRET"] = getenv("CLIENT_SECRET")
app.config["DISCORD_REDIRECT_URI"] = getenv("RI")
app.config["DISCORD_BOT_TOKEN"] = getenv("token")
dauth	= DiscordOAuth2Session(app)

# ANCHOR: ROOT
@app.route("/")
async def webroot():
	return await render_template("index.html")

# ANCHOR: INVITE
@app.route("/invite")
async def webinvite():
	return await render_template("invite.html")

# ANCHOR: INVITE SUCCESS
@app.route("/success")
async def websuccess():
	return await render_template("success.html")

# ANCHOR: DASHBOARD
@app.route("/dashboard")
async def webdashboard():
	logged = False
	if await dauth.authorized: logged = True
	return await render_template("dash.html", logged=logged)

# END SECTION
app.run_task("0.0.0.0")