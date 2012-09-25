flask-sauth
===========

Complete user authentication code for flask & mongodb.

It builds upon the flask-login package to provide complete user login, logout,
password reset/change functionality.

Usage
=====

Step 1. Create a class that will represent a 'User' in your application. It
should extend flask_sauth.models.BaseUser class.

```
# auth/models.py

from flask_sauth.models import BaseUser

class User( BaseUser):
    ...
```

Step 2: In your application configuration, add "USER_MODEL_CLASS" and make it
point to the class path for your User class.

```
app.config["USER_MODEL_CLASS"] = "auth.models.User"
```

Step 3: During application initialization, reguster the flask_sauth blueprint.

```
from flask_sauth.views import auth_views

app.register_blueprint( auth_views)
```

Step 4: Take a look at the template files in the source (for reference) and add
similar files to your templates/auth folder.


User Management Commands
========================

To add user management commands to your flask-script manage.py, just add the
following code snippet (to manage.py):

```
import flask_sauth.commands

manager = Manager( app)

flask_sauth.commands.add_commands( manager)
```

This will add following commands to manage.py:

* add_user: for adding a user to the database.
* add_role: Add a role to a user.
* remove_role: Remove a role from a user.
* show_roles: Show the roles a user has.
* show_users: Show the list of users in the database.
