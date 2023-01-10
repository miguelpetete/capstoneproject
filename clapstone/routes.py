from flask import render_template
from flask import Blueprint

routes = Blueprint("routes", __name__)


@routes.route("/")
@routes.route("/home")
def home():
    return render_template("home.html")
