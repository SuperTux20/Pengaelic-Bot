#!/usr/bin/python3.9
# -*- coding: utf-8 -*-

from dotenv import load_dotenv as dotenv
from json import loads
from os import getenv as env
from subprocess import check_output
from time import time
from tinydb import TinyDB, Query


class Stopwatch:
    start_time = 0

    def start(self):
        self.start_time = time()

    def end(self) -> str:
        try:
            elapsed = time() - self.start_time
            m = elapsed / 60
            minutes = int(m)
            s = (m - minutes) * 60
            seconds = int(s)
            ms = int(round(s - seconds, 3) * 1000)
            if len(str(minutes)) == 1:
                minutes = f"0{minutes}"
            if len(str(seconds)) == 1:
                seconds = f"0{seconds}"
            if minutes == "00":
                if seconds == "00":
                    return f"{ms}ms"
                return f"{int(seconds)}.{ms} seconds"
            else:
                return f"{minutes}:{seconds}"
        except AttributeError:
            return "The stopwatch was never started."

    # specific to the infinite monkey generator
    def monkeywatch(self, start: time) -> str:
        elapsed = time() - start
        m = elapsed / 60
        minutes = int(m)
        s = (m - minutes) * 60
        seconds = int(s)
        ms = int(round(s - seconds, 3) * 1000)
        if len(str(minutes)) == 1:
            minutes = f"0{minutes}"
        if len(str(seconds)) == 1:
            seconds = f"0{seconds}"
        if minutes == "00":
            if seconds == "00":
                return f"{ms}ms"
            return f"{int(seconds)}.{ms} seconds"
        else:
            return f"{minutes}:{seconds}"


# load all developer user IDs
class Developers:
    dotenv(".env")
    everyone = loads(env("DEVELOPER_IDS"))

    def check(self, user, dev=None) -> bool:
        if dev == None:
            if user.id in list(Developers.everyone.values()):  # check if user is a dev
                return True
            else:
                return False
        else:
            if user.id == Developers.everyone[dev]:  # check if user is specific dev
                return True
            else:
                return False

    def get(self, dev=None):
        if dev == None:
            return Developers.everyone  # get all devs
        else:
            return Developers.everyone[dev.lower()]  # get specific dev


def list2str(inlist: list, mode: int = 0, _and: bool = False) -> str:
    # if mode == 0: proper sentence formatting (minus period)
    # if mode == 1: remove all separation
    # if mode == 2: remove commas, leaving spaces behind
    # if mode == 3: replace commas and spaces with newlines
    if mode == 1:
        outstr = "".join(inlist)
    else:
        if _and and len(inlist) > 1:
            inlist.append(inlist[-1])
            inlist[-2] = "and"
        outstr = (
            str(inlist)[1:-1]  # cut off opening and closing brackets
            .replace("'", "")
            .replace("\\n", "")  # remove single quotes and newlines
        )
        if _and:
            if len(inlist) == 3:
                outstr = "".join(outstr.split(","))  # remove all commas
            else:
                outstr = "".join(outstr.rsplit(",", 1))  # remove the last comma
        if mode == 2:
            outstr = outstr.replace(", ", " ")
        elif mode == 3:
            outstr = outstr.replace(", ", "\n")
    return outstr


def unhandling(error, tux_in_server) -> str:
    error = str(error)
    author = tux_in_server[1]
    tux_in_server = tux_in_server[0]
    output = (
        "<:winxp_critical_error:869760946816553020>Unhandled error occurred:\n"
        + f"> {error}\n"
    )
    if tux_in_server:
        if author == Developers.get(None, "tux"):
            output = "<:winxp_critical_error:869760946816553020>"
            tux_msg = error
        else:
            tux_msg = "Pinging <@!686984544930365440> (my developer) so he can see this error."
    else:
        tux_msg = "Run `p!bugreport` <error> to send Tux (my developer) a message, replacing <error> with the copy/pasted error message and some details about what was happening shortly before the error appeared (such as what command caused the error)"
    return output + tux_msg


