# pylint: skip-file
class Config:
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://postgres:secret@localhost:5432/clapstone"
    )
    SECRET_KEY = "5791628bb0b13ce0c676dfde280ba245"
