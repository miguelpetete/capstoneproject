# pylint: skip-file
import click
from flask import Flask
from flask.cli import with_appcontext
from .models.person import RecruiterDB


@with_appcontext
@click.command("create")
@click.argument("creator_password")
@click.argument("name")
@click.argument("email")
@click.argument("admin_password")
def createadmin(creator_password, name, email, admin_password):
    from . import db

    if creator_password != "123abc":
        click.echo("Contraseña incorrecta")
    else:
        recruiter = RecruiterDB(
            email=email,
            password=admin_password,
            name=name,
        )
        db.session.add(recruiter)
        db.session.commit()
        click.echo("Admin added to database")
