# pylint:skip-file
from clapstone import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_recruiter(email):
    return User.query.get(str(email))


class Person:
    def __init__(self, name, first_surname, second_surname, username=None):
        self.name = name
        self.first_surname = first_surname
        self.second_surname = second_surname
        self.username = username

    def get_full_name(self):
        return f"{self.name} {self.first_surname} {self.second_surname}"

    def get_username(self):
        return f"{self.username}"


class Recruiter(Person):
    def __init__(self, name, first_surname, second_surname, username, email, password):
        super().__init__(name, first_surname, second_surname, username)
        self.email = email
        self.password = password

    def get_full_name(self):
        return f"{self.name} {self.first_surname} {self.second_surname}"

    def get_username(self):
        return f"{self.username}"


class Candidate(Person):
    def __init__(
        self, name, first_surname, second_surname, username, email, password=None
    ):
        super().__init__(name, first_surname, second_surname, username)
        self.email = email
        self.password = password

    def get_full_name(self):
        return f"{self.name} {self.first_surname} {self.second_surname}"

    def get_username(self):
        return f"{self.username}"

    def create_payload(self, job_id):
        self.payload = {
            "candidate": {
                "name": self.name + self.first_surname + self.second_surname,
                "emails": [self.email],
            },
            "offers": [job_id],
        }

    def get_dictionary(self):
        d = {
            "name": self.name + self.first_surname + self.second_surname,
            "email": self.email,
        }
        return d


class RecruiterDB(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(50))
    first_surname = db.Column(db.String(50))
    second_surname = db.Column(db.String(50))
    username = db.Column(db.String(50))


class CandidateDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(60))
    name = db.Column(db.String(50), nullable=False)
    first_surname = db.Column(db.String(50), nullable=False)
    second_surname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50))
