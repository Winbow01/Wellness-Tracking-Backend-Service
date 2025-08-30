from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class WellnessActivity(db.Model):
    """Wellness activity data model"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # meditation, workout, hydration, sleep
    value = db.Column(db.Float, nullable=False)  # Value (minutes, liters, hours, etc.)
    unit = db.Column(db.String(20), nullable=False)  # Unit
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.Index('idx_user_date', 'user_id', 'date'),)

class DeviceSync(db.Model):
    """Device synchronization record model"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    sync_date = db.Column(db.Date, nullable=False)
    last_sync_at = db.Column(db.DateTime, default=datetime.utcnow)
