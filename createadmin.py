import click
from clapstone.models.person import RecruiterDB
from clapstone import db


@click.group()
def cli():
    pass


@click.command()
@click.argument("creator_password")
@click.argument("name")
@click.argument("email")
@click.argument("admin_password")
def createadmin(creator_password, name, email, admin_password):
    if creator_password != "123abc":
        click.echo("Contraseña incorrecta")
    else:
        recruiter = RecruiterDB(
            email=email,
            password=admin_password,
            name=name,
        )
        db.session.add(recruiter)  # pylint: disable=no-member
        db.session.commit()  # pylint: disable=no-member


cli.add_command(createadmin)

if __name__ == "__main__":
    cli()
