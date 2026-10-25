from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_admin
from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.inventory import PurchaseRequest, RestockRequest
from app.schemas.vehicle import VehicleOut
from app.services.inventory_service import InventoryService

router = APIRouter(prefix="/api/vehicles", tags=["inventory"], dependencies=[Depends(get_current_user)])


def get_inventory_service(db: Session = Depends(get_db)) -> InventoryService:
    return InventoryService(VehicleRepository(db))


@router.post("/{vehicle_id}/purchase", response_model=VehicleOut)
def purchase_vehicle(
    vehicle_id: int,
    body: PurchaseRequest | None = None,
    service: InventoryService = Depends(get_inventory_service),
):
    return service.purchase(vehicle_id, body.quantity if body else 1)


@router.post("/{vehicle_id}/restock", response_model=VehicleOut, dependencies=[Depends(require_admin)])
def restock_vehicle(
    vehicle_id: int,
    body: RestockRequest,
    service: InventoryService = Depends(get_inventory_service),
):
    return service.restock(vehicle_id, body.amount)
