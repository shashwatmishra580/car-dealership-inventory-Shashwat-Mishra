"""FastAPI application entrypoint."""
import importlib
import pkgutil
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app import models, routers  # noqa: F401  (importing models registers the tables)
from app.database import Base, engine
from app.errors import DomainError


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="Car Dealership Inventory API", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.exception_handler(DomainError)
async def domain_error_handler(_request: Request, exc: DomainError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.get("/api/health", tags=["meta"])
def health():
    return {"status": "ok"}


# Every module in app/routers exposes a `router`; they are registered alphabetically,
# so "search" is mounted before "vehicles" and /vehicles/search never clashes with /vehicles/{id}.
for module_info in sorted(pkgutil.iter_modules(routers.__path__), key=lambda m: m.name):
    app.include_router(importlib.import_module(f"app.routers.{module_info.name}").router)

# Serve the built React app when present (single-server deployment).
FRONTEND_DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
