from models import User

from flask.ext.script import Command, Option

class AddUser( Command):
    """Adds a user to the database."""

    option_list = (
        Option( "--name", "-n", dest="name", help="User's name"),
        Option( "--email", "-e", dest="email", help="User's email"),
        Option( "--password", "-p", dest="password", help="User's password"),
    )

    def run( self, name, email, password):
        email = email.lower().strip()
        if( User.objects(email=email).count()):
            print "This email address already exists."
            return

        user = User.create_user( name, email, password)
        print "Created user with slug", user.slug

class AddRole( Command):
    """Adds a role to a user"""

    option_list = (
        Option( "--email", "-e", dest="email", help="User's email"),
        Option( "--role", "-r", dest="role", help="Role to add"),
    )

    def run( self, email, role):
        email = email.lower().strip()
        user = User.objects( email=email).first()
        if( not user):
            print "This email address does not exist."
            return

        user.add_role( role)
        user.save()

class RemoveRole( Command):
    """Removes a role from a user"""

    option_list = (
        Option( "--email", "-e", dest="email", help="User's email"),
        Option( "--role", "-r", dest="role", help="Role to remove"),
    )

    def run( self, email, role):
        email = email.lower().strip()
        user = User.objects( email=email).first()
        if( not user):
            print "This email address does not exist."
            return

        user.remove_role( role)
        user.save()

class ShowRoles( Command):
    """Shows the roles a user has"""

    option_list = (
        Option( "--email", "-e", dest="email", help="User's email"),
    )

    def run( self, email):
        email = email.lower().strip()
        user = User.objects( email=email).first()
        if( not user):
            print "This email address does not exist."
            return

        if( user.roles):
            print "User's roles are:", ' '.join( user.roles)
        else:
            print "No roles found for the user."

class ShowUsers( Command):
    """Show the list of users"""

    def run( self):
        print "Total Users:", User.objects().count()

        for u in User.objects().order_by( "date_joined"):
            print "%s, %s" % (u.email, u.name)

def add_commands( manager):
    manager.add_command( 'user_add', AddUser())
    manager.add_command( 'user_add_role', AddRole())
    manager.add_command( 'user_remove_role', RemoveRole())
    manager.add_command( 'user_show_roles', ShowRoles())
    manager.add_command( 'user_showall', ShowUsers())
