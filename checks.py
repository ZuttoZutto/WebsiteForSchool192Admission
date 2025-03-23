from flask_login import current_user, AnonymousUserMixin
from flask import current_app

def check_user_role():
    with current_app.app_context():
        if current_user.is_anonymous:
            print(0)
            return 0
        print(current_user.RoleId)
        return current_user.RoleId