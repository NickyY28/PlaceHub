from datetime import datetime
from sqlalchemy import Enum
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db


def ensure_sqlite_dir(uri: str):
    if not uri.startswith("sqlite:///"):
        return
    import os

    path = uri.replace("sqlite:///", "")
    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)


def create_all_tables():
    db.create_all()


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class User(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_blocked = db.Column(db.Boolean, default=False)
    role = db.Column(
        Enum("admin", "company", "student", name="role_enum"), nullable=False
    )

    # Relationships
    company_profile = db.relationship(
        "CompanyProfile", back_populates="user", uselist=False
    )
    student_profile = db.relationship(
        "StudentProfile", back_populates="user", uselist=False
    )

    # Methods
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class CompanyProfile(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    company_name = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(255))
    location = db.Column(db.String(255))
    description = db.Column(db.Text)

    approval_status = db.Column(
        Enum(
            "pending",
            "approved",
            "rejected",
            name="company_approval_status"
        ),
        default="pending",
        nullable=False
    )

    # Relationships
    user = db.relationship("User", back_populates="company_profile")
    placement_drives = db.relationship(
        "PlacementDrive", back_populates="company", cascade="all, delete-orphan"
    )


class StudentProfile(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    college = db.Column(db.String(255))
    cgpa = db.Column(db.Float)
    skills = db.Column(db.String(255))  # Comma-separated skills
    resume = db.Column(db.String(255))  # Path to resume file

    # Relationships
    user = db.relationship("User", back_populates="student_profile")
    applications = db.relationship(
        "Application", back_populates="student", cascade="all, delete-orphan"
    )


class PlacementDrive(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey(
        "company_profile.id"), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    package = db.Column(db.Float)
    location = db.Column(db.String(255))
    deadline = db.Column(db.Date)
    eligibility = db.Column(db.String(255))  # e.g., "CGPA >= 7.0"

    # Relationships
    company = db.relationship(
        "CompanyProfile", back_populates="placement_drives")
    applications = db.relationship(
        "Application", back_populates="drive", cascade="all, delete-orphan"
    )


class Application(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(
        "student_profile.id"), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey(
        "placement_drive.id"), nullable=False)
    status = db.Column(
        Enum("applied", "in-touch", "shortlisted",
             "rejected", name="application_status"),
        default="applied",
    )
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    student = db.relationship("StudentProfile", back_populates="applications")
    drive = db.relationship("PlacementDrive", back_populates="applications")
