"""API routes."""

from fastapi import APIRouter
from pydantic import BaseModel

from app.config import settings

router = APIRouter()


class MessageResponse(BaseModel):
    """A plain text message returned by the API."""

    message: str


class HealthResponse(BaseModel):
    """Service liveness information."""

    status: str
    environment: str


@router.get("/hello", response_model=MessageResponse, tags=["sanity"])
async def hello_world() -> MessageResponse:
    """Sanity-check endpoint required by the technical start checklist."""
    return MessageResponse(message="Hello world!")


@router.get("/health", response_model=HealthResponse, tags=["system"])
async def health() -> HealthResponse:
    """Health probe used by the hosting platform and by CI."""
    return HealthResponse(status="ok", environment=settings.environment)
