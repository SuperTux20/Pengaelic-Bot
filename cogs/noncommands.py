import discord
from discord.utils import get
from discord.ext import commands
from json import load
from random import choice

class Noncommands(commands.Cog):
    name = "noncommands"
    description = "Automatic message responses that aren't commands."
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        with open(rf"../pengaelicbot.data/configs/{member.guild.id}.json", "r") as optionsfile:
            allOptions = load(optionsfile)
        if allOptions["toggles"]["welcome"] == True:
            possiblechannels = ["member-log", "members-log", "welcome", "arrivals", "entrance", "entry", "log", "general"]
            for channel in possiblechannels:
                try:
                    await get(member.guild.text_channels, name=channel).send(f"Welcome to {member.guild.name}, {member.mention}!")
                    break
                except:
                    continue
            print(f"{member} has joined {member.guild.name}.")

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            with open(rf"../pengaelicbot.data/configs/{message.guild.id}.json", "r") as optionsfile:
                allOptions = load(optionsfile)
        except:
            pass

        if message.author.id == 721092139953684580 or message.author.id == 503720029456695306: # that's the ID for Dad Bot, this is to prevent conflict.
            return

        # this section is for Dad Bot-like responses
        if allOptions["toggles"]["jokes"]["dad"] == True:
            dadprefs = ["I'm ", "Im ", "I am "]
            dadprefixes = dadprefs.copy()
            for dad in dadprefixes:
                dadprefs.append(dad.lower())
            for dad in dadprefs:
                if dad == message.content[0:len(dad)]:
                    if dad[0] == message.content[0] and dad[1] == message.content[1]:
                        if "Pengaelic Bot" in message.content or "Pengaelic bot" in message.content or "pengaelic bot" in message.content:
                            if "not" in message.content:
                                await message.channel.send("Darn right, you're not!")
                            else:
                                await message.channel.send("You're not the Pengaelic Bot, I am!")
                        elif ("chicken" in message.content and "meister" in message.content) or dad + "Tux" == message.content or dad + "tux" == message.content:
                            if message.author.name == "chickenmeister" and message.author.discriminator == 7140:
                                await message.channel.send("Yes you are! Hiya!")
                            else:
                                await message.channel.send("You dare to impersonate my creator?! ***You shall be punished.***")
                        else:
                            if dad + "a " == message.content[0:len(dad)+2]:
                                await message.channel.send(f"Hi {message.content[len(dad)+2:]}, I'm the Pengaelic Bot!")
                            else:
                                await message.channel.send(f"Hi {message.content[len(dad):]}, I'm the Pengaelic Bot!")

        # this section is to auto-delete messages containing a keyword contained in the text file
        if allOptions["toggles"]["censor"] == True:
            try:
                open(rf"../pengaelicbot.data/censorfilters/{message.guild.id}.txt", "x").close()
                print("Censor file created for " + str(message.guild.name))
            except FileExistsError:
                pass
            with open(rf"../pengaelicbot.data/censorfilters/{message.guild.id}.txt", "r") as bads_file:
                all_bads = bads_file.read().split(", ")
                if all_bads == [""]:
                    pass
                else:
                    for bad in range(len(all_bads)):
                        if all_bads[bad] in message.content or all_bads[bad].lower() in message.content or all_bads[bad] == message.content:
                            await message.delete()

        # this section reprimands people when they're rude to the bots, does not reprimand if rudeness level is above 1
        if allOptions["numbers"]["rudeness"] < 2:
            insults = ["Your mother was a calculator and your dad ran on Windows Vista", "Fuck you", "Screw you", "Stfu", "Shut up"]
            bots = [str(member)[:-5] for member in message.guild.members if member.bot is True]
            if "YAGPDB.xyz" in bots:
                bots.append("YAGPBD")
                bots.append("YAG")
            for insult in range(len(insults)):
                if insults[insult] in message.content or insults[insult].lower() in message.content:
                    if "pengaelicbot" in message.content or "pengaelic bot" in message.content or "Pengaelic bot" in message.content or "Pengaelic Bot" in message.content:
                        await message.channel.send(choice([";-;", ":sob:", ":cry:"]))
                    else:
                        for bot in range(len(bots)):
                            if bots[bot] in message.content or bots[bot].lower() in message.content:
                                defenseP1 = ["Hey", "Dude", "Whoa"]
                                defenseP2 = ["be nice to " + bots[bot], "be nice", "chill out"]
                                defenseP3 = ["its job", "what it was told", "what it's supposed to"]
                                await message.channel.send(f"{choice(defenseP1)}, {choice(defenseP2)}, it's only doing {choice(defenseP3)}!")

        # this section randomizes yo mama jokes, does not work if rudeness is below 2
        if allOptions["toggles"]["jokes"]["yoMama"] == True:
            with open(r"Yo Mama Jokes.json", "r") as AllTheJokes:
                jokes = load(AllTheJokes)
                mamatypes = list(jokes.keys())
            failedtypes = []
            for mom in range(len(mamatypes)):
                if "Yo mama so " == message.content[0:11] or "yo mama so " in message.content[0:11]:
                        if mamatypes[mom] in message.content:
                            if allOptions["numbers"]["rudeness"] > 1:
                                await message.channel.send(choice(jokes[mamatypes[mom]]))
                            else:
                                await message.channel.send("Yo Mama jokes are disabled: rudeness level below 2.")
                        else:
                            if "dumb" in message.content or "retarded" in message.content:
                                    await message.channel.send(choice(jokes["stupid"]))
                            else:
                                failedtypes.append(mamatypes[mom])
                elif "Yo mama list" == message.content or "yo mama list" in message.content:
                    if allOptions["numbers"]["rudeness"] > 1:
                        await message.channel.send(str(mamatypes)[1:-1].replace("'",""))
                    else:
                        await message.channel.send("Yo Mama jokes are disabled: rudeness level below 2.")
                    break
            if failedtypes == mamatypes:
                await message.channel.send(f"Invalid Yo Mama type detected...")
                await message.channel.send(f"Type `yo mama list` for a list of valid types!")

        if ("dead" in message.content) and ("chat" in message.content or "server"  in message.content) or "<:deadchat:720311826608291852>" == message.content:
            await message.channel.send(f"{choice(['N','n'])}o {choice(['U','u'])}")

        if message.content == "You know the rules" or message.content == "you know the rules":
            responses = []
            death_threats = ["It's time to die <:handgun:706698375592149013>", "And so do I :pensive:\nSay goodbye <:handgun:706698375592149013>"]
            for _ in range(5):
                responses.append("And so do I :pensive:")
            responses.append(choice(death_threats))
            await message.channel.send(choice(responses))

def setup(client):
    client.add_cog(Noncommands(client))