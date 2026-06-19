"""Integration tests for complete workflows."""
import pytest


def test_complete_signup_flow(client, reset_activities, sample_emails, sample_activities):
    """Test complete flow: view activities -> sign up -> view updated list."""
    email = sample_emails["new_student"]
    activity = sample_activities["without_participants"]
    
    # Step 1: Get activities
    get_response = client.get("/activities")
    assert get_response.status_code == 200
    activities_before = get_response.json()
    
    # Step 2: Verify activity exists and has no participants
    assert activity in activities_before
    assert len(activities_before[activity]["participants"]) == 0
    
    # Step 3: Sign up
    signup_response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert signup_response.status_code == 200
    
    # Step 4: Get updated activities
    get_response_2 = client.get("/activities")
    activities_after = get_response_2.json()
    
    # Step 5: Verify participant was added
    assert len(activities_after[activity]["participants"]) == 1
    assert email in activities_after[activity]["participants"]


def test_signup_and_unregister_flow(client, reset_activities, sample_emails, sample_activities):
    """Test signup followed by unregister."""
    email = sample_emails["new_student"]
    activity = sample_activities["without_participants"]
    
    # Sign up
    signup_response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert signup_response.status_code == 200
    
    # Verify signup
    check_response = client.get("/activities")
    assert email in check_response.json()[activity]["participants"]
    
    # Unregister
    unregister_response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    assert unregister_response.status_code == 200
    
    # Verify unregister
    final_response = client.get("/activities")
    assert email not in final_response.json()[activity]["participants"]


def test_multiple_students_signup_workflow(client, reset_activities, sample_activities):
    """Test multiple students signing up for the same activity."""
    activity = sample_activities["without_participants"]
    students = [
        "alice@mergington.edu",
        "bob@mergington.edu",
        "charlie@mergington.edu",
    ]
    
    # All students sign up
    for student in students:
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": student}
        )
        assert response.status_code == 200
    
    # Verify all registered
    final_response = client.get("/activities")
    participants = final_response.json()[activity]["participants"]
    assert len(participants) == len(students)
    for student in students:
        assert student in participants
    
    # One student unregisters
    unregister_response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": students[0]}
    )
    assert unregister_response.status_code == 200
    
    # Verify correct student removed
    updated_response = client.get("/activities")
    updated_participants = updated_response.json()[activity]["participants"]
    assert len(updated_participants) == len(students) - 1
    assert students[0] not in updated_participants
    for student in students[1:]:
        assert student in updated_participants


def test_signup_for_multiple_activities(client, reset_activities, sample_emails):
    """Test a single student signing up for multiple activities."""
    email = sample_emails["new_student"]
    activities = ["Chess Club", "Programming Class", "Art Studio", "Science Club"]
    
    # Sign up for all activities
    for activity in activities:
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Verify registered in all
    final_response = client.get("/activities")
    all_activities = final_response.json()
    for activity in activities:
        assert email in all_activities[activity]["participants"]


def test_activities_state_persistence_across_requests(client, reset_activities, sample_emails, sample_activities):
    """Test that activity state persists across multiple API calls."""
    email1 = sample_emails["new_student"]
    email2 = sample_emails["another_student"]
    activity = sample_activities["without_participants"]
    
    # Sign up first student
    client.post(f"/activities/{activity}/signup", params={"email": email1})
    
    # Get activities
    response1 = client.get("/activities")
    participants1 = response1.json()[activity]["participants"]
    assert email1 in participants1
    
    # Sign up second student
    client.post(f"/activities/{activity}/signup", params={"email": email2})
    
    # Get activities again - both should still be there
    response2 = client.get("/activities")
    participants2 = response2.json()[activity]["participants"]
    assert email1 in participants2
    assert email2 in participants2
    assert len(participants2) == 2


def test_error_handling_with_valid_recovery(client, reset_activities, sample_emails, sample_activities):
    """Test that system recovers from errors appropriately."""
    email = sample_emails["existing_chess"]
    activity = sample_activities["with_participants"]
    
    # Try to sign up existing participant (should fail)
    fail_response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert fail_response.status_code == 400
    
    # Get activities - should still work fine
    get_response = client.get("/activities")
    assert get_response.status_code == 200
    
    # Try with new student - should succeed
    new_email = sample_emails["new_student"]
    success_response = client.post(
        f"/activities/{activity}/signup",
        params={"email": new_email}
    )
    assert success_response.status_code == 200
