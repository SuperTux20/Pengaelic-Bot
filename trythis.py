from json import loads
from dotenv import load_dotenv as dotenv
from os import getenv as env
dotenv('.env')
everyone = loads(env('DEVELOPER_IDS'))
print(everyone['cherry'])
