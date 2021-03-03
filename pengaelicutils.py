import sqlite3
from time import time


def stopwatch(intime):
    outtime = time() - intime
    y = outtime/365/24/60/60
    years = int(y)
    d = (y - years)*365
    days = int(d)
    h = (d - days)*24
    hours = int(h)
    m = (h - hours)*60
    minutes = int(m)
    s = (m - minutes)*60
    seconds = int(s)
    ms = int(round(s - seconds, 3)*1000)
    if len(str(hours)) == 1:
        hours = f"0{hours}"
    if len(str(minutes)) == 1:
        minutes = f"0{minutes}"
    if len(str(seconds)) == 1:
        seconds = f"0{seconds}"
    if years == 0:
        if days == 0:
            if hours == "00":
                if minutes == "00":
                    if seconds == "00":
                        return f"{ms}ms"
                    return f"{int(seconds)}.{ms} seconds"
                return f"{minutes}:{seconds}"
            return f"{hours}:{minutes}:{seconds}"
        return f"{days}d {hours}:{minutes}:{seconds}"
    else:
        return f"{years}y {days}d {hours}:{minutes}:{seconds}"


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
    if mode == 1:
        # remove all separation
        outstr = "".join(inlist)
    else:
        outstr = str(inlist)[1:-1].replace("'", "").replace("\\n", "")
        if mode == 2:
            # remove commas, leaving spaces behind
            outstr = outstr.replace(", ", " ")
        elif mode == 3:
            # replace commas and spaces with newlines
            outstr = outstr.replace(", ", "\n")
    # mode = 0 leaves commas and spaces unaffected
    return outstr


def remove_duplicates(inlist: list):
    return list(dict.fromkeys(inlist))
