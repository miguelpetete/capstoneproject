# pylint: skip-file
from flask import Blueprint, render_template, flash
from dotenv import dotenv_values
from clapstone.admins.forms import AdminLoginForm
from clapstone.models.person import RecruiterDB
from clapstone import bcrypt, db
from clapstone.jobOffers.forms import JobOfferForm
from clapstone.models.joboffer import JobOffer, JobOfferDB
from clapstone.models.headers import RequestHeaders
from clapstone.models.request import APIRepository
from flask_login import login_user, current_user

admins = Blueprint("admins", __name__)
envs = dotenv_values(".env")
recruitee_key = envs["RECRUITEE_KEY"]
recruitee_company_id = envs["RECRUITEE_COMPANY_ID"]
repo = APIRepository("https://api.recruitee.com/c")
repo.add_to_base_url(recruitee_company_id)


@admins.route("/sign-in", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return render_template("admingui.html")
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = RecruiterDB.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin, remember=form.remember.data)
            return render_template("admingui.html")
    return render_template("adminlogin.html", form=form)


@admins.route("/createoffer", methods=["POST", "GET"])
def admin_create():
    form = JobOfferForm()
    if form.validate_on_submit():
        offer = JobOffer(
            title=form.title.data,
            city=form.city.data,
            description=form.description.data,
            requirements=form.requirements.data,
            postal_code=form.postal_code.data,
        )
        offer.create_payload()
        payload = offer.payload
        headers = RequestHeaders(str(recruitee_key))
        headers.add_content_type()
        response = repo.post("/offers", data=payload, headers=headers.headers)
        recruitee_id = response.json()["offer"]["id"]
        offer.add_id(recruitee_id)
        offerdb = JobOfferDB(
            recruitee_id=offer.id,
            title=offer.title,
            kind=offer.kind,
            description=offer.description,
            requirements=offer.requirements,
            postal_code=offer.postal_code,
            city=offer.city,
            state_code=offer.state_code,
            country_code=offer.country_code,
        )
        db.session.add(offerdb)
        db.session.commit()
        flash("Your offer has been created!", "success")
        return render_template("admingui.html")
    return render_template("admincreate.html", form=form)


@admins.route("/updateoffer", methods=["GET", "POST", "PATCH"])
def admin_update():

    return render_template("done.html")


@admins.route("/deleteoffer", methods=["DELETE"])
def admin_delete():
    return render_template("done.html")
