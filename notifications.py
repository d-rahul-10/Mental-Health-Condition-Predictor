from flask import Blueprint, jsonify, request
from src.models.user import Notification, db
from src.routes.auth import token_required
from datetime import datetime, timedelta
import json

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('', methods=['GET'])
@token_required
def get_notifications(current_user):
    try:
        status = request.args.get('status')  # pending, sent, read, dismissed
        notification_type = request.args.get('type')  # reminder, alert, motivation, instruction
        limit = request.args.get('limit', 50, type=int)
        
        query = Notification.query.filter_by(user_id=current_user.id)
        
        if status:
            query = query.filter_by(status=status)
        
        if notification_type:
            query = query.filter_by(type=notification_type)
        
        notifications = query.order_by(Notification.created_at.desc()).limit(limit).all()
        
        return jsonify([notification.to_dict() for notification in notifications]), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to fetch notifications: {str(e)}'}), 500

@notifications_bp.route('', methods=['POST'])
@token_required
def create_notification(current_user):
    try:
        data = request.json
        
        if not data.get('type') or not data.get('title') or not data.get('message'):
            return jsonify({'message': 'Type, title, and message are required'}), 400
        
        # Validate notification type
        valid_types = ['reminder', 'alert', 'motivation', 'instruction']
        if data['type'] not in valid_types:
            return jsonify({'message': f'Invalid notification type. Must be one of: {", ".join(valid_types)}'}), 400
        
        notification = Notification(
            user_id=current_user.id,
            type=data['type'],
            title=data['title'],
            message=data['message'],
            scheduled_for=datetime.fromisoformat(data['scheduled_for'].replace('Z', '+00:00')) if data.get('scheduled_for') else None,
            priority=data.get('priority', 'normal'),
            status=data.get('status', 'pending')
        )
        
        db.session.add(notification)
        db.session.commit()
        
        return jsonify({
            'message': 'Notification created successfully',
            'notification': notification.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'message': f'Failed to create notification: {str(e)}'}), 500

@notifications_bp.route('/<int:notification_id>', methods=['GET'])
@token_required
def get_notification(current_user, notification_id):
    try:
        notification = Notification.query.filter_by(id=notification_id, user_id=current_user.id).first()
        
        if not notification:
            return jsonify({'message': 'Notification not found'}), 404
        
        return jsonify(notification.to_dict()), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to fetch notification: {str(e)}'}), 500

@notifications_bp.route('/<int:notification_id>/read', methods=['PUT'])
@token_required
def mark_notification_read(current_user, notification_id):
    try:
        notification = Notification.query.filter_by(id=notification_id, user_id=current_user.id).first()
        
        if not notification:
            return jsonify({'message': 'Notification not found'}), 404
        
        notification.status = 'read'
        notification.read_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Notification marked as read',
            'notification': notification.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to mark notification as read: {str(e)}'}), 500

@notifications_bp.route('/<int:notification_id>', methods=['DELETE'])
@token_required
def delete_notification(current_user, notification_id):
    try:
        notification = Notification.query.filter_by(id=notification_id, user_id=current_user.id).first()
        
        if not notification:
            return jsonify({'message': 'Notification not found'}), 404
        
        db.session.delete(notification)
        db.session.commit()
        
        return jsonify({'message': 'Notification deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to delete notification: {str(e)}'}), 500

@notifications_bp.route('/mark-all-read', methods=['PUT'])
@token_required
def mark_all_notifications_read(current_user):
    try:
        notifications = Notification.query.filter_by(
            user_id=current_user.id,
            status='sent'
        ).all()
        
        for notification in notifications:
            notification.status = 'read'
            notification.read_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': f'Marked {len(notifications)} notifications as read'
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to mark all notifications as read: {str(e)}'}), 500

