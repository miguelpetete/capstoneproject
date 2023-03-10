from flask import render_template, Blueprint, request
from clapstone.models.joboffer import JobOfferDB

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    joboffers = JobOfferDB.query.paginate(page=page, per_page=3)
    return render_template("home.html", joboffers=joboffers)
