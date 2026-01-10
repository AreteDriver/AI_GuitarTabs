"""FastAPI backend for tabsynth.

Run with: uvicorn tabsynth.api:app --reload
"""

import os
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

from tabsynth.fretboard import STANDARD_TUNING_HZ
from tabsynth.model import NoteEvent, ChordEvent, Event
from tabsynth.pipeline import events_to_tablature

# --- Pydantic Models ---


class NoteEventRequest(BaseModel):
    """Single note event."""

    type: Literal["note"] = "note"
    pitch_hz: float = Field(..., gt=0, description="Pitch in Hz")
    start: float = Field(..., ge=0, description="Start time in seconds")
    duration: float = Field(..., gt=0, description="Duration in seconds")


class ChordEventRequest(BaseModel):
    """Chord event (multiple simultaneous pitches)."""

    type: Literal["chord"]
    pitches_hz: list[float] = Field(..., min_length=1, description="Pitches in Hz")
    start: float = Field(..., ge=0, description="Start time in seconds")
    duration: float = Field(..., gt=0, description="Duration in seconds")

    @field_validator("pitches_hz")
    @classmethod
    def validate_pitches(cls, v: list[float]) -> list[float]:
        for p in v:
            if p <= 0:
                raise ValueError("All pitches must be positive")
        return v


EventRequest = NoteEventRequest | ChordEventRequest


class TablatureRequest(BaseModel):
    """Request body for tablature generation."""

    events: list[EventRequest] = Field(..., min_length=1)
    output_format: Literal["ascii", "json", "compact"] = "ascii"
    max_fret: int = Field(default=15, ge=0, le=24)
    tolerance_cents: float = Field(default=50.0, ge=0, le=100)
    tuning: list[str] | None = Field(
        default=None,
        description="Custom tuning as note names (e.g., ['E2', 'A2', 'D3', 'G3', 'B3', 'E4'])",
    )
    capo: int = Field(default=0, ge=0, le=12, description="Capo position (0 = no capo)")


class TabStateResponse(BaseModel):
    """Single tab state in JSON response."""

    index: int
    start: float
    duration: float
    kind: str
    strings: list[int]
    frets: dict[str, int]
    mean_fret: float
    min_fret: int
    max_fret: int
    requires_barre: bool
    chord_id: str | None


class TablatureJsonResponse(BaseModel):
    """Response for /tablature/json endpoint."""

    states: list[TabStateResponse]
    tuning: list[str]
    capo: int


class ErrorDetail(BaseModel):
    """Error detail structure."""

    code: str
    message: str
    details: dict | None = None


class ErrorResponse(BaseModel):
    """Consistent error response."""

    error: ErrorDetail


# --- Helper Functions ---


def parse_tuning(tuning: list[str] | None, capo: int) -> dict[int, float]:
    """
    Parse tuning note names to Hz frequencies.

    For MVP, we accept tuning but use standard tuning.
    Full tuning support is Phase 2.
    """
    # TODO: Implement full tuning parsing (Phase 2)
    # For now, return standard tuning (capo-adjusted if needed)
    base = STANDARD_TUNING_HZ.copy()
    if capo > 0:
        # Raise each string by capo semitones
        for string in base:
            base[string] = base[string] * (2 ** (capo / 12))
    return base


def get_tuning_names() -> list[str]:
    """Return standard tuning as note names."""
    return ["E2", "A2", "D3", "G3", "B3", "E4"]


def convert_event(event: EventRequest) -> Event:
    """Convert Pydantic event to domain model."""
    if event.type == "note":
        return NoteEvent(
            pitch_hz=event.pitch_hz,
            start=event.start,
            duration=event.duration,
        )
    else:
        return ChordEvent(
            pitches_hz=event.pitches_hz,
            start=event.start,
            duration=event.duration,
        )


# --- FastAPI App ---

app = FastAPI(
    title="TabSynth API",
    description="Convert musical events to guitar tablature",
    version="1.0.0",
)

# CORS configuration
CORS_ORIGINS = os.environ.get(
    "CORS_ORIGINS",
    "http://localhost:8081,http://127.0.0.1:8081,http://localhost:19006,http://127.0.0.1:19006,http://10.0.2.2:8081",
).split(",")

# In development, allow all origins
if os.environ.get("TABSYNTH_DEV", "").lower() in ("1", "true"):
    CORS_ORIGINS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Error Handlers ---


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Return consistent JSON error responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail,
                "details": None,
            }
        },
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    """Handle validation errors."""
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": str(exc),
                "details": None,
            }
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected errors."""
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "details": {"type": type(exc).__name__},
            }
        },
    )


# --- Root Endpoints (backwards compatibility) ---


@app.get("/health")
async def health() -> dict:
    """Health check endpoint."""
    return {"status": "ok", "version": "1.0.0"}


@app.post("/tablature")
async def generate_tablature(request: TablatureRequest) -> dict:
    """
    Generate tablature from musical events.

    Returns tablature in the requested format (ascii, json, or compact).
    """
    events = [convert_event(e) for e in request.events]

    result = events_to_tablature(
        events=events,
        output_format=request.output_format,
        max_fret=request.max_fret,
        tolerance_cents=request.tolerance_cents,
    )

    return {
        "tablature": result,
        "format": request.output_format,
        "tuning": get_tuning_names(),
        "capo": request.capo,
    }


@app.post("/tablature/json", response_model=TablatureJsonResponse)
async def generate_tablature_json(request: TablatureRequest) -> TablatureJsonResponse:
    """
    Generate tablature as structured JSON.

    Returns list of TabState objects for programmatic use.
    """
    import json as json_module

    events = [convert_event(e) for e in request.events]

    # Force JSON output format
    result = events_to_tablature(
        events=events,
        output_format="json",
        max_fret=request.max_fret,
        tolerance_cents=request.tolerance_cents,
    )

    # Parse the JSON string back to objects
    states_raw = json_module.loads(result)
    states = [TabStateResponse(**s) for s in states_raw]

    return TablatureJsonResponse(
        states=states,
        tuning=get_tuning_names(),
        capo=request.capo,
    )


# --- V1 Versioned Endpoints ---


@app.get("/v1/health")
async def health_v1() -> dict:
    """Health check endpoint (v1)."""
    return {"status": "ok", "version": "1.0.0", "api_version": "v1"}


@app.post("/v1/tablature")
async def generate_tablature_v1(request: TablatureRequest) -> dict:
    """Generate tablature from musical events (v1)."""
    return await generate_tablature(request)


@app.post("/v1/tablature/json", response_model=TablatureJsonResponse)
async def generate_tablature_json_v1(
    request: TablatureRequest,
) -> TablatureJsonResponse:
    """Generate tablature as structured JSON (v1)."""
    return await generate_tablature_json(request)


# --- CLI entry point ---


def run_dev_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    """Run the development server."""
    import uvicorn

    uvicorn.run("tabsynth.api:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    run_dev_server()
