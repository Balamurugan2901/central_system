from app.database.session import SessionLocal
from app.models.user_model import User
from app.core.security import hash_password

db = SessionLocal()

admin = User(
    email="admin@gmail.com",
    password=hash_password("admin123"),
    role="admin"
)

db.add(admin)
db.commit()
db.close()

print("Admin created")
