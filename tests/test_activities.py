"""Tests for the GET /activities endpoint."""
import pytest


def test_get_activities_returns_all_activities(client, reset_activities):
    """Test that GET /activities returns all activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    
    activities = response.json()
    assert len(activities) == 9
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Basketball Team" in activities


def test_get_activities_response_structure(client, reset_activities):
    """Test that activities have the correct structure."""
    response = client.get("/activities")
    assert response.status_code == 200
    
    activities = response.json()
    activity = activities["Chess Club"]
    
    # Check required fields
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    
    # Check types
    assert isinstance(activity["description"], str)
    assert isinstance(activity["schedule"], str)
    assert isinstance(activity["max_participants"], int)
    assert isinstance(activity["participants"], list)


def test_get_activities_shows_existing_participants(client, reset_activities):
    """Test that activities show correct participant lists."""
    response = client.get("/activities")
    assert response.status_code == 200
    
    activities = response.json()
    
    # Chess Club should have 2 participants
    assert len(activities["Chess Club"]["participants"]) == 2
    assert "michael@mergington.edu" in activities["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in activities["Chess Club"]["participants"]
    
    # Basketball Team should have 0 participants
    assert len(activities["Basketball Team"]["participants"]) == 0


def test_get_activities_content(client, reset_activities):
    """Test that activities contain expected content."""
    response = client.get("/activities")
    assert response.status_code == 200
    
    activities = response.json()
    
    # Check a specific activity
    gym = activities["Gym Class"]
    assert "Physical education" in gym["description"]
    assert "Mondays, Wednesdays, Fridays" in gym["schedule"]
    assert gym["max_participants"] == 30
