from flask_jwt_extended import jwt_required
from . import auth
from .authentication import login, refresh, register, logout

@auth.route("/login", methods=["GET", "POST"])
def login_():
    return login()


@auth.route("/register", methods=["GET", "POST"])
def register_():
    return register()

@auth.route("/logout", methods=["GET", "POST"])
def logout_():
    return logout()

@auth.route("/refresh", methods=["GET", "POST"])
@jwt_required(refresh=True)
def refresh_():
    return refresh()