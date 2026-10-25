from pydantic import BaseModel, Field


class PurchaseRequest(BaseModel):
    quantity: int = Field(default=1, gt=0)


class RestockRequest(BaseModel):
    amount: int = Field(gt=0)
