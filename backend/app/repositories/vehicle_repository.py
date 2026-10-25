from sqlalchemy import select, update  # `update` is used by the stock operations
from sqlalchemy.orm import Session

from app.models import Vehicle


class VehicleRepository:
    """Data access for vehicles."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def add(self, **data) -> Vehicle:
        vehicle = Vehicle(**data)
        self.db.add(vehicle)
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def get(self, vehicle_id: int) -> Vehicle | None:
        return self.db.get(Vehicle, vehicle_id)

    def list_all(self) -> list[Vehicle]:
        return list(self.db.scalars(select(Vehicle).order_by(Vehicle.id)))

    def update(self, vehicle: Vehicle, **changes) -> Vehicle:
        for field, value in changes.items():
            setattr(vehicle, field, value)
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def delete(self, vehicle: Vehicle) -> None:
        self.db.delete(vehicle)
        self.db.commit()

    def search(self, make=None, model=None, category=None, min_price=None, max_price=None) -> list[Vehicle]:
        """Filter vehicles; text filters are case-insensitive partial matches."""
        stmt = select(Vehicle)
        if make:
            stmt = stmt.where(Vehicle.make.ilike(f"%{make}%"))
        if model:
            stmt = stmt.where(Vehicle.model.ilike(f"%{model}%"))
        if category:
            stmt = stmt.where(Vehicle.category.ilike(f"%{category}%"))
        if min_price is not None:
            stmt = stmt.where(Vehicle.price >= min_price)
        if max_price is not None:
            stmt = stmt.where(Vehicle.price <= max_price)
        return list(self.db.scalars(stmt.order_by(Vehicle.id)))
