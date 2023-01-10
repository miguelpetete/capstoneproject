from flask import Blueprint, render_template
from clapstone.admins.forms import AdminLoginForm


admins = Blueprint("admins", __name__)


@admins.route("/sign-in", methods=["GET", "POST"])
def login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        return render_template("done.html")
    return render_template("adminlogin.html", form=form)
