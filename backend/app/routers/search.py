from fastapi import APIRouter, Depends, Query

from app.deps import get_current_user, get_vehicle_service
from app.schemas.vehicle import VehicleOut
from app.services.vehicle_service import VehicleService

router = APIRouter(prefix="/api/vehicles", tags=["vehicles"], dependencies=[Depends(get_current_user)])


@router.get("/search", response_model=list[VehicleOut])
def search_vehicles(
    make: str | None = None,
    model: str | None = None,
    category: str | None = None,
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, ge=0),
    service: VehicleService = Depends(get_vehicle_service),
):
    return service.search(make=make, model=model, category=category, min_price=min_price, max_price=max_price)
