import discord
from discord.ext import commands
from random import choice, randint
from json import load

class Games(commands.Cog):
    name = "games"
    description = "All sorts of fun stuff!"
    def __init__(self, client):
        self.client = client

    @commands.command(name="8ball", help="Ask the ball and receive wisdom... :eyes:", aliases=["magic8ball"], usage="[question]")
    async def _8ball(self, ctx, *, question=None):
        with open(rf"../pengaelicbot.data/configs/{ctx.guild.id}.json", "r") as optionsfile:
                allOptions = load(optionsfile)
        with open(rf"8ball/level_{allOptions['numbers']['rudeness']}.txt", "r") as responsefile:
            ballResponses = responsefile.read().split(", ")
        if question:
            await ctx.send(":8ball:" + choice(ballResponses))
        else:
            await ctx.send(":8ball:You didn't ask the 8-ball anything.")

    @commands.command(name="roll", help="Roll some dice!", aliases=["dice"], usage="[number of dice (1)] [number of sides (6)]")
    async def rollem(self, ctx, dice: int=1, sides: int=6):
        if dice == 0:
            await ctx.send(":game_die:You didn't roll any dice.")
        elif sides == 0:
            await ctx.send(":game_die:You rolled thin air.")
        elif dice < 0:
            await ctx.send(":game_die:You rolled NaN dice and got [REDACTED]")
        elif sides < 0:
            if dice == 1:
                await ctx.send(":game_die:You rolled a [ERROR]-sided die and got `DivideByZeroError`")
            if dice > 1:
                await ctx.sendf(f":game_die:You rolled {dice} `err`-sided dice and got [NULL]")
        else:
            sideList = []
            rollResults = []
            for side in range(sides):
                sideList.append(side + 1)
            for _ in range(dice):
                rollResults.append(sideList[randint(0, sideList[-1])-1])
            total = sum(rollResults)
            if dice > 1:
                response = f":game_die:You rolled {str(rollResults[:-1])[1:-1]}, and {rollResults[-1]}, totalling {total}"
            else:
                response = f":game_die:You rolled {total}"
            await ctx.send(response)

    @commands.command(name="flip", help="Flip some coins!", aliases=["coin"], usage="[number of coins (1)]")
    async def flipem(self, ctx, coins: int=1):
        results = []
        if coins == 1:
            await ctx.send(f":moneybag:You flipped a {choice(['head','tail'])}")
        elif coins == 0:
            await ctx.send(":moneybag:You flicked your thumb in the air.")
        elif coins == -1:
            await ctx.send(":moneybag:You flipped a [REDACTED]")
        elif coins < -1:
            await ctx.semd(":moneybag:You flipped NaN heads and [ERROR] tails.")
        else:
            if coins > 1000000:
                await ctx.send(f":moneybag:{coins} coins? That's just silly.")
            else:
                for _ in range(int(str(coins))):
                    result = randint(0,2)
                    if result == 2:
                        result = randint(0,2)
                        if result == 2:
                            result = randint(0,2)
                            if result == 2:
                                result = randint(0,2)
                                if result == 2:
                                    result = randint(0,2)
                                    if result == 2:
                                        result = randint(0,2)
                    results.append(result)
                if results.count(2) > 0:
                    if results.count(2) == 1:
                        await ctx.send(f":moneybag:You flipped {results.count(0)} heads and {results.count(1)} tails, and a coin even landed on its edge.")
                    else:
                        await ctx.send(f":moneybag:You flipped {results.count(0)} heads and {results.count(1)} tails, and {results.count(2)} coins landed on their edges.")
                else:
                    await ctx.send(f":moneybag:You flipped {results.count(0)} heads and {results.count(1)} tails.")

    @commands.command(name="draw", help="Draw some cards!", aliases=["card"], usage="[number of cards (1)] [replace cards in deck (no)]")
    async def drawem(self, ctx, cards: int=1, replaceCards: str="no", emoji: str="no"):
        suits = ["Diamonds", "Spades", "Hearts", "Clubs"]
        values = {1: 'Ace', 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 'Jack', 12: 'Queen', 13: 'King'}
        suits_emoji = [":diamonds:", ":spades:", ":hearts:", ":clubs:"]
        values_emoji = {1: ':regional_indicator_a:', 2: ':two:', 3: ':three:', 4: ':four:', 5: ':five:', 6: ':six:', 7: ':seven:', 8: ':eight:', 9: ':nine:', 10: ':keycap_ten:', 11: ':regional_indicator_j:', 12: ':regional_indicator_q:', 13: ':regional_indicator_k:'}
        allCards = []
        faces = []
        nums = []
        drawn = []
        if replaceCards == "no":
            for suit in range(int(len(suits)/1)):
                for value in values:
                    if emoji == "no":
                        if value == 10:
                            length = 2
                        elif value == 1:
                            length = 3
                        elif value == 11 or value == 13:
                            length = 4
                        elif value == 12:
                            length = 5
                        else:
                            length = 1
                        allCards.append(str(values[value]) + (" " * (6 - length) + "of ") + suits[suit])
                    else:
                        allCards.append(values_emoji[value] + suits_emoji[suit])
            if cards > 52:
                await ctx.send(":black_joker:You can't draw more than the entire deck!")
                return
            elif cards == 52:
                await ctx.send(":black_joker:You picked up the entire deck. What was the point of that?")
                return
            else:
                for _ in range(cards):
                    card = choice(allCards)
                    if emoji == "no":
                        if card[1] == "0" or card[1] == "1" or card[1] == "2" or card[1] == "3":
                            faces.append(card)
                        else:
                            nums.append(card)
                    else:
                        emojiname = card[1:-1].split("::")[0]
                        if emojiname == "regional_indicator_j" or emojiname == "regional_indicator_q" or emojiname == "regional_indicator_k":
                            faces.append(card)
                        else:
                            nums.append(card)
                    allCards.remove(card)
                drawn = faces + nums
        else:
            for _ in range(cards):
                if emoji == "no":
                    chosenValue = str(choice(list(values.values())))
                    card = str(chosenValue + (" " * (6 - len(chosenValue)) + "of ") + choice(suits))
                    if card[1] == "0" or card[1] == "1" or card[1] == "2" or card[1] == "3":
                        faces.append(card)
                    else:
                        nums.append(card)
                else:
                    card = choice(list(values_emoji.values())) + choice(suits_emoji)
                    emojiname = card[1:-1].split("::")[0]
                    if emojiname == "regional_indicator_j" or emojiname == "regional_indicator_q" or emojiname == "regional_indicator_k":
                        faces.append(card)
                    else:
                        nums.append(card)
            drawn = faces + nums
        if cards == 1:
            while "  " in drawn[0]:
                drawn[0] = drawn[0].replace("  "," ")
            await ctx.send(":black_joker:You drew " + drawn[0])
        else:
            if emoji == "no":
                await ctx.send(":black_joker:You drew...```" + str(drawn)[1:-1].replace("'","").replace(", ","\n") + "```")
            else:
                await ctx.send(":black_joker:You drew...\n" + str(drawn)[1:-1].replace("'","").replace(", ","\n"))

    @commands.command(name="pop", help="Get a sheet of bubble wrap! Click to pop.", aliases=["bubblewrap", "bubble", "wrap", "bubbles"], usage="[width of sheet (5)] [height of sheet (5)]")
    async def summonsheet(self, ctx, width: int=5, height: int=5):
        if width == 1 and height == 1:
            await ctx.send(r"""```
 ____   ___  ____
|  _ \ / _ \|  _ \
| |_) | | | | |_) |
|  __/| |_| |  __/
|_|    \___/|_|
```""")
        else:
            sheet = ""
            for _ in range(height):
                row = ""
                for _ in range(width):
                    if width < 5 and height < 5:
                        if width == 2 and height == 2:
                            row = row + "||:regional_indicator_p: :regional_indicator_o: :regional_indicator_p:||"
                        else:
                            row = row + "||POP||"
                    else:
                        row = row + "||pop||"
                sheet = sheet + row + "\n"
            await ctx.send(sheet)

    @_8ball.error
    @rollem.error
    @flipem.error
    @drawem.error
    @summonsheet.error
    async def error(self, ctx, error):
        await ctx.send("Sorry, you specified numbers that were too large. Try again with smaller numbers!")

def setup(client):
    client.add_cog(Games(client))