@notifications_bp.route('/reminders', methods=['POST'])
@token_required
def create_reminder(current_user):
    try:
        data = request.json
        
        if not data.get('title') or not data.get('message') or not data.get('scheduled_for'):
            return jsonify({'message': 'Title, message, and scheduled_for are required'}), 400
        
        reminder = Notification(
            user_id=current_user.id,
            type='reminder',
            title=data['title'],
            message=data['message'],
            scheduled_for=datetime.fromisoformat(data['scheduled_for'].replace('Z', '+00:00')),
            priority=data.get('priority', 'normal'),
            status='pending'
        )
        
        db.session.add(reminder)
        db.session.commit()
        
        return jsonify({
            'message': 'Reminder created successfully',
            'reminder': reminder.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'message': f'Failed to create reminder: {str(e)}'}), 500

@notifications_bp.route('/medication-reminders', methods=['POST'])
@token_required
def create_medication_reminder(current_user):
    try:
        data = request.json
        
        if not data.get('medication_name') or not data.get('dosage') or not data.get('times'):
            return jsonify({'message': 'Medication name, dosage, and times are required'}), 400
        
        medication_name = data['medication_name']
        dosage = data['dosage']
        times = data['times']  # List of time strings like ["08:00", "14:00", "20:00"]
        
        reminders = []
        
        # Create reminders for each time
        for time_str in times:
            hour, minute = map(int, time_str.split(':'))
            
            # Schedule for today and next 30 days
            for day_offset in range(31):
                scheduled_time = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0) + timedelta(days=day_offset)
                
                reminder = Notification(
                    user_id=current_user.id,
                    type='reminder',
                    title=f'Medication Reminder: {medication_name}',
                    message=f'Time to take your {medication_name} ({dosage})',
                    scheduled_for=scheduled_time,
                    priority='high',
                    status='pending'
                )
                
                reminders.append(reminder)
                db.session.add(reminder)
        
        db.session.commit()
        
        return jsonify({
            'message': f'Created {len(reminders)} medication reminders for {medication_name}',
            'reminders_count': len(reminders)
        }), 201
        
    except Exception as e:
        return jsonify({'message': f'Failed to create medication reminders: {str(e)}'}), 500

@notifications_bp.route('/motivational', methods=['POST'])
@token_required
def send_motivational_message(current_user):
    try:
        motivational_messages = [
            "Great job on tracking your health! Keep up the excellent work! 🌟",
            "Every small step counts towards your health goals. You're doing amazing! 💪",
            "Remember: Your health is your wealth. Keep investing in yourself! 💎",
            "Consistency is key! You're building healthy habits one day at a time. 🎯",
            "Your future self will thank you for the healthy choices you're making today! 🚀",
            "Progress, not perfection! Every healthy choice matters. 🌱",
            "You're stronger than you think and more capable than you imagine! ⭐",
            "Health is a journey, not a destination. Enjoy the process! 🛤️"
        ]
        
        import random
        message = random.choice(motivational_messages)
        
        notification = Notification(
            user_id=current_user.id,
            type='motivation',
            title='Daily Motivation',
            message=message,
            priority='normal',
            status='sent',
            sent_at=datetime.utcnow()
        )
        
        db.session.add(notification)
        db.session.commit()
        
        return jsonify({
            'message': 'Motivational message sent',
            'notification': notification.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'message': f'Failed to send motivational message: {str(e)}'}), 500

@notifications_bp.route('/pending', methods=['GET'])
@token_required
def get_pending_notifications(current_user):
    try:
        # Get notifications that should be sent now
        current_time = datetime.utcnow()
        
        pending_notifications = Notification.query.filter_by(
            user_id=current_user.id,
            status='pending'
        ).filter(
            Notification.scheduled_for <= current_time
        ).order_by(Notification.scheduled_for.asc()).all()
        
        # Mark them as sent
        for notification in pending_notifications:
            notification.status = 'sent'
            notification.sent_at = current_time
        
        db.session.commit()
        
        return jsonify([notification.to_dict() for notification in pending_notifications]), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to fetch pending notifications: {str(e)}'}), 500

