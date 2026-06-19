"""Tests for the DELETE /activities/{activity_name}/unregister endpoint."""
import pytest


def test_unregister_existing_participant_success(client, reset_activities, sample_emails, sample_activities):
    """Test successful unregistration of an existing participant."""
    email = sample_emails["existing_chess"]
    activity = sample_activities["with_participants"]
    
    # Verify participant exists
    initial_response = client.get("/activities")
    assert email in initial_response.json()[activity]["participants"]
    
    # Unregister
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert "message" in result


def test_unregister_removes_participant_from_activity(client, reset_activities, sample_emails, sample_activities):
    """Test that unregister actually removes the participant from the activity."""
    email = sample_emails["existing_chess"]
    activity = sample_activities["with_participants"]
    
    # Get initial count
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity]["participants"])
    
    # Unregister
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Check updated state
    updated_response = client.get("/activities")
    updated_participants = updated_response.json()[activity]["participants"]
    assert len(updated_participants) == initial_count - 1
    assert email not in updated_participants


def test_unregister_nonexistent_participant_fails(client, reset_activities, sample_emails, sample_activities):
    """Test that unregistering a non-participant fails."""
    email = sample_emails["new_student"]
    activity = sample_activities["with_participants"]
    
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result


def test_unregister_nonexistent_activity_fails(client, reset_activities, sample_emails, sample_activities):
    """Test that unregister for a non-existent activity fails."""
    email = sample_emails["existing_chess"]
    activity = sample_activities["nonexistent"]
    
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "not found" in result["detail"].lower()


def test_unregister_multiple_participants_one_at_time(client, reset_activities, sample_activities):
    """Test unregistering multiple participants from an activity one at a time."""
    activity = sample_activities["with_participants"]
    
    # Get initial participants
    initial_response = client.get("/activities")
    initial_participants = initial_response.json()[activity]["participants"].copy()
    
    # Unregister first participant
    response1 = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": initial_participants[0]}
    )
    assert response1.status_code == 200
    
    # Unregister second participant
    response2 = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": initial_participants[1]}
    )
    assert response2.status_code == 200
    
    # Verify both are removed
    final_response = client.get("/activities")
    final_participants = final_response.json()[activity]["participants"]
    assert len(final_participants) == 0
    assert initial_participants[0] not in final_participants
    assert initial_participants[1] not in final_participants


def test_unregister_then_signup_again(client, reset_activities, sample_emails, sample_activities):
    """Test that a student can unregister and then sign up again."""
    email = sample_emails["existing_chess"]
    activity = sample_activities["with_participants"]
    
    # Unregister
    unregister_response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    assert unregister_response.status_code == 200
    
    # Verify not registered
    check_response = client.get("/activities")
    assert email not in check_response.json()[activity]["participants"]
    
    # Sign up again
    signup_response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert signup_response.status_code == 200
    
    # Verify registered again
    final_response = client.get("/activities")
    assert email in final_response.json()[activity]["participants"]
