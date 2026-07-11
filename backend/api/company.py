from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from extensions import db
from models import CompanyProfile, PlacementDrive, Application
from utils.decorators import company_required

company = Blueprint("company", __name__)


@company.get("/profile")
@jwt_required()
@company_required
def get_profile(user):
    try:
        profile = CompanyProfile.query.filter_by(user_id=user.id).first()

        return jsonify(
            {
                "id": profile.id,
                "company_name": profile.company_name,
                "website": profile.website,
                "location": profile.location,
                "description": profile.description,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@company.put("/profile")
@jwt_required()
@company_required
def update_profile(user):
    try:
        profile = CompanyProfile.query.filter_by(user_id=user.id).first()
        data = request.get_json() or {}

        profile.company_name = data.get("company_name", profile.company_name)
        profile.website = data.get("website", profile.website)
        profile.location = data.get("location", profile.location)
        profile.description = data.get("description", profile.description)

        db.session.commit()

        return jsonify({"message": "Profile updated successfully"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@company.get("/dashboard")
@jwt_required()
@company_required
def dashboard(user):
    try:

        profile = CompanyProfile.query.filter_by(user_id=user.id).first()
        drives = PlacementDrive.query.filter_by(company_id=profile.id).all()
        drive_ids = [d.id for d in drives]

        total_applications = Application.query.filter(
            Application.drive_id.in_(drive_ids)
        ).count()

        shortlisted = Application.query.filter(
            Application.drive_id.in_(
                drive_ids), Application.status == "shortlisted"
        ).count()

        rejected = Application.query.filter(
            Application.drive_id.in_(
                drive_ids), Application.status == "rejected"
        ).count()

        return jsonify(
            {
                "company": profile.company_name,
                "total_drives": len(drives),
                "total_applications": total_applications,
                "shortlisted": shortlisted,
                "rejected": rejected,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
