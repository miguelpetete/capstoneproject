from flask import Blueprint

admins = Blueprint("admins", __name__)


@admins.route("/sign-in", methods=["GET", "POST"])
def login():
    ...
