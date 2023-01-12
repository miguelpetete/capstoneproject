from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email


class ApplicationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=50)])
    first_surname = StringField(
        "First Surname", validators=[DataRequired(), Length(max=50)]
    )
    second_surname = StringField("Second Surname", validators=[Length(max=50)])
    email = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Apply for job")

    def validate_email(self, email):
        # candidate = Candidate.query.filter_by(email=email.data).first()
        # if candidate:
        # raise ValidationError(
        # "You have apply with this email before. You will receive the info soon."
        # )
        pass
