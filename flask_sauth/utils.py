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


def user_has_role( func, role):
    """ decorator: Ensures the user is an administrator, usually required to allow to view admin pages """
    def method_to_check_admin ( *args, **kw ):
        from flask_login import current_user, logout_user
        from flask import flash, redirect
        if current_user.is_authenticated() and current_user.has_role( role):
            return func (*args, **kw)
        else:
            flash( "You do not have necessary permissions.", "error")
            return redirect ( "/")

    return method_to_check_admin

def user_is_staff( func):
    return user_has_role( func, "staff")
