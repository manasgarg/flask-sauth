import hashlib
import random

def get_hexdigest(algorithm, salt, raw_password):
    if algorithm == 'md5':
        return hashlib.md5(salt + raw_password).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(salt + raw_password).hexdigest()
    raise ValueError('Got unknown password algorithm type in password')

righthand = '23456qwertasdfgzxcvbQWERTASDFGZXCVB'
lefthand = '789yuiophjknmYUIPHJKLNM'
allchars = righthand + lefthand
def generate_random_password(length=8):
    chars = []
    for i in range(0,length):
        chars.append( random.choice(allchars))

    return ''.join( chars)