def newops() -> dict:
    return {
        "channels": {
            channel_id + "Channel": None
            for channel_id in ["drama", "suggestions", "welcome"]
        },
        "lists": {"censorList": []},
        "messages": {
            "welcomeMessage": "Welcome to SERVER, USER!",
            "goodbyeMessage": "See you later, USER.",
        },
        "roles": {
            role_id + "Role": None
            for role_id in [
                "botCommander",
                "customRoleLock",
                "drama",
                "mute",
            ]
        },
        "toggles": {
            toggle: False
            for toggle in [
                "atSomeone",
                "censor",
                "dadJokes",
                "deadChat",
                "jsonMenus",
                "lockCustomRoles",
                "rickRoulette",
                "suggestions",
                "welcome",
            ]
        },
        "customRoles": {},
    }


def getops(guild: str, category: str = None, option: str = None) -> dict:
    db = TinyDB("config.json")
    server = Query()
    if option == None:
        options = dict(sorted(db.search(server.guildID == guild)[0].items()))
        options.pop("guildName")
        options.pop("guildID")
        if options["lists"]["censorList"] == []:
            options["lists"]["censorList"] = None
        else:
            options["lists"]["censorList"] = options["lists"]["censorList"].tostr()
    else:
        options = db.search(server.guildID == guild)[0][category][option]
    return options


def updop(guild: str, category: str, option: str, value):
    db = TinyDB("config.json")
    server = Query()
    options = db.search(server.guildID == guild)[0][category]
    options[option] = value
    db.update({category: options}, server.guildID == guild)


def eldritch_syllables() -> list:
    vowels = list("aeiouy")
    consonants = list("bcdfghjklmnpqrstvwxz")
    syllables = []
    for v in vowels:
        syllables.append(v)
        for c in consonants:
            syllables.append(c)
            for v2 in vowels:
                for c2 in consonants:
                    syllables.append(c + v)
                    syllables.append(v + c)
                    syllables.append(c + v + v)
                    syllables.append(v + c + v)
                    syllables.append(v + v + c)
                    syllables.append(v + c + c)
                    syllables.append(c + v + c)
                    syllables.append(c + c + v)
                    syllables.append(c + v + v2)
                    syllables.append(v2 + c + v)
                    syllables.append(v + v2 + c)
                    syllables.append(v + c + c2)
                    syllables.append(c2 + v + c)
                    syllables.append(c + c2 + v)
        syllables.append(v2 + v)
        syllables.append(v + v2)
    return list(set(syllables))


syllables = [
    "a",
    "ae",
    "ag",
    "ah",
    "al",
    "am",
    "an",
    "art",
    "as",
    "au",
    "av",
    "ayn",
    "az",
    "be",
    "bi",
    "bo",
    "bor",
    "burn",
    "by",
    "ca",
    "cai",
    "car",
    "cat",
    "ce",
    "cei",
    "cer",
    "cha",
    "ci",
    "co",
    "cu",
    "da",
    "dal",
    "dam",
    "dan",
    "dap",
    "dar",
    "das",
    "del",
    "dem",
    "den",
    "dep",
    "der",
    "des",
    "di",
    "dil",
    "dim",
    "din",
    "dip",
    "dir",
    "dis",
    "do",
    "dol",
    "dom",
    "don",
    "dop",
    "dor",
    "dos",
    "dy",
    "dyl",
    "e",
    "el",
    "em",
    "en",
    "ev",
    "ex",
    "fi",
    "fin",
    "finn",
    "fly",
    "fu",
    "ga",
    "go",
    "gor",
    "gy",
    "he",
    "hy",
    "i",
    "ig",
    "il",
    "in",
    "is",
    "iss",
    "ja",
    "ji",
    "jo",
    "jor",
    "ka",
    "kes",
    "kev",
    "kla",
    "ko",
    "lan",
    "lar",
    "ler",
    "li",
    "lo",
    "lu",
    "ly",
    "ma",
    "mar",
    "me",
    "mel",
    "mi",
    "mo",
    "mol",
    "mu",
    "mus",
    "na",
    "nar",
    "ne",
    "nei",
    "no",
    "nor",
    "nos",
    "o",
    "ob",
    "ok",
    "ol",
    "om",
    "on",
    "or",
    "os",
    "pe",
    "pen",
    "per",
    "pu",
    "ra",
    "ral",
    "ran",
    "ras",
    "re",
    "res",
    "rez",
    "ri",
    "rin",
    "rob",
    "ry",
    "sa",
    "sac",
    "sam",
    "san",
    "sans",
    "ser",
    "sey",
    "sha",
    "sky",
    "son",
    "st",
    "str",
    "ta",
    "tam",
    "tay",
    "ter",
    "tha",
    "than",
    "tif",
    "ti",
    "tin",
    "to",
    "tor",
    "tur",
    "u",
    "um",
    "un",
    "ur",
    "va",
    "vac",
    "van",
    "ve",
    "vi",
    "wa",
    "wyn",
    "yu",
    "za",
    "zal",
    "ze",
    "zi",
    "zil",
    "zo",
    "zu",
]

