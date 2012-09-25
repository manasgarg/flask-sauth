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

Step 3: Take a look at the template files in the source (for reference) and add
similar files to your templates/auth folder.
