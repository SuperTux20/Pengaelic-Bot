import discord
from discord.ext import commands
from random import choice
from json import load
from time import sleep

class Actions(commands.Cog):    
    def __init__(self, client):
        self.client = client
        self.isNomming = True
        self.nomSuccess = False

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.emoji == "👄":
            if user.id != 721092139953684580:
                if self.isNomming == True:
                    self.isNomming = False
                    self.nomSuccess = False

    @commands.command(name="slap", help="Slap someone...?")
    async def slap(self, ctx, slap: discord.User=""):
        with open(rf"../options/{ctx.guild.id}.json", "r") as optionsfile:
                allOptions = load(optionsfile)
        if allOptions["numbers"]["rudeness"] > 0:
            slapper = str(ctx.author.mention)
            try:
                slapped = "<@" + str(slap.id) + ">"
            except:
                await ctx.send("You can't just slap thin air! (Unless you're slapping a ghost?)")
                return
            responses = [slapped + " just got slapped by " + slapper, slapper + " slapped " + slapped]
            selfresponses = ["Hey, you can't slap yourself!", "Please don't", "y tho"]
            botresponses = [";-;", "ow! ;-;", "ow!"]
            if slap == ctx.author:
                await ctx.send(choice(selfresponses) + " :(")
            else:
                await ctx.send(choice(responses))
                if str(slap.id) == "721092139953684580":
                    await ctx.send(choice(botresponses))
        else:
            await ctx.send("Slapping is disabled: Rudeness level is 0")

    @commands.command(name="hug", help="Give somebody a hug!")
    async def hug(self, ctx, hug: discord.User=""):
        hugger = str(ctx.author.mention)
        try:
            hugged = "<@" + str(hug.id) + ">"
        except:
            await ctx.send("You can't just hug thin air! (Unless you're hugging a ghost?)")
            return
        responses = [hugged + " just got hugged by " + hugger, hugger + " hugged " + hugged, hugger + " gave a hug to " + hugged]
        selfresponses = ["You wrap your arms tightly around yourself.", "Reaching through the 4th dimension, you manage to give yourself a hug.", "You hug yourself, somehow."]
        botresponses = ["aww!", "thanks <:happy:708534449310138379>", "*gasp*"]
        if hug == ctx.author:
            await ctx.send(choice(selfresponses))
        else:
            await ctx.send(choice(responses))
            if str(hug.id) == "721092139953684580":
                await ctx.send(choice(botresponses))

    @commands.command(name="boop", help="Boop someone's nose :3")
    async def boop(self, ctx, boop: discord.User=""):
        booper = str(ctx.author.mention)
        try:
            booped = "<@" + str(boop.id) + ">"
        except:
            await ctx.send("You can't just boop thin air! (Unless you're booping a ghost?)")
            return
        responses = [booped + " just got booped by " + booper, booper + " booped " + booped, booper + " booped " + booped + "'s nose!", booper + " booped " + booped + " on the nose!"]
        selfresponses = ["You boop your own nose, I guess...? ", "You miss your nose and poke yourself in the eye. ", "Somehow, your hand clips through your nose and appears on the other side of your head. "]
        botresponses = ["<:happy:708534449310138379>", "<:uwu:708534448949559328>", "thaaanks :3"]
        if booped == "":
            await ctx.send("You can't just boop thin air! (Unless you're booping a ghost?)")
        elif boop == ctx.author:
            oops = choice(selfresponses)
            if oops == selfresponses[1]:
                await ctx.send(oops + choice(["Ouch", "Oops", "Whoops"]) + "!")
            else:
                await ctx.send(oops)
        else:
            await ctx.send(choice(responses))
            if str(boop.id) == "721092139953684580":
                await ctx.send(choice(botresponses))

    @commands.command(name="pat", help="Pat someone on the head!")
    async def pat(self, ctx, pat: discord.User="", *, bodypart="head"):
        patter = str(ctx.author.mention)
        try:
            patted = "<@" + str(pat.id) + ">"
        except:
            await ctx.send("You can't just pat thin air! (Unless you're patting a ghost?)")
            return
        responses = [patted + " just got patted on the " + bodypart + " by " + patter, patter + " patted " + patted + " on the " + bodypart + "."]
        botresponses = ["<:happy:708534449310138379>", "hehe", "aw, you're cute :3"]
        if pat == ctx.author:
            await ctx.send("You pat yourself on the " + bodypart + ".")
        else:
            await ctx.send(choice(responses))
            if str(pat.id) == "721092139953684580":
                await ctx.send(choice(botresponses))

    @commands.command(name="nom", help="Give someone a good nom >:3")
    async def nom(self, ctx, nom: discord.User=""):
        nommer = str(ctx.author.mention)
        try:
            nommed = "<@" + str(nom.id) + ">"
        except:
            await ctx.send("You can't just nom thin air! (Unless you're nomming a ghost?)")
            return
        responses = [nommed + " just got nommed by " + nommer, nommer + " nommed " + nommed, nommer + " ate " + nommed]
        selfresponses = ["You eat yourself and create a black hole. Thanks a lot.", "You chew on your own finger. Why...?", "Uh..."]
        botresponses = ["mmmph!", "nmmmmmmmph!", "hmmmnnnnn!!"]
        if nom == ctx.author:
            await ctx.send(choice(selfresponses))
        else:
            if str(nom.id) == "721092139953684580":
                await ctx.send(choice(responses))
                await ctx.send(choice(botresponses))
            else:
                Actions.isNomming = True
                Actions.nomSuccess = False
                stupidchannel = await ctx.guild.create_text_channel("nom-command-stupidity")
                await stupidchannel.set_permissions(read_messages=False)
                NoNomSense = await ctx.send(f"{nommer} is trying to eat you, {nommed}! Quick, react to get away!")
                await NoNomSense.add_reaction("👄")
                for _ in range(5):
                    sleep(1)
                    await stupidchannel.send("The command doesn't work without this message for some stupid reason.")
                    if self.isNomming == False:
                        break
                if self.isNomming == True:
                    self.isNomming = False
                    self.nomSuccess = True
                await NoNomSense.delete()
                if self.nomSuccess == True:
                    await ctx.send(choice(responses))
                else:
                    await ctx.send(nommed + " got away!")
                await stupidchannel.delete()

    @commands.command(name="tickle", help="Tickle tickle tickle... >:D")
    async def tickle(self, ctx, tickle: discord.User=""):
        tickler = str(ctx.author.mention)
        try:
            tickled = "<@" + str(tickle.id) + ">"
        except:
            await ctx.send("You can't just tickle thin air! (Unless you're tickling a ghost?)")
            return
        responses = [tickled + " just got tickled by " + tickler, tickler + " tickled " + tickled]
        selfresponses = ["You try to tickle yourself, but your body reflexively flinches away.", "You tickle yourself, and you burst out laughing the moment your finger touches that sweet spot of ticklishness..", "You try to tickle yourself, but nothing happens."]
        botresponses = ["hahahahahahahaha", "eeeeeehahahahaha", "aaaaaahahahahahaahaSTAHPhahahaha"]
        if tickle == ctx.author:
            await ctx.send(choice(selfresponses))
        else:
            await ctx.send(choice(responses))
            if str(tickle.id) == "721092139953684580":
                await ctx.send(choice(botresponses))

    @commands.command(name="kiss", help="Give somebody a kiss~ :kissing_heart:")
    async def kiss(self, ctx, kiss: discord.User=""):
        kisser = str(ctx.author.mention)
        try:
            kissed = "<@" + str(kiss.id) + ">"
        except:
            await ctx.send("You can't just hug thin air! (Unless you're kissing a ghost?)")
            return
        responses = [kissed + " just got kissed by " + kisser, kisser + " kissed " + kissed, kisser + " gave a kiss to " + kissed, kisser + " gave " + kissed + " a kiss"]
        selfresponses = ["You... Huh... How does this work...?", "You kiss your reflection in the mirror.", "You kiss the back of your own hand."]
        botresponses = ["aww!", "<:happy:708534449310138379>", "*gasp*"]
        if kiss == ctx.author:
            await ctx.send(choice(selfresponses))
        else:
            await ctx.send(choice(responses))
            if str(kiss.id) == "721092139953684580":
                await ctx.send(choice(botresponses))

def setup(client):
    client.add_cog(Actions(client))