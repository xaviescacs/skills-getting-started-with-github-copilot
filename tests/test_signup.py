"""Tests for the POST /activities/{activity_name}/signup endpoint."""
import pytest


def test_signup_new_student_success(client, reset_activities, sample_emails, sample_activities):
    """Test successful signup for a new student."""
    email = sample_emails["new_student"]
    activity = sample_activities["without_participants"]
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert activity in result["message"]


def test_signup_adds_participant_to_activity(client, reset_activities, sample_emails, sample_activities):
    """Test that signup actually adds the participant to the activity."""
    email = sample_emails["new_student"]
    activity = sample_activities["without_participants"]
    
    # Get initial state
    initial_response = client.get("/activities")
    initial_participants = initial_response.json()[activity]["participants"]
    initial_count = len(initial_participants)
    
    # Perform signup
    signup_response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert signup_response.status_code == 200
    
    # Check updated state
    updated_response = client.get("/activities")
    updated_participants = updated_response.json()[activity]["participants"]
    assert len(updated_participants) == initial_count + 1
    assert email in updated_participants


def test_signup_duplicate_email_fails(client, reset_activities, sample_emails, sample_activities):
    """Test that signing up an already-registered student fails."""
    email = sample_emails["existing_chess"]
    activity = sample_activities["with_participants"]
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "already signed up" in result["detail"].lower()


def test_signup_nonexistent_activity_fails(client, reset_activities, sample_emails, sample_activities):
    """Test that signup for a non-existent activity fails."""
    email = sample_emails["new_student"]
    activity = sample_activities["nonexistent"]
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "not found" in result["detail"].lower()


def test_signup_multiple_different_students(client, reset_activities, sample_activities):
    """Test that multiple different students can sign up for the same activity."""
    activity = sample_activities["without_participants"]
    emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
    
    for email in emails:
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Verify all were added
    final_response = client.get("/activities")
    participants = final_response.json()[activity]["participants"]
    assert len(participants) == 3
    for email in emails:
        assert email in participants


def test_signup_same_student_different_activities(client, reset_activities, sample_emails):
    """Test that the same student can sign up for multiple activities."""
    email = sample_emails["new_student"]
    activities = ["Basketball Team", "Swimming Club", "Art Studio"]
    
    for activity in activities:
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Verify signup in all activities
    final_response = client.get("/activities")
    all_activities = final_response.json()
    for activity in activities:
        assert email in all_activities[activity]["participants"]
