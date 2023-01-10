# pylint:skip-file
from clapstone import db


class JobOffer:
    def __init__(self, title, city, description=None, requirements=None):
        self.title = title
        self.kind = "job"
        self.postal_code = "11111"
        self.city = city
        self.state_code = "MAD"
        self.country_code = "ES"
        self.id = None
        self.description = description
        self.requirements = requirements

    def add_id(self, identifier):
        self.id = identifier

    def add_description(self, description):
        self.description = description

    def add_requirements(self, requirements):
        self.requirements = requirements


class JobOfferDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    kind = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    requirements = db.Column(db.String(500), nullable=False)
    postal_code = db.Column(db.String(5), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    state_code = db.Column(db.String(3), nullable=False)
    country_code = db.Column(db.String(2), nullable=False)
