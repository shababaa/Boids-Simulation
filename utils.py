from copy import deepcopy

def limit(vector, length):
    tmp = deepcopy(vector)
    if tmp.length() > length:
        tmp.normalize_ip()
        tmp *= length
    return tmp
