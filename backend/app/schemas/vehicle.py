from pydantic import BaseModel, ConfigDict, Field


class VehicleCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    make: str = Field(min_length=1, max_length=100)
    model: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=1, max_length=50)
    price: float = Field(gt=0)
    quantity: int = Field(default=0, ge=0)


class VehicleUpdate(BaseModel):
    """All fields optional: only the provided ones are changed."""

    model_config = ConfigDict(str_strip_whitespace=True)

    make: str | None = Field(default=None, min_length=1, max_length=100)
    model: str | None = Field(default=None, min_length=1, max_length=100)
    category: str | None = Field(default=None, min_length=1, max_length=50)
    price: float | None = Field(default=None, gt=0)
    quantity: int | None = Field(default=None, ge=0)


class VehicleOut(VehicleCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
