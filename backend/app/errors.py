"""Domain errors. Each carries its HTTP status so one handler can translate them all."""


class DomainError(Exception):
    status_code = 400
    detail = "Bad request"

    def __init__(self, detail: str | None = None) -> None:
        self.detail = detail or self.detail
        super().__init__(self.detail)


class DuplicateEmailError(DomainError):
    status_code = 409
    detail = "Email already registered"


class InvalidCredentialsError(DomainError):
    status_code = 401
    detail = "Invalid email or password"


class VehicleNotFoundError(DomainError):
    status_code = 404
    detail = "Vehicle not found"


class OutOfStockError(DomainError):
    status_code = 409
    detail = "Not enough stock available"


class InvalidPriceRangeError(DomainError):
    status_code = 400
    detail = "min_price cannot be greater than max_price"
