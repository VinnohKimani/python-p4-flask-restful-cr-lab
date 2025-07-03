#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return make_response(jsonify([plant.to_dict() for plant in plants]), 200)

    def post(self):
        data = request.get_json()
        try:
            new_plant = Plant(
                name=data.get("name"), image=data.get("image"), price=data.get("price")
            )
            db.session.add(new_plant)
            db.session.commit()
            return make_response(jsonify(new_plant.to_dict()), 201)
        except Exception as e:
            return make_response({"error": str(e)}, 400)


class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return make_response({"error": "Plant not found"}, 404)
        return make_response(jsonify(plant.to_dict()), 200)


api.add_resource(Plants, "/plants")
api.add_resource(PlantByID, "/plants/<int:id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
