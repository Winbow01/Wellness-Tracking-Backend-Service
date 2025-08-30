from flask import Flask, jsonify, request
from datetime import date, timedelta
import random

app = Flask(__name__)

activity_type = ["running", "walking", "hydration_liters", "meditation", "sleep"]

@app.route('/device-activity', methods=['GET'])
def get_device_activity():
    """Mock device activity data API"""
    user_id = request.args.get('user_id', 'default_user')
    
    # Generate mock data
    device_data = []
    
    # Generate data for the last 7 days
    for i in range(7):
        activity_date = date.today() - timedelta(days=i)
        
        # Simulate different activity data
        data = {
            "user_id": user_id,
            "date": activity_date.isoformat(),
            "activity_type": random.choice(activity_type),
            "value": round(random.uniform(1.0, 3.0), 1),
            "unit": "minutes"
            # "hydration_liters": round(random.uniform(1.0, 3.0), 1),
            # "sleep_hours": round(random.uniform(6.0, 9.0), 1),
            # "exercise_minutes": random.randint(0, 60),
            # "meditation_minutes": random.randint(0, 30)
        }
        device_data.append(data)
    
    return jsonify(device_data)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check"""
    return jsonify({"status": "healthy", "service": "mock-device-api"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
