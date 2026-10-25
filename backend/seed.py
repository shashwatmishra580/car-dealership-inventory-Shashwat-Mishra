"""Create an admin user and sample vehicles so the app can be tried immediately.

Run from the backend folder:  python seed.py
"""
from app.database import Base, SessionLocal, engine
from app.models import User, Vehicle
from app.security import hash_password

ADMIN_EMAIL, ADMIN_PASSWORD = "admin@example.com", "Admin@12345"

VEHICLES = [
    ("Toyota", "Camry", "Sedan", 28000, 5),
    ("Toyota", "RAV4", "SUV", 32000, 3),
    ("Honda", "Civic", "Sedan", 24000, 0),
    ("Honda", "CR-V", "SUV", 31000, 4),
    ("Ford", "F-150", "Truck", 45000, 2),
    ("Tesla", "Model 3", "Electric", 42000, 6),
    ("Mazda", "MX-5", "Coupe", 29000, 1),
    ("Volkswagen", "Golf", "Hatchback", 26000, 7),
]


def seed() -> None:
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        if db.query(User).filter_by(email=ADMIN_EMAIL).first() is None:
            db.add(User(email=ADMIN_EMAIL, password_hash=hash_password(ADMIN_PASSWORD), role="ADMIN"))
        if db.query(Vehicle).count() == 0:
            db.add_all(
                Vehicle(make=m, model=mo, category=c, price=p, quantity=q) for m, mo, c, p, q in VEHICLES
            )
        db.commit()
    print(f"Seeded. Admin login: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")


if __name__ == "__main__":
    seed()