hangman_words = {
    "pengaelic": "The Pengaelics are a humanoid species that live in the Caretaker's Garden. They're doomed to go extinct, even more so after their planet was destroyed, but that won't stop them from trying to live the best lives they can.",
    "endron": "The Endrons are a curious humanoid species, they can perform extraordinary feats of magic, and it is said that they are descended from long-lost gods. Their magic is directly tied to the amount of mass on their bodies, converting the mass into magic energy like a sort of fuel.",
    "symbiote": "A peculiar thing about the Endrons... Inside their stomachs, there is no acid, instead there are little sentient slimes that they have built a symbiotic relationship with. They can tell the difference between friend and food, though there is influence from their hosts as to what they should digest or not.",
    "xikolarian": "The Xikolarians are a violent warrior species with an ungodly amount of arms. The more arms you have, the higher you are in society. They have created incredible technology and have gone so far as to create vast mechanical fortresses to protect against invaders.",
    "kragonian": "Not much is known about the Kragonians. They are all identical at birth, differentiating each other with colored paint.",
    "giblof": "The Giblof are a colossal humanoid species, though you could say that they're mostly gentle giants. They have an unusual internal anatomy, most notably two parallel stomachs on either side of the torso.",
    "pengaelus": "Pengaelus was a small planet, only a little bigger than Earth's moon. A species known as the Pengaelics came to exist there, almost entirely by accident! In 1995, the Pioneer 11 lost communication with Earth because it was pulled into some freak warp accident and transported an entire lightyear away in mere moments. It crashed on Pengaelus, and the traces of human DNA jumpstarted evolution at an astronomical rate.",
    "endrolus": "Endrolus is an average-sized planet where the Endrons call home. There's beautiful scenery everywhere, all under a pale violet sky.",
    "catamunara": "Catamunara is a slightly smaller planet near Endrolus, but there's a secret about it. The planet actually used to be an Endron, who was also named Catamunara. And now people live on her, collecting resources grown on the rich soil around her. Watch out for the subterranean ocean though, because it's alive.",
    "xikolara": "Xikolara is a huge planet where the Xikolarians reside. The Xikolarians inadvertently made the climate very harsh, so there aren't many small towns on it anymore, the population is concentrated into a handful of huge cities. The surface of the planet is covered in sprawling machinery created by the Xikolarians, which are what affected the climate in the first place, creating lots of greenhouse gases.",
    "kragon": "Kragon is a fairly average planet. Like its inhabitants, not much is known about it.",
    "giblona": "Giblona is a planet that was unfortunately lost to a great nuclear winter, and the Giblof have left to wander the galaxy in their Starcity. The gods are working to fix the planet, but it's taking a long time...",
    "garden": "Somewhere between the universes, there will almost always be a Garden hidden away somewhere. Usually they seem fairly ordinary compared to what you would see on any Class M planet like Earth, but sometimes they are very special, very special indeed.",
    "tree": "In every Garden, there is the Mother Tree. She holds the Garden together, fills it with magic, and makes sure it can heal itself.",
    "caretaker": "The Caretaker is the primary person you'll see tending to the Garden. A Caretaker usually has a tall, plump body and a beautiful face, and it is in her nature to be very motherly to any visitors she may have.",
    "starweaver": "The Starweaver was created with the omniverse, and she will die with it as she creates the next. She can create a silk not unlike a spider's, and she uses it to make sure the stars stay in a stable condition and weave new stars into existence.",
    "artist": "The Artist is one of the Starweaver's daughters, and she created everything other than the stars with her pencil. Whatever she draws, it comes into existence right in front of her.",
    "eraser": "The Eraser is the Starweaver's other daughter, and her job is to keep the Artist in check, keep the balance between creation and destruction.",
    "beloved": "The Beloved is the fertility goddess ruler of Endrolus. She embodies life and its creation, and she is truly beautiful.",
    "legendmaker": "The Legendmaker is the Beloved's brother, the god who guides lost souls to the Other Side. He wouldn't describe his job as particularly fun, but rather satisfying, knowing that the lost souls have found peace with his guidance.",
    "judge": "The Judge is the high balance goddess, making sure everything is as it should be, nothing too far above its opposite.",
    "resonant": "The Resonant is a young goddess, altering the thoughts and emotions of all who hear her music. She almost constantly emanates music from her body, which changes depending on her state of mind.",
}

