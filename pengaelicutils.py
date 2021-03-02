import sqlite3
from time import time


def stopwatch(intime):
    value = time() - intime
    h = (((value)/24)/60)
    hours = int(h)
    m = (h - hours)*24
    minutes = int(m)
    s = (m - minutes)*60
    seconds = int(s)
    if len(str(hours)) == 1:
        hours = f"0{hours}"
    if len(str(minutes)) == 1:
        minutes = f"0{minutes}"
    if len(str(seconds)) == 1:
        seconds = f"0{seconds}"
    return f"{hours}:{minutes}:{seconds}"


def options(guild):
    conn = sqlite3.connect("config.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    rows = cur.execute("SELECT * from options").fetchall()
    conn.commit()
    conn.close()
    currentserver = [
        server
        for server in [
            dict(ix)
            for ix in rows
        ]
        if server["id"] == guild
    ][0]
    currentserver.pop("id")
    for value in currentserver:
        currentserver[value] = bool(currentserver[value])
    return dict(sorted(currentserver.items()))


def list2str(inlist: list, mode: int = 0):
    outstr = str(inlist)[1:-1].replace("'", "").replace("\\n", "")
    if mode == 0:
        pass  # leave commas alone
    elif mode == 1:
        outstr = outstr.replace(", ", " ")  # remove commas
    elif mode == 2:
        outstr = outstr.replace(", ", "\n")  # replace commas with newlines
    return outstr


def remove_duplicates(inlist: list):
    return list(dict.fromkeys(inlist))
