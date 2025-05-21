from flask import Flask, request, Response, jsonify
from pydantic import ValidationError
from app.schemas import UserRequest
from app.recommender_registry import get_generator
from .Generators import inference_generator
import json
import pandas as pd
from pathlib import Path
from app.db_bill import get_dynamic_recommendations


app = Flask(__name__)

DATA_DIR = Path("data")
SOURCES_DIR = DATA_DIR / "sources"

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

# GET Αίτημα
@app.route("/sync/<company>", methods=["GET"])
def sync_company_data(company):
    try:
        users_file = SOURCES_DIR / f"{company.lower()}_users.csv"
        coupons_file = SOURCES_DIR / f"{company.lower()}_coupons.csv"

        main_users_file = DATA_DIR / "users.csv"
        main_coupons_file = DATA_DIR / "coupons.csv"

        new_users = pd.read_csv(users_file)
        new_coupons = pd.read_csv(coupons_file, parse_dates=["timestamp"])

        new_coupons["sport"] = new_coupons["sport"].str.lower().str.strip()
        new_coupons["league"] = new_coupons["league"].str.lower().str.strip()

        existing_users = pd.read_csv(main_users_file)
        existing_coupons = pd.read_csv(main_coupons_file, parse_dates=["timestamp"])

        updated_users = pd.concat([existing_users, new_users]).drop_duplicates(subset="user_id")
        updated_coupons = pd.concat([existing_coupons, new_coupons]).drop_duplicates(subset="coupon_id")

        updated_users.to_csv(main_users_file, index=False)
        updated_coupons.to_csv(main_coupons_file, index=False)

        return jsonify({"message": f"Company '{company}' synchronized successfully!"})
    except FileNotFoundError:
        return jsonify({"error": f"No data found for company '{company}'"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/recommendations", methods=["GET"])
def fetch_dynamic_recommendations():
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    try:
        recs = get_dynamic_recommendations(user_id)
        return jsonify(recs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
