from flask import Blueprint, render_template, abort, request, session, g, redirect, flash, current_app
from jinja2 import TemplateNotFound
from flask_login import current_user, login_user, logout_user, login_required

from forms import RegistrationForm, LoginForm, ResetPasswordForm, NewPasswordForm, ChangePasswordForm
from models import User

from djmail import send_mail
import urlparse, hashlib

from blinker import signal

signal_user_registered = signal( 'user-registered')

auth_views = Blueprint('auth_views', __name__,
                        template_folder='templates')

@auth_views.route('/accounts/login', methods=["GET", "POST"])
def login():
    next_url = request.form.get( "next", None) or request.args.get( "next", None) or session.get("next_url", None)

    if( request.method == "GET" and not next_url and request.referrer):
        urldata = urlparse.urlparse( request.referrer)
        if( urldata.path.find("/accounts") != 0):
            host = request.headers.get("HOST", "")
            if( host and urldata.netloc.find(host) > -1):
                next_url = request.referrer

    if( not next_url): next_url = "/"

    session["next_url"] = next_url

    def do_redirect():
        del( session["next_url"])
        return redirect( next_url)

    if( current_user.is_authenticated()):
        return do_redirect()

    if request.method == "POST":
        is_login = False
        if( request.form.has_key( "name")):
            register_form = RegistrationForm( request.form)
            login_form = LoginForm()
            form = register_form
        else:
            is_login = True
            login_form = LoginForm( request.form)
            register_form = RegistrationForm()
            form = login_form

        if( form.validate()):
            if( not is_login):
                user = form.save()
                signal_user_registered.send("flask-satuh", user=user)

                login_user( user)
                return do_redirect()
            else:
                login_user( form.user_cache)
                return do_redirect()
        else:
            kwargs = {"login_form": login_form, "register_form": register_form, "is_login": is_login}
            return render_template( "auth/login.html", **kwargs)
    else:
        if( request.args.get("l", "") == "1"):
            is_login = True

        login_form = LoginForm()
        register_form = RegistrationForm()

    kwargs = locals()
    return render_template("auth/login.html", **kwargs)

@auth_views.route("/accounts/logout")
def logout():
    logout_user()
    return redirect( "/")

@auth_views.route("/accounts/password/reset", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        form = ResetPasswordForm( request.form)
        if( form.validate()):
            user = User.objects.get( email=form.email.data)
            password_reset_token = user.generate_password_reset_token()

            host = request.headers["HOST"]
            link = "http://%s/accounts/password/reset/%s" % (host, password_reset_token)

            mesg = "Hi %s,\n\nSomeone (probably you) requested for a password reset at %s. Please visit the following link if you wish to reset your password:\n\n%s\n\nHave a good day!" % (user.name, host, link)
            send_mail( "[%s] Reset Password" % host, mesg, current_app.config["SERVER_EMAIL"], [user.email], fail_silently=False)

            flash( "Sent you a mail to reset the password. Do remember to check your spam folder as well.", "success")
    else:
        form = ResetPasswordForm()
    return render_template( "auth/reset_password.html", **locals())

@auth_views.route("/accounts/password/reset/<password_reset_token>", methods=["GET", "POST"])
def do_reset_password( password_reset_token):
    user = User.objects( password_reset_token=password_reset_token).first()
    if( not user):
        flash( "Invalid request parameters. Please try resetting again.", "error")
        return redirect( "/accounts/password/reset")

    if request.method == "POST":
        form = NewPasswordForm( request.form)
        if( form.validate()):
            user.set_password( form.password1.data)
            login_user( user)
            flash( "Your password was changed successfully.", "success")
            return redirect( "/")

    form = NewPasswordForm()
    return render_template( "auth/new_password.html", **locals())

@auth_views.route("/accounts/password/change", methods=["GET", "POST"])
@login_required
def change_password():
    if( request.method == "POST"):
        form = ChangePasswordForm( request.form)
        if( form.validate()):
            current_user.set_password( form.password1.data)
            flash( "Your password was changed successfully.", "success")
            return redirect( "/")
    else:
        form = ChangePasswordForm()
    return render_template( "auth/change_password.html", **locals())
