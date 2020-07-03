import discord
from discord.ext import commands
from json import load
from random import choice

class Noncommands(commands.Cog):
    name = "noncommands"
    description = "Automatic message responses that aren't commands."
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            with open(rf"../pengaelicbot.data/configs/{message.guild.id}.json", "r") as optionsfile:
                allOptions = load(optionsfile)
        except:
            pass
        if message.author.mention == "<@721092139953684580>" or message.author.mention == "<@503720029456695306>": # that's the ID for Dad Bot, this is to prevent conflict.
            return

        # this section is for Dad Bot-like responses
        if allOptions["toggles"]["dad"] == True:
            dadprefixes = ["I'm ", "Im ", "I am "]
            for dad in range(len(dadprefixes)):
                dadprefixes.append(dadprefixes[dad].lower())
            for dad in range(len(dadprefixes)):
                if dadprefixes[dad] == message.content[0:len(dadprefixes[dad])]:
                    dadjoke = dadprefixes[dad]
                    if dadprefixes[dad].lower() in message.content:
                        dadjoke = dadjoke.lower()
                    if dadjoke[0] == message.content[0] and dadjoke[1] == message.content[1]:
                        if "Pengaelic Bot" in message.content or "Pengaelic bot" in message.content or "pengaelic bot" in message.content:
                            await message.channel.send("You're not the Pengaelic Bot, I am!")
                        else:
                            if dadprefixes[dad] + "a " == message.content[0:len(dadprefixes[dad])+2]:
                                await message.channel.send(f"Hi {message.content[len(dadjoke)+2:]}, I'm the Pengaelic Bot!")
                            else:
                                await message.channel.send(f"Hi {message.content[len(dadjoke):]}, I'm the Pengaelic Bot!")

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
        if allOptions["toggles"]["yoMama"] == True:
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
                mamatype = choice(mamatypes)
                await message.channel.send(f"Invalid Yo Mama type detected... Sending a {mamatype} joke.")
                await message.channel.send(f"Yo mama so {mamatype}")

def setup(client):
    client.add_cog(Noncommands(client))