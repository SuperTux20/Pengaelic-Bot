import quart
import os
import requests
from dotenv	import load_dotenv as	dotenv
from os	import getenv

dotenv(".env")

app	= quart.Quart("")
app.secret_key	= bytes(getenv("SESSION_KEY"), "utf-8")