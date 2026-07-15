import csv
import os

from flask import current_app

from extensions import celery
from models import (
    StudentProfile,
    Application,
    PlacementDrive,
    CompanyProfile,
)


@celery.task
def export_student_applications(student_id):

    student = StudentProfile.query.get(student_id)

    if not student:
        raise ValueError("Student not found")

    applications = Application.query.filter_by(
        student_id=student.id
    ).all()

    # Create exports directory
    export_dir = os.path.join(
        current_app.root_path,
        "exports"
    )

    os.makedirs(
        export_dir,
        exist_ok=True
    )

    filename = f"student_{student.id}_applications.csv"

    file_path = os.path.join(
        export_dir,
        filename
    )

    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:

        writer = csv.writer(csv_file)

        # CSV Header
        writer.writerow([
            "Student ID",
            "Company Name",
            "Drive Title",
            "Application Status",
            "Applied Date",
        ])

        for application in applications:

            drive = PlacementDrive.query.get(
                application.drive_id
            )

            company = CompanyProfile.query.get(
                drive.company_id
            )

            writer.writerow([
                student.id,
                company.company_name,
                drive.title,
                application.status,
                application.applied_at,
            ])

    return {
        "filename": filename
    }
