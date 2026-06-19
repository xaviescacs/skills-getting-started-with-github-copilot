"""Pytest configuration and fixtures for FastAPI tests."""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Create a TestClient instance for testing FastAPI endpoints."""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test."""
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball training and games",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 15,
            "participants": []
        },
        "Swimming Club": {
            "description": "Swimming training and water sports",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": []
        },
        "Art Studio": {
            "description": "Express creativity through painting and drawing",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": []
        },
        "Drama Club": {
            "description": "Theater arts and performance training",
            "schedule": "Tuesdays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": []
        },
        "Debate Team": {
            "description": "Learn public speaking and argumentation skills",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": []
        },
        "Science Club": {
            "description": "Hands-on experiments and scientific exploration",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": []
        }
    }
    
    # Clear and repopulate activities
    activities.clear()
    activities.update(original_activities)
    
    yield activities
    
    # Cleanup after test
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def sample_emails():
    """Provide sample email addresses for testing."""
    return {
        "existing_chess": "michael@mergington.edu",
        "existing_gym": "john@mergington.edu",
        "new_student": "alice@mergington.edu",
        "another_student": "bob@mergington.edu",
    }


@pytest.fixture
def sample_activities():
    """Provide sample activity names for testing."""
    return {
        "with_participants": "Chess Club",
        "without_participants": "Basketball Team",
        "nonexistent": "Underwater Basket Weaving",
    }
