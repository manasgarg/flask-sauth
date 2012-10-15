#!/usr/bin/env python

from mongoengine import *

from flask_login import UserMixin

from random import randint, random
import time, hashlib, datetime

from utils import get_hexdigest

class BaseUser(Document, UserMixin):
    email = StringField( unique=True)
    name = StringField()
    password = StringField(max_length=128)

    date_joined = DateTimeField(default=datetime.datetime.now)
    email_activation_key = StringField(default="")
    is_email_activated = BooleanField( default=True)
    password_reset_token = StringField()

    roles = ListField( StringField(), default=[])

    meta = {"abstract": True}

    @property
    def first_name( self):
        return name.split(" ")[0]

    @property
    def last_name( self):
        arr = name.split(" ")
        if( len( arr) > 1):
            return ' '.join( arr[1:])
        else:
            return ''

    @property
    def short_name( self):
        if( re.search( "[A-Z]", self.name[1])): return self.name

        arr = self.name.split( " ")
        if( len( arr) == 1): return self.name

        s = ""
        for i in range( 0, len( arr)-1):
            s += arr[i][0]
        s += " " + arr[-1]

        return s.strip()

    def has_role( self, role):
        if( not self.roles or role not in self.roles):
            return False

        return True

    def add_role( self, role):
        if( role not in self.roles):
            self.roles.append( role)

    def remove_role( self, role):
        if( role in self.roles):
            self.roles.remove( role)

    def mark_email_for_activation( self):
        self.is_email_activated = False
        self.email_activation_key = sha_constructor(str(time.time()) + str( randint( 1,1000000))).hexdigest()

    def set_password(self, raw_password):
        """Sets the user's password - always use this rather than directly
        assigning to :attr:`~mongoengine.django.auth.User.password` as the
        password is hashed before storage.
        """
        algo = 'sha1'
        salt = get_hexdigest(algo, str(random()), str(random()))[:5]
        hash = get_hexdigest(algo, salt, raw_password)
        self.password = '%s$%s$%s' % (algo, salt, hash)
        self.save()
        return self

    def check_password(self, raw_password):
        """Checks the user's password against a provided password - always use
        this rather than directly comparing to
        :attr:`~mongoengine.django.auth.User.password` as the password is
        hashed before storage.
        """
        algo, salt, hash = self.password.split('$')
        return hash == get_hexdigest(algo, salt, raw_password)

    def generate_password_reset_token( self):
        self.password_reset_token = hashlib.sha1( "%s-%s-%d" % ( str(self.id), str(time.time()), random())).hexdigest()
        self.save()
        return self.password_reset_token

    @classmethod
    def create_user(cls, name, email, password, email_verified=True):
        """Create (and save) a new user with the given password and
        email address.
        """
        now = datetime.datetime.utcnow()
        
        # Normalize the address by lowercasing the domain part of the email
        # address.
        try:
            email_name, domain_part = email.strip().split('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name.lower(), domain_part.lower()])
            
        user = User(name=name, email=email, date_joined=now)

        if( not password):
            password = generate_password()
        user.set_password(password)

        if( not email_verified):
            user.mark_email_for_activation()
        else:
            user.is_email_activated = True

        user.save()

        return user

def authenticate(email=None, password=None):
    user = User.objects(email=email).first()
    if user:
        if password and user.check_password(password):
            return user
    return None

from werkzeug import import_string, LocalProxy
from flask import current_app
User = LocalProxy( lambda: import_string( current_app.config.get( "USER_MODEL_CLASS", "flask_mongo_auth.default_models.User")))
