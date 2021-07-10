"""
Module for managing project
"""
from flask.cli import FlaskGroup

from app import app, db
cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    """
    Method for creating database
    :return:
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()
