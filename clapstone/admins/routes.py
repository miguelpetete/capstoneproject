# pylint: skip-file
from flask import Blueprint, render_template, flash, request, redirect, url_for
from dotenv import dotenv_values
from clapstone.admins.forms import AdminLoginForm
from clapstone.models.person import RecruiterDB
from clapstone import bcrypt, db
from clapstone.jobOffers.forms import JobOfferForm
from clapstone.models.joboffer import JobOffer, JobOfferDB
from clapstone.models.headers import RequestHeaders
from clapstone.models.request import APIRepository
from flask_login import login_user, current_user, login_required, logout_user

admins = Blueprint("admins", __name__)
envs = dotenv_values(".env")
recruitee_key = envs["RECRUITEE_KEY"]
recruitee_company_id = envs["RECRUITEE_COMPANY_ID"]
repo = APIRepository("https://api.recruitee.com/c")
repo.add_to_base_url(recruitee_company_id)


@admins.route("/sign-in", methods=["GET", "POST"])
def login():
    page = request.args.get("page", 1, type=int)
    joboffers = JobOfferDB.query.paginate(page=page, per_page=3)
    if current_user.is_authenticated:
        return render_template("home.html", joboffers=joboffers)
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = RecruiterDB.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin, remember=form.remember.data)
            return render_template("home.html", joboffers=joboffers)
    return render_template("adminlogin.html", form=form)


@admins.route("/createoffer", methods=["POST", "GET"])
@login_required
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
        page = request.args.get("page", 1, type=int)
        joboffers = JobOfferDB.query.paginate(page=page, per_page=3)
        return render_template("home.html", joboffers=joboffers)
    return render_template("admincreate.html", form=form)


@admins.route("/updateoffer/<int:recruitee_id>", methods=["GET", "POST"])
@login_required
def admin_update(recruitee_id):
    offer = JobOfferDB.query.filter_by(recruitee_id=str(recruitee_id)).first()
    page = request.args.get("page", 1, type=int)
    joboffers = JobOfferDB.query.paginate(page=page, per_page=3)
    form = JobOfferForm()
    if form.validate_on_submit():
        offer.title = form.title.data
        offer.description = form.description.data
        offer.requirements = form.requirements.data
        offer.postal_code = form.postal_code.data
        offer.city = form.city.data
        db.session.commit()
        offerREC = JobOffer(
            title=form.title.data,
            city=form.city.data,
            description=form.description.data,
            requirements=form.requirements.data,
            postal_code=form.postal_code.data,
        )
        offerREC.create_payload()
        payload = offerREC.payload
        headers = RequestHeaders(str(recruitee_key))
        headers.add_content_type()
        response = repo.patch(
            f"/offers/{recruitee_id}", data=payload, headers=headers.headers
        )
        flash("Job offer has been updated", "success")
        return render_template("home.html", joboffers=joboffers)
    elif request.method == "GET":
        form.title.data = offer.title
        form.description.data = offer.description
        form.requirements.data = offer.requirements
        form.postal_code.data = offer.postal_code
        form.city.data = offer.city
    return render_template("admincreate.html", form=form)


@admins.route("/deleteoffer/<int:recruitee_id>", methods=["GET", "POST", "DELETE"])
@login_required
def admin_delete(recruitee_id):
    offer = JobOfferDB.query.filter_by(recruitee_id=str(recruitee_id)).first()
    db.session.delete(offer)
    db.session.commit()
    headers = RequestHeaders(str(recruitee_key))
    response = repo.delete(f"/offers/{recruitee_id}", headers=headers.headers)
    flash("Your offer has been deleted!", "danger")
    page = request.args.get("page", 1, type=int)
    joboffers = JobOfferDB.query.paginate(page=page, per_page=3)
    return render_template("home.html", joboffers=joboffers)


@admins.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))
