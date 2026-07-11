from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import User, CompanyProfile, PlacementDrive

drive = Blueprint("drive", __name__)


@drive.post("/")
@jwt_required()
def create_drive():
    try:
        user = User.query.get(int(get_jwt_identity()))

        if not user or user.role != "company":
            return jsonify({"error": "Unauthorized"}), 403

        company = CompanyProfile.query.filter_by(user_id=user.id).first()

        data = request.get_json() or {}

        required = [
            "title",
            "description",
            "package",
            "location",
            "deadline",
            "eligibility",
        ]

        if not all(data.get(field) for field in required):
            return jsonify({"error": "Missing required fields"}), 400

        drive_obj = PlacementDrive(
            company_id=company.id,
            title=data["title"],
            description=data["description"],
            package=data["package"],
            location=data["location"],
            deadline=datetime.strptime(
                data["deadline"], "%Y-%m-%d"
            ).date(),
            eligibility=data["eligibility"],
        )

        db.session.add(drive_obj)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Placement drive created successfully",
                    "drive_id": drive_obj.id,
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@drive.get("/")
@jwt_required()
def get_drives():

    try:

        user = User.query.get(int(get_jwt_identity()))

        if user.role != "company":
            return jsonify({"error": "Unauthorized"}), 403

        company = CompanyProfile.query.filter_by(user_id=user.id).first()

        drives = PlacementDrive.query.filter_by(
            company_id=company.id
        ).all()

        result = []

        for d in drives:
            result.append(
                {
                    "id": d.id,
                    "title": d.title,
                    "package": d.package,
                    "location": d.location,
                    "deadline": d.deadline,
                    "eligibility": d.eligibility,
                }
            )

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@drive.get("/<int:drive_id>")
@jwt_required()
def get_drive(drive_id):

    try:

        user = User.query.get(int(get_jwt_identity()))

        if user.role != "company":
            return jsonify({"error": "Unauthorized"}), 403

        company = CompanyProfile.query.filter_by(user_id=user.id).first()

        d = PlacementDrive.query.filter_by(
            id=drive_id,
            company_id=company.id,
        ).first()

        if not d:
            return jsonify({"error": "Drive not found"}), 404

        return jsonify(
            {
                "id": d.id,
                "title": d.title,
                "description": d.description,
                "package": d.package,
                "location": d.location,
                "deadline": d.deadline,
                "eligibility": d.eligibility,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@drive.put("/<int:drive_id>")
@jwt_required()
def update_drive(drive_id):

    try:

        user = User.query.get(int(get_jwt_identity()))

        if user.role != "company":
            return jsonify({"error": "Unauthorized"}), 403

        company = CompanyProfile.query.filter_by(user_id=user.id).first()

        drive_obj = PlacementDrive.query.filter_by(
            id=drive_id,
            company_id=company.id,
        ).first()

        if not drive_obj:
            return jsonify({"error": "Drive not found"}), 404

        data = request.get_json() or {}

        drive_obj.title = data.get("title", drive_obj.title)
        drive_obj.description = data.get(
            "description",
            drive_obj.description,
        )
        drive_obj.package = data.get("package", drive_obj.package)
        drive_obj.location = data.get("location", drive_obj.location)
        drive_obj.eligibility = data.get(
            "eligibility",
            drive_obj.eligibility,
        )

        if data.get("deadline"):
            drive_obj.deadline = datetime.strptime(
                data["deadline"], "%Y-%m-%d"
            ).date()

        db.session.commit()

        return jsonify(
            {
                "message": "Drive updated successfully"
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@drive.delete("/<int:drive_id>")
@jwt_required()
def delete_drive(drive_id):

    try:

        user = User.query.get(int(get_jwt_identity()))

        if user.role != "company":
            return jsonify({"error": "Unauthorized"}), 403

        company = CompanyProfile.query.filter_by(user_id=user.id).first()

        drive_obj = PlacementDrive.query.filter_by(
            id=drive_id,
            company_id=company.id,
        ).first()

        if not drive_obj:
            return jsonify({"error": "Drive not found"}), 404

        db.session.delete(drive_obj)
        db.session.commit()

        return jsonify(
            {
                "message": "Drive deleted successfully"
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
