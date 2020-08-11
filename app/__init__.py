from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from config import Config
from sqlalchemy import event  # type: ignore
from flask_httpauth import HTTPBasicAuth  # type: ignore

app: Flask = Flask(__name__)
app.config.from_object(Config)
db: SQLAlchemy = SQLAlchemy(app)
auth: HTTPBasicAuth = HTTPBasicAuth()

from .models import Values, Principles, Base
from app import api

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@event.listens_for(Values.__table__, "after_create")
def insert_initial_values(*args, **kwargs):
    db.session.add(
        Values(data="Individuals and interactions over processes and tools.")
    )
    db.session.add(Values(data="Working software over comprehensive documentation."))
    db.session.add(Values(data="Customer collaboration over contract negotiation."))
    db.session.add(Values(data="Responding to change over following a plan."))
    db.session.commit()


@event.listens_for(Principles.__table__, "after_create")
def insert_initial_principles(*args, **kwargs):
    db.session.add(
        Principles(
            data="Our highest priority is to satisfy the customer through early and continuous delivery of valuable software."
        )
    )
    db.session.add(
        Principles(
            data="Welcome changing requirements, even late in development. Agile processes harness change for the customer’s competitive advantage."
        )
    )
    db.session.add(
        Principles(
            data="Deliver working software frequently, from a couple of weeks to a couple of months, with a preference to the shorter timescale."
        )
    )
    db.session.add(
        Principles(
            data="Business people and developers must work together daily throughout the project."
        )
    )
    db.session.add(
        Principles(
            data="Build projects around motivated individuals. Give them the environment and support they need, and trust them to get the job done."
        )
    )
    db.session.add(
        Principles(
            data="The most efficient and effective method of conveying information to and within a development team is face-to-face conversation."
        )
    )
    db.session.add(
        Principles(data="Working software is the primary measure of progress.")
    )
    db.session.add(
        Principles(
            data="Agile processes promote sustainable development. The sponsors, developers, and users should be able to maintain a constant pace indefinitely."
        )
    )
    db.session.add(
        Principles(
            data="Continuous attention to technical excellence and good design enhances agility."
        )
    )
    db.session.add(
        Principles(
            data="Simplicity–the art of maximizing the amount of work not done–is essential."
        )
    )
    db.session.add(
        Principles(
            data="The best architectures, requirements, and designs emerge from self-organizing teams."
        )
    )
    db.session.add(
        Principles(
            data="At regular intervals, the team reflects on how to become more effective, then tunes and adjusts its behavior accordingly."
        )
    )
    db.session.commit()


if __name__ == "__main__":
    Base.metadata.create_all(bind=db.engine)
    app.run(debug=True)
