from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from utils.decorators import company_required

from extensions import db
from models import CompanyProfile, PlacementDrive

drive = Blueprint("drive", __name__)


@drive.post("")
@jwt_required()
@company_required
def create_drive(user):
    try:
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
        try:
            package = float(data["package"])
        except (ValueError, TypeError):
            return jsonify({"error": "Package must be a valid number"}), 400

        try:
            deadline = datetime.strptime(
                data["deadline"],
                "%Y-%m-%d"
            ).date()
        except ValueError:
            return jsonify({"error": "Invalid deadline format (YYYY-MM-DD required)"}), 400

        drive_obj = PlacementDrive(
            company_id=company.id,
            title=data["title"],
            description=data["description"],
            package=package,
            location=data["location"],
            deadline=deadline,
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


@drive.get("")
@jwt_required()
@company_required
def get_drives(user):
    try:

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
@company_required
def get_drive(user, drive_id):

    try:

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
@company_required
def update_drive(user, drive_id):

    try:

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
@company_required
def delete_drive(user, drive_id):
    try:
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
