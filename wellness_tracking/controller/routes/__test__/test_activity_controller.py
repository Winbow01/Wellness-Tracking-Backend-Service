import pytest
import json
from datetime import datetime, date, timedelta
from wellness_tracking.main import create_app
from wellness_tracking.repository import db, WellnessActivity, DeviceSync

@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
def sample_user_id():
    return "test_user_123"

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'timestamp' in data

def test_log_activity_success(client, sample_user_id):
    """Test successful activity logging"""
    activity_data = {
        "user_id": sample_user_id,
        "activity_type": "meditation",
        "value": 15.0,
        "unit": "minutes"
    }
    
    response = client.post('/api/activities',
                          data=json.dumps(activity_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'Activity logged successfully'
    assert data['activity']['user_id'] == sample_user_id
    assert data['activity']['activity_type'] == 'meditation'
    assert data['activity']['value'] == 15.0

def test_log_activity_missing_fields(client):
    """Test missing required fields"""
    activity_data = {
        "user_id": "test_user",
        "activity_type": "meditation"
        # Missing value and unit
    }
    
    response = client.post('/api/activities',
                          data=json.dumps(activity_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_log_activity_invalid_type(client, sample_user_id):
    """Test invalid activity type"""
    activity_data = {
        "user_id": sample_user_id,
        "activity_type": "invalid_type",
        "value": 15.0,
        "unit": "minutes"
    }
    
    response = client.post('/api/activities',
                          data=json.dumps(activity_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_get_user_activities_empty(client, sample_user_id):
    """Test getting empty activity list"""
    response = client.get(f'/api/activities/{sample_user_id}')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['user_id'] == sample_user_id
    assert len(data['activities']) == 0

def test_get_user_activities_with_data(client, sample_user_id):
    """Test getting activity list with data"""
    # First create some test data
    with client.application.app_context():
        activities = [
            WellnessActivity(
                user_id=sample_user_id,
                date=date.today(),
                activity_type='meditation',
                value=15.0,
                unit='minutes'
            ),
            WellnessActivity(
                user_id=sample_user_id,
                date=date.today() - timedelta(days=1),
                activity_type='workout',
                value=30.0,
                unit='minutes'
            )
        ]
        for activity in activities:
            db.session.add(activity)
        db.session.commit()
    
    response = client.get(f'/api/activities/{sample_user_id}')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['user_id'] == sample_user_id
    assert len(data['activities']) == 2

def test_get_user_summary_week(client, sample_user_id):
    """Test getting weekly summary"""
    # First create some test data
    with client.application.app_context():
        activities = [
            WellnessActivity(
                user_id=sample_user_id,
                date=date.today(),
                activity_type='meditation',
                value=15.0,
                unit='minutes'
            ),
            WellnessActivity(
                user_id=sample_user_id,
                date=date.today(),
                activity_type='meditation',
                value=10.0,
                unit='minutes'
            ),
            WellnessActivity(
                user_id=sample_user_id,
                date=date.today() - timedelta(days=1),
                activity_type='workout',
                value=30.0,
                unit='minutes'
            )
        ]
        for activity in activities:
            db.session.add(activity)
        db.session.commit()
    
    response = client.get(f'/api/summary/{sample_user_id}?period=week')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['user_id'] == sample_user_id
    assert data['period'] == 'week'
    assert 'meditation' in data['summary']
    assert 'workout' in data['summary']
    assert data['summary']['meditation']['total_value'] == 25.0
    assert data['summary']['meditation']['count'] == 2

def test_sync_device_data_success(client, sample_user_id):
    """Test successful device data sync"""
    sync_data = {
        "user_id": sample_user_id
    }
    
    response = client.post('/api/sync-device',
                          data=json.dumps(sync_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Device data synced successfully'
    assert data['user_id'] == sample_user_id
    assert len(data['synced_activities']) > 0

def test_get_sync_status_no_records(client, sample_user_id):
    """Test getting sync status with no records"""
    response = client.get(f'/api/sync-status/{sample_user_id}')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['user_id'] == sample_user_id
    assert 'message' in data

if __name__ == '__main__':
    pytest.main([__file__])
