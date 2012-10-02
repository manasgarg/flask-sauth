#!/usr/bin/env python

from datetime import datetime
from wtforms import Form, TextField, PasswordField, HiddenField, ValidationError
from wtforms import validators as v

from models import User, authenticate

class RegistrationForm( Form):
    name = TextField( validators=[v.DataRequired(), v.Length(max=256)])
    email = TextField( validators=[v.DataRequired(), v.Length(max=256), v.Email()])
    password = PasswordField( validators=[v.DataRequired(), v.Length(max=256)])
    next = HiddenField()

    def validate_email( form, field):
        email = field.data.lower().strip()
        if( User.objects(email=email).count()):
            raise ValidationError( "Hey! This email is already registered with us. Did you forget your password?")

    def save( self):
        user = User.create_user( self.name.data, self.email.data, self.password.data, email_verified=True)
        user.save()

        return user

class LoginForm( Form):
    email = TextField(u"Email Address", validators=[v.DataRequired()])
    password = PasswordField( validators=[v.DataRequired()])
    next = HiddenField()

    def validate_email( self, field):
        if( not  User.objects( email=field.data).count()):
            raise ValidationError( "This email address is not registered.")
        
    def validate_password( self, field):
        self.user_cache = authenticate(email=self.email.data, password=field.data)
        if self.user_cache is None:
            raise ValidationError("Please enter correct information. Note that password is case-sensitive.")
        elif not self.user_cache.is_email_activated:
            raise ValidationError("This account is inactive.")


class ResetPasswordForm(Form):
    email = TextField(u"Email Address", validators=[v.DataRequired()])

    def validate_email( self, field):
        email = field.data.lower().strip()

        if( User.objects.filter( email=email).count() == 0):
            raise ValidationError( "This email address is not registered with us.")

        return True

class NewPasswordForm( Form):
    password1 = PasswordField( "Please enter your password", validators=[v.DataRequired()])
    password2 = PasswordField( "Please re-enter your password", validators=[v.DataRequired()])

    def validate_password2( self, field):
        password1 = self.password1.data
        password2 = self.password2.data
        if( password1 != password2):
            raise ValidationError( "The passwords don't match.")

class ChangePasswordForm( Form):
    password = PasswordField( "Current Password", validators=[v.DataRequired()])
    password1 = PasswordField( "New Password", validators=[v.DataRequired()])
    password2 = PasswordField( "Re-enter New Password", validators=[v.DataRequired()])

    def __init__( self, *args, **kwargs):
        super( ChangePasswordForm, self).__init__( *args, **kwargs)

    def validate_password( self, field):
        from flask_login import current_user

        user_cache = authenticate(email=current_user.email, password=field.data)
        if( not user_cache):
            raise ValidationError( "The current password that you entered is wrong.")

    def validate_password2( self, field):
        password1 = self.password1.data
        password2 = self.password2.data
        if( password1 != password2):
            raise ValidationError( "The passwords don't match.")
