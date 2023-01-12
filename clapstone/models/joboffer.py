# pylint:skip-file
from clapstone import db


class JobOffer:
    def __init__(
        self, title, city, description=None, requirements=None, postal_code=None
    ):
        self.title = title
        self.kind = "job"
        self.postal_code = postal_code
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

    def create_payload(self):
        self.payload = {
            "offer": {
                "kind": self.kind,
                "remote": False,
                "title": self.title,
                "description": self.description,
                "requirements": self.requirements,
                "postal_code": self.postal_code,
                "city": self.city,
                "state_code": self.state_code,
                "country_code": self.country_code,
                "status": "published",
            }
        }


class JobOfferDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recruitee_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    kind = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    requirements = db.Column(db.String(500), nullable=False)
    postal_code = db.Column(db.String(5), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    state_code = db.Column(db.String(3), nullable=False)
    country_code = db.Column(db.String(2), nullable=False)
