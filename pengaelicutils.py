# -*- coding: utf-8 -*-

from time import time
from tinydb import TinyDB


def stopwatch(start_time: time):
    elapsed = time() - start_time
    m = elapsed/60
    minutes = int(m)
    s = (m - minutes)*60
    seconds = int(s)
    ms = int(round(s - seconds, 3)*1000)
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


def list2str(inlist: list, mode: int = 0):
    # if mode == 0: leave commas and spaces unaffected
    # if mode == 1: remove all separation
    # if mode == 2: remove commas, leaving spaces behind
    # if mode == 3: replace commas and spaces with newlines
    if mode == 1:
        outstr = "".join(inlist)
    else:
        # remove single quotes and newlines
        outstr = str(inlist)[1:-1].replace("'", "").replace("\\n", "")
        if mode == 2:
            outstr = outstr.replace(", ", " ")
        elif mode == 3:
            outstr = outstr.replace(", ", "\n")
    return outstr


def remove_duplicates(inlist: list):
    return list(dict.fromkeys(inlist))


def newops():
    return {
        "channels": {
            channel_id: None
            for channel_id in [
                "suggestionsChannel",
                "welcomeChannel"
            ]
        },
        "lists": {
            "censorList": []
        },
        "messages": {
            "welcomeMessage": "Welcome to SERVER, USER!",
            "goodbyeMessage": "See you later, USER."
        },
        "roles": {
            role_id: None
            for role_id in [
                "customRoleLock",
                "modRole",
                "muteRole",
            ]
        },
        "toggles": {
            toggle_bool: False
            for toggle_bool in [
                "censor",
                "dadJokes",
                "deadChat",
                "jsonMenus",
                "lockCustomRoles",
                "rickRoulette",
                "suggestions",
                "welcome"
            ]
        },
        "customRoles": {}
    }


def getops(guild: str, category: str = None, option: str = None):
    db = TinyDB("config.json")
    options = db.all()[0]
    if option == None:
        options = dict(sorted(options[str(guild)].items()))
        if options["lists"]["censorList"] == []:
            options["lists"]["censorList"] = None
        else:
            options["lists"]["censorList"] = list2str(
                options["lists"]["censorList"])
    else:
        options = options[str(guild)][category][option]
    return options


def updop(guild: str, category: str, option: str, value):
    db = TinyDB("config.json")
    options = db.all()[0][str(guild)]
    options[category][option] = value
    db.update({guild: options})
