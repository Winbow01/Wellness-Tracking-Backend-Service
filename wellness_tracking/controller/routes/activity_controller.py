from flask import Blueprint, request, jsonify
from datetime import datetime
import requests
from ...service import ActivityService
from ...repository import db

# Create Blueprint
activity_bp = Blueprint('activity', __name__)

# Mock API URL
MOCK_API_BASE = "http://localhost:5001"  # Local mock API service

@activity_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})

@activity_bp.route('/api/activities', methods=['POST'])
def log_activity():
    """Log wellness activity"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'activity_type', 'value', 'unit']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Validate activity type
        valid_activity_types = ['meditation', 'workout', 'hydration', 'sleep', 'running', 'walking']
        if data['activity_type'] not in valid_activity_types:
            return jsonify({"error": f"Invalid activity type. Must be one of: {valid_activity_types}"}), 400
        
        # Call service layer
        result = ActivityService.log_activity(
            user_id=data['user_id'],
            activity_type=data['activity_type'],
            value=data['value'],
            unit=data['unit']
        )
        
        return jsonify({
            "message": "Activity logged successfully",
            "activity_id": result['activity_id'],
            "activity": result['activity']
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@activity_bp.route('/api/activities/<user_id>', methods=['GET'])
def get_user_activities(user_id):
    """Get user's historical activity records"""
    try:
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        activity_type = request.args.get('activity_type')
        
        # Call service layer
        result = ActivityService.get_user_activities(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            activity_type=activity_type
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@activity_bp.route('/api/summary/<user_id>', methods=['GET'])
def get_user_summary(user_id):
    """Get user's summary statistics"""
    try:
        # Get query parameters
        period = request.args.get('period', 'week')  # week, month, year
        end_date = request.args.get('end_date')
        
        # Call service layer
        result = ActivityService.get_user_summary(
            user_id=user_id,
            period=period,
            end_date=end_date
        )
        
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@activity_bp.route('/api/sync-device', methods=['POST'])
def sync_device_data():
    """Sync device data"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400
        
        # Call Mock API to get device data
        try:
            # In production environment, this would call the real device API
            response = requests.get(f"{MOCK_API_BASE}/device-activity?user_id={user_id}")
            device_data = response.json()
            
            # Simulate device data response
            # device_data = [
            #     {
            #         "user_id": user_id,
            #         "date": datetime.now().date().isoformat(),
            #         "activity_type": "running",
            #         "value": 30.0,
            #         "unit": "minutes"
            #     }
            # ]
            
        except Exception as e:
            return jsonify({"error": f"Failed to fetch device data: {str(e)}"}), 500
        
        # Call service layer
        result = ActivityService.sync_device_data(user_id, device_data)
        
        return jsonify({
            "message": "Device data synced successfully",
            "user_id": user_id,
            "synced_activities": result['synced_activities']
        }), 200
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@activity_bp.route('/api/sync-status/<user_id>', methods=['GET'])
def get_sync_status(user_id):
    """Get device sync status"""
    try:
        # Call service layer
        result = ActivityService.get_sync_status(user_id)
        
        if 'message' in result:
            return jsonify(result), 404
        else:
            return jsonify(result), 200
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500
