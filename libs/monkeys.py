# The Infinite Monkey Generator.
# To run it, use 'import monkeys', and call 'monkeys.generate()'.
# To change what letters are in the alphabet, set the variable 'monkeys.alphabet' to some array of letters, numbers, or symbols.
# If you use a keyword that contains symbols that aren't on the 'alphabet' array, the generator will run forever.
# Try to avoid that, if possible.
# This module serves no practical purpose, it's just for fun.
# Enjoy ¯\_(ツ)_/¯

from random import randint
from time import time


def stopwatch(value):
    value_d = (((value/365)/24)/60)
    days = int(value_d)

    value_h = (value_d - days)*365
    hours = int(value_h)

    value_m = (value_h - hours)*24
    minutes = int(value_m)

    value_s = (value_m - minutes)*60
    seconds = int(value_s)

    return str(hours) + ":" + str(minutes) + ":" + str(seconds)


async def generate(word, alphabet: list = "abcdefghijklmnopqrstuvwxyz"):
    starttime = time()
    text = ""
    success = True
    while text.find(word) == -1:
        letter = alphabet[randint(0, len(alphabet) - 1)]
        text = text + letter
        if stopwatch(time()-starttime) == "0:1:0":
            success = False
            break
    endtime = time()
    cutoff = ""
    textlen = len(text)
    if len(text) > 1000:
        text = f"...{text[-1000:]}"
        cutoff = " (last 1000 shown)"
    if success:
        return f'{text}\nKeyword "{word}" found after {textlen} characters{cutoff} in {stopwatch(endtime-starttime)}'
    else:
        return f'Could not find keyword "{word}" within one minute. :frowning:'
