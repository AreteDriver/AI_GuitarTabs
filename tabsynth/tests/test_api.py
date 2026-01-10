"""Tests for the FastAPI backend."""

import pytest
from fastapi.testclient import TestClient

from tabsynth.api import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints."""

    def test_health(self, client):
        """Test root health endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data

    def test_health_v1(self, client):
        """Test v1 health endpoint."""
        response = client.get("/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["api_version"] == "v1"


class TestTablatureEndpoints:
    """Test tablature generation endpoints."""

    @pytest.fixture
    def simple_note_request(self):
        """A simple single-note request."""
        return {
            "events": [
                {"type": "note", "pitch_hz": 440.0, "start": 0.0, "duration": 0.5}
            ]
        }

    @pytest.fixture
    def multi_note_request(self):
        """Request with multiple notes."""
        return {
            "events": [
                {"type": "note", "pitch_hz": 329.63, "start": 0.0, "duration": 0.5},
                {"type": "note", "pitch_hz": 392.00, "start": 0.5, "duration": 0.5},
                {"type": "note", "pitch_hz": 440.00, "start": 1.0, "duration": 0.5},
            ]
        }

    @pytest.fixture
    def chord_request(self):
        """Request with a chord."""
        return {
            "events": [
                {
                    "type": "chord",
                    "pitches_hz": [329.63, 392.00, 493.88],
                    "start": 0.0,
                    "duration": 1.0,
                }
            ]
        }

    def test_tablature_ascii(self, client, simple_note_request):
        """Test ASCII tablature generation."""
        response = client.post("/tablature", json=simple_note_request)
        assert response.status_code == 200
        data = response.json()
        assert "tablature" in data
        assert data["format"] == "ascii"
        assert "Guitar Tablature" in data["tablature"]

    def test_tablature_json_format(self, client, simple_note_request):
        """Test JSON tablature generation via /tablature endpoint."""
        request = {**simple_note_request, "output_format": "json"}
        response = client.post("/tablature", json=request)
        assert response.status_code == 200
        data = response.json()
        assert data["format"] == "json"

    def test_tablature_compact(self, client, simple_note_request):
        """Test compact tablature generation."""
        request = {**simple_note_request, "output_format": "compact"}
        response = client.post("/tablature", json=request)
        assert response.status_code == 200
        data = response.json()
        assert data["format"] == "compact"

    def test_tablature_json_endpoint(self, client, simple_note_request):
        """Test /tablature/json endpoint."""
        response = client.post("/tablature/json", json=simple_note_request)
        assert response.status_code == 200
        data = response.json()
        assert "states" in data
        assert len(data["states"]) == 1
        assert "tuning" in data
        assert "capo" in data
        assert data["capo"] == 0

    def test_tablature_multi_notes(self, client, multi_note_request):
        """Test with multiple notes."""
        response = client.post("/tablature/json", json=multi_note_request)
        assert response.status_code == 200
        data = response.json()
        assert len(data["states"]) == 3

    def test_tablature_chord(self, client, chord_request):
        """Test with chord event."""
        response = client.post("/tablature/json", json=chord_request)
        assert response.status_code == 200
        data = response.json()
        assert len(data["states"]) == 1
        state = data["states"][0]
        assert state["kind"] == "chord"
        # Frets dict should have entries for the played strings
        assert len(state["frets"]) >= 3

    def test_v1_tablature(self, client, simple_note_request):
        """Test v1 tablature endpoint."""
        response = client.post("/v1/tablature", json=simple_note_request)
        assert response.status_code == 200
        data = response.json()
        assert "tablature" in data

    def test_v1_tablature_json(self, client, simple_note_request):
        """Test v1 tablature/json endpoint."""
        response = client.post("/v1/tablature/json", json=simple_note_request)
        assert response.status_code == 200
        data = response.json()
        assert "states" in data


class TestRequestValidation:
    """Test request validation."""

    def test_empty_events_rejected(self, client):
        """Test that empty events list is rejected."""
        response = client.post("/tablature", json={"events": []})
        assert response.status_code == 422

    def test_invalid_pitch_rejected(self, client):
        """Test that invalid pitch is rejected."""
        response = client.post(
            "/tablature",
            json={
                "events": [
                    {"type": "note", "pitch_hz": -100, "start": 0.0, "duration": 0.5}
                ]
            },
        )
        assert response.status_code == 422

    def test_invalid_duration_rejected(self, client):
        """Test that invalid duration is rejected."""
        response = client.post(
            "/tablature",
            json={
                "events": [
                    {"type": "note", "pitch_hz": 440, "start": 0.0, "duration": 0}
                ]
            },
        )
        assert response.status_code == 422

    def test_invalid_max_fret(self, client):
        """Test that invalid max_fret is rejected."""
        response = client.post(
            "/tablature",
            json={
                "events": [
                    {"type": "note", "pitch_hz": 440, "start": 0.0, "duration": 0.5}
                ],
                "max_fret": 30,
            },
        )
        assert response.status_code == 422

    def test_invalid_chord_pitches(self, client):
        """Test that chord with invalid pitches is rejected."""
        response = client.post(
            "/tablature",
            json={
                "events": [
                    {
                        "type": "chord",
                        "pitches_hz": [440, -100],
                        "start": 0.0,
                        "duration": 0.5,
                    }
                ]
            },
        )
        assert response.status_code == 422


class TestTuningAndCapo:
    """Test tuning and capo parameters."""

    def test_capo_accepted(self, client):
        """Test that capo parameter is accepted."""
        response = client.post(
            "/tablature/json",
            json={
                "events": [
                    {"type": "note", "pitch_hz": 440, "start": 0.0, "duration": 0.5}
                ],
                "capo": 2,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["capo"] == 2

    def test_tuning_accepted(self, client):
        """Test that tuning parameter is accepted (MVP: stored but not applied)."""
        response = client.post(
            "/tablature/json",
            json={
                "events": [
                    {"type": "note", "pitch_hz": 440, "start": 0.0, "duration": 0.5}
                ],
                "tuning": ["D2", "A2", "D3", "G3", "B3", "E4"],
            },
        )
        assert response.status_code == 200

    def test_invalid_capo_rejected(self, client):
        """Test that invalid capo is rejected."""
        response = client.post(
            "/tablature",
            json={
                "events": [
                    {"type": "note", "pitch_hz": 440, "start": 0.0, "duration": 0.5}
                ],
                "capo": 15,
            },
        )
        assert response.status_code == 422


class TestResponseStructure:
    """Test response structure compliance."""

    def test_tab_state_structure(self, client):
        """Test that TabState response has all required fields."""
        response = client.post(
            "/tablature/json",
            json={
                "events": [
                    {"type": "note", "pitch_hz": 440, "start": 0.0, "duration": 0.5}
                ]
            },
        )
        assert response.status_code == 200
        data = response.json()
        state = data["states"][0]

        required_fields = [
            "index",
            "start",
            "duration",
            "kind",
            "strings",
            "frets",
            "mean_fret",
            "min_fret",
            "max_fret",
            "requires_barre",
            "chord_id",
        ]
        for field in required_fields:
            assert field in state, f"Missing field: {field}"
