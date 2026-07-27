"""Tests for signup and participant management endpoints"""
import pytest


def test_signup_for_activity(client, sample_activity_name):
    """Test signing up for an activity"""
    # Arrange
    new_email = "newsignup@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{sample_activity_name}/signup",
        params={"email": new_email}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]


def test_signup_duplicate_participant(client, sample_activity_name):
    """Test that duplicate signup is rejected"""
    # Arrange
    email = "michael@mergington.edu"  # Already in Chess Club
    
    # Act
    response = client.post(
        f"/activities/{sample_activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity(client):
    """Test signup for non-existent activity"""
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "test@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_remove_participant(client, sample_activity_name):
    """Test removing a participant from an activity"""
    # Arrange
    email = "michael@mergington.edu"  # Known participant in Chess Club
    
    # Act
    response = client.delete(
        f"/activities/{sample_activity_name}/participants/{email}"
    )
    
    # Assert
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]
    
    # Verify participant was actually removed
    check_response = client.get("/activities")
    activities = check_response.json()
    assert email not in activities[sample_activity_name]["participants"]


def test_remove_nonexistent_participant(client, sample_activity_name):
    """Test removing a participant who is not signed up"""
    # Arrange
    email = "notexist@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{sample_activity_name}/participants/{email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert "not signed up" in response.json()["detail"]


def test_remove_from_nonexistent_activity(client):
    """Test removing a participant from a non-existent activity"""
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "test@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_and_remove_flow(client, sample_activity_name):
    """Test the complete flow of signing up and then removing a participant"""
    # Arrange
    new_email = "flow@mergington.edu"
    
    # Act - Sign up
    signup_response = client.post(
        f"/activities/{sample_activity_name}/signup",
        params={"email": new_email}
    )
    
    # Assert - Signup successful
    assert signup_response.status_code == 200
    
    # Act - Verify participant is in the list
    check_response = client.get("/activities")
    activities = check_response.json()
    
    # Assert - Participant added
    assert new_email in activities[sample_activity_name]["participants"]
    
    # Act - Remove participant
    remove_response = client.delete(
        f"/activities/{sample_activity_name}/participants/{new_email}"
    )
    
    # Assert - Removal successful
    assert remove_response.status_code == 200
    
    # Act - Verify participant was removed
    final_check = client.get("/activities")
    final_activities = final_check.json()
    
    # Assert - Participant removed
    assert new_email not in final_activities[sample_activity_name]["participants"]
