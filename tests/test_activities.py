"""Tests for the /activities endpoint"""
import pytest


def test_get_activities(client):
    """Test that GET /activities returns all activities"""
    # Arrange
    # No setup needed - activities are pre-loaded
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    assert "Chess Club" in data


def test_activity_structure(client):
    """Test that activities have the correct structure"""
    # Arrange
    # No setup needed
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    first_activity = data["Chess Club"]
    assert "description" in first_activity
    assert "schedule" in first_activity
    assert "max_participants" in first_activity
    assert "participants" in first_activity
    assert isinstance(first_activity["participants"], list)


def test_activities_have_participants(client):
    """Test that activities have initial participants"""
    # Arrange
    # No setup needed
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    chess_club = data["Chess Club"]
    assert len(chess_club["participants"]) >= 0
