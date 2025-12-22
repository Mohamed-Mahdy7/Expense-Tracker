from . import auth
from .authentication import login

@auth.route("/login", methods=["GET", "POST"])
def login_():
    return login()