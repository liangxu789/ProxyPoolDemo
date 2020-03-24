import string
import random


def getRandomCode():
    return ''.join(random.sample(string.ascii_letters, 8))
