from app import app
from werkzeug.security import generate_password_hash, check_password_hash
from app import auth, db
from .models import Values, Principles, Base
from flask import Flask, jsonify, abort, request, make_response

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