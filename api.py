from flask import Flask, jsonify, abort, request, make_response
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from config import Config
from sqlalchemy import event  # type: ignore
from flask_httpauth import HTTPBasicAuth  # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash

app: Flask = Flask(__name__)
app.config.from_object(Config)
db: SQLAlchemy = SQLAlchemy(app)
auth: HTTPBasicAuth = HTTPBasicAuth()

from models import Values, Principles, Base

users = {"admin": generate_password_hash("password")}

permissions = {"admin": ["view", "add", "change", "delete"]}


@auth.verify_password
def verify_password(username: str, password: str):
    if username in users and check_password_hash(users.get(username), password):
        return username


@auth.error_handler
def unauthorized():
    return make_response(jsonify({"error": "Unauthorized access"}), 401)


@app.route("/api/v1.0/values", methods=["GET"])
@auth.login_required
def get_values():
    if "view" not in permissions[auth.username()]:
        return make_response(jsonify({"error": "Unauthorized access"}), 401)

    values = []
    models = db.session.query(Values)
    for value in models:
        values.append({"id": value.id, "data": value.data})
    return jsonify({"values": values})


@app.route("/api/v1.0/principles", methods=["GET"])
@auth.login_required
def get_principles():
    if "view" not in permissions[auth.username()]:
        return make_response(jsonify({"error": "Unauthorized access"}), 401)

    principles = []
    models = db.session.query(Principles)
    for principle in models:
        principles.append({"id": principle.id, "data": principle.data})
    return jsonify({"principles": principles})


@app.route("/api/v1.0/values/<int:value_id>", methods=["GET"])
@auth.login_required
def get_value(value_id: int):
    if "view" not in permissions[auth.username()]:
        return make_response(jsonify({"error": "Unauthorized access"}), 401)

    value = db.session.query(Values).get(value_id)
    if value is None:
        abort(404)
    return jsonify({"id": value.id, "data": value.data})


@app.route("/api/v1.0/principles/<int:principle_id>", methods=["GET"])
@auth.login_required
def get_principle(principle_id: int):
    if "view" not in permissions[auth.username()]:
        return make_response(jsonify({"error": "Unauthorized access"}), 401)

    principle = db.session.query(Principles).get(principle_id)
    if principle is None:
        abort(404)
    return jsonify({"id": principle.id, "data": principle.data})


@app.route("/api/v1.0/values", methods=["POST"])
@auth.login_required
def create_value():
    if "add" not in permissions[auth.username()]:
        return make_response(jsonify({"error": "Unauthorized access"}), 401)

    if not request.json or not "data" in request.json:
        abort(404)
    value = Values()
    value.data = request.json["data"]
    db.session.add(value)
    db.session.commit()
    return jsonify({"id": value.id, "data": value.data})


@app.route("/api/v1.0/principles", methods=["POST"])
@auth.login_required
def create_principle():
    if "add" not in permissions[auth.username()]:
        return make_response(jsonify({"error": "Unauthorized access"}), 401)

    if not request.json or not "data" in request.json:
        abort(404)
    principle = Principles()
    principle.data = request.json["data"]
    db.session.add(principle)
    db.session.commit()
    return jsonify({"id": principle.id, "data": principle.data})


@app.route("/api/v1.0/values/<int:value_id>", methods=["PUT"])
@auth.login_required
def update_value(value_id: int):
    if "change" not in permissions[auth.username()]:
        return make_response(jsonify({"error": "Unauthorized access"}), 401)

    value = db.session.query(Values).get(value_id)
    if value is None:
        abort(404)
    if not request.json:
        abort(404)
    if "data" not in request.json and type(request.json["data"]) != str:
        abort(404)
    value.data = request.json["data"]
    db.session.commit()
    return jsonify({"id": value.id, "data": value.data})


@app.route("/api/v1.0/principles/<int:principle_id>", methods=["PUT"])
@auth.login_required
def update_principle(principle_id: int):
    if "change" not in permissions[auth.username()]:
        return make_response(jsonify({"error": "Unauthorized access"}), 401)

    principle = db.session.query(Principles).get(principle_id)
    if principle is None:
        abort(404)
    if not request.json:
        abort(404)
    if "data" not in request.json and type(request.json["data"]) != str:
        abort(404)
    principle.data = request.json["data"]
    db.session.commit()
    return jsonify({"id": principle.id, "data": principle.data})


@app.route("/api/v1.0/values/<int:value_id>", methods=["DELETE"])
@auth.login_required
def delete_value(value_id: int):
    if "delete" not in permissions[auth.username()]:
        return make_response(jsonify({"error": "Unauthorized access"}), 401)

    value = db.session.query(Values).get(value_id)
    if value is None:
        abort(404)
    db.session.delete(value)
    db.session.commit()
    return jsonify({"Result": True})


@app.route("/api/v1.0/principles/<int:principle_id>", methods=["DELETE"])
@auth.login_required
def delete_principle(principle_id):
    if "delete" not in permissions[auth.username()]:
        return make_response(jsonify({"error": "Unauthorized access"}), 401)

    principle = db.session.query(Principles).get(principle_id)
    if principle is None:
        abort(404)
    db.session.delete(principle)
    db.session.commit()
    return jsonify({"Result": True})


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
