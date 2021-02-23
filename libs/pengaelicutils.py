import discord
import sqlite3


def get_options(guild):
    conn = sqlite3.connect("data/config.db")
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
    return currentserver
