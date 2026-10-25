from fastapi import APIRouter, Depends

from app.deps import get_current_user, get_vehicle_service, require_admin
from app.schemas.vehicle import VehicleCreate, VehicleOut, VehicleUpdate
from app.services.vehicle_service import VehicleService

# Every vehicle endpoint requires a valid token.
router = APIRouter(prefix="/api/vehicles", tags=["vehicles"], dependencies=[Depends(get_current_user)])


@router.post("", response_model=VehicleOut, status_code=201)
def create_vehicle(body: VehicleCreate, service: VehicleService = Depends(get_vehicle_service)):
    return service.create(body.model_dump())


@router.get("", response_model=list[VehicleOut])
def list_vehicles(service: VehicleService = Depends(get_vehicle_service)):
    return service.list_all()


@router.put("/{vehicle_id}", response_model=VehicleOut)
def update_vehicle(vehicle_id: int, body: VehicleUpdate, service: VehicleService = Depends(get_vehicle_service)):
    return service.update(vehicle_id, body.model_dump(exclude_none=True))


@router.delete("/{vehicle_id}", status_code=204, dependencies=[Depends(require_admin)])
def delete_vehicle(vehicle_id: int, service: VehicleService = Depends(get_vehicle_service)):
    service.delete(vehicle_id)
