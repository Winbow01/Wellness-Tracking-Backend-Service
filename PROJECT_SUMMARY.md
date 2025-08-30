# Wellness Tracking Backend Service

A comprehensive wellness tracking backend service built with Python Flask, featuring activity logging, device synchronization, and statistical analysis.

## Project Structure

```
|- docs/                          # Design documents
|- wellness_tracking/             # Main application
   |- controller/routes/          # API routes and controllers
      |- __test__/               # Controller tests
      |- activity_controller.py  # Activity API endpoints
   |- service/                   # Business logic layer
      |- activity_service.py     # Activity business logic
   |- repository/                # Data access layer
      |- models.py               # Database models
   |- main.py                    # Application entry point
   |- config.env                 # Environment configuration
   |- requirements.txt           # Python dependencies
|- mock-service/                 # Mock external services
   |- mock_api.py               # Mock device API
   |- requirements.txt          # Mock service dependencies
|- README.md                     # Project documentation
```

## Features

- **Activity Logging**: Log wellness activities (meditation, workout, hydration, sleep)
- **Device Synchronization**: Sync data from wearable devices
- **Statistical Analysis**: Generate summaries by week, month, or year
- **RESTful API**: Standard HTTP endpoints with JSON responses
- **Database Integration**: SQLite database with SQLAlchemy ORM
- **Testing**: Comprehensive test suite with pytest
- **Mock Services**: Simulated external device APIs

## Quick Start

### 1. Install Dependencies

```bash
# Install main application dependencies
cd wellness-tracking
pip install -r requirements.txt

# Install mock service dependencies
cd ../mock-service
pip install -r requirements.txt
```

### 2. Start Services

```bash
# From project root directory
python start_server.py
```

This will start:
- Wellness Tracking Service on http://localhost:5000
- Mock Service on http://localhost:5001

### 3. Run Tests

```bash
# Run all tests
cd wellness_tracking
python -m pytest controller/routes/__test__/ -v

# Run example usage
cd ..
python example_usage.py
```

## API Endpoints

### Health Check
- `GET /health` - Service health status

### Activities
- `POST /api/activities` - Log new activity
- `GET /api/activities/<user_id>` - Get user activities
- `GET /api/summary/<user_id>` - Get user summary statistics

### Device Sync
- `POST /api/sync-device` - Sync device data
- `GET /api/sync-status/<user_id>` - Get sync status

### Assumptions:
Modified the Response Format to include activity type, value, and unit for future extensibility of activity types.

### Logic explaination:
User Device → Mock API →    Wellness Service →     Database
    ↓           ↓                   ↓                  ↓
  Raw Data   Simulated Data  Business Logic      Persistent Storage


###   Some considerations regarding scope, edge cases, and any missing details:
Activity Type Extensibility：
Is support for custom activity types available?
Are the units fixed for each activity type?

Value Ranges and Unit Standardization：
Reasonable value ranges for different activity types.
Time Statistics Boundaries

Handling of the period parameter:
For example, does 'week' refer to Monday to Sunday, or the past 7 days from today?

Data volume limits:
Maximum number of activity records per user.
Maximum amount of data for a single synchronization.

Handling Device Synchronization Failures