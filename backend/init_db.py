from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from auth import get_password_hash

def init_db():
    print("Creating initial data...")
    
    # Create tables
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if admin user exists
        test_user = db.query(models.User).filter(models.User.username == "admin").first()
        if not test_user:
            # Create admin user
            admin_user = models.User(
                username="admin",
                email="admin@casino.com",
                hashed_password=get_password_hash("admin123"),
                is_active=True,
                is_admin=True
            )
            db.add(admin_user)
            db.commit()
            print("Created test user: admin/admin123")
        else:
            print("Test user already exists")
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating initial data...")
    init_db()
    print("Initial data created") 