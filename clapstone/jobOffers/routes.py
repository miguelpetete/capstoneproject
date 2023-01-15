# pylint: skip-file
import json
from flask import render_template, Blueprint, flash, request, redirect, url_for
from dotenv import dotenv_values
from clapstone.models.joboffer import JobOfferDB
from clapstone.models.forms import ApplicationForm
from clapstone.models.person import CandidateDB, Candidate
from clapstone import db, bcrypt
from clapstone.models.request import APIRepository
from clapstone.models.headers import RequestHeaders
from clapstone.models.rabbitmq import RabbitMQ
from flask_login import current_user, login_required
from clapstone.jobOffers.forms import JobOfferForm

joboffer = Blueprint("joboffer", __name__)
envs = dotenv_values(".env")
recruitee_key = envs["RECRUITEE_KEY"]
recruitee_company_id = envs["RECRUITEE_COMPANY_ID"]
repo = APIRepository("https://api.recruitee.com/c")
repo.add_to_base_url(recruitee_company_id)


@joboffer.route("/offer/<int:recruitee_id>", methods=["GET", "POST"])
def view_job(recruitee_id):
    offer = JobOfferDB.query.filter_by(recruitee_id=str(recruitee_id)).first()
    form = ApplicationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        candidatedb = CandidateDB(
            email=form.email.data,
            password=hashed_password,
            name=form.name.data,
            first_surname=form.first_surname.data,
            second_surname=form.second_surname.data,
        )
        candidate = Candidate(
            name=form.name.data,
            first_surname=form.first_surname.data,
            second_surname=form.second_surname.data,
            email=form.email.data,
            username="None",
        )
        db.session.add(candidatedb)
        db.session.commit()
        headers = RequestHeaders(str(recruitee_key))
        headers.add_content_type()
        rabbit = RabbitMQ()
        rabbit.channel.queue_declare(queue="candidates")
        message = {
            "candidate": candidate.get_dictionary(),
            "offers": [str(recruitee_id)],
        }
        rabbit.send_message("", "candidates", json.dumps(message))
        page = request.args.get("page", 1, type=int)
        joboffers = JobOfferDB.query.paginate(page=page, per_page=3)
        flash("You have succesfully apply for this job", "success")
        return render_template("home.html", joboffers=joboffers)
    return render_template("joboffer.html", joboffer=offer, form=form)
