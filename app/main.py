from flask import Flask, request, Response, jsonify
from pydantic import ValidationError
from app.schemas import UserRequest
from app.recommender_registry import get_generator
from .Generators import inference_generator
import json
from app.db_bill import (
    get_dynamic_recommendations,
    get_user_company,
    get_display_config,
    save_company_config
)
from app.utils.schema_mapper import generate_schema_from_config
from marshmallow import Schema, fields, post_load, ValidationError as MarshmallowValidationError
from datetime import datetime

app = Flask(__name__)

# === /recommendations [POST] ===
@app.route("/recommendations", methods=["POST"])
def get_recommendations():
    try:
        data = UserRequest(**request.json)
        generator = get_generator(data.algorithm)

        if not generator:
            return Response(
                json.dumps({"error": f"Unknown algorithm '{data.algorithm}'"}),
                status=400,
                mimetype="application/json"
            )

        recommendations = generator(data.user_id, data.sport)
        return Response(
            json.dumps([rec.dict() for rec in recommendations], indent=2),
            mimetype="application/json"
        )

    except ValidationError as e:
        return Response(
            json.dumps({"error": e.errors()}),
            status=400,
            mimetype="application/json"
        )

    except ValueError as ve:
        return Response(
            json.dumps({"error": str(ve)}),
            status=400,
            mimetype="application/json"
        )

# === /recommendations [GET] ===
@app.route("/recommendations", methods=["GET"])
def fetch_dynamic_recommendations():
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    try:
        company = get_user_company(user_id)
        if not company:
            return jsonify({"error": "User not found in any company"}), 404

        config = get_display_config(company)
        recommendation_conf = config.get("recommendation", {})
        fields_config = recommendation_conf.get("fields", {})

        schema_cls = generate_schema_from_config(fields_config)
        schema = schema_cls()

        recs = get_dynamic_recommendations(user_id)
        formatted = schema.dump(recs, many=True)

        json_data = json.dumps(formatted, indent=2)
        return Response(json_data, mimetype="application/json")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === /config [GET] ===
@app.route("/config", methods=["GET"])
def get_static_config():
    config = {
        "user": {
            "fields": ["user_id", "name", "gender", "currency"],
            "labels": {
                "user_id": "ID",
                "name": "Full Name",
                "gender": "Gender",
                "currency": "Currency"
            }
        },
        "event": {
            "fields": ["event_id", "sport", "league", "participants"],
            "labels": {
                "event_id": "Event",
                "sport": "Sport Type",
                "league": "League",
                "participants": "Teams"
            }
        },
        "recommendation": {
            "fields": ["event_id", "user_id", "home_team", "away_team", "odds_home", "odds_away", "stake"],
            "labels": {
                "event_id": "Match ID",
                "user_id": "User",
                "home_team": "Home",
                "away_team": "Away",
                "odds_home": "Home Odds",
                "odds_away": "Away Odds",
                "stake": "Suggested Stake"
            }
        }
    }
    return jsonify(config)

# === /config [POST] ===
class ConfigSchema(Schema):
    recommender_type = fields.String(required=True)
    recommendation_schema = fields.Dict(required=True)
    timestamp = fields.String(dump_only=True)

    @post_load
    def add_timestamp(self, data, **kwargs):
        data["timestamp"] = datetime.utcnow().isoformat()
        return data

@app.route("/config", methods=["POST"])
def set_config():
    casino_id = request.headers.get("Casino-ID")
    if not casino_id:
        return jsonify({"error": "Casino-ID header is required"}), 400

    try:
        casino_id = int(casino_id)
    except ValueError:
        return jsonify({"error": "Casino-ID must be an integer"}), 400

    config_data = request.get_json()
    if not config_data:
        return jsonify({"error": "JSON body is required"}), 400

    try:
        config_schema = ConfigSchema()
        validated = config_schema.load(config_data)
    except MarshmallowValidationError as err:
        return jsonify({"error": err.messages}), 400

    try:
        save_company_config(casino_id, validated)
    except Exception as e:
        return jsonify({"error": f"Failed to save config: {str(e)}"}), 500

    return jsonify({
        "message": "Configuration saved successfully to DB",
        "config": validated
    }), 200
