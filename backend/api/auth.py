from datetime import timedelta
from flask import request, jsonify, Blueprint

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

from extensions import db
from models import (
    User,
    CompanyProfile as Company,
    StudentProfile as Student
)

auth = Blueprint("auth", __name__)


@auth.post("/register/company")
def register_company():
    try:
        data = request.get_json() or {}
        required = ["name", "email", "password",
                    "website", "location", "description"]
        if not all(k in data for k in required):
            return jsonify({"error": "Missing fields"}), 400

        if User.query.filter_by(email=data.get("email")).first():
            return jsonify({"error": "Email already exists"}), 400
        user = User(name=data["name"], email=data["email"], role="company")
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()

        company_profile = Company(
            user_id=user.id,
            company_name=data["name"],
            website=data["website"],
            location=data["location"],
            description=data["description"],
        )
        db.session.add(company_profile)
        db.session.commit()
        if not company_profile:
            return jsonify({"error": "Invalid company profile data"}), 400

        return jsonify({
            "msg": "Company registered successfully",
            "data": {
                "user_id": user.id,
                "company_id": company_profile.id,
                "company_name": company_profile.company_name,
                "email": user.email
            }}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth.post("/register/student")
def register_student():
    try:
        data = request.get_json() or {}
        required = ["name", "email", "password",
                    "college", "cgpa", "skills", "resume_url"]
        if not all(k in data for k in required):
            return jsonify({"error": "Missing fields"}), 400
        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Username already exists"}), 400
        user = User(name=data["name"],
                    email=data["email"], role="student")
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()

        student_profile = Student(
            user_id=user.id,
            college=data["college"],
            cgpa=data["cgpa"],
            skills=data["skills"],
            resume=data["resume_url"],
        )
        db.session.add(student_profile)
        db.session.commit()
        if not student_profile:
            return jsonify({"error": "Invalid student profile data"}), 400
        return jsonify({
            "msg": "Student registered successfully",
            "data": {
                "user_id": user.id,
                "student_id": student_profile.id,
                "name": user.name,
                "email": user.email
            }}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth.post("/login")
def login():
    try:
        data = request.get_json() or {}
        if not data.get("email") or not data.get("password"):
            return jsonify({"error": "Email and password are required"}), 400
        user = User.query.filter_by(email=data.get("email")).first()
        if not user or not user.check_password(data.get("password", "")):
            return jsonify({"error": "Invalid credentials"}), 401
        elif user.is_blocked:
            return jsonify({"error": "User is blocked"}), 403

        if user.role == "company":
            profile = Company.query.filter_by(user_id=user.id).first()
            if not profile:
                return jsonify({"error": "Company profile not found"}), 404
            if profile.approval_status != "approved":
                return jsonify({"error": "Company not approved"}), 403

        token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(hours=8),
            additional_claims={"role": user.role},
        )

        return jsonify({"token": token, "role": user.role, "name": user.name})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth.patch("/logout")
@jwt_required()
def logout():
    try:
        # Invalidate the token by adding it to a blocklist (if implemented)
        return jsonify({"msg": "Logged out successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth.get("/me")
@jwt_required()
def me():
    try:
        uid = get_jwt_identity()
        uid = int(uid)
        u = User.query.get(uid)
        print("user_id", u.id)
        print("user_role", u.role)
        if not u:
            return jsonify({"error": "Not found"}), 404

        if u.role == "company":
            profile = Company.query.filter_by(user_id=u.id).first()
            return jsonify({
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "role": u.role,
                "company_profile": {
                    "company_name": profile.company_name,
                    "website": profile.website,
                    "location": profile.location,
                    "description": profile.description
                }
            })
        elif u.role == "student":
            profile = Student.query.filter_by(user_id=u.id).first()
            return jsonify({
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "role": u.role,
                "student_profile": {
                    "college": profile.college,
                    "cgpa": profile.cgpa,
                    "skills": profile.skills,
                    "resume_url": profile.resume
                }
            })
        else:
            return jsonify({
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "role": u.role
            })

    except Exception as e:
        if isinstance(e, ValueError):
            return jsonify({"error": "Invalid user ID"}), 400
        return jsonify({"error": str(e)}), 500