regional_indicators = {
    "🇦": "a",
    "🇧": "b",
    "🇨": "c",
    "🇩": "d",
    "🇪": "e",
    "🇫": "f",
    "🇬": "g",
    "🇭": "h",
    "🇮": "i",
    "🇯": "j",
    "🇰": "k",
    "🇱": "l",
    "🇲": "m",
    "🇳": "n",
    "🇴": "o",
    "🇵": "p",
    "🇶": "q",
    "🇷": "r",
    "🇸": "s",
    "🇹": "t",
    "🇺": "u",
    "🇻": "v",
    "🇼": "w",
    "🇽": "x",
    "🇾": "y",
    "🇿": "z",
}

magic_responses = [
    [
        r"¯\\\_(ツ)\_/¯",
        ":(\nYour computer ran into a problem and needs to restart",
        "Answer is kinda hazy rn... Try again later",
        "Ask again later",
        "Better not tell you now",
        "Cannot predict now",
        r"Can't tell ¯\\\_(ツ)\_/¯",
        "Concentrate and ask again",
        "Concentrate harder and ask again",
        "Couldn't tell ya if I wanted to, pal",
        "idk lol",
        "I like to keep secrets",
        "I'm busy",
        "`panic: cannot mount volume /dev/disk-by-label/8-Ball-Responses`",
        "Probably shouldn't tell you now, lol",
        "Reply hazy... Try again",
        "The universe is weird sometimes... I can't find an answer",
        "Try again, but harder",
        "Try again later",
        "Why would you ask such a stupid question?",
    ],
    [
        "Don’t count on it",
        "Don’t count on it, buster",
        "Heck no",
        "I don't think so",
        "I don't think so, pal",
        "I doubt it",
        "LOL, no",
        "My reply is no",
        "My sources say no",
        "My sources say no. My sources are Wikipedia",
        "Not a chance",
        "Outlook is terrible. Get Thunderbird instead",
        "Outlook not so good",
        "Outlook not so good. Use Gmail instead",
        "Pfft, don’t count on it",
        'The law requires that I answer "no"',
        "Very doubtful",
        "Uh, no",
        ":thumbsdown:",
        ":x:",
    ],
    [
        "Absolutely",
        "Always",
        "Always and forever",
        "Certainly",
        "Definitely",
        "Definitively",
        "Doubtless",
        "I'd say so",
        "It is certain",
        "It is decidedly so",
        "I think so",
        "I would think so",
        "I'm pretty sure, yeah",
        "It is obvious",
        "Lookin' good",
        "Maybe...",
        "mhm",
        "Most likely",
        "Obviously",
        "Oh yeah",
    ],
    [
        "Outlook good",
        "Pfft, yeah!",
        "Probably lol",
        "Probably",
        "Seems like it",
        "Signs point to yes",
        "Sure",
        "Sure, why not?",
        "Totally",
        "Uh... yeah!",
        "Without a doubt",
        "ye",
        "Yeah",
        "Yeah, sure",
        "Yeah, totally!",
        "Yep",
        "Yes",
        "You may rely on it",
        ":thumbsup:",
        ":white_check_mark:",
    ],
]


def jsoncheck(guild: str) -> bool:
    return getops(guild, "toggles", "jsonMenus")


def tux_in_guild(ctx, client) -> list:
    return [
        bool(ctx.guild.get_member(client.get_user(Developers.get(None, "tux")).id)),
        ctx.author.id,
    ]


def shell(command) -> str:
    return check_output(command, shell=True).decode()[:-1]
