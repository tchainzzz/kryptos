
import string

def __init__(self):
    pass

def shift(msg, key=0):
    char_list = list(msg.lower())
    for i in range(len(msg)):
        try:
            target_index = (string.ascii_lowercase.index(char_list[i]) + key) % len(string.ascii_lowercase)
            char_list[i] = string.ascii_lowercase[target_index]
        except ValueError:
            pass
    return ''.join(char_list)

def deshift(msg, key=0):
    return shift(msg, -1 * key)

def brute_force_deshift(msg):
    plaintexts = []
    for i in range(len(string.ascii_lowercase)):
        plaintexts.append(shift(msg, i))
        print("Key", "-", string.ascii_lowercase[i] + ":", plaintexts[i])
    return plaintexts
