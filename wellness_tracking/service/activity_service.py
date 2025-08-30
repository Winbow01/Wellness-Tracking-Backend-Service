from datetime import datetime, date, timedelta
from ..repository import db, WellnessActivity, DeviceSync

class ActivityService:
    """Service layer for wellness activity operations"""
    
    @staticmethod
    def log_activity(user_id, activity_type, value, unit):
        """Log a new wellness activity"""
        try:
            activity = WellnessActivity(
                user_id=user_id,
                date=date.today(),
                activity_type=activity_type,
                value=value,
                unit=unit
            )
            
            db.session.add(activity)
            db.session.commit()
            
            return {
                "success": True,
                "activity_id": activity.id,
                "activity": {
                    "id": activity.id,
                    "user_id": activity.user_id,
                    "date": activity.date.isoformat(),
                    "activity_type": activity.activity_type,
                    "value": activity.value,
                    "unit": activity.unit,
                    "created_at": activity.created_at.isoformat()
                }
            }
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_user_activities(user_id, start_date=None, end_date=None, activity_type=None):
        """Get user's historical activity records"""
        try:
            query = WellnessActivity.query.filter_by(user_id=user_id)
            
            if start_date:
                query = query.filter(WellnessActivity.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
            if end_date:
                query = query.filter(WellnessActivity.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
            if activity_type:
                query = query.filter_by(activity_type=activity_type)
            
            activities = query.order_by(WellnessActivity.date.desc()).all()
            
            return {
                "user_id": user_id,
                "activities": [{
                    "id": activity.id,
                    "date": activity.date.isoformat(),
                    "activity_type": activity.activity_type,
                    "value": activity.value,
                    "unit": activity.unit,
                    "created_at": activity.created_at.isoformat()
                } for activity in activities]
            }
        except Exception as e:
            raise e
    
    @staticmethod
    def get_user_summary(user_id, period='week', end_date=None):
        """Get user's summary statistics"""
        try:
            if not end_date:
                end_date = date.today().isoformat()
            
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            # Calculate start date based on period
            if period == 'week':
                start_date = end_date_obj - timedelta(days=7)
            elif period == 'month':
                start_date = end_date_obj.replace(day=1)
            elif period == 'year':
                start_date = end_date_obj.replace(month=1, day=1)
            else:
                raise ValueError("Invalid period. Must be week, month, or year")
            
            # Query activity data
            activities = WellnessActivity.query.filter(
                WellnessActivity.user_id == user_id,
                WellnessActivity.date >= start_date,
                WellnessActivity.date <= end_date_obj
            ).all()
            
            # Group statistics by activity type
            summary = {}
            for activity in activities:
                if activity.activity_type not in summary:
                    summary[activity.activity_type] = {
                        "total_value": 0,
                        "unit": activity.unit,
                        "count": 0
                    }
                summary[activity.activity_type]["total_value"] += activity.value
                summary[activity.activity_type]["count"] += 1
            
            return {
                "user_id": user_id,
                "period": period,
                "start_date": start_date.isoformat(),
                "end_date": end_date_obj.isoformat(),
                "summary": summary
            }
        except Exception as e:
            raise e
    
    @staticmethod
    def sync_device_data(user_id, device_data):
        """Sync device data and save to database"""
        try:
            synced_activities = []
            
            for device_record in device_data:
                activity = WellnessActivity(
                    user_id=device_record['user_id'],
                    date=datetime.strptime(device_record['date'], '%Y-%m-%d').date(),
                    activity_type=device_record['activity_type'],
                    value=device_record['value'],
                    unit=device_record['unit']
                )
                
                db.session.add(activity)
                synced_activities.append({
                    "activity_type": device_record['activity_type'],
                    "value": device_record['value'],
                    "unit": device_record['unit']
                })
            
            # Record sync status
            sync_record = DeviceSync(
                user_id=user_id,
                sync_date=date.today()
            )
            db.session.add(sync_record)
            
            db.session.commit()
            
            return {
                "success": True,
                "synced_activities": synced_activities
            }
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_sync_status(user_id):
        """Get device sync status"""
        try:
            sync_record = DeviceSync.query.filter_by(user_id=user_id).order_by(DeviceSync.last_sync_at.desc()).first()
            
            if sync_record:
                return {
                    "user_id": user_id,
                    "last_sync_date": sync_record.sync_date.isoformat(),
                    "last_sync_at": sync_record.last_sync_at.isoformat()
                }
            else:
                return {
                    "user_id": user_id,
                    "message": "No sync records found"
                }
        except Exception as e:
            raise e
