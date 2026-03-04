#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test script for REST API endpoints"""

import sys
import requests
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Goal, ProgressLog
from dotenv import load_dotenv
import os

# Configure UTF-8 encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

load_dotenv()

# Database setup for creating test data
database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url)
SessionLocal = sessionmaker(bind=engine)

def create_test_data():
    """Create test user and goal for API testing"""
    db = SessionLocal()
    try:
        # Check if test user exists
        user = db.query(User).filter(User.phone_number == "+1234567890").first()
        if not user:
            user = User(phone_number="+1234567890", name="Test User")
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"Created test user with ID: {user.id}")
        else:
            print(f"Test user already exists with ID: {user.id}")

        # Check if test goal exists
        goal = db.query(Goal).filter(Goal.user_id == user.id).first()
        if not goal:
            goal = Goal(
                user_id=user.id,
                goal_type="fitness",
                title="Bajar de peso",
                description="Objetivo de fitness para bajar de peso",
                status="active",
                goal_data={
                    "current_weight": 85,
                    "target_weight": 75,
                    "height": 175,
                    "age": 30,
                    "gender": "M",
                    "deadline": "En 3 meses"
                }
            )
            db.add(goal)
            db.commit()
            db.refresh(goal)
            print(f"Created test goal with ID: {goal.id}")
        else:
            print(f"Test goal already exists with ID: {goal.id}")

        return user.id, goal.id
    finally:
        db.close()

def test_api_endpoints(base_url="http://localhost:8000"):
    """Test all REST API endpoints"""

    print("\n" + "="*60)
    print("TESTING REST API ENDPOINTS")
    print("="*60)

    # Create test data
    user_id, goal_id = create_test_data()

    # Test 1: GET /api/users/{phone}
    print("\n[TEST 1] GET /api/users/{phone}")
    print("-" * 60)
    response = requests.get(f"{base_url}/api/users/+1234567890")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
        print("✓ PASSED")
    else:
        print(f"✗ FAILED: {response.text}")

    # Test 2: GET /api/users/{user_id}/goals
    print("\n[TEST 2] GET /api/users/{user_id}/goals")
    print("-" * 60)
    response = requests.get(f"{base_url}/api/users/{user_id}/goals")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
        print("✓ PASSED")
    else:
        print(f"✗ FAILED: {response.text}")

    # Test 3: GET /api/goals/{goal_id}/progress
    print("\n[TEST 3] GET /api/goals/{goal_id}/progress")
    print("-" * 60)
    response = requests.get(f"{base_url}/api/goals/{goal_id}/progress")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
        print("✓ PASSED")
    else:
        print(f"✗ FAILED: {response.text}")

    # Test 4: GET /api/goals/{goal_id}/logs
    print("\n[TEST 4] GET /api/goals/{goal_id}/logs")
    print("-" * 60)
    response = requests.get(f"{base_url}/api/goals/{goal_id}/logs")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
        print("✓ PASSED")
    else:
        print(f"✗ FAILED: {response.text}")

    # Test 5: GET /api/users/{user_id}/stats
    print("\n[TEST 5] GET /api/users/{user_id}/stats")
    print("-" * 60)
    response = requests.get(f"{base_url}/api/users/{user_id}/stats")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
        print("✓ PASSED")
    else:
        print(f"✗ FAILED: {response.text}")

    # Test 6: Test 404 error handling
    print("\n[TEST 6] GET /api/users/{invalid_phone} (should return 404)")
    print("-" * 60)
    response = requests.get(f"{base_url}/api/users/+9999999999")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 404:
        print("✓ PASSED - Correctly returned 404")
    else:
        print(f"✗ FAILED - Expected 404, got {response.status_code}")

    print("\n" + "="*60)
    print("API TESTING COMPLETE")
    print("="*60)

if __name__ == "__main__":
    try:
        test_api_endpoints()
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Could not connect to the server.")
        print("Make sure the FastAPI server is running:")
        print("  python main.py")
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
