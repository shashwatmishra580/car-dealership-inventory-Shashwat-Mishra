from app.errors import OutOfStockError, VehicleNotFoundError
from app.models import Vehicle
from app.repositories.vehicle_repository import VehicleRepository


class InventoryService:
    """Stock-changing use-cases: purchase and restock."""

    def __init__(self, vehicles: VehicleRepository) -> None:
        self.vehicles = vehicles

    def purchase(self, vehicle_id: int, quantity: int = 1) -> Vehicle:
        if self.vehicles.get(vehicle_id) is None:
            raise VehicleNotFoundError()
        if not self.vehicles.decrement_stock(vehicle_id, quantity):
            raise OutOfStockError()
        return self.vehicles.get(vehicle_id)

    def restock(self, vehicle_id: int, amount: int) -> Vehicle:
        if not self.vehicles.increment_stock(vehicle_id, amount):
            raise VehicleNotFoundError()
        return self.vehicles.get(vehicle_id)
