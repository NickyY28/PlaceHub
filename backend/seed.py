from extensions import db
from models import User


def ensure_seed_data():
    # Admin
    admin = User.query.filter_by(role="admin").first()
    if not admin:
        admin = User(name="Admin", email="admin@gmail.com", role="admin")
        admin.set_password("adminpass")
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created with email:admin@gmail.com")
