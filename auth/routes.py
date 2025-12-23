from . import auth
from .authentication import login, register

@auth.route("/login", methods=["GET", "POST"])
def login_():
    return login()


@auth.route("/register", methods=["GET", "POST"])
def register_():
    return register()

