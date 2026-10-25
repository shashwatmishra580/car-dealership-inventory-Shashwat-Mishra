from app.errors import InvalidPriceRangeError, VehicleNotFoundError
from app.models import Vehicle
from app.repositories.vehicle_repository import VehicleRepository


class VehicleService:
    """Catalogue use-cases: create, list, search, update, delete."""

    def __init__(self, vehicles: VehicleRepository) -> None:
        self.vehicles = vehicles

    def create(self, data: dict) -> Vehicle:
        return self.vehicles.add(**data)

    def list_all(self) -> list[Vehicle]:
        return self.vehicles.list_all()

    def update(self, vehicle_id: int, changes: dict) -> Vehicle:
        vehicle = self._get_or_raise(vehicle_id)
        return self.vehicles.update(vehicle, **changes)

    def delete(self, vehicle_id: int) -> None:
        self.vehicles.delete(self._get_or_raise(vehicle_id))

    def _get_or_raise(self, vehicle_id: int) -> Vehicle:
        vehicle = self.vehicles.get(vehicle_id)
        if vehicle is None:
            raise VehicleNotFoundError()
        return vehicle
