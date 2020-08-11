import discord
from discord.ext import commands
from random import choice, randint
from os import listdir
from time import sleep

class oddcommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.isNomming = True
        self.nomSuccess = False
        self.formatChars = "*`~|"
        self.cyan = 32639
    name = "odd commands"
    name_typable = "oddcommands"
    description = "Commands that didn't quite fit anywhere else."
    description_long = description[:-1] + ", or that I didn't *want* to fit anywhere else."

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.emoji == "👄":
            if user.id != 721092139953684580:
                if self.isNomming == True:
                    self.isNomming = False
                    self.nomSuccess = False

    @commands.command(name = "nom", help = "Eat someone > :3", usage = " < username or nickname or @mention > ")
    async def nom(self, ctx, *, nom: discord.Member = None):
        nommer = ctx.author.display_name
        for char in self.formatChars:
            nommer = nommer.replace(
                char,
                "\\" + char
            )
        try:
            nommed = nom.display_name
            for char in self.formatChars:
                nommed = nommed.replace(
                    char,
                    "\\" + char
                )
        except:
            await ctx.send(
                "You can't just nom thin air! (Unless you're nomming a ghost?)"
            )
            return
        responses = [
            nommed + " just got nommed by " + nommer,
            nommer + " nommed " + nommed
        ]
        selfresponses = [
            "You eat yourself and create a black hole. Thanks a lot.",
            "You chew on your own finger. Why...?",
            "Uh... what?"
        ]
        botresponses = [
            "mmmph!",
            "nmmmmmmmph!",
            "hmmmnnnnn!!"
        ]
        embed = discord.Embed(
            title = choice(
                responses
            ),
            color = self.cyan
        ).set_image(
            url = f"""https://supertux20.github.io/Pengaelic-Bot/images/gifs/nom/{
                randint(
                    1,
                    len(
                        listdir(
                            '../Pengaelic-Bot/images/gifs/nom'
                        )
                    ) - 1
                )
            }.gif"""
        )
        if nom == ctx.author:
            await ctx.send(
                choice(
                    selfresponses
                )
            )
        else:
            if str(nom.id) == "721092139953684580":
                await ctx.send(
                    embed = embed
                )
                await ctx.send(
                    choice(
                        botresponses
                    )
                )
            else:
                self.isNomming = True
                self.nomSuccess = False
                stupidchannel = await ctx.guild.create_text_channel(
                    name = "nom-command-stupidity",
                    overwrites = {
                        ctx.guild.default_role: discord.PermissionOverwrite(
                            read_messages = False
                        ),
                        ctx.guild.me: discord.PermissionOverwrite(
                            read_messages = True
                        )
                    }
                )
                NoNomSense = await ctx.send(
                    f"""{
                        nommer
                    } is trying to eat you, {
                        nommed
                    }! Quick, click on the reaction to get away!"""
                )
                await NoNomSense.add_reaction(
                    "👄"
                )
                for _ in range(10):
                    sleep(
                        1
                    )
                    await stupidchannel.send(
                        "The command doesn't work without this message for some stupid reason."
                    )
                    if self.isNomming == False:
                        break
                if self.isNomming == True:
                    self.isNomming = False
                    self.nomSuccess = True
                await NoNomSense.delete()
                if self.nomSuccess == True:
                    await ctx.send(
                        embed = embed
                    )
                else:
                    await ctx.send(
                        f"""{
                            nommed
                        } got away!"""
                    )
                await stupidchannel.delete()

    @nom.error
    async def error(self, ctx, error):
        if "Member" in str(error) and "not found" in str(error):
            await ctx.send("Invalid user specified!")
        else:
            await ctx.send(f"""Unhandled error occurred:
        {
            error
        }
If my developer (<@!686984544930365440>) is not here, please tell him what the error is so that he can add handling or fix the issue!""")

def setup(client):
    client.add_cog(
        oddcommands(
            client
        )
    )