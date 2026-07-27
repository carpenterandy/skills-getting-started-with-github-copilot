import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Fixture to provide a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def sample_activity_name():
    """Fixture providing a sample activity name"""
    return "Chess Club"


@pytest.fixture
def sample_email():
    """Fixture providing a sample student email"""
    return "test@mergington.edu"
