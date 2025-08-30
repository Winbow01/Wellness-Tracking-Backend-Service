#!/usr/bin/env python3
"""
Wellness Tracking Backend Service Usage Example
Demonstrates how to use the API for various operations
"""

import requests
import json
from datetime import datetime

# API Configuration
WELLNESS_API_BASE = "http://localhost:5000"
MOCK_API_BASE = "http://localhost:5001"

def test_health_check():
    """Test health check endpoint"""
    print("Testing Health Check...")
    try:
        response = requests.get(f"{WELLNESS_API_BASE}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("Connection Error: Please ensure the wellness service is running")
    print("-" * 50)

def test_log_activity():
    """Test logging an activity"""
    print("Testing Activity Logging...")
    activity_data = {
        "user_id": "user_123",
        "activity_type": "meditation",
        "value": 15.0,
        "unit": "minutes"
    }
    
    try:
        response = requests.post(
            f"{WELLNESS_API_BASE}/api/activities",
            json=activity_data
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("Connection Error: Please ensure the wellness service is running")
    print("-" * 50)

def test_get_user_activities():
    """Test getting user activities"""
    print("Testing Get User Activities...")
    user_id = "user_123"
    
    try:
        response = requests.get(f"{WELLNESS_API_BASE}/api/activities/{user_id}")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("Connection Error: Please ensure the wellness service is running")
    print("-" * 50)

def test_get_user_summary():
    """Test getting user summary"""
    print("Testing Get User Summary...")
    user_id = "user_123"
    
    try:
        response = requests.get(f"{WELLNESS_API_BASE}/api/summary/{user_id}?period=week")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("Connection Error: Please ensure the wellness service is running")
    print("-" * 50)

def test_sync_device_data():
    """Test device data synchronization"""
    print("Testing Device Data Sync...")
    sync_data = {
        "user_id": "user_123"
    }
    
    try:
        response = requests.post(
            f"{WELLNESS_API_BASE}/api/sync-device",
            json=sync_data
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("Connection Error: Please ensure the wellness service is running")
    print("-" * 50)

def test_get_sync_status():
    """Test getting sync status"""
    print("Testing Get Sync Status...")
    user_id = "user_123"
    
    try:
        response = requests.get(f"{WELLNESS_API_BASE}/api/sync-status/{user_id}")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("Connection Error: Please ensure the wellness service is running")
    print("-" * 50)

def test_mock_api():
    """Test mock API"""
    print("Testing Mock API...")
    try:
        response = requests.get(f"{MOCK_API_BASE}/device-activity?user_id=user_123")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("Connection Error: Please ensure the mock service is running")
    print("-" * 50)

def test_error_cases():
    """Test error cases"""
    print("Testing Error Cases...")
    
    # Test missing fields
    print("1. Testing missing fields...")
    try:
        response = requests.post(
            f"{WELLNESS_API_BASE}/api/activities",
            json={"user_id": "user_123"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("Connection Error: Please ensure the wellness service is running")
    
    # Test invalid activity type
    print("2. Testing invalid activity type...")
    try:
        response = requests.post(
            f"{WELLNESS_API_BASE}/api/activities",
            json={
                "user_id": "user_123",
                "activity_type": "invalid_type",
                "value": 15.0,
                "unit": "minutes"
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("Connection Error: Please ensure the wellness service is running")
    
    print("-" * 50)

def main():
    """Main function to run all tests"""
    print("Wellness Tracking API Example Usage")
    print("=" * 50)
    
    # Test all endpoints
    test_health_check()
    test_log_activity()
    test_get_user_activities()
    test_get_user_summary()
    test_sync_device_data()
    test_get_sync_status()
    test_mock_api()
    test_error_cases()
    
    print("Example usage completed!")

if __name__ == "__main__":
    main()